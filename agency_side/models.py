from django.db import models
from authentication.models import User
from cloudinary.models import CloudinaryField


class CreateNewAgencyTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=500, unique=True)
    client_assigned = models.CharField(max_length=400, null=True, blank=True)
    team_image = CloudinaryField(resource_type="image", folder="team_profile_images", null=True, blank=True)
    unique_link = models.CharField(max_length=400)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name


class JoinAgencyTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team_unique_link = models.CharField(max_length=400)
    date_joined_team = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
    

class CreateNewClientContainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_team = models.ForeignKey(CreateNewAgencyTeam, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=400, unique=True)
    client_description = models.TextField()
    client_email = models.CharField(max_length=100)
    client_budget = models.CharField(max_length=200)
    date_assigned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name


class CreateNewClientTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_team = models.ForeignKey(CreateNewAgencyTeam, on_delete=models.CASCADE)
    current_client_container = models.ForeignKey(CreateNewClientContainer, on_delete=models.CASCADE)
    task_title = models.CharField(max_length=300)
    task_short_description = models.TextField()
    task_due_date = models.CharField(max_length=200)
    task_current_status = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task_title} - {self.current_client_container.client_name}"
    

class CreateNewClientFolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_team = models.ForeignKey(CreateNewAgencyTeam, on_delete=models.CASCADE)
    assigned_client_container = models.ForeignKey(CreateNewClientContainer, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.folder_name
    

class CreateNewClientFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_team = models.ForeignKey(CreateNewAgencyTeam, on_delete=models.CASCADE)
    assigned_client_container = models.ForeignKey(CreateNewClientContainer, on_delete=models.CASCADE)
    assigned_client_folder = models.ForeignKey(CreateNewClientFolder, on_delete=models.CASCADE)
    client_file_name = models.CharField(max_length=300)
    client_file = CloudinaryField(resource_type="auto", null=True, blank=True, folder="client_files/")
    client_file_extension = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_file_name



