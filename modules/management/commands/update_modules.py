from django.core.management.base import BaseCommand, CommandError
from modules.models import Module
import subprocess
import os
import glob

PRIMARY_KEYWORDS = ['programming language', 'quantum chemistry', 'molecular dynamics', 'engineering', 'MRI', 'linear algebra', 'genomics']

LIST_OF_MODULES_TO_SEARCH = {
'abaqus' : ['finite element analysis', 'engineering'],
'abinit' : ['quantum chemistry', 'materials modeling', 'density functional theory', 'optimization', 'simulation'],
'ADF' : ['quantum chemistry', 'molecular dynamics', 'quantum mechanics', 'density functional theory', 'parallel binaries'],
'AFNI' : ['MRI'],
'alphafold' : ['chemistry'],
'alsa-lib' : [],
'ambertools' : ['molecular dynamics'],
'ampl' : [],
'anicalculator': [],
'ansys' : ['engineering'],
'AnsysEM' : ['engineering'],
'Ansys-Fluent' : ['engineering'],
'ant' : [],
'ants' : ['MRI'],
'anvio' : [],
'aria' : [],
'armadillo' : ['linear algebra'],
'ase' : ['molecular dynamics'],
'aspera' : [],
'atk' : ['quantum chemistry'],
'ATLAS' : ['linear algebra'],
'atom' : ['text editor'],
'at-spi2-atk' : [],
'at-spi2-core' : [],
'awscli' : [],
'bam-readcount' : ['genomics', 'BAM/SAM', 'genomics utility'],
'bamtools' : ['genomics', 'DNA sequence aligner', 'RNA sequence aligner', 'BAM/SAM'],
'baron' : [],
'bart' : [],
'basespace' : [],
'bazel' : ['compiler'],
'BBMap' : [],
'bcbio_nextgen' : [],
'BCBToolKit' : [],
'bcftools' : ['genomics', 'BCF/VCF', 'genomics utility'],
'bcl2fastq' : ['genomics', 'BCL', 'fastq', 'genomics utility'],
'beagle-cpu' : [],
'bedops' : [],
'bedtools' : [],
'bismark' : [],
'blas-lapack' : ['linear algebra'],
'blast' : ['genomics', 'DNA sequence aligner', 'RNA sequence aligner', 'protein sequence aligner', 'database search'],
'blatsuite' : [],
'blcr' : [],
'boost' : ['linear algebra'],
'bowtie' : ['genomics', 'DNA sequence aligner'],
'bowtie2' : ['genomics', 'DNA sequence aligner'],
'bsmap' : [],
'bwa' : ['genomics', 'DNA sequence aligner', 'RNA sequence aligner'],
'bwrap' : [],
'cairo' : [],
'casa' : [],
'cassi' : [],
'cellranger' : ['genomics', 'RNA sequence aligner', 'single-cell RNA-seq'],
'cellranger-atac' : ['genomics', 'single-cell ATAC-seq'],
'CfitsIO' : ['IO Libraries and Formats'],
'cgal' : [],
'charm' : ['parallel'],
'charmpp' : ['parallel'],
'checkm' : [],
'chemaxon_marvin' : [],
'chemaxon_structure_rep' : [],
'chimera' : [],
'clang' : ['compiler'],
'cmake' : [],
'cmdstan' : [],
'connectome_workbench' : ['MRI'],
'copasul' : [],
'cp2k' : ['quantum chemistry', 'molecular dynamics', 'quantum mechanics'],
'cplex' : [],
'CrisprCasFinder' : [],
'cuda' : ['compiler'],
'cufflinks' : [],
'curl' : [],
'cytoscape' : [],
'db' : [],
'ddd' : [],
'deeptools' : [],
'diamond' : ['genomics', 'protein sequence aligner'],
'diffreps' : [],
'dynare' : [],
'dyninst' : [],
'eclipse' : [],
'eigen' : ['linear algebra'],
'elfutils' : [],
'emacs' : ['text editor'],
'epacts' : [],
'espresso' : ['quantum chemistry'],
'expansionhunter' : [],
'expat' : [],
'fastani' : [],
'fastqc' : [],
'fasttree' : [],
'FastTreeMP' : [],
'fenics27' : [],
'ffmpeg' : [],
'fftw' : [],
'fMRIPrep' : ['MRI'],
'freesurfer' : ['MRI'],
'freetype' : [],
'fsl' : ['MRI'],
'gamess' : ['quantum chemistry'],
'gap' : [],
'gatk' : [],
'gauss' : ['programming language'],
'Gaussian' : ['quantum chemistry'],
'Gaussian16' : ['quantum chemistry'],
'gcc' : ['compiler'],
'gcloud' : [],
'gdal' : [],
'gdb' : [],
'gdbm' : [],
'gdc-client' : [],
'gdk-pixbuf' : [],
'geany' : [],
'GeneTorrent' : [],
'GenomeBrowse' : [],
'geos' : [],
'gettext' : [],
'gffcompare' : [],
'gffread' : [],
'ghc' : [],
'ghostscript' : [],
'git' : [],
'gnumeric' : [],
'gnuplot' : [],
'go' : [],
'gold' : [],
'GotoBlas' : [],
'gpaw' : [],
'grace' : [],
'gradle' : [],
'graphlib' : [],
'graphviz' : [],
'GRASS' : [],
'gromacs' : ['molecular dynamics'],
'gsl' : ['linear algebra'],
'gstreamer' : [],
'gtk+' : [],
'gtool' : [],
'guppy' : [],
'gurobi' : [],
'hdf5' : ['IO Libraries and Formats'],
'hic-pro' : [],
'hisat2' : [],
'hmmer' : ['genomics', 'database search', 'DNA sequence aligner', 'protein sequence aligner'],
'homer' : [],
'htslib' : [],
'hypre' : [],
'icu4c' : [],
'idba' : [],
'igv' : [],
'ImageJ' : [],
'ImageMagick' : [],
'impute2' : [],
'imsl' : [],
'indelocator' : [],
'intel' : ['compiler'],
'intel-mkl' : ['linear algebra'],
'intltool' : [],
'ipopt' : [],
'iread' : [],
'jags' : ['statistical computing'],
'java' : [],
'jellyfish' : [],
'jq' : [],
'juicer' : [],
'julia' : ['programming language'],
'kallisto' : [],
'kentUtils' : [],
'kim-api' : [],
'knitro' : [],
'kraken' : [],
'krona' : [],
'kSNP' : [],
'lammps' : ['molecular dynamics'],
'latte' : [],
'launchmon' : [],
'lazarus' : [],
'leptonica' : [],
'lftp' : [],
'libreoffice' : [],
'liggghts-public' : [],
'lp_solve' : [],
'lumerical' : [],
'MACS2' : [],
'mafft' : [],
'mageck' : [],
'mageck_vispr' : [],
'makedepf90' : [],
'manta' : [],
'mathematica' : ['programming language'],
'matlab' : ['programming language'],
'matlabstan' : [],
'meep' : [],
'megahit' : [],
'meme' : [],
'mercurial' : [],
'metabat' : [],
'metal' : [],
'metamap' : [],
'metaxa2' : [],
'metis' : [],
'mlpack' : [],
'mono' : [],
'motif' : [],
'mpb' : [],
'mpi' : ['parallel', 'compiler'],
'mpi4py' : ['parallel'],
'mricrogl' : [],
'mrnet' : [],
'mrtrix3' : ['MRI'],
'MS-Ropen' : [],
'multiqc' : [],
'mumps' : [],
'muscle' : [],
'mutect' : [],
'mysql' : [],
'namd' : ['molecular dynamics'],
'nano' : ['text editor'],
'ncl' : [],
'nco' : [],
'ncurses' : [],
'ndiff' : [],
'netCDF' : ['IO Libraries and Formats'],
'netcdf-c' : ['IO Libraries and Formats'],
'netcdf-fortran' : ['IO Libraries and Formats'],
'netlib-scalapack' : ['linear algebra'],
'netlogo' : [],
'ngsplot' : [],
'nlopt' : [],
'novocraft' : [],
'numactl' : [],
'numpy' : [],
'nwchem' : ['quantum chemistry', 'molecular dynamics', 'quantum mechanics'],
'ocaml' : [],
'octave' : ['programming language'],
'oncotator' : [],
'openbabel' : [],
'openblas' : ['linear algebra'],
'OpenBugs' : ['statistical computing'],
'opencl' : [],
'openmd' : [],
'opera' : [],
'orca' : ['quantum chemistry'],
'osu-micro-benchmarks' : [],
'oxconsole' : [],
'oxedit' : [],
'p7zip' : [],
'pandoc' : [],
'papi' : [],
'parallel' : [],
'paraview' : [],
'parmetis' : [],
'parsec' : ['quantum chemistry'],
'pBWA' : [],
'pdflib-lite' : [],
'peer' : [],
'penncnv' : [],
'perl' : ['programming language'],
'petsc' : [],
'pexsi' : [],
'phylocsf' : [],
'picard' : [],
'pigz' : [],
'pindel' : [],
'plink' : [],
'plumed' : ['molecular dynamics'],
'poppler' : [],
'povray' : [],
'pplacer' : [],
'prada' : [],
'prodigal' : [],
'proj' : [],
'protobuf' : [],
'PRSice' : [],
'python' : ['programming language'],
'python-anaconda3' : ['programming language'],
'python-miniconda3' : ['programming language'],
'qchem' : ['quantum chemistry'],
'qctool' : [],
'qe' : ['quantum chemistry'],
'qhull' : [],
'qiime2' : [],
'qt' : [],
'qualimap' : [],
'quantum-espresso' : ['quantum chemistry'],
'R' : ['programming language', 'statistical computing'],
'raxml' : [],
'rfmix' : [],
'rmats2sashimiplot' : [],
'rmats_turbo' : [],
'rsem' : [],
'ruby' : ['programming language'],
'rufus' : [],
'sage' : [],
'sailfish' : [],
'salmon' : [],
'samtools' : ['genomics', 'DNA sequence aligner', 'RNA sequence aligner', 'BAM/SAM'],
'sas' : ['programming language'],
'scala' : [],
'scalapack' : ['linear algebra'],
'scallop' : [],
'schrodinger' : [],
'scons' : [],
'sdpt3' : [],
'seqkit' : [],
'seqtk' : [],
'shapeit' : [],
'singularity' : [],
'sirius' : [],
'slepc' : [],
'snakemake' : [],
'snpEff' : [],
'snptest' : [],
'soapdenovo2' : [],
'SolexaQA++' : [],
'spades' : [],
'spark' : [],
'specfem3d_globe' : [],
'speedseq' : [],
'spfft' : [],
'spglib' : [],
'spla' : [],
'spm' : ['MRI'],
'sqlite' : [],
'sratoolkit' : [],
'STAR' : [],
'STAR-Fusion' : [],
'stat' : [],
'stata' : ['programming language'],
'stattransfer' : [],
'strelka' : [],
'stress' : [],
'stringtie' : [],
'subread' : [],
'SuiteSparse' : [],
'superlu' : [],
'superlu-dist' : [],
'suppa' : [],
'swig' : [],
'tar' : [],
'tau' : [],
'tcl' : [],
'telseq' : [],
'tesseract' : [],
'texlive' : [],
'tickwrite' : [],
'tig' : [],
'tmux' : [],
'tophat' : [],
'Tramonto' : [],
'TrimGalore' : [],
'trimmomatic' : [],
'uchime' : [],
'udunits2' : [],
'utilities' : [],
'valgrind' : [],
'vasp' : ['quantum chemistry'],
'vcftools' : [],
'velvet' : [],
'vesta' : [],
'vim' : ['text editor'],
'visit' : [],
'vmd' : [],
'voropp' : [],
'vtk' : [],
'wannier' : ['quantum chemistry'],
'wine' : [],
'wxwidgets' : [],
'xander_assembler' : [],
'xcb-proto' : [],
'xmlsec' : [],
'xpdf' : [],
'xz' : [],
'yaml-cpp' : [],
'yasm' : [],
'zstd' : [],
}

class Command(BaseCommand):
    help = 'Update the database with the latest modules'

    def handle(self, *args, **options):

        result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "spider"], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
        dictionary_modules_and_versions = [{ii[0]: ii[-1].split(",")} for ii in [i.replace(' ','').split(":") for i in result.stderr.decode("utf-8").split("\n") if i]][8:-9]
        for software in dictionary_modules_and_versions:
            for name, versions in software.items():
                if name not in LIST_OF_MODULES_TO_SEARCH.keys():
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
                obj.primary_keywords = primary_keywords
                obj.secondary_keywords = secondary_keywords

                result = subprocess.run(["/software/lmod/lmod/libexec/lmod", "help", versions[-1]], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
                obj.help_info = ' '.join(list(filter(None, result.stderr.decode("utf-8").split("\n")[2:])))
                # there may be a single example job or multiple
                name = name.lower()
                if name in os.listdir("examplejobs"):
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
                obj.save()