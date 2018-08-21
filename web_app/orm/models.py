# -*- coding: utf-8 -*-

import logging
import traceback
import uuid
import json
import datetime

from django.db import models
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import Group, User

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import models

from settings import ugettext_lazy as _

DEFAULT_UNIT_SERIAL_NR="0000-0000"
DEFAULT_UNIT_FTP_URL="ftp://1.1.1.1/metusco"

class TvStoreUnit(models.Model):

    id = models.UUIDField(verbose_name=_('UUID'), default=uuid.uuid4, primary_key=True, unique=True, null=False, blank=False, editable=False)
    name            = models.CharField(verbose_name=_('name'), max_length=200)
    ftp_url         = models.CharField(verbose_name=_('ftp_url'), max_length=200, default=DEFAULT_UNIT_FTP_URL)
    serial_nr       = models.CharField(verbose_name=_('serial_nr'), max_length=200, unique=True, null=False, blank=False, db_index=True, default=DEFAULT_UNIT_SERIAL_NR)
    creation_date   = models.DateTimeField(default=timezone.now)
    expire_date     = models.DateTimeField(null=True, blank=True)
    group           = models.ForeignKey(Group, verbose_name=_('group'), null=True, on_delete=models.SET_NULL)
    user            = models.ForeignKey(User,  verbose_name=_('user'),  null=True, on_delete=models.SET_NULL)
    js_attributes   = models.TextField(_(u'js_attributes'), null=False, blank=True)

    def user_name(self):
        
        if self.user:
            return self.user.username

class TvStoreContact(models.Model):

    STATUS = (
        (0, _(u"in progress")),
        (1, _(u"completed")),
        (2, _(u"aborted")),
        (3, _(u"saved")),
    )

    TYPES = (
        (0, _(u"PING"  )),
        (1, _(u"CREATE")),
        (2, _(u"UPDATE")),
        (3, _(u"ALERT" )),
    )

    id = models.UUIDField(verbose_name=_('UUID'), default=uuid.uuid4, primary_key=True, unique=True, null=False, blank=False, editable=False)
    type            = models.PositiveIntegerField(choices=TYPES, default=0, null=False, db_index=True)
    status          = models.PositiveIntegerField(choices=STATUS, default=0, null=False, db_index=True)
    creation_date   = models.DateTimeField(default=timezone.now)
    unit            = models.ForeignKey(TvStoreUnit, verbose_name=_('unit'), null=True, on_delete=models.SET_NULL)
    user            = models.ForeignKey(User, verbose_name=_('user'), null=True, on_delete=models.SET_NULL)
    unit_serial_nr  = models.CharField(verbose_name=_('unit_serial_nr'), max_length=200, unique=False, null=False, blank=False, default=DEFAULT_UNIT_SERIAL_NR)
    js_attributes   = models.TextField(_(u'js_attributes'), null=False, blank=True)

    def unit_name(self):
        
        return self.unit.name

@receiver(models.signals.pre_save, sender=TvStoreContact)
def pre_save_handler_contact(sender, instance=None, created=False, **kwargs):

    # ~ logging.warning("pre_save_handler_contact() instance:{}".format(instance))
    # ~ logging.warning("pre_save_handler_contact() instance.unit_serial_nr:{}".format(instance.unit_serial_nr))
    # ~ logging.warning("pre_save_handler_contact() instance.user :{}".format(instance.user))

    try:
        obj = TvStoreContact.objects.get(id=instance.id)
    except:
        obj = None

    if obj is None:

        unit = TvStoreUnit.objects.get(serial_nr=instance.unit_serial_nr)
        instance.unit = unit
        
        if instance.user != unit.user:
            raise PermissionDenied("contact instance's user differs from the user the related unit belongs to.")


