from django.core.management.base import BaseCommand, CommandError
from modules.models import Module
import subprocess

class Command(BaseCommand):
    help = 'Update the database with the latest modules'

    def handle(self, *args, **options):

        result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "spider"], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)                                                                                                
        dictionary_modules_and_versions = [{ii[0]: ii[-1].split(",")} for ii in [i.replace(' ','').split(":") for i in result.stderr.decode("utf-8").split("\n") if i]][8:-9]
        for software in dictionary_modules_and_versions:
            for name, versions in software.items():
                obj, created = Module.objects.get_or_create(name=name,)
                obj.versions = versions
                obj.preferred = versions[-1]
            obj.save()
