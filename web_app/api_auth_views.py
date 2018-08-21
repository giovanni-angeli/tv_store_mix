# -*- coding: utf-8 -*-

import logging
import traceback
import time

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import (HttpResponseRedirect, HttpResponse, JsonResponse)
from django.urls import reverse

from django.contrib.auth.models import User

from django.core.paginator import Paginator

from rest_framework import (viewsets, status)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers 

from orm.models import (TvStoreUnit, TvStoreContact)

class TvStoreUnitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TvStoreUnit
        fields = (
            'user', 
            'name', 
            'ftp_url', 
            'serial_nr',
            'js_attributes', 
        )
        safe = False

class TvStoreContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TvStoreContact
        fields = (
            'type', 
            'status', 
            'user', 
            'unit_serial_nr', 
            'js_attributes', 
        )
        safe = False


class TvStoreListViewBase(APIView):

    serializer_class = None

    def get(self, request, format=None):

        qs = self.queryset
        query_params_ = request.query_params.dict()

        if not request.user.is_superuser:
            query_params_['user'] = User.objects.all().filter(username=request.user)[0].id

        objs_ = qs.filter(**query_params_)
        data_ = self.serializer_class(objs_, many=True).data
        return JsonResponse(data_, safe=False)

    def post(self, request, format=None):

        data_ = request.data.dict()
        data_['user'] = User.objects.all().filter(username=request.user)[0].id

        serializer = self.serializer_class(data=data_)

        r_ = None
        if serializer.is_valid():
            try:
                r_ = serializer.save()
            except:
                logging.error(traceback.format_exc())
                r_ = None

        if r_ is not None:    
            ret_ = JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            ret_ = JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return ret_ 


class TvStoreContactList(TvStoreListViewBase):
    
    queryset = TvStoreContact.objects.all()
    serializer_class = TvStoreContactSerializer

class TvStoreUnitList(TvStoreListViewBase):
    
    queryset = TvStoreUnit.objects.all()
    serializer_class = TvStoreUnitSerializer
    

def main(request):

    ctx_ = {}

    # ~ logging.warning("main() request:{}, ctx_:{}".format(request, ctx_))
    # ~ logging.warning("main() dir(request):{}".format(dir(request)))

    return render(request, 'main.html', ctx_)

