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
from authentication.models import UserProfile
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from agency_side.models import CreateNewAgencyTeam, CreateNewClientContainer
from .models import JoinAgencyTeamAsClient, CreateNewClientRequest, CreateNewClientTaskClientSide, CreateNewClientFolderClientSide, CreateNewClientFileClientSide
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.renderers import JSONRenderer

@api_view(["GET"])
def index(request):
    return Response({"message": "This is the agency client side"})


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def join_agency_team_as_client(request):
    current_user = request.user
    current_team_link = request.data.get("teamUniqueLink")
    current_client_container_name = request.data.get("currentClientContainerName")

    if JoinAgencyTeamAsClient.objects.filter(user=current_user, current_unique_link=current_team_link, current_team_name=current_client_container_name).exists():
        return Response({"message": "You have already joined the agency team as a client."}, status=status.HTTP_200_OK)
    
    new_team_client = JoinAgencyTeamAsClient.objects.create(user=current_user, current_unique_link=current_team_link, current_team_name=current_client_container_name, client_container_name=current_client_container_name)
    new_team_client.save()

    return Response({"message": "You have been added to the agency team as a client"})


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_clients_agency_teams(request):
    if request.user.is_authenticated:
        current_user = request.user
        client_teams_partof = JoinAgencyTeamAsClient.objects.filter(user=current_user)

        if client_teams_partof.exists():
            # Iterate over each instance in the queryset
            teams_data = []
            for team_partof in client_teams_partof:
                client_container_name = team_partof.client_container_name
                # Get the associated agency team using unique_link
                users_agency_team = CreateNewAgencyTeam.objects.filter(unique_link=team_partof.current_unique_link).first()
                if users_agency_team:
                    single_team_data = {
                        "team_name": users_agency_team.team_name,
                        "team_image": users_agency_team.team_image.url,
                        "team_unique_link": users_agency_team.unique_link,
                        "current_joined_client_container": client_container_name
                    }
                    teams_data.append(single_team_data)
                else:
                    return Response({"error": "No agency teams found for the current user."}, status=404)
            return Response(teams_data)
        else:
            return Response({"error": "User is not part of any agency teams."}, status=404)
    else:
        return Response({"error": "User is not authenticated."}, status=401)


# this doesnt work coz i am sending the team name instead of the actual client container name
# i need to associate a request with the join agency team as client model instead of doing it individually
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_new_client_request(request, currentTeamUniqueLink):
    current_user = request.user
    request_title = request.data.get("requestTitle")
    short_description = request.data.get("requestShortDescription")
    client_request_body = request.data.get("requestBody")
    actualCurrentClientContainerName = request.data.get("actualCurrentClientContainerName")

    client_name = actualCurrentClientContainerName.strip()
    print("currentTeamUniqueLink:", currentTeamUniqueLink)
    print("actualCurrentClientContainerName:", client_name)
    
    try:
        current_team_assigned = JoinAgencyTeamAsClient.objects.get(user=current_user, current_unique_link=currentTeamUniqueLink, current_team_name=actualCurrentClientContainerName, client_container_name=actualCurrentClientContainerName)

        new_client_request = CreateNewClientRequest.objects.create(
            user=current_user,
            request_title=request_title,
            clients_assigned_agency_team=current_team_assigned,
            short_description=short_description,
            client_request_body=client_request_body
        )
        
        return Response({"message": "Your new client request has been created for the team"}, status=status.HTTP_201_CREATED)
    
    except JoinAgencyTeamAsClient.DoesNotExist:
        return Response({"error": "JoinAgencyTeamAsClient matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_team_requests(request, currentTeamUniqueLink, currentClientContainer):
    current_user = request.user
    
    print("the recieved team link", currentTeamUniqueLink)
    print("the recieved client container name", currentClientContainer)
    
    client_joined_team = JoinAgencyTeamAsClient.objects.get(current_unique_link=currentTeamUniqueLink, client_container_name=currentClientContainer)
    
    requests_inside_team = CreateNewClientRequest.objects.filter(clients_assigned_agency_team=client_joined_team)
    client_requests_array = []

    for single_request in requests_inside_team:
        single_request_data = {
            "request_title": single_request.request_title,
            "short_description": single_request.short_description,
            "client_request_body": single_request.client_request_body,
            "date_requested": single_request.date_requested
        }

        client_requests_array.append(single_request_data)

    return Response(client_requests_array)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_client_request_detail(request, currentTeamUniqueLink, currentClientContainer, currentClientRequestTitle):
    assigned_agency_team_instance = JoinAgencyTeamAsClient.objects.get(client_container_name=currentClientContainer, current_unique_link=currentTeamUniqueLink)
    
    print("current team link", currentTeamUniqueLink)
    print("current client container name link", currentClientContainer)
    print("current client request title", currentClientRequestTitle)
    
    current_client_request = CreateNewClientRequest.objects.get(clients_assigned_agency_team=assigned_agency_team_instance, request_title=currentClientRequestTitle)
    
    single_request_data = {
        "request_title": current_client_request.request_title,
        "client_request_body": current_client_request.client_request_body,
        "date_requested": current_client_request.date_requested
    }
    
    return Response(single_request_data)
 
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_new_client_task_client_side(request, currentTeamLink, currentClientContainerName):
    current_user = request.user
    current_assigned_team_instance = JoinAgencyTeamAsClient.objects.get(client_container_name=currentClientContainerName, current_unique_link=currentTeamLink)
    task_title = request.data.get("taskTitle")
    task_short_description = request.data.get("taskDescription")
    task_due_date = request.data.get("taskDate")
    task_current_status = request.data.get("taskStatus")
    
    new_clients_task = CreateNewClientTaskClientSide.objects.create(user=current_user, task_title=task_title, task_short_description=task_short_description, task_due_date=task_due_date, task_current_status=task_current_status, current_assigned_team_for_client=current_assigned_team_instance)
    new_clients_task.save()
    
    return Response({"message": "the new client task has been added to the database"})


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_clients_request_they_made(request, currentTeamLink, currentClientContainerName):
    current_user = request.user
    current_assigned_team_instance = JoinAgencyTeamAsClient.objects.get(client_container_name=currentClientContainerName, current_unique_link=currentTeamLink)
    tasks_in_db = CreateNewClientTaskClientSide.objects.filter(current_assigned_team_for_client=current_assigned_team_instance)
    tasks_array = []
    
    for single_task in tasks_in_db:
        single_task_data = {
            "task_title": single_task.task_title,
            "task_short_description": single_task.task_short_description,
            "task_due_date": single_task.task_due_date,
            "task_current_status": single_task.task_current_status
        }
        
        tasks_array.append(single_task_data)
        
    return Response(tasks_array)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_new_client_folder_clientside(request, agencyTeamUniqueLink, agencyClientContainerName):
    current_user = request.user
    folder_name = request.data.get("folderName")
    
    current_assigned_agency_team = JoinAgencyTeamAsClient.objects.get(client_container_name=agencyClientContainerName, current_unique_link=agencyTeamUniqueLink)
    
    new_client_folder = CreateNewClientFolderClientSide.objects.create(user=current_user, current_assigned_team_for_client=current_assigned_agency_team, folder_name=folder_name)
    new_client_folder.save()
    
    return Response({"message": "The new client folder has been created"})

    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_clients_folders_client_side(request, agencyTeamUniqueLink, agencyClientContainerName):
    current_user = request.user
    current_assigned_team = JoinAgencyTeamAsClient.objects.get(client_container_name=agencyClientContainerName, current_unique_link=agencyTeamUniqueLink)
    
    all_client_folders = CreateNewClientFolderClientSide.objects.filter(current_assigned_team_for_client=current_assigned_team)
    folders_array = []
    
    for single_folder in all_client_folders:
        single_folder_data = {
            "foldername": single_folder.folder_name,
            "date_created": single_folder.date_created,
            "user_who_created": single_folder.user.username
        }
        
        folders_array.append(single_folder_data)
    
    return Response(folders_array)



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_new_client_file_clientside(request, agencyTeamUniqueLink, agencyClientContainerName, clientFolderName):
    current_user = request.user
    client_file_name = request.data.get("newFileName")
    client_file = request.FILES.get("newActualClientFile")
    client_file_extension = request.data.get("fileExtension")
    
    current_assigned_team_for_client = JoinAgencyTeamAsClient.objects.get(client_container_name=agencyClientContainerName, current_unique_link=agencyTeamUniqueLink)
    current_client_folder = CreateNewClientFolderClientSide.objects.get(current_assigned_team_for_client=current_assigned_team_for_client, folder_name=clientFolderName)
    
    new_client_file = CreateNewClientFileClientSide.objects.create(user=current_user, current_assigned_team_for_client=current_assigned_team_for_client, current_client_folder=current_client_folder, client_file_name=client_file_name, client_file=client_file, client_file_extension=client_file_extension)
    new_client_file.save()
    
    return Response({"message": "the new client file has been added to db"})


