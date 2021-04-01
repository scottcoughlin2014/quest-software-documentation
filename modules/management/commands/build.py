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

slurm_job = """#!/bin/bash
#SBATCH --account=a9009
#SBATCH --partition=master
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --time=02:00:00
#SBATCH --mem-per-cpu=2G
#SBATCH --job-name=build_{0}
#SBATCH --output=build_{0}_{1}_{2}.out
#SBATCH --mail-type=END
#SBATCH --mail-user=s-coughlin@northwestern.edu

. /projects/a9009/sbc538/spack/spack/share/spack/setup-env.sh
module load utilities
module load bzip2/1.0.8-gcc-4.8.5
module load tar/1.32-gcc-4.8.5

{3}
"""

class Command(BaseCommand):
    help = 'Populate the Spack model with the information needed to build the package'

    def handle(self, *args, **options):

        # check if spack provides any of the modules listed above, and if yes, populate the spack model.
        spack_packages_to_be_built = Spack.objects.filter(built=False)
        # construct submission file
        for spack_package in spack_packages_to_be_built:
            package_name = spack_package.module.name
            preferred_version = spack_package.preferred_version
            compiler = spack_package.compiler
            # are there any variants?
            print(spack_package.variants_available)
            if spack_package.variants_available is not None:
                variants_available = spack_package.variants_available
                variants_enabled = spack_package.variants_enabled
                set_variants = ' '.join(["{0}={1}".format(i[0], i[1]) for i in zip(variants_available, variants_enabled)])
            else:
                set_variants = ""
            arch = spack_package.arch
            build_command = "spack install {0}@{1}%{2} {3} arch={4}".format(package_name, preferred_version, compiler, set_variants, arch)
            print(build_command)

            with open("build_{0}_{1}_{2}".format(package_name, preferred_version, compiler), "w") as submit_file:
                submit_file.write(slurm_job.format(package_name, preferred_version, compiler, build_command)) 
