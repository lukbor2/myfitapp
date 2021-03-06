# Generated by Django 2.0.3 on 2018-03-13 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfit', '0008_device_owner_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_date',
            field=models.DateField(verbose_name='Activity Date'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_duration',
            field=models.IntegerField(default=0, verbose_name='Activity Duration'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Activity ID'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_time',
            field=models.TimeField(verbose_name='Activity Time'),
        ),
    ]
