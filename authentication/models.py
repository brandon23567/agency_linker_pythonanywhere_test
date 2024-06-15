from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

User = get_user_model()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_bio = models.TextField(max_length=300, null=True, blank=True)
    profile_img = CloudinaryField(resource_type="image", folder="user_profiles", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class AgencyUserSignup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agency_email = models.CharField(max_length=300)
    agency_profile_img = CloudinaryField(resource_type="image", folder="agency_profile_images", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class ClientUserSignup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_email = models.CharField(max_length=300)
    client_profile_img = CloudinaryField(resource_type="image", folder="client_user_profile_images", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
