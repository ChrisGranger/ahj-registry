"""
Have ``python3 manage.py makemigrations`` ignore additions and changes
for certain attributes of the fields of Django models.

Taken from the comment of this GitHub `gist`_.

.. _gist: https://gist.github.com/vdboor/e3754e19551f2fbbcc31b01eec99ee8e#gistcomment-2901290
"""

from django.core.management.commands.makemigrations import Command
from django.db import models

IGNORED_ATTRS = ['help_text']

original_deconstruct = models.Field.deconstruct


def new_deconstruct(self):
    name, path, args, kwargs = original_deconstruct(self)
    for attr in IGNORED_ATTRS:
        kwargs.pop(attr, None)
    return name, path, args, kwargs


models.Field.deconstruct = new_deconstruct
