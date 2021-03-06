from django.core.management.base import BaseCommand, CommandError
from modules.models import Module
import subprocess
import os
import glob

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
                # We need to get the versions ina  different way if there are lots of them because the above method will ellipsis
                if len(versions) > 2:
                    result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "spider", "{0}/".format(name)], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                    versions = result.stderr.decode("utf-8").split("Versions:\n")[-1].split("\n\n")[0].replace(" ", "").split("\n")
                obj, created = Module.objects.get_or_create(name=name,)
                obj.versions = versions
                obj.preferred = versions[-1]
                if obj.whatis is None:
                    result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "whatis", versions[-1]], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                    obj.whatis = ''.join(result.stderr.decode("utf-8").split(":")[1:])
                if obj.help_info is None:
                    result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "help", versions[-1]], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                    obj.help_info = ''.join(result.stderr.decode("utf-8").split("\n")[2:])
                if name in os.listdir("examplejobs"):
                    try:
                        submit_script = glob.glob(os.path.join("examplejobs", name, "*.sh"))[0]
                    except:
                        continue
                    with open(submit_script, "r") as f:
                        tmp = f.readlines()
                        obj.slurm_submission_example = ''.join(tmp)
            obj.save()
