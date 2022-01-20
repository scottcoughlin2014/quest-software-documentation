from django.shortcuts import render, get_object_or_404
from .models import Module
import string

# Create your views here.
LIST_OF_POPULAR_SOFTWARE = [
"ADF",
"R",
"abaqus",
"abinit",
"ansys",
"aspera",
"blas-lapack",
"cp2k",
"cuda",
"fftw",
"freesurfer",
"fsl",
"gcc",
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
"lumerical",
"mathematica",
"matlab",
"mpi",
"namd",
"netcdf-c",
"netcdf-fortran",
"nwchem",
"openblas",
"orca",
"paraview",
"python",
"python-anaconda3",
"python-miniconda3",
"qchem",
"quantum-espresso",
"singularity",
"stata",
"vasp",
]

letters_a_to_z = [ i for i in string.ascii_uppercase]

def index(request):
    modules = Module.objects.order_by('name')
    all_keywords = []
    for module in modules:
        if module.primary_keywords is not None:
            for keyword in module.primary_keywords:
                all_keywords.append(keyword)
    all_keywords = set(sorted(all_keywords))
    
    return render(request, 'modules/index.html', {"modules" : modules, "popular_software" : set(LIST_OF_POPULAR_SOFTWARE), "all_keywords" : all_keywords, 'letters_a_to_z' : letters_a_to_z})

#def detail(request, module_id):
#    module = get_object_or_404(Module, pk=module_id)
#    return render(request, 'grbs/individual_page.html', {'module': module})
