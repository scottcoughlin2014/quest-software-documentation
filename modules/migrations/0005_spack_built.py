# Generated by Django 3.1.7 on 2021-03-14 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0004_spack'),
    ]

    operations = [
        migrations.AddField(
            model_name='spack',
            name='built',
            field=models.BooleanField(default=False),
        ),
    ]