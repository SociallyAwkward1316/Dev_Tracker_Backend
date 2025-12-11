from django.urls import path
from .views import (CustomTokenObtainPairView,CustomRefreshTokenView, logout, RegisterUser, ProjectList, CreateProject, IndividualProjectDetail,
                    CreateCategory, CreateTask, ToggleTask,DeleteProject, DeleteCategory, DeleteTask)

urlpatterns = [
   path('login/', CustomTokenObtainPairView.as_view(), name='login'),
   path('refresh/', CustomRefreshTokenView.as_view(), name='refresh'),
   path('register/', RegisterUser, name='register'),
   path("logout/", logout, name="logout"),

   #------ API Home Page ENDPOINTS -------#
   path('project_list/', ProjectList, name='home'),
   path('create_project/', CreateProject, name='create_project'),
   #------ API Project Detail/Create ENDPOINTS ------#
   path('project/<int:project_id>/', IndividualProjectDetail, name="project_detail" ),
   path('project/<int:project_id>/create_category/', CreateCategory, name="create_category"),
   path('project/category/<int:category_id>/create_task/', CreateTask, name="create_task"),
   path('project/task/<int:task_id>/toggle/', ToggleTask, name="toggle_task"),
   path('project/<int:project_id>/delete/', DeleteProject, name="delete_project"),
   path('project/task/<int:task_id>/delete/', DeleteTask, name="delete_task"),
   path('project/category/<int:category_id>/delete/', DeleteCategory, name="delete_category"),

]