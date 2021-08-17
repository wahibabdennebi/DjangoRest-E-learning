from django.shortcuts import render
from .models import Abonne
from rest_framework.generics import ListAPIView
from accounts.serializers import ViewUserSerializer, UpdateUserSerializer,LogoutSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics,status
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication

from rest_framework import generics, permissions,authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

class ListUsers(generics.GenericAPIView):
  
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [BasicAuthentication,]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
    
        user =Abonne.objects.values()
        # if not ParticipantsAccounts.is_superuser:
        # user.get()
        # user = get_user_model()
        # user.objects.all()
        return Response(user)
    


class ProfileAPI(APIView):
    authentication_classes = [BasicAuthentication,]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Abonne, pk=kwargs['user_id'])
        profile_serializer = ViewUserSerializer(user)
        return Response(profile_serializer.data)

# update user
class UpdateUserView(generics.UpdateAPIView):
    queryset = Abonne.objects.all()
    authentication_classes = [BasicAuthentication,]
    # permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = UpdateUserSerializer
    

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    authentication_classes = [BasicAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileUser(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.email for user in Abonne.objects.all()]
        # content ={
        #     'user' :str(request.user),
        #     'auth' :str(request.auth)
        # }
        return Response(usernames)





# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })



