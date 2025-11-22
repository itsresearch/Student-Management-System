from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('home_auth', '0008_alter_passwordresetrequest_token'),
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('department', models.CharField(blank=True, max_length=120)),
                ('subject_specialty', models.CharField(blank=True, max_length=120)),
                ('experience_years', models.PositiveIntegerField(default=0)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('bio', models.TextField(blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClassSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('class_name', models.CharField(max_length=100)),
                ('topic', models.CharField(max_length=255)),
                ('total_students', models.PositiveIntegerField(default=0)),
                ('present_students', models.PositiveIntegerField(default=0)),
                ('syllabus_coverage', models.PositiveIntegerField(default=0, help_text='Percentage of coverage for this session')),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date', '-start_time'),
            },
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('subject', models.CharField(max_length=120)),
                ('class_name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('assigned_on', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('assigned', 'Assigned'), ('in_review', 'In Review'), ('completed', 'Completed'), ('overdue', 'Overdue')], default='assigned', max_length=20)),
                ('completed_count', models.PositiveIntegerField(default=0)),
                ('pending_count', models.PositiveIntegerField(default=0)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('due_date',),
            },
        ),
    ]

