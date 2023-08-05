import re

from django.db import models
from django.db.models import signals

from ..data.models import Field, MetadataStandard, FieldSetField, FieldSet, FieldValue, standardfield


class VRACore4FieldValue(FieldValue):
    notes = models.TextField(blank=True)
    dataDate = models.DateTimeField(auto_now=True)
    extent = models.TextField(blank=True)
    href = models.TextField(blank=True)
    pref = models.BooleanField(null=True, blank=True)
    refid = models.CharField(max_length=255, blank=True)
    rules = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    vocab = models.CharField(max_length=255, blank=True)


STANDARD = 'vra-core-4'
STANDARD_PREFIX = 'vra4'
STANDARD_TITLE = 'VRA Core 4'
# TODO: update when core 5 is out:
STANDARD_NAMESPACE = 'http://www.vraweb.org/vracore4.htm'

FIELDS = """
work
collection
image
agent
agent-attribution
agent-culture
agent-dates
agent-dates-earliestDate
agent-dates-latestDate
agent-name
agent-role
culturalContext
date
date-earliestDate
date-latestDate
description
inscription
inscription-author
inscription-position
inscription-text
location
location-name
location-refid
material
measurements
relation
rights
rights-rightsHolder
rights-text
source
source-name
source-refid
stateEdition
stateEdition-description
stateEdition-name
stylePeriod
subject
subject-term
technique
textref
textref-name
textref-refid
title
worktype
"""


def create_data_fixtures(sender, *args, **kwargs):
    """
    Signal handler
    """
    create_vra_core_5_fields()


def _format_label(name):
    return ' '.join(n.capitalize() for n in re.sub(r'([A-Z])', r' \1', name).replace('-', ' ').split(' '))


def create_vra_core_5_fields():

    dc_id_field = standardfield('identifier')
    dc_title_field = standardfield('title')

    standard, _ = MetadataStandard.objects.get_or_create(
        name=STANDARD,
        defaults=dict(
            prefix=STANDARD_PREFIX,
            title=STANDARD_TITLE,
        )
    )

    fieldset, _ = FieldSet.objects.get_or_create(
        name=STANDARD,
        defaults=dict(
            standard=True,
            title=STANDARD_TITLE,
        )
    )

    fields = dict()
    for index, field_name in enumerate(n for n in FIELDS.split('\n') if n):
        fields[field_name], _ = Field.objects.get_or_create(
            name=field_name,
            standard=standard,
            defaults=dict(
                label=_format_label(field_name),
            )
        )
        FieldSetField.objects.get_or_create(
            fieldset=fieldset,
            field=fields[field_name],
            defaults=dict(
                order=(index + 1) * 10,
                label=fields[field_name].label,
            )
        )

    fields['title'].equivalent.add(dc_title_field)
    fields['work'].equivalent.add(dc_id_field)
    fields['collection'].equivalent.add(dc_id_field)
    fields['image'].equivalent.add(dc_id_field)


signals.post_migrate.connect(create_data_fixtures)
