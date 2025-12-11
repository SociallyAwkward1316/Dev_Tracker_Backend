from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated,AllowAny

from .serializers import UserRegisterSerializer, HomePageProjectListSerializer, ProjectCreateSerializer, IndividualProjectDetailSerializer
from .serializers import CreateCategorySerializer, CreateTaskSerializer
from .models import Projects, Categories, Tasks

# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens =response.data

            access_token = tokens['access']
            refresh_token = tokens['refresh']

            res = Response()

            res.data = {"success":True}

            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                path="/",
            )

            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                path="/",
            )
            return res

        except:
            return Response({"success":False})
        

class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token

            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']
            res = Response()
            res.data = {"refreshed":True}

            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="None",
                path="/",
            )

            return res
        except:
            return Response({"refreshed":False})
        

@api_view(['POST'])
def logout(request):
    res = Response({"logout":True})
    res.delete_cookie("access_token", path="/")
    res.delete_cookie("refresh_token", path="/")
    return res


@api_view(['POST'])
@permission_classes([AllowAny])
def RegisterUser(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True}, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProjectList(request):
    projects = Projects.objects.filter(user=request.user)
    serializer = HomePageProjectListSerializer(projects, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateProject(request):
    serializer = ProjectCreateSerializer(data=request.data, context={"request":request})
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


#----------Individual Project Detail Views... Detail/Create/Del ------#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IndividualProjectDetail(request, project_id):
    project = get_object_or_404(Projects, pk=project_id, user=request.user)
    serializer = IndividualProjectDetailSerializer(project)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateCategory(request, project_id):
    project = get_object_or_404(Projects, pk=project_id, user=request.user)
    serializer = CreateCategorySerializer(data=request.data, context={"project":project})
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateTask(request, category_id):
    category = get_object_or_404(Categories, pk=category_id, project__user=request.user)
    serializer = CreateTaskSerializer(data=request.data, context={"category":category})
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def ToggleTask(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    
    task.is_completed = not task.is_completed
    task.save()
    
    return Response({"success":True}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteProject(request, project_id):
    project = get_object_or_404(Projects, pk=project_id)
    if project.user != request.user:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    project.delete()
    return Response({"success":True}, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteCategory(request, category_id):
    category = get_object_or_404(Categories, pk=category_id)
     # Security check
    if category.project.user != request.user:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    category.delete()
    return Response({"success":True}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteTask(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    # Security check
    if task.category.project.user != request.user:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    task.delete()
    return Response({"success":True}, status=status.HTTP_200_OK)
    




    


