from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import auth
from rest_framework import status
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from django.contrib.auth.models import User
from authentication.models import UserProfile, AgencyUserSignup, ClientUserSignup
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.decorators import login_required
from .models import CreateNewAgencyTeam, JoinAgencyTeam, CreateNewClientContainer, CreateNewClientTask, CreateNewClientFolder, CreateNewClientFile
import random
import string
from agency_client_side.models import CreateNewClientRequest, JoinAgencyTeamAsClient
from django.http import JsonResponse
import requests
import re


@api_view(["GET"])
def index(request):
    return Response({"message": "This is the agency side"})

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_new_agency_team(request):
    team_name = request.data.get("teamName")
    team_assigned_client = request.data.get("teamAssignedClient")
    team_profile_img = request.FILES.get("teamProfileImg")
    current_user = request.user
    random_generated_text = generate_random_string(20)
    
    team_unique_link = f"${random_generated_text}-${team_name}"

    new_agency_team = CreateNewAgencyTeam.objects.create(user=current_user, team_name=team_name, client_assigned=team_assigned_client, team_image=team_profile_img, unique_link=team_unique_link)
    new_agency_team.save()
    
    return Response({"message": "created the new team", "agency_team_unique_link": team_unique_link})


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def join_agency_team(request, agency_unique_link):
    current_user = request.user
    agency_link = request.data.get("agencyUniqueLink")

    try:
        agency_team = CreateNewAgencyTeam.objects.get(unique_link=agency_link)
    except CreateNewAgencyTeam.DoesNotExist:
        return Response({"message": "The agency link is not valid. Please create a new team instead."}, status=status.HTTP_404_NOT_FOUND)
    
    if JoinAgencyTeam.objects.filter(user=current_user, team_unique_link=agency_link).exists():
        return Response({"message": "You are already part of the organization"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the join record
    join_record = JoinAgencyTeam.objects.create(user=current_user, team_unique_link=agency_link)
    join_record.save()
    
    return Response({"message": "You have successfully joined the organization."}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_teams(request):
    current_user = request.user
    user_teams = JoinAgencyTeam.objects.filter(user=current_user)

    team_details = []
    for team_join_record in user_teams:
        team_unique_link = team_join_record.team_unique_link
        try:
            team = CreateNewAgencyTeam.objects.get(unique_link=team_unique_link)
            num_members = JoinAgencyTeam.objects.filter(team_unique_link=team_unique_link).count()
            team_detail = {
                'team_name': team.team_name,
                'team_unique_link': team.unique_link,
                'client_assigned': team.client_assigned,
                'team_image': team.team_image.url if team.team_image else None,
                'user_who_created': team.user.username,
                'num_members': num_members
            }
            team_details.append(team_detail)
        except CreateNewAgencyTeam.DoesNotExist:
            pass

    return Response({"user_teams": team_details}, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def go_to_agency_team_detail(request, agency_unique_link):
    current_agency_team = get_object_or_404(CreateNewAgencyTeam, unique_link=agency_unique_link)

    context = {
        "team_name": current_agency_team.team_name,
        "client_assigned": current_agency_team.client_assigned,
        "agency_team_image": current_agency_team.team_image.url,
        "agency_unique_link": current_agency_team.unique_link
    }

    return Response(context)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_new_client_container(request):
    current_user = request.user
    client_name = request.data.get("clientName")
    client_description = request.data.get("clientDescription")
    client_email = request.data.get("clientEmail")
    client_budget = request.data.get("clientBudget")
    team_unique_link = request.data.get("currentTeamUniqueLink")

    try:
        current_team_join = JoinAgencyTeam.objects.get(team_unique_link=team_unique_link)
        current_team = CreateNewAgencyTeam.objects.get(unique_link=team_unique_link)
    except JoinAgencyTeam.DoesNotExist:
        return Response({"message": "No such client container, please create a new one"}, status=status.HTTP_404_NOT_FOUND)
    except CreateNewAgencyTeam.DoesNotExist:
        return Response({"message": "No such client container, please create a new one"}, status=status.HTTP_404_NOT_FOUND)

    if current_team.user.username != current_user.username:
        return Response({"message": "Only user who created team can add new client container"}, status=status.HTTP_403_FORBIDDEN)

    new_client_container = CreateNewClientContainer.objects.create(
        user=current_user,
        client_name=client_name,
        client_description=client_description,
        client_email=client_email,
        client_budget=client_budget,
        assigned_team=current_team
    )

    new_client_container.save()

    return Response({"message": "New client container has been created"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_client_containers_inside_agency_team(request, actualCurrentTeamContainerName):
    current_user = request.user

    try:
        team = CreateNewAgencyTeam.objects.get(unique_link=actualCurrentTeamContainerName)
    except CreateNewAgencyTeam.DoesNotExist:
        return Response({"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

    if not JoinAgencyTeam.objects.filter(user=current_user, team_unique_link=actualCurrentTeamContainerName).exists():
        return Response({"message": "You are not authorized to view this team"}, status=status.HTTP_403_FORBIDDEN)

    client_containers = CreateNewClientContainer.objects.filter(assigned_team=team)

    client_containers_data = []
    for container in client_containers:
        container_data = {
            'client_name': container.client_name,
            'client_description': container.client_description,
            'client_email': container.client_email,
            'client_budget': container.client_budget,
        }
        client_containers_data.append(container_data)

    team_detail = {
        'team_name': team.team_name,
        'team_unique_link': team.unique_link,
        'client_assigned': team.client_assigned,
        'team_image': team.team_image.url if team.team_image else None,
        'user_who_created': team.user.username,
        'num_members': JoinAgencyTeam.objects.filter(team_unique_link=team.unique_link).count(),
        'client_containers': client_containers_data
    }

    return Response({"team_details": team_detail}, status=status.HTTP_200_OK)



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_new_client_task(request):
    current_user = request.user
    task_title = request.data.get("taskTitle")
    task_short_description = request.data.get("taskDescription")
    task_due_date = request.data.get("taskDate")
    task_current_status = request.data.get("taskStatus")
    current_team_unique_link = request.data.get("currentTeamUniqueLink")
    client_container_name_from_frontend = request.data.get("currentTeamName")

    try:
        current_team_instance = CreateNewAgencyTeam.objects.get(unique_link=current_team_unique_link)
        # current_client_container_instance = CreateNewClientContainer.objects.filter(assigned_team=current_team_instance).first()
        current_client_container_instance = CreateNewClientContainer.objects.get(client_name=client_container_name_from_frontend)
    except CreateNewAgencyTeam.DoesNotExist:
        return Response({"message": "No such team exists, please create a new one"}, status=status.HTTP_404_NOT_FOUND)
    except CreateNewClientContainer.DoesNotExist:
        return Response({"message": "No client container assigned to this team, please create a new one"}, status=status.HTTP_404_NOT_FOUND)

    # Check if there are multiple client containers assigned to the team
    if current_client_container_instance is None:
        return Response({"message": "No client container assigned to this team, please create a new one"}, status=status.HTTP_404_NOT_FOUND)

    # Create new client task instance
    new_client_task = CreateNewClientTask.objects.create(
        user=current_user,
        assigned_team=current_team_instance,
        current_client_container=current_client_container_instance,
        task_title=task_title,
        task_short_description=task_short_description,
        task_due_date=task_due_date,
        task_current_status=task_current_status
    )

    return Response({"message": "New client task has been created"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_tasks_inside_client_container(request, actualTeamUniqueLink, actualClientContainerName):
    try:
        team = get_object_or_404(CreateNewAgencyTeam, unique_link=actualTeamUniqueLink)

        tasks = CreateNewClientTask.objects.filter(
            assigned_team=team,
            current_client_container__client_name=actualClientContainerName
        )

        task_data = []
        for task in tasks:
            task_detail = {
                'task_title': task.task_title,
                'task_short_description': task.task_short_description,
                'task_due_date': task.task_due_date,
                'task_current_status': task.task_current_status,
            }
            task_data.append(task_detail)

        return Response({"tasks": task_data}, status=HTTP_200_OK)

    except CreateNewClientTask.DoesNotExist:
        return Response({"message": "No tasks found for the specified client container"}, status=HTTP_404_NOT_FOUND)



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_new_client_folder(request, actualTeamUniqueLink, actualClientName):
    current_user = request.user
    client_folder_name = request.data.get("clientFolderName")

    current_agency_team = get_object_or_404(CreateNewAgencyTeam, unique_link=actualTeamUniqueLink)
    current_client_container = get_object_or_404(CreateNewClientContainer, client_name=actualClientName)

    new_client_folder = CreateNewClientFolder.objects.create(user=current_user, assigned_team=current_agency_team, assigned_client_container=current_client_container, folder_name=client_folder_name)
    new_client_folder.save()

    return Response({"message": "New client folder has been created"})


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_folders_inside_current_container(request, actualTeamUniqueLink, actualClientName):
    current_user = request.user
    
    current_assigned_team = get_object_or_404(CreateNewAgencyTeam, unique_link=actualTeamUniqueLink)
    current_assigned_client_container = get_object_or_404(CreateNewClientContainer, client_name=actualClientName)
    folders_in_backend = CreateNewClientFolder.objects.filter(assigned_team=current_assigned_team, assigned_client_container=current_assigned_client_container)


    folders_array = []

    for single_folder in folders_in_backend:
        single_folder_data = {
            "folder_name": single_folder.folder_name,
            "date_created": single_folder.date_created,
            "user_who_created": single_folder.user.username
        }

        folders_array.append(single_folder_data)

    return Response(folders_array)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_new_client_file(request, actualTeamUniqueLink, actualClientName, clientFolderName):
    current_user = request.user
    current_assigned_team = get_object_or_404(CreateNewAgencyTeam, unique_link=actualTeamUniqueLink)
    current_assigned_client_container = get_object_or_404(CreateNewClientContainer, client_name=actualClientName)
    client_file_name = request.data.get("newFileName")
    client_actual_file = request.FILES.get("newActualClientFile")
    client_file_extension = request.data.get("fileExtension")

    current_client_folder_name = CreateNewClientFolder.objects.get(assigned_team=current_assigned_team, assigned_client_container=current_assigned_client_container, folder_name=clientFolderName)

    response = 200

    if response == 200:
        new_client_file = CreateNewClientFile.objects.create(
            user=current_user,
            assigned_team=current_assigned_team,
            assigned_client_container=current_assigned_client_container,
            assigned_client_folder=current_client_folder_name,
            client_file_name=client_file_name,
            client_file=client_actual_file,
            client_file_extension=client_file_extension
        )
        return Response({"message": "New client file has been created"})
    else:
        return Response({"message": "Failed to upload file"})


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_client_files_inside_client_container(request, actualTeamUniqueLink, actualClientName, clientFolderName):
    current_user = request.user
    current_assigned_team = get_object_or_404(CreateNewAgencyTeam, unique_link=actualTeamUniqueLink)
    current_assigned_client_container = get_object_or_404(CreateNewClientContainer, client_name=actualClientName)
    current_client_folder = get_object_or_404(CreateNewClientFolder, assigned_team=current_assigned_team, assigned_client_container=current_assigned_client_container, folder_name=clientFolderName)

    client_files = CreateNewClientFile.objects.filter(assigned_client_folder=current_client_folder)

    client_files_array = []

    for single_file in client_files:
        single_file_data = {
            "file_name": single_file.client_file_name,
            "file_extension": single_file.client_file_extension,
            "user_who_uploaded": single_file.user.username,
            "date_uploaded": single_file.date_created,
            "file_path": single_file.client_file.url
        }

        client_files_array.append(single_file_data)


    return Response(client_files_array)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_team_members_inside_team(request, actualCurrentTeamUniqueLink):
    try:
        team = CreateNewAgencyTeam.objects.get(unique_link=actualCurrentTeamUniqueLink)
        team_members = JoinAgencyTeam.objects.filter(team_unique_link=actualCurrentTeamUniqueLink)
        
        members_data = []
        for member in team_members:
            user = member.user
            team_member_user_profile = AgencyUserSignup.objects.get(user=user)
            member_data = {
                'username': user.username,
                'email': user.email,
                'profile_img': team_member_user_profile.agency_profile_img.url
            }
            members_data.append(member_data)

        return Response({"team_members": members_data}, status=HTTP_200_OK)

    except CreateNewAgencyTeam.DoesNotExist:
        return Response({"message": "Team not found"}, status=HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_client_requests_inside_container(request, currentTeamUniqueLink, currentClientContainer):
    try:
        assigned_agency_team_instance = JoinAgencyTeamAsClient.objects.get(client_container_name=currentClientContainer, current_unique_link=currentTeamUniqueLink)
        client_requests = CreateNewClientRequest.objects.filter(clients_assigned_agency_team=assigned_agency_team_instance)

        # Prepare response data
        client_requests_array = []
        for single_request in client_requests:
            single_request_data = {
                "request_title": single_request.request_title,
                "short_description": single_request.short_description,
                "client_request_body": single_request.client_request_body,
                "date_requested": single_request.date_requested
            }
            client_requests_array.append(single_request_data)

        return Response(client_requests_array)
        
    except (JoinAgencyTeamAsClient.DoesNotExist, CreateNewClientContainer.DoesNotExist):
        return JsonResponse({'error': 'Agency team or client container not found for the provided unique link or name.'}, status=404)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_client_request_detail(request, currentTeamUniqueLink, currentClientContainer, currentClientRequestTitle):
    current_user = request.user
    
    assigned_agency_team_instance = JoinAgencyTeamAsClient.objects.get(client_container_name=currentClientContainer, current_unique_link=currentTeamUniqueLink)
    
    current_client_request = CreateNewClientRequest.objects.get(clients_assigned_agency_team=assigned_agency_team_instance, request_title=currentClientRequestTitle)
    
    single_request_data = {
        "request_title": current_client_request.request_title,
        "client_request_body": current_client_request.client_request_body,
        "date_requested": current_client_request.date_requested
    }
    
    return Response(single_request_data)




