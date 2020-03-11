# Generated by Django 2.2.9 on 2020-03-07 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapping', '0079_auto_20200307_0114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mappingreleasecandidate',
            old_name='codesystem',
            new_name='source_codesystem',
        ),
        migrations.AddField(
            model_name='mappingreleasecandidate',
            name='target_codesystem',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='target_codesystem', to='mapping.MappingCodesystem'),
        ),
    ]
