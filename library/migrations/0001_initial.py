# Generated by Django 4.0.2 on 2022-06-11 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('wikipedia', models.URLField(blank=True, max_length=500)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('picture_url', models.URLField(blank=True, max_length=500)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('website', models.URLField(blank=True, max_length=500)),
            ],
            options={
                'verbose_name': 'Publisher',
                'verbose_name_plural': 'Publishers',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('subtitle', models.CharField(blank=True, max_length=150)),
                ('synopsis', models.TextField(blank=True)),
                ('language', models.CharField(max_length=20)),
                ('is_available', models.BooleanField(default=False)),
                ('isbn', models.IntegerField()),
                ('picture_url', models.URLField(blank=True, max_length=500)),
                ('author', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='library.author')),
                ('publisher', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='library.publisher')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
    ]
