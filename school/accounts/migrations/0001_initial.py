# Generated by Django 4.1.4 on 2022-12-21 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_checked', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programs_user', to='authentication.profile')),
                ('program_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.programlist')),
            ],
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('number', models.CharField(max_length=5)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.programlist')),
            ],
        ),
        migrations.CreateModel(
            name='TaskAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('grade', models.CharField(choices=[('A', '5'), ('B', '4'), ('C', '3'), ('D', '2'), ('F', '1')], max_length=1)),
                ('programs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.programs')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.tasklist')),
            ],
        ),
    ]
