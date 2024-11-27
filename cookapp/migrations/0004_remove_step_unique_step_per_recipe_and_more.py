# Generated by Django 4.0 on 2024-11-26 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookapp', '0003_step_unique_step_per_recipe'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='step',
            name='unique_step_per_recipe',
        ),
        migrations.AddConstraint(
            model_name='step',
            constraint=models.UniqueConstraint(fields=('recipe', 'step_number'), name='unique_step_per_recipe'),
        ),
    ]
