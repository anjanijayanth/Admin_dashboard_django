from django.contrib import admin

# Register your models here.

from . import models
admin.site.register(models.User)
admin.site.register(models.AgencyDetail)
admin.site.register(models.Organization)
admin.site.register(models.Module)
admin.site.register(models.PermissionRule)
admin.site.register(models.UserPermission)
admin.site.register(models.AgentStatusLogs)
admin.site.register(models.StaffDetail)
admin.site.register(models.Product)
admin.site.register(models.AgentDetail)



