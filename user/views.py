from ast import If
import json
import uuid
from rest_framework.decorators import api_view, permission_classes
import requests
from votingBackend.settings import SIMPLE_JWT

from .serializers import UserSerializer
from .models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
import jwt
import datetime
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["GET"])
def welcome(request):
    content = {"message": "Welcome to the User's Endpoint!"}
    return JsonResponse(content)

@api_view(["POST"])
def login(request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()

    if user is None:
        raise AuthenticationFailed('User Not Found')

    if user.check_password(password):
        raise AuthenticationFailed('Incorrect Password')

    refresh = RefreshToken.for_user(user)

    response = Response()

    response.data = {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }
    response.set_cookie(key='jwt', value=str(refresh), httponly=True)

    return response


@api_view(["GET"])
def get_profile(request):
    token = request.headers['Authorization']

    if not token:
        raise AuthenticationFailed('User Not Authenticated!')

    try:
        payload = jwt.decode(
            token,
            SIMPLE_JWT['SIGNING_KEY'],
            algorithms=[SIMPLE_JWT['ALGORITHM']]
        )

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('User Not Authenticated!')

    users = User.objects.filter(id=payload['user_id']).first()

    serializer = UserSerializer(users, many=False)
    return Response({'success': 'true', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user_profile(request,user_id):
    user = User.objects.filter(id=user_id).first()

    serializer = UserSerializer(user, many=False)
    return Response({'success': 'true', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }


@api_view(["POST"])
def register(request):
    req = json.loads(json.dumps(request.data))
    email = req["email"]
    url = "https://api.luxand.cloud/photo/search"
    payload = { "photo": req["photo"] }
    headers = { 'token': "b4a771e51ce54de2a65841db6d8259f1" }
    files = {}
    response1 = requests.request("POST", url, data=payload, headers=headers, files=files)
    if (response1.text == '[]\n'):
        # face doesn't exist in db
        req = json.loads(json.dumps(request.data))
        url = "https://api.luxand.cloud/subject/v2"
        payload = {"name":req["last_name"]+" "+req["first_name"]+str(uuid.uuid1()),"store":"1", "photo": req["photo"]}
        headers = { 'token': "b4a771e51ce54de2a65841db6d8259f1" }
        files = {}
        response = requests.request("POST", url, data=payload, headers=headers, files=files)
        resp = json.loads(response.text)
        face_id = resp["id"]
        image_url = resp["url"]

        # add face to person
        req = json.loads(json.dumps(request.data))
        url = "https://api.luxand.cloud/subject/"+str(face_id)
        payload = {"store":"1", "photo": image_url}
        headers = { 'token': "b4a771e51ce54de2a65841db6d8259f1" }
        files = {}
        response = requests.request("POST", url, data=payload, headers=headers, files=files)

        resp1 = json.loads(response.text)
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        currentUser = User.objects.filter(email=email).update(face_id=face_id, image_url=image_url)
        # currentUser.save()

        status_code = status.HTTP_201_CREATED
        message = 'User registered  successfully'
    else:
        status_code = status.HTTP_302_FOUND
        message  = "Face Already Exists"

    # send email for verification
    fresponse = {
        'success': 'True',
        'status_code': status_code,
        'message': message
    }
    return Response(fresponse)


@api_view(["PUT"])
def update_profile(request, user_id):
    return
    # payload = json.loads(request.body)
    # try:
    #     poll_item = Poll.objects.filter(id=poll_id)
    #     # returns 1 or 0
    #     poll_item.update(**payload)
    #     poll = Poll.objects.get(id=poll_id)
    #     serializer = PollSerializer(poll)
    #     return JsonResponse({'poll': serializer.data}, safe=False, status=status.HTTP_200_OK)
    # except ObjectDoesNotExist as e:
    #     return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    # except Exception:
    #     return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
