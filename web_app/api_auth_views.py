# -*- coding: utf-8 -*-

import logging
import traceback
import time

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import (HttpResponseRedirect, HttpResponse, JsonResponse)
from django.urls import reverse

from rest_framework import (viewsets, status)
from rest_framework.views import APIView
from rest_framework.response import Response

from orm.models import (TvStoreUnit, TvStoreContact, TvStoreUnitSerializer, TvStoreContactSerializer)

class TvStoreContactList(APIView):
    
    queryset = TvStoreContact.objects.all()

    def get(self, request, format=None):

        units_ = TvStoreContact.objects.filter(**request.query_params.dict())
        data_ = TvStoreContactSerializer(units_, many=True).data
        
        return JsonResponse(data_, safe=False)

    def post(self, request, format=None):
        
        serializer = TvStoreContactSerializer(data=request.data)

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

class TvStoreUnitList(APIView):
    
    queryset = TvStoreUnit.objects.all()
    
    def get(self, request, format=None):

        units_ = TvStoreUnit.objects.filter(**request.query_params.dict())
        data_ = TvStoreUnitSerializer(units_, many=True).data
        
        return JsonResponse(data_, safe=False)

    def post(self, request, format=None):
        
        serializer = TvStoreUnitSerializer(data=request.data)

        if serializer.is_valid():
            
            r_ = serializer.save()
            
            obj = TvStoreUnit.objects.get(id=r_.id)
            
            ret_ = JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            
            ret_ = JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return ret_ 


def main(request):

    ctx_ = {}

    # ~ logging.warning("main() request:{}, ctx_:{}".format(request, ctx_))
    # ~ logging.warning("main() dir(request):{}".format(dir(request)))

    return render(request, 'main.html', ctx_)

"""

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(APIView):
    
    " Retrieve, update or delete a snippet instance. "
    
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
"""
