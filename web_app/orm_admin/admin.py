# -*- coding: utf-8 -*-

import logging
import json

from django.utils.safestring import mark_safe
from django.contrib import admin

from orm.models import (TvStoreUnit, TvStoreContact)
from settings import ugettext_lazy as _


@admin.register(TvStoreUnit)
class TvStoreUnitAdmin(admin.ModelAdmin):

    list_display = ('name', 'creation_date', 'expire_date', 'group', 'user')
    # ~ readonly_fields = ('id', 'serial_nr', )
    readonly_fields = ('id', )
    
    fieldsets = (
        ('Main section', {'fields': (('name', 'serial_nr', 'ftp_url', 'group', 'user', 'expire_date'))}),
        ('js_attributes section', {'fields': (('js_attributes', ))}),
    )

    def get_list_filter(self, request):
        
        list_filter = ['creation_date', 'group', 'user']

        if not request.user.is_superuser:
                
            list_filter = ['creation_date', 'group']

        return list_filter 

    def get_queryset(self, request):
        
        """
        Filter the objects displayed in the change_list to only
        display those for the currently signed in user.
        """
        
        logging.warning("request.user:{}".format(request.user))
        
        qs = super(TvStoreUnitAdmin, self).get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(user=request.user)


@admin.register(TvStoreContact)
class TvStoreContactAdmin(admin.ModelAdmin):

    list_display = ('creation_date', 'type', 'status', 'unit_serial_nr')
    readonly_fields = ('id', 'unit', )
    
    fieldsets = (
        ('Main section', {'fields': (('type', 'status', 'unit_serial_nr', 'creation_date'))}),
        ('js_attributes section', {'fields': (('js_attributes', ))}),
    )

    list_filter = ['status', 'unit_serial_nr']

    def get_queryset(self, request):
        
        """
        Filter the objects displayed in the change_list to only
        display those for the currently signed in user.
        """
        
        logging.warning("request.user:{}".format(request.user))
        
        qs = super(TvStoreContactAdmin, self).get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(user=request.user)

