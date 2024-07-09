# Generated by Django 5.0 on 2024-07-09 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='members',
        ),
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='orgId',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='userId',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
