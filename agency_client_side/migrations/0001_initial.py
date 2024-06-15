# Generated by Django 5.0.3 on 2024-06-15 19:07

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinAgencyTeamAsClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_team_name', models.CharField(max_length=400)),
                ('client_container_name', models.CharField(default='testing123', max_length=500)),
                ('current_unique_link', models.CharField(max_length=500)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CreateNewClientTaskClientSide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(max_length=300)),
                ('task_short_description', models.TextField()),
                ('task_due_date', models.CharField(max_length=200)),
                ('task_current_status', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('current_assigned_team_for_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency_client_side.joinagencyteamasclient')),
            ],
        ),
        migrations.CreateModel(
            name='CreateNewClientRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_title', models.CharField(max_length=300)),
                ('short_description', models.TextField()),
                ('client_request_body', models.TextField()),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('clients_assigned_agency_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency_client_side.joinagencyteamasclient')),
            ],
        ),
        migrations.CreateModel(
            name='CreateNewClientFolderClientSide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_name', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('current_assigned_team_for_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency_client_side.joinagencyteamasclient')),
            ],
        ),
        migrations.CreateModel(
            name='CreateNewClientFileClientSide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_file_name', models.CharField(max_length=300)),
                ('client_file', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True)),
                ('client_file_extension', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('current_client_folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency_client_side.createnewclientfolderclientside')),
                ('current_assigned_team_for_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency_client_side.joinagencyteamasclient')),
            ],
        ),
    ]
