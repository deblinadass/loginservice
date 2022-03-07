from hstloginservice.serializer.hstloginserializer import LoginViaGripSerializer
from hstloginservice.model.hstloginmodel import Login
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime



@csrf_exempt
def get_user(pk):
    try:
        return Login.objects.getUser(pk)
    except Login.DoesNotExist:
        return ''

@api_view(["post"])
def LoginViaGrip(request):
    if request.data['role'] == ['User','Admin','Read']:
        usergroup = '01000010'
    pk = request.data['id']
    loginuser = get_user(pk)
    serializer = LoginViaGripSerializer(data=request.data)
    data=''
    
    if serializer.is_valid():
        if loginuser == '':
            serializer.save(usergroup=usergroup,useractive='1')
            response = Response(request.data,status=status.HTTP_201_CREATED,content_type="application/json")
            response['Location'] = "https://api.example.com/v1/users/"+ request.data['id']
            return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["put"])
def UpdateViaGrip(request):
        pk = request.data['id']
        loginuser = get_user(pk)
        serializerbefore = LoginViaGripSerializer(loginuser).data

        

        serializer = LoginViaGripSerializer(loginuser, data=request.data)
        now = datetime.now()
        if request.data['role'] == ['Admin','Read']:
            usergroupupdate = '01000011'
        if serializer.is_valid():
            serializer.save(updateddate=now,usergroup=usergroupupdate)
            response = Response(request.data, status=status.HTTP_200_OK, content_type="application/json")
            response['Location'] = "https://api.example.com/v1/users/"+ request.data['id']
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["delete"])   
def DeleteViaGrip(request,pk):
        loginuser = get_user(pk)
        serializer = LoginViaGripSerializer(loginuser)
        data=''
        if serializer.data:
            Login.objects.filter(gripid=pk).delete()
        return Response(status=status.HTTP_200_OK)

