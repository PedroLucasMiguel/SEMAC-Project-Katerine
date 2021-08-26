# Generated by Django 3.2.6 on 2021-08-26 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemacUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=128, primary_key=True, serialize=False)),
                ('is_email_authenticated', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('date_and_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPersonalData',
            fields=[
                ('cpf', models.CharField(max_length=14, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=128)),
                ('dob', models.DateField()),
                ('state', models.CharField(max_length=2)),
                ('city', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('contact_number', models.CharField(max_length=14)),
                ('user_email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personal_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserUnespData',
            fields=[
                ('ra', models.CharField(max_length=9, primary_key=True, serialize=False, unique=True)),
                ('course_name', models.CharField(max_length=128)),
                ('user_cpf', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='unesp_data', to='usermanager.userpersonaldata')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=64)),
                ('is_payed', models.BooleanField(default=False)),
                ('user_cpf', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='usermanager.userpersonaldata')),
            ],
        ),
        migrations.CreateModel(
            name='SemacUserAuthenticationCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=12)),
                ('user_email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_code', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonOnLecture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lecture_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_lectures', to='usermanager.lecture')),
                ('user_cpf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participated_lectures', to='usermanager.userpersonaldata')),
            ],
        ),
        migrations.AddField(
            model_name='lecture',
            name='lecturer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture', to='usermanager.lecturer'),
        ),
    ]
