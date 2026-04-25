from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

# Create your models here.

# It's a best practice to extend the User model using a One-to-One relationship
# with a profile model instead of modifying the built-in User model directly.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    designation = models.CharField(max_length=100)
    description = models.TextField(help_text="Short description for hero section.")
    about_me = models.TextField(help_text="Longer description for about section.")
    contact_description = models.TextField(blank=True, help_text="Text for the contact section.")
    phone = models.CharField(max_length=20, blank=True)
    experience = models.CharField(max_length=50, help_text="e.g., '5+ Years'")
    location = models.CharField(max_length=100)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    image1 = models.ImageField(upload_to='profile_images/', help_text="Image for hero section.")
    image2 = models.ImageField(upload_to='profile_images/', help_text="Image for about section.")
    cv = models.FileField(upload_to='cvs/')

    def __str__(self):
        return self.user.username

class Experience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='experiences')
    name = models.CharField(max_length=200, help_text="Name of the qualification or job title.")
    company = models.CharField(max_length=200, help_text="Name of the institution or company.")
    description = models.TextField(blank=True, help_text="Optional description of your role or achievements.")
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} at {self.company}"

class Skill(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Percentage from 0 to 100")
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Tool(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tools')
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='tool_icons/', help_text="Upload an icon for the tool (SVG, PNG, JPG, etc.).", validators=[FileExtensionValidator(['svg', 'png', 'jpg', 'jpeg'])])
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['name']

class Project(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/')
    live_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    order = models.PositiveIntegerField()
    technologies = models.ManyToManyField(Technology, through='ProjectTechnology')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ('project', 'technology')
        verbose_name = "Project Technology"
        verbose_name_plural = "Project Technologies"

    def __str__(self):
        return f"{self.project.name} - {self.technology.name}"

class Contact(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

# --- Signal Handlers for File Cleanup ---

@receiver(pre_save, sender=UserProfile)
@receiver(pre_save, sender=Project)
@receiver(pre_save, sender=Tool)
def delete_old_file_on_update(sender, instance, **kwargs):
    """
    When a model instance with a file is updated, this signal handler
    deletes the old file from the filesystem if a new file has been uploaded.
    """
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return  # Instance is new, no old file to delete.

    # Iterate over all fields in the model to find FileFields or ImageFields
    for field in sender._meta.fields:
        if isinstance(field, (models.FileField, models.ImageField)):
            old_file = getattr(old_instance, field.name)
            new_file = getattr(instance, field.name)

            # If an old file exists and it's different from the new file, delete it.
            if old_file and old_file != new_file:
                old_file.delete(save=False)


@receiver(post_delete, sender=UserProfile)
@receiver(post_delete, sender=Project)
@receiver(post_delete, sender=Tool)
def delete_file_on_delete(sender, instance, **kwargs):
    """
    When a model instance with a file is deleted, this signal handler
    deletes the associated file from the filesystem.
    """
    for field in sender._meta.fields:
        if isinstance(field, (models.FileField, models.ImageField)):
            file_to_delete = getattr(instance, field.name)
            if file_to_delete:
                file_to_delete.delete(save=False)

@receiver(post_save, sender=ProjectTechnology)
@receiver(post_delete, sender=ProjectTechnology)
def cleanup_orphan_technologies(sender, **kwargs):
    """
    Cleans up any technologies that are not associated with any project.
    Uses transaction.on_commit to ensure it only runs after the save/delete
    is fully complete, avoiding issues during multi-row admin saves.
    """
    transaction.on_commit(lambda: Technology.objects.filter(projecttechnology__isnull=True).delete())

