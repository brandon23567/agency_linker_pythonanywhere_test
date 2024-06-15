from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="agency_client_side_index"),
    path("join_agency_team_as_client/", views.join_agency_team_as_client, name="join_agency_team_as_client"),
    path("get_current_clients_agency_teams/", views.get_current_clients_agency_teams, name="get_current_clients_agency_teams"),
    path("create_new_client_request/<str:currentTeamUniqueLink>/", views.create_new_client_request, name="create_new_client_request"),
    path("get_current_team_requests/<str:currentTeamUniqueLink>/<str:currentClientContainer>/", views.get_current_team_requests, name="get_current_team_requests"),
    
    path("get_current_client_request_detail/<str:currentTeamUniqueLink>/<str:currentClientContainer>/<str:currentClientRequestTitle>/", views.get_current_client_request_detail, name="get_current_client_request_detail"),
    path("create_new_client_task_client_side/<str:currentTeamLink>/<str:currentClientContainerName>/", views.create_new_client_task_client_side, name="create_new_client_task_client_side"),
    path("get_current_clients_request_they_made/<str:currentTeamLink>/<str:currentClientContainerName>/", views.get_current_clients_request_they_made, name="get_current_clients_request_they_made"),
    
    path("create_new_client_folder_clientside/<str:agencyTeamUniqueLink>/<str:agencyClientContainerName>/", views.create_new_client_folder_clientside, name="create_new_client_folder_clientside"),
    path("get_current_clients_folders_client_side/<str:agencyTeamUniqueLink>/<str:agencyClientContainerName>/", views.get_current_clients_folders_client_side, name="get_current_clients_folders_client_side"),
    path("create_new_client_file_clientside/<str:agencyTeamUniqueLink>/<str:agencyClientContainerName>/<str:clientFolderName>/", views.create_new_client_file_clientside, name="create_new_client_file_clientside"),
]
