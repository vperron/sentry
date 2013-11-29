"""
sentry.db.transactions
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2013 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from django.db import transaction


class Savepoint(object):
    def __init__(self, using='default'):
        self.using = using

    def __enter__(self):
        self._in_trans = not transaction.get_autocommit(using=self.using)
        if not self._in_trans:
            return
        self.sid = transaction.savepoint(using=self.using)

    def __exit__(self, *exc_info):
        if not self._in_trans:
            return
        if exc_info:
            transaction.savepoint_rollback(self.sid, using=self.using)
        else:
            transaction.savepoint_commit(self.sid, using=self.using)


def rollback_unless_autocommit(using=None):
    # Django 1.6 removes this nescesary API
    if transaction.get_autocommit(using=using):
        transaction.rollback()
