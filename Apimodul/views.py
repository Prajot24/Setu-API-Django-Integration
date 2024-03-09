import json
from rest_framework.views import APIView
from rest_framework import viewsets,generics
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.response import Response
import requests

class SetuAPITokenView(APIView):
    def post(self, request, *args, **kwargs):
        url = "https://orgservice-prod.setu.co/v1/users/login"
        payload = {
            "clientID": request.data.get("clientID"),
            "grant_type": request.data.get("grant_type"),
            "secret": request.data.get("secret")
        }

        data = request.data
        headers = {
            "client": "bridge"
            
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            # Assuming the API returns a token, return it to the client
            return Response(response.json())
        else:
            # Return the error from the Setu API to the client
            return Response(response.json(), status=response.status_code)


class ConsentView(generics.CreateAPIView, generics.RetrieveAPIView, viewsets.GenericViewSet):
    queryset = None
    serializer_class = None
    def create(self, request):
        data = request.data

        print(data)
        

        url = "https://fiu-sandbox.setu.co/v2/consents"
        
        # print(bearer_token)
         
        headers = {
            # "Content-Type": "application/json",
            "Authorization":  request.headers.get('Authorization'),
            "x-client_id" : request.headers.get("x-client_id"),
            "x-client-secret":request.headers.get("x-client-secret"),
            "x-product-instance-id":request.headers.get("x-product-instance-id")
                   
        }

        response = requests.post(url, json=data, headers=headers)

        print(response)

        if response.status_code == 201:
            

            return Response(response.json(), status=status.HTTP_201_CREATED)
        else:
            
            return Response(response.json(), status=response.status_code)
    
    def retrieve(self, request, *args, **kwargs):

        id = self.kwargs.get('pk')
        # print(id)
        # URL to which you want to send the GET request
        url = f"https://fiu-sandbox.setu.co/v2/consents/{id}?expanded=true"
        headers = {
            "Content-Type": "application/json",
            "Authorization": request.headers.get('Authorization'),
            "x-product-instance-id":request.headers.get("x-product-instance-id")
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)
        
    
    @action(detail=True,methods=['get'],)
    def LastFetchStatus(self, request, *args, **kwargs):
        consent_id = self.kwargs.get('pk')

        url = f"https://fiu-sandbox.setu.co/v2/consents/{consent_id}/fetch/status"
        headers = {
            "Content-Type": "application/json",
            "Authorization": request.headers.get('Authorization'),
            "x-product-instance-id":request.headers.get("x-product-instance-id")
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)

    
    
class FetchView(viewsets.GenericViewSet,generics.CreateAPIView,generics.RetrieveAPIView):
    queryset = None
    serializer_class = None

    def create(self, request ):
        data = request.data

        url = "https://fiu-sandbox.setu.co/v2/sessions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": request.headers.get('Authorization'),
            "x-product-instance-id":request.headers.get("x-product-instance-id")
        }

        response = requests.post(url,json=data,headers=headers)
        
        if response.status_code == 201:
            
            return Response(response.json(), status=status.HTTP_201_CREATED)
        else:
            
            return Response(response.json(), status=response.status_code)

    def retrieve(self, request, *args, **kwargs):

        id = self.kwargs.get('pk')

        url = f"https://fiu-sandbox.setu.co/v2/sessions/{id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": request.headers.get('Authorization'),
            "x-product-instance-id":request.headers.get("x-product-instance-id")
        }

        response = requests.get(url,headers=headers)
        if response.status_code == 201:
            return Response(response.json(), status=status.HTTP_201_CREATED)
        else:
            return Response(response.json(),status=response.status_code)
        
        
        
    