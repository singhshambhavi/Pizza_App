# DRF Imports
from django.shortcuts import render
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.status import ( HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR)

# Misc Imports
import json
from pizza_app.pagination import PostLimitOffsetPagination

# Model Imports
from pizza_app.models import Pizza

# Serializer Import
from pizza_app.serializer import PizzaListSerializer

# Create your views here.
class PizzaView(ModelViewSet):
    pagination_class = PostLimitOffsetPagination
    
    def list(self, request, *args, **kwargs):
        try:
            pizza_list = Pizza.objects.filter().values()
            return Response({"pizza_list": pizza_list})
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request, *args, **kwargs):
        try:
            size = request.POST.get("size")
            types = request.POST.get("types")
            toppings = request.POST.get("toppings")
            if not size and types:
                return Response({"message": "Parameters Missing."}, status=HTTP_400_BAD_REQUEST)
            toppings = json.dumps(toppings)
            pizza_obj = Pizza.objects.create(size=size, types=types, toppings=toppings)
            return Response({"message":"Created"},HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            query = Pizza.objects.filter(id=pk).values().first()
            if not query:
                return Response({"message": "Invalid ID."}, status=HTTP_400_BAD_REQUEST)
            size = request.data.get("size") or query["size"]
            types = request.data.get("types") or query["types"]
            toppings = request.data.get("toppings") or query["toppings"]
            Pizza.objects.filter(id=pk).update(size=size, types=types, toppings=toppings)
            return Response({"message":"Updated"})
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            obj = Pizza.objects.filter(id=pk)
            if not obj:
                return Response({"message": "Invalid ID."}, status=HTTP_400_BAD_REQUEST)
            obj.delete()
            return Response({"message": "Deleted."})
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class PizzaList(ListAPIView):
    serializer_class = PizzaListSerializer
    pagination_class = PostLimitOffsetPagination
    
    def get_queryset(self, *args, **kwargs):
        try:
            search = self.request.GET.get("search")
            obj = Pizza.objects.filter().values()
            if search:
                return(Pizza.filter(Q(size__icontains=search) | Q(types__icontains=search)))
            return obj
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

