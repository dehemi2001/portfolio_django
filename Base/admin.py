from django.contrib import admin
from Base.models import User, Skill, Project, Contact

# Register your models here.
admin.site.register(User)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Contact)