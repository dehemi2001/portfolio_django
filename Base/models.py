from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    avatar = models.ImageField(upload_to='avatars/')
    description = models.TextField()
    email = models.EmailField()
    number = models.CharField(max_length=20)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # This logic handles the deletion of old files when new ones are uploaded.
        if self.pk:
            try:
                old_instance = User.objects.get(pk=self.pk)

                # Check if the avatar has changed and delete the old one.
                if old_instance.avatar and old_instance.avatar != self.avatar:
                    old_instance.avatar.delete(save=False)

                # Check if the resume has changed and delete the old one.
                if old_instance.resume and old_instance.resume != self.resume:
                    old_instance.resume.delete(save=False)
            except User.DoesNotExist:
                # This happens when creating a new user, so we do nothing.
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Also delete files from storage when a User object is deleted.
        self.avatar.delete(save=False)
        self.resume.delete(save=False)
        super().delete(*args, **kwargs)

class Skill(models.Model):
    name = models.CharField(max_length=50)
    percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    color = models.CharField(max_length=20, help_text="Hex color code, e.g., #RRGGBB", blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name= models.CharField(max_length=40)
    email=models.EmailField(max_length=40)
    content=models.TextField(max_length=400)
    number=models.CharField(max_length=12)

    def __str__(self):
        return self.name