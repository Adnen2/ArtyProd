from django.contrib import admin
from .models import Project, Service, Team, Detail, ContactMessage,TeamMember,Portfolio,Comment

admin.site.register(Project)
admin.site.register(Service)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Detail)
admin.site.register(ContactMessage)
admin.site.register(Portfolio)
admin.site.register(Comment)