# Generated by Django 4.1.4 on 2022-12-26 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('accounts', '0001_initial'),
	]

	operations = [
		migrations.AddField(
			model_name='usertranslation',
			name='meta_description',
			field=models.TextField(blank=True),
		),
		migrations.AddField(
			model_name='usertranslation',
			name='page_title',
			field=models.CharField(blank=True, max_length=200),
		),
		migrations.AddField(
			model_name='usertranslation',
			name='processed_description',
			field=models.TextField(blank=True, editable=False),
		),
	]
