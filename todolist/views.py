from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import TodoItem
from todolist.serializers import TodoItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# class TodoItemView(APIView):
   
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         # todos = TodoItem.objects.all()
#         todos = TodoItem.objects.filter(author=request.user)
#         serializer = TodoItemSerializer(todos, many=True)
#         return Response(serializer.data)


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
        
# class CreateTodoItemView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request, format=None):
#         title = request.data.get('title')
#         chacked = request.data.get('chacked')
#         if title is None:
#             return Response({"error": "Titel fehlt"}, status=400)
#         author= request.user
#         new_todo = TodoItem.objects.create( title=title, author=author,chacked=chacked)
#         serializer = TodoItemSerializer(new_todo)
#         return Response(serializer.data, status=201)

class TodoItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        todos = TodoItem.objects.filter(author=request.user)
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        title = request.data.get('title')
        chacked = request.data.get('chacked')
        if title is None:
            return Response({"error": "Titel fehlt"})
        author = request.user
        new_todo = TodoItem.objects.create(title=title, author=author, chacked=chacked)
        serializer = TodoItemSerializer(new_todo)
        return Response(serializer.data)
    
    # def put(self, request, pk, format=None):
    #     todo = TodoItem.objects.get(pk=pk)
    #     serializer = TodoItemSerializer(todo, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=400)