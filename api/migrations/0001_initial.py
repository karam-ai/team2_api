# Generated by Django 3.1.7 on 2021-04-03 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dev_id', models.CharField(blank=True, max_length=500)),
                ('hardware_serial', models.CharField(blank=True, max_length=500)),
                ('meta_data', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drone_name', models.CharField(blank=True, max_length=50)),
                ('drone_number', models.CharField(blank=True, max_length=50)),
                ('long', models.FloatField(blank=True, default=0)),
                ('lat', models.FloatField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Measures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=50)),
                ('value', models.CharField(blank=True, max_length=50)),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.drone')),
            ],
        ),
    ]
