from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Projects, Categories, Tasks

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']

        )
        user.set_password(validated_data['password'])

        user.save()
        return user
    


class HomePageProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ['id', 'title', 'description']


class ProjectCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ['id', 'title', 'description']

    def create(self, validated_data):
        user = self.context['request'].user
        return Projects.objects.create(
            user = user,
            title = validated_data['title'],
            description = validated_data['description'],
        )
    

#-----------Individual Project Serializers + Nested Serializers for Project-------#
class ProjectDetailTaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'is_completed']


class ProjectDetailCategorySerializer(serializers.ModelSerializer):
    tasks = ProjectDetailTaskSerializer(many=True, read_only=True)
    class Meta:
        model = Categories
        fields = ['id', 'title', 'tasks']


class IndividualProjectDetailSerializer(serializers.ModelSerializer):
    categories = ProjectDetailCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Projects
        fields = ['id','title', 'description', 'categories']


class CreateCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['id', 'title']

    def create(self, validated_data):
        project = self.context['project']

        return Categories.objects.create(
            project=project,
            title=validated_data['title']
        )
    

class CreateTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = ['id', 'title']

    def create(self, validated_data):
        category = self.context['category']
        return Tasks.objects.create(
            category = category,
            title = validated_data['title']
        )


