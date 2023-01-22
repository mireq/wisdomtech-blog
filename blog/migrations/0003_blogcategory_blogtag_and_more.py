# Generated by Django 4.1.5 on 2023-01-22 16:29

from django.db import migrations, models
import django.db.models.deletion
import django_autoslugfield.fields
import parler.fields
import parler.models


class Migration(migrations.Migration):

	dependencies = [
		('blog', '0002_alter_blogpost_options_and_more'),
	]

	operations = [
		migrations.CreateModel(
			name='BlogCategory',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
			],
			options={
				'verbose_name': 'Blog category',
				'verbose_name_plural': 'Blog categories',
				'ordering': ('-id',),
			},
			bases=(parler.models.TranslatableModelMixin, models.Model),
		),
		migrations.CreateModel(
			name='BlogTag',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
			],
			options={
				'verbose_name': 'Blog tag',
				'verbose_name_plural': 'Blog tags',
				'ordering': ('-id',),
			},
			bases=(parler.models.TranslatableModelMixin, models.Model),
		),
		migrations.AddField(
			model_name='blogpost',
			name='words',
			field=models.IntegerField(default=0),
		),
		migrations.AlterUniqueTogether(
			name='blogposttranslation',
			unique_together={('language_code', 'slug'), ('language_code', 'master')},
		),
		migrations.AddField(
			model_name='blogpost',
			name='category',
			field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.blogcategory'),
		),
		migrations.AddField(
			model_name='blogpost',
			name='tags',
			field=models.ManyToManyField(blank=True, to='blog.blogtag'),
		),
		migrations.CreateModel(
			name='BlogTagTranslation',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
				('language_code', models.CharField(db_index=True, max_length=15)),
				('title', models.CharField(max_length=200)),
				('slug', django_autoslugfield.fields.AutoSlugField(in_respect_to=('pk',), max_length=200, reserve_chars=0, title_field='title')),
				('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='blog.blogtag')),
			],
			options={
				'verbose_name': 'Blog tag Translation',
				'db_table': 'blog_blogtag_translation',
				'db_tablespace': '',
				'managed': True,
				'default_permissions': (),
				'unique_together': {('language_code', 'title'), ('language_code', 'slug'), ('language_code', 'master')},
			},
			bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
		),
		migrations.CreateModel(
			name='BlogCategoryTranslation',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
				('language_code', models.CharField(db_index=True, max_length=15)),
				('title', models.CharField(max_length=200)),
				('slug', django_autoslugfield.fields.AutoSlugField(in_respect_to=('pk',), max_length=200, reserve_chars=0, title_field='title')),
				('page_title', models.CharField(blank=True, max_length=200)),
				('meta_description', models.TextField(blank=True)),
				('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='blog.blogcategory')),
			],
			options={
				'verbose_name': 'Blog category Translation',
				'db_table': 'blog_blogcategory_translation',
				'db_tablespace': '',
				'managed': True,
				'default_permissions': (),
				'unique_together': {('language_code', 'title'), ('language_code', 'slug'), ('language_code', 'master')},
			},
			bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
		),
	]
