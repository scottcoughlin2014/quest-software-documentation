from django.core.management.base import BaseCommand, CommandError
from modules.models import Module
from modules import views
import subprocess
import os
import glob

PRIMARY_KEYWORDS = ['Has SLURM Example', 'Files and IO', 'Compiler', 'Programming Language', 'Chemistry', 'Molecular Dynamics', 'Engineering', 'Magnetic Resonance Imaging (MRI)', 'Economics', 'Linear Algebra', 'Genomics', 'Audio and Visualization Libraries and Tools', 'Software Tools', 'Astrophysics']
LIST_OF_MODULES_TO_SEARCH = views.LIST_OF_MODULES_TO_SEARCH

class Command(BaseCommand):
    help = 'Update the database with the latest modules'
    def add_arguments(self, parser):
        parser.add_argument("--update-keywords-only", action="store_true", default=False)

    def handle(self, *args, **options):

        result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "spider"], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
        dictionary_modules_and_versions = [{ii[0]: ii[-1].split(",")} for ii in [i.replace(' ','').split(":") for i in result.stderr.decode("utf-8").split("\n") if i]][8:-9]
        for software in dictionary_modules_and_versions:
            for name, versions in software.items():
                if name not in LIST_OF_MODULES_TO_SEARCH.keys():
                    continue

                obj, created = Module.objects.get_or_create(name=name,)
                obj.primary_keywords = None
                obj.secondary_keywords = None
                obj.save()
                # Add keywords/tags to either primary or secondary keywords 
                primary_keywords = []
                secondary_keywords = []
                for kw in LIST_OF_MODULES_TO_SEARCH[name]:
                    if kw == "None":
                        continue
                    if kw in PRIMARY_KEYWORDS:
                        primary_keywords.append(kw)
                    else:
                        secondary_keywords.append(kw)

                # Add examples of submitting the job using SLURM if an example exists 
                name = name.lower()
                if name in os.listdir("examplejobs"):
                    # a special tag for denoting if the software/application has a slurm example
                    primary_keywords.append('Has SLURM Example')
                    all_example_scripts = glob.glob(os.path.join("examplejobs", name, "*.sh"))
                    all_example_scripts.extend(glob.glob(os.path.join("examplejobs", name, "*", "*.sh")))
                    all_lines = []
                    if len(all_example_scripts) > 1:
                        obj.slurm_submission_example = "Examples of SLURM jobs for {0} can be found <a href=https://github.com/nuitrcs/examplejobs/tree/master/{0}>here</a>.".format(name)
                    else:
                        for submit_script in all_example_scripts:
                            with open(submit_script, "r") as f:
                                tmp = f.readlines()
                                all_lines.extend(tmp)
                        obj.slurm_submission_example = ''.join(all_lines)

                obj.primary_keywords = primary_keywords
                obj.secondary_keywords = secondary_keywords

                if options['update_keywords_only']:
                    obj.save()
                    continue

                # We need to get the versions in a  different way if there are lots of them because the above method will ellipsis
                if len(versions) > 2:
                    result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "spider", "{0}/".format(name)], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                    versions = result.stderr.decode("utf-8").split("Versions:\n")[1].split("\n\n")[0].replace(" ", "").split("\n")

                obj.versions = versions
                obj.preferred = versions[-1]
                whatis_output = subprocess.run(["/software/lmod/lmod/libexec/lmod", "whatis", versions[-1]], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                whatis_output = [i.split(":") for i in whatis_output.stderr.decode("utf-8").split("\n")]

                if whatis_output[0][0] != "":
                    obj.whatis = whatis_output[0][1]

                result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "help", versions[-1]], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                obj.help_info = ' '.join(list(filter(None, result.stderr.decode("utf-8").split("\n")[2:])))
                obj.save()
