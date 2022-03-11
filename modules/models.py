from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Module(models.Model):
    name = models.CharField(help_text='The name of the module/software', max_length=100)
    versions = models.JSONField(help_text='All still available versions of this software', null=True, blank=True)
    preferred = models.CharField(help_text='preferred version of this module (possibly should also be the default)', max_length=100, null=True, blank=True)
    help_info = RichTextField(help_text='Help information that comes from running module help XXX.', null=True, blank=True,)
    whatis = RichTextField(help_text='module whatis that comes from running module whatis', null=True, blank=True,)
    slurm_submission_example = RichTextField(help_text='If available, an example of running this software with slurm. All options should be here: https://github.com/scottcoughlin2014/examplejobs/', null=True, blank=True,)
    primary_keywords = models.JSONField(help_text='Primary top-level words to describe the use of this module like chemistry or data analysis.', null=True, blank=True)
    secondary_keywords = models.JSONField(help_text='Additional words that might be used to describe the purposes of this software like DFT.', null=True, blank=True)

    def __str__(self):
        return self.name


class Spack(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    preferred_version = models.CharField(help_text='preferred version of this software according to spack', max_length=100, null=True, blank=True)

    GCC_4_8_5 = 'gcc@4.8.5'
    GCC_10_2_0 = 'gcc@10.2.0'
    INTEL_19_0_5_281 = 'intel@19.0.5.281'

    COMPILER_CHOICES = (
        (GCC_4_8_5, 'GCC 4.8.5'),
        (GCC_10_2_0, 'GCC 10.2.0'),
        (INTEL_19_0_5_281, 'INTEL 19.0.5.281'),
    )
    compiler = models.CharField(max_length=100, choices=COMPILER_CHOICES, help_text='If we were to build this module using spack, what compiler should be used', default=GCC_4_8_5)
    variants_available = models.JSONField(help_text='What variants are allowed for this module', null=True, blank=True)
    variants_enabled = models.JSONField(help_text='List with length variants_available that indicates which variants we decided to turn off or on.', null=True, blank=True)
    arch = models.CharField(default="linux-rhel7-x86_64", max_length=100)
    built = models.BooleanField(default=False)

    def __str__(self):
        return "Spack info for module {0}".format(self.module.name)
