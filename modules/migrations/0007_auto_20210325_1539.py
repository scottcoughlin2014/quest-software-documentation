# Generated by Django 3.1.7 on 2021-03-25 15:39

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0006_auto_20210314_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='keywords',
            field=models.JSONField(blank=True, help_text='A list of descriptors like chemistry or data analysis which describe the uses of this module', null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='help_info',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Help information that comes from running module help XXX.', null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='slurm_submission_example',
            field=ckeditor.fields.RichTextField(blank=True, help_text='If available, an example of running this software with slurm. All options should be here: https://github.com/scottcoughlin2014/examplejobs/', null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='versions',
            field=models.JSONField(blank=True, help_text='All still available versions of this software', null=True),
        ),
    ]