from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import (
    UserProfile,
    Experience,
    Skill,
    Tool,
    Technology,
    Project,
    ProjectTechnology,
    Contact
)

# Register your models here.
admin.site.unregister(Group)

# --- Inlines ---

# Inline for UserProfile to be attached to the main User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# Inline for Project to manage its technologies
class ProjectTechnologyInline(admin.StackedInline):
    model = ProjectTechnology
    extra = 1
    ordering = ['order']
    autocomplete_fields = ['technology']

# --- ModelAdmins ---

class SingleUserProfileMixin:
    exclude = ('user_profile',)

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'user_profile_id', None):
            obj.user_profile = UserProfile.objects.first()
        super().save_model(request, obj, form, change)

# Custom User admin to include the UserProfile
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

@admin.register(Experience)
class ExperienceAdmin(SingleUserProfileMixin, admin.ModelAdmin):
    list_display = ('name', 'company', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'company')

@admin.register(Skill)
class SkillAdmin(SingleUserProfileMixin, admin.ModelAdmin):
    list_display = ('name', 'percentage', 'order')
    list_editable = ('order',)
    search_fields = ('name',)

@admin.register(Tool)
class ToolAdmin(SingleUserProfileMixin, admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(SingleUserProfileMixin, admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    inlines = [ProjectTechnologyInline]

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    def has_module_permission(self, request):
        """Hides the Technology model from the main admin index but allows it to be accessed for autocomplete and green plus."""
        return False

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    exclude = ('user_profile',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# Re-register User model with our custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
