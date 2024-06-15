from django.db import models
from authentication.models import User
from agency_side.models import CreateNewAgencyTeam, CreateNewClientContainer
from cloudinary.models import CloudinaryField

class JoinAgencyTeamAsClient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_team_name = models.CharField(max_length=400)
    client_container_name = models.CharField(max_length=500, default="testing123")
    current_unique_link = models.CharField(max_length=500)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class CreateNewClientRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_title = models.CharField(max_length=300)
    clients_assigned_agency_team = models.ForeignKey(JoinAgencyTeamAsClient, on_delete=models.CASCADE)
    short_description = models.TextField()
    client_request_body = models.TextField()
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.request_title


class CreateNewClientTaskClientSide(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_assigned_team_for_client = models.ForeignKey(JoinAgencyTeamAsClient, on_delete=models.CASCADE)
    task_title = models.CharField(max_length=300)
    task_short_description = models.TextField()
    task_due_date = models.CharField(max_length=200)
    task_current_status = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __tsr__(self):
        return self.task_title
    
    
class CreateNewClientFolderClientSide(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_assigned_team_for_client = models.ForeignKey(JoinAgencyTeamAsClient, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.folder_name
    
class CreateNewClientFileClientSide(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_assigned_team_for_client = models.ForeignKey(JoinAgencyTeamAsClient, on_delete=models.CASCADE)
    current_client_folder = models.ForeignKey(CreateNewClientFolderClientSide, on_delete=models.CASCADE)
    client_file_name = models.CharField(max_length=300)
    client_file = CloudinaryField(resource_type="auto", null=True, blank=True, folder="client_files_client_side/")
    client_file_extension = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.client_file_name