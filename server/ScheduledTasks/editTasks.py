# update-edit-task.py
# The AHJ Registry
# March, 2021

from django.db import connection, transaction
import sys
sys.path.append('..')
from ahj_app.views_edits import apply_edits

def test_proc():
    with connection.cursor() as cursor:
        # pass
        print('CALLING DB PROCEDURES')
        apply_edits()


def edits_take_effect():
    with connection.cursor() as cursor:
        # apply_edits()
        pass

