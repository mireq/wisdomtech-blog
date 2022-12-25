# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.contrib.postgres.aggregates import JSONBAgg
from django.db import models
from django.db.models import Q, F, Value as V, OuterRef, Subquery, Case, When, JSONField
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import JSONObject, Cast
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from parler.managers import TranslatableQuerySet as BaseTranslatableQuerySet
from parler.models import TranslatableModel as BaseTranslatableModel


class NOT_SET(object):
	pass


class TimestampModelMixin(models.Model):
	date_created = models.DateTimeField(
		_("Date created"),
		editable=False
	)
	date_updated = models.DateTimeField(
		_("Date updated"),
		editable=False
	)

	def save(self, *args, **kwargs):
		self.date_updated = timezone.now()
		if not self.id and not self.date_created:
			self.date_created = self.date_updated
		return super().save(*args, **kwargs)

	class Meta:
		abstract = True


class TranslatableQuerySet(BaseTranslatableQuerySet):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._translated_fields_prefix = 'fast_translation_'

	def _clone(self, *args, **kwargs):
		clone = super()._clone(*args, **kwargs)
		clone._translated_fields_prefix = self._translated_fields_prefix
		return clone

	def _fetch_all(self, *args, **kwargs):
		super()._fetch_all(*args, **kwargs)
		for obj in self._result_cache:
			if isinstance(obj, models.Model):
				obj._translated_fields_prefix = self._translated_fields_prefix

	def translated_field_name(self, name):
		return f'{self._translated_fields_prefix}{name}'

	def fast_translate(self, language_code=None, fields=None, hide_untranslated=NOT_SET, fallback=None, fetch_all=False, prefix='fast_translation_', **filters):
		"""Annotates queryset with translated fields.

		Args:
			langauge_code (str): Language code or None for current language.
			fields (list of strings): Requested translated fields or None for all
				fields.
			hide_untranslated (bool): Filter objects without requested translation
				or fallback.
			fallback (str, list, or True): Fallback language or list of fallback
				languages. True selects any language.
			fetch_all (bool): This allows to fetch all languages and use object
				from various language contexts
			prefix (str): Prefix added to annotated fields.
			filters (dict): Extra filters applied to queryset (to prevent extra joins)

		Returns:
			QuerySet: New queryset with annotated fields.

			If translated queryset has field `title` then new queryset has annotated field `<prefix>title`.
		"""
		q_filters = []
		named_filters = {}
		for filter_name, filter_value in filters.items():
			if isinstance(filter_value, Q):
				q_filters.append(filter_value)
			else:
				if not filter_name.startswith('translations__'):
					filter_name = f'translations__{filter_name}'
				named_filters[filter_name] = filter_value

		translated_model = self.model.translations.rel.related_model
		self._translated_fields_prefix = prefix

		if language_code is None:
			if self._language is None:
				language_code = translation.get_language()
			else:
				language_code = self._language

		if fetch_all:
			if hide_untranslated is not NOT_SET and hide_untranslated:
				raise ValueError("Option hide_untranslated can't be used with fetch_all")
		else:
			if hide_untranslated is NOT_SET:
				hide_untranslated = True
			self._language = language_code

		if fields is None:
			fields = self.model._parler_meta.get_all_fields()
		# Simple case when selecting single language without fallback
		if hide_untranslated and fallback is None and not fetch_all:
			annotations = {}
			for field in fields:
				annotations[prefix + field] = F('translations__' + field)
			return (self
				.filter(translations__language_code=language_code, *q_filters, **named_filters)
				.annotate(**annotations))
		# Complex cases with fallbakck
		else:
			if isinstance(fallback, str):
				fallback = [fallback]
			field_selects = {}
			json_annotations = {}
			field_selects['language_code'] = Cast('language_code', models.CharField(null=True))
			for field in fields:
				field_selects[field] = Cast(field, models.CharField(null=True))
				json_annotations[prefix + field] = KeyTextTransform(field, 'translation_data', output_field=models.CharField(null=True))

			language_priority = [language_code]
			if fallback is True or not fallback:
				language_priority += [lang[0] for lang in settings.LANGUAGES if lang[0] != language_code]
			else:
				language_priority += list(fallback)

			if fetch_all:
				translations = (translated_model.objects
					.filter(master_id=OuterRef('pk'))
					.annotate(translation_data=JSONObject(**field_selects))
					.values('master_id')
					.annotate(all_translations=JSONBAgg('translation_data')))
				translation_metadata = {}
				if fallback:
					translation_metadata['fallback'] = V(language_priority, output_field=JSONField())
				qs = (self
					.annotate(all_translations=JSONObject(
						translations=Subquery(translations.values('all_translations'), output_field=JSONField()),
						**translation_metadata
					)))
			else:
				translations = (translated_model.objects
					.filter(master_id=OuterRef('pk'))
					.annotate(translation_data=JSONObject(**field_selects))
					.values('translation_data'))

				if fallback is None:
					translations = translations.filter(language_code=language_code)
				else:
					if fallback is not True:
						translations = translations.filter(language_code__in=language_priority)
					priority_rules = [
						When(Q(language_code=lang), then=len(language_priority) - i)
						for i, lang
						in enumerate(language_priority)
					]
					priority = Case(*priority_rules, output_field=models.IntegerField(), default=V(0))
					translations = translations.annotate(priority=priority).order_by('-priority', 'pk')
				qs = (self
					.annotate(translation_data=Subquery(translations.values('translation_data')[:1], output_field=JSONField()))
					.annotate(**json_annotations))
				if hide_untranslated:
					qs = qs.filter(*q_filters, **named_filters).exclude(translation_data__isnull=True)
				else:
					qs = qs.filter(*q_filters, **named_filters)
			return qs


class TranslatableManager(models.Manager.from_queryset(TranslatableQuerySet)):
	def fast_translate(self, language_code=None, fields=None, hide_untranslated=NOT_SET, fallback=None, fetch_all=False, prefix='fast_translation_'):
		return self.all().fast_translate(language_code, fields, hide_untranslated, fallback, fetch_all, prefix)


class TranslatableModel(BaseTranslatableModel):
	objects = TranslatableManager()

	def fast_translation_getter(self, fieldname):
		if not hasattr(self.__class__, '_translation_model_instance'):
			self.__class__._translation_model_instance = self.__class__._parler_meta.root_model()
		fast_field_name = getattr(self, '_translated_fields_prefix', 'fast_translation_') + fieldname
		if hasattr(self, fast_field_name):
			return self._db_value_to_python(getattr(self, fast_field_name), fieldname)
		elif hasattr(self, 'all_translations'):
			all_translations = self.all_translations
			if isinstance(all_translations['translations'], list):
				all_translations['translations'] = {obj['language_code']: obj for obj in all_translations['translations']}
				if all_translations.get('fallback') and isinstance(all_translations['fallback'], str):
					all_translations['fallback'] = json.loads(all_translations['fallback'])
			translations = all_translations['translations']
			if translations:
				lang = translation.get_language()
				if lang in translations:
					return self._db_value_to_python(translations[lang].get(fieldname), fieldname)
				for lang in all_translations.get('fallback', []):
					if lang in translations and fieldname in translations[lang]:
						return self._db_value_to_python(translations[lang].get(fieldname), fieldname)
			return None
		return self.safe_translation_getter(fieldname, any_language=settings.ALWAYS_TRANSLATION_FALLBACK)

	def save_translation(self, translation, *args, **kwargs):
		if hasattr(self, 'site_id'):
			translation.site_id = self.site_id
		return super().save_translation(translation, *args, **kwargs)

	def _get_translated_model(self, language_code=None, use_fallback=None, auto_create=False, meta=None):
		if use_fallback is None and language_code is None and settings.ALWAYS_TRANSLATION_FALLBACK:
			use_fallback = True
		return super()._get_translated_model(language_code, use_fallback, auto_create, meta)

	def _db_value_to_python(self, value, field_name):
		# convert value using field descriptor
		try:
			setattr(self.__class__._translation_model_instance, field_name, value)
			value = getattr(self.__class__._translation_model_instance, field_name)
		except Exception:
			pass
		return value

	def _set_translated_fields(self, language_code=None, **fields):
		objects = super()._set_translated_fields(language_code, **fields)
		for translation, parler_data in zip(objects, self._parler_meta._split_fields(**fields)):
			parler_meta, model_fields = parler_data
			for field, value in model_fields.items():
				model_field = parler_meta.model._meta.get_field(field)
				if isinstance(model_field, models.FileField):
					model_field.save_form_data(translation, value)
		return objects

	class Meta:
		abstract = True
