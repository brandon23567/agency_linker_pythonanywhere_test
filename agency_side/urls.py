from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="agency_side_index"),
    path("create_new_agency_team/", views.create_new_agency_team, name="create_new_agency_team"),
    path("join_agency_team/<str:agency_unique_link>/", views.join_agency_team, name="join_agency_team"),

    path("get_user_teams/", views.get_user_teams, name="get_user_teams"),
    path("go_to_agency_team_detail/<str:agency_unique_link>/", views.go_to_agency_team_detail, name="go_to_agency_team_detail"),

    path("create_new_client_container/", views.create_new_client_container, name="create_new_client_container"),
    path("get_client_containers_inside_agency_team/<str:actualCurrentTeamContainerName>/", views.get_client_containers_inside_agency_team, name="get_client_containers_inside_agency_team"),
    path("create_new_client_task/", views.create_new_client_task, name="create_new_client_task"),
    path("get_all_tasks_inside_client_container/<str:actualTeamUniqueLink>/client_container/<str:actualClientContainerName>/", views.get_all_tasks_inside_client_container, name="get_all_tasks_inside_client_container"),
    path("create_new_client_folder/<str:actualTeamUniqueLink>/create_new_container/<str:actualClientName>/", views.create_new_client_folder, name="create_new_client_folder"),
    path("get_folders_inside_current_container/<str:actualTeamUniqueLink>/client_folders/<str:actualClientName>/", views.get_folders_inside_current_container, name="get_folders_inside_current_container"),
    path("create_new_client_file/<str:actualTeamUniqueLink>/create_client_file/<str:actualClientName>/<str:clientFolderName>/", views.create_new_client_file, name="create_new_client_file"),

    path("get_all_client_files_inside_client_container/<str:actualTeamUniqueLink>/client_files/<str:actualClientName>/<str:clientFolderName>/", views.get_all_client_files_inside_client_container, name="get_all_client_files_inside_client_container"),
    path("get_current_team_members_inside_team/<str:actualCurrentTeamUniqueLink>/", views.get_current_team_members_inside_team, name="get_current_team_members_inside_team"),

    path("get_all_client_requests_inside_container/<str:currentTeamUniqueLink>/<str:currentClientContainer>/", views.get_all_client_requests_inside_container, name="get_all_client_requests_inside_container"),
    
    path("get_current_client_request_detail/<str:currentTeamUniqueLink>/<str:currentClientContainer>/<str:currentClientRequestTitle>/", views.get_current_client_request_detail, name="get_current_client_request_detail"),
]


