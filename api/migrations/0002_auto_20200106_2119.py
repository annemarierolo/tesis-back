# Generated by Django 3.0 on 2020-01-06 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rol',
        ),
        migrations.AddField(
            model_name='usuario',
            name='rol',
            field=models.CharField(default='Invitado', max_length=11),
        ),
    ]