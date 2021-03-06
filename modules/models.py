from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Module(models.Model):
    name = models.CharField(help_text='The name of the module/software', max_length=100)
    versions = models.JSONField(help_text='All still avaialble versions of this software', null=True, blank=True)
    preferred = models.CharField(help_text='preferred version of this module (possibly should also be the default)', max_length=100, null=True, blank=True)
    help_info = RichTextField(help_text='module help that comes from running module help XXX.', null=True, blank=True,)
    whatis = RichTextField(help_text='module whatis that comes from running module whatis', null=True, blank=True,)
    slurm_submission_example = RichTextField(help_text='module whatis that comes from running module whatis', null=True, blank=True,)

    def __str__(self):
        return self.name
