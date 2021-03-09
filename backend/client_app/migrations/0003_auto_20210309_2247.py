# Generated by Django 3.1.7 on 2021-03-09 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0002_auto_20201119_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=8)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='client_app.client')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', related_query_name='clients', to='client_app.department'),
        ),
    ]