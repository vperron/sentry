"""
sentry.db.transactions
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2013 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from django.db import transaction, connections


class Savepoint(object):
    def __init__(self, using='default'):
        self.using = using

    def __enter__(self):
        self._in_trans = in_transaction(self.using)
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


def in_transaction(using='default'):
    return connections[using].in_atomic_block


def rollback_unless_autocommit(using='default'):
    # Django 1.6 removes this nescesary API
    if in_transaction(using):
        transaction.rollback()
