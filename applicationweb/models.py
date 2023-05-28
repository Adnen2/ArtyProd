
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Service(models.Model):
    SERVICE_CHOICES = [
        ('CG', 'Charte graphique'),
        ('OD', 'Objet 3D'),
        ('SC', 'Scénarisation'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    service_type = models.CharField(max_length=2, choices=SERVICE_CHOICES)

    def __str__(self):
        return self.title

class Team(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('AC', 'En cours'),
        ('FN', 'Fini'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    client_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    services = models.ManyToManyField(Service, through='Detail')
    
    def __str__(self):
        return self.title

class Detail(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')


class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.message

class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    linkedin_url = models.URLField(blank=True)
    personal_website_url = models.URLField(blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        default=lambda: getattr(get_user_model(), 'objects', None).get(id=1),
        blank=True
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content