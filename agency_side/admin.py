from django.contrib import admin
from .models import CreateNewAgencyTeam, JoinAgencyTeam, CreateNewClientContainer, CreateNewClientTask, CreateNewClientFolder, CreateNewClientFile

admin.site.register(CreateNewAgencyTeam)
admin.site.register(JoinAgencyTeam)
admin.site.register(CreateNewClientContainer)
admin.site.register(CreateNewClientTask)
admin.site.register(CreateNewClientFolder)
admin.site.register(CreateNewClientFile)


