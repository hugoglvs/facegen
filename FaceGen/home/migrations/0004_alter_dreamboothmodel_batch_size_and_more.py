# Generated by Django 5.0.6 on 2024-06-25 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_generatedimage_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dreamboothmodel',
            name='batch_size',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='dreamboothmodel',
            name='identifier',
            field=models.CharField(default='sks', max_length=100),
        ),
        migrations.AlterField(
            model_name='dreamboothmodel',
            name='training_steps',
            field=models.IntegerField(default=100),
        ),
    ]