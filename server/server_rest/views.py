import simplejson as simplejson
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json
import requests

from server_rest.models import ImageSearch

from traitement.decode import buildAndReturnLabel

from server_rest.models import ResponseServer

from server_rest.online_search import online_search

from server_rest.indexing import indexing


class ServerList(APIView):
    """def get(self, request, format=None):
        serv = ImageSearch.objects.all()
        serializer = ImageSearchSerializer(serv)
        return Response(serializer.data)"""

    def post(self, request, format=None):
        errors = {"error": "body must not be empty"}
        if len(request.data) is not 0:

            # Récupération de l'image en base 64 et décodage
            image_64 = request.data["base64"]
            i64 = image_64.split(',')[1]
            type = image_64.split(',')[0]
            if 'png' in type:
                img_type = 'png'
            else:
                img_type = 'jpg'
            image_path = buildAndReturnLabel(i64, img_type)

            # Traitement de l'image avec un retriever
            indexing()
            t = online_search()
            print(t)

            # Enregistrement du résultat dans la BDD
            img1 = ImageSearch(client="PC1")
            img1.save()
            i = 0

            for tab in t:
                if i < 3:
                    print(tab[0])
                    print(tab[1])

                    resp = ResponseServer(result=tab[0], score=float(tab[1]))
                    resp.save()
                    img1.response.add(resp)
                    img1.save()
                    i = i + 1
            i = 0
            print(img1)
            rep = {"id": str(img1.id)}

            # Retourne l'id du résultat du traitement
            return JsonResponse(rep)

        return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_img(request):
    # Récupère l'id du traitement à renvoyer
    img = request.GET['search_id']
    print(img)

    # Récupère le json du résultat
    res = ImageSearch.objects.get(id=img)
    data = res.get_data()

    return JsonResponse(data)


"""
class ServerListDetail(APIView):

    def get(self, **kwargs):
        img = ImageSearch.objects.get(id=kwargs['img_id'])
        #print(img)
        return Response("Reponse reçue", status=status.HTTP_200_OK)
"""
