from django.core.management.base import BaseCommand, CommandError
from modules.models import Module
import subprocess
import os
import glob

PRIMARY_KEYWORDS = ["chemistry"]

LIST_OF_MODULES_TO_SEARCH = [
"ADF",
"R",
"abaqus",
"abinit",
"ansys",
"aspera",
"blas-lapack",
"boost",
"charmpp",
"cmake",
"cp2k",
"cuda",
"fftw",
"firefox",
"freesurfer",
"fsl",
"gatk",
"gauss",
"gcc",
"gdal",
"geos",
"git",
"gromacs",
"gsl",
"gurobi",
"hdf5",
"intel",
"java",
"julia",
"knitro",
"lammps",
"latte",
"lumerical",
"mathematica",
"matlab",
"mercurial",
"mpi",
"namd",
"netcdf-c",
"netcdf-fortran",
"nwchem",
"openblas",
"opera",
"orca",
"paraview",
"proj",
"python",
"python-anaconda3",
"qchem",
"qt",
"quantum-espresso",
"scalapack",
"singularity",
"sratoolkit",
"stat",
"stata",
"stattransfer",
"tcl",
"texlive",
"vasp",
]

class Command(BaseCommand):
    help = 'Update the database with the latest modules'

    def handle(self, *args, **options):

        result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "spider"], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
        dictionary_modules_and_versions = [{ii[0]: ii[-1].split(",")} for ii in [i.replace(' ','').split(":") for i in result.stderr.decode("utf-8").split("\n") if i]][8:-9]
        for software in dictionary_modules_and_versions:
            for name, versions in software.items():
                if name not in LIST_OF_MODULES_TO_SEARCH:
                    continue
                # We need to get the versions in a  different way if there are lots of them because the above method will ellipsis
                if len(versions) > 2:
                    result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "spider", "{0}/".format(name)], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                    versions = result.stderr.decode("utf-8").split("Versions:\n")[1].split("\n\n")[0].replace(" ", "").split("\n")

                obj, created = Module.objects.get_or_create(name=name,)
                obj.primary_keywords = None
                obj.secondary_keywords = None
                obj.save()
                obj.versions = versions
                obj.preferred = versions[-1]
                whatis_output = subprocess.run(["/software/lmod/lmod/libexec/lmod", "whatis", versions[-1]], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                whatis_output = [i.split(":") for i in whatis_output.stderr.decode("utf-8").split("\n")]

                if whatis_output[0][0] != "":
                    obj.whatis = whatis_output[0][1]

                # now we need to see if there is more to the whatis, i.e. have keywords been added to it.
                if len(whatis_output) > 1:
                    for i in whatis_output:
                        for ii in i:
                            if "Keywords" in ii:
                                keywords = [tmp1.replace(" ", "", 1) for tmp1 in [tmp.split(",") for tmp in ii.split(";")[1:]][0]]
                                keywords[-1] = " ".join(keywords[-1].split(" ")[0:-1])
                                primary_keywords = []
                                secondary_keywords = []
                                for kw in keywords:
                                    if kw in PRIMARY_KEYWORDS:
                                        primary_keywords.append(kw)
                                    else:
                                        secondary_keywords.append(kw)
                                obj.primary_keywords = primary_keywords
                                obj.secondary_keywords = secondary_keywords

                result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "help", versions[-1]], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                obj.help_info = ' '.join(list(filter(None, result.stderr.decode("utf-8").split("\n")[2:])))
                if name in os.listdir("examplejobs"):
                    try:
                        submit_script = glob.glob(os.path.join("examplejobs", name, "*.sh"))[0]
                    except:
                        continue
                    with open(submit_script, "r") as f:
                        tmp = f.readlines()
                        obj.slurm_submission_example = ''.join(tmp)
                obj.save()
