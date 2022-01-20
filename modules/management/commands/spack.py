from django.core.management.base import BaseCommand, CommandError
from modules.models import Spack, Module
import subprocess
import os
import glob

LIST_OF_MODULES_TO_SEARCH = [
"git",
"mercurial",
"gnuplot",
]

class Command(BaseCommand):
    help = 'Populate the Spack model with the information needed to build the package'

    def handle(self, *args, **options):

        # check if spack provides any of the modules listed above, and if yes, populate the spack model.
        for package in LIST_OF_MODULES_TO_SEARCH:
            result = subprocess.run(["spack", "info", "{0}".format(package.lower())], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
            result = result.stdout.decode("utf-8")
            if result:
                # find the module
                module, m_created = Module.objects.get_or_create(name=package)
                # find the spack model that goes with this module or create a new one
                spack, s_created = Spack.objects.get_or_create(module=module) 
                # extract the preferred version from spack
                preferred_version = ' '.join(result.split()).split("Preferred version: ")[-1].split( )[0]

                # Has the preferred_version changed?
                if spack.preferred_version != preferred_version:
                    spack.preferred_version = preferred_version

                # locate the variant section of spack info
                variants = ' '.join(' '.join(result.split()).split("Variants: ")[-1].split( )).split(" Installation")[0].split( )[8:]
                # does this even have variants
                if variants:
                    # figure out the possible variants and then record their defaults
                    idxs = [idx for idx, i in enumerate(variants) if (i == "[off]") or (i == "[on]")]
                    variant_names = [variants[i-1] for i in idxs]
                    variant_defaults = []
                    for i in idxs:
                        if variants[i] == "[off]":
                            variant_defaults.append("False")
                        else:
                            variant_defaults.append("True")
                else:
                    variant_names = None
                    variant_defaults = None

                spack.variants_available = variant_names
                spack.variants_enabled = variant_defaults
                spack.compiler="gcc@4.8.5"
                spack.save()
