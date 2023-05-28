from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Service, Team, Detail, ContactMessage,TeamMember,Portfolio, Comment
from .forms import ContactForm, ProjectForm,CommentForm,UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

def index(request):
    projects = Project.objects.all()
    projects_count = Project.objects.filter(status='FN').count()
    contacts_count = ContactMessage.objects.count()
    comment_count = Comment.objects.count()
    services = Service.objects.all()
    member = TeamMember.objects.all()
    portfolio = Portfolio.objects.all()
    return render(request, 'index.html', {'projects': projects, 'services': services, 'member': member ,'portfolio': portfolio, 'projects_count': projects_count, 'contacts_count': contacts_count, 'comment_count': comment_count})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    comments = Comment.objects.filter(project_id=project_id)
    details = Detail.objects.filter(project=project)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            return redirect('project_detail', project_id=project_id)
    else:
        if request.user.is_authenticated:
            form = CommentForm(project_id=project_id)
        else:
            form = None

    return render(request, 'project_detail.html', {'project': project, 'details': details, 'comments': comments, 'form': form})


def portfolio_detail(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    return render(request, 'portfolio_detail.html', {'portfolio': portfolio})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            form.save_m2m()
            messages.success(request, 'Project created successfully.')
            return redirect('index')
    else:
        form = ProjectForm()
    return render(request, 'project_create.html', {'form': form})


@login_required
def project_update(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.user != request.user:
        messages.error(request, 'You are not authorized to update this project.')
        return redirect('index')
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            form.save_m2m()
            messages.success(request, 'Project updated successfully.')
            return redirect('index')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_update.html', {'form': form, 'project': project})


@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.user != request.user:
        messages.error(request, 'You are not authorized to delete this project.')
        return redirect('index')
    project.delete()
    messages.success(request, 'Project deleted successfully.')
    return redirect('index')

def scenerisation_services(request):
    services = Service.objects.filter(service_type='SC')
    return render(request, 'scenerisation_services.html', {'services': services})

def object3d_service(request):
    service = Service.objects.filter(service_type='OD')
    return render(request, 'object3d_service.html', {'services': service})

def show_charte_graphique(request):
    service = Service.objects.filter(service_type='CG')
    return render(request, 'charte_graphique.html', {'services': service})

def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    projects = Project.objects.filter(services=service)
    return render(request, 'service_detail.html', {'service': service, 'projects': projects})

@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    comments = portfolio.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.portfolio = portfolio
            comment.user = request.user
            comment.save()
            return redirect('portfolio_detail', portfolio_id=portfolio_id)
    else:
        if request.user.is_authenticated:
            form = CommentForm(portfolio_id=portfolio_id)
        else:
            form = None

    return render(request, 'portfolio_detail.html', {'portfolio': portfolio, 'comments': comments, 'form': form})

@login_required
def my_projects(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'my_projects.html', {'projects': projects})


@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            subject = 'New message from {} {}'.format(request.user.first_name, request.user.last_name)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.DEFAULT_TO_EMAIL]
            message_text = 'From: {} <{}>\n\n{}'.format(request.user.get_full_name(), request.user.email, message.message)
            send_mail(subject, message_text, from_email, to_email, fail_silently=True)
            messages.success(request, 'Message sent successfully.')
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

# Create
def team_member_create(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team_member_list')
    else:
        form = TeamMemberForm()
    return render(request, 'team_member_create.html', {'form': form})

# Retrieve
def team_member_detail(request, team_member_id):
    team_member = get_object_or_404(TeamMember, id=team_member_id)
    return render(request, 'team_member_detail.html', {'team_member': team_member})

# Update
def team_member_update(request, team_member_id):
    team_member = get_object_or_404(TeamMember, id=team_member_id)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, instance=team_member)
        if form.is_valid():
            form.save()
            return redirect('team_member_detail', team_member_id=team_member.id)
    else:
        form = TeamMemberForm(instance=team_member)
    return render(request, 'team_member_update.html', {'form': form, 'team_member': team_member})

# Delete
def team_member_delete(request, team_member_id):
    team_member = get_object_or_404(TeamMember, id=team_member_id)
    if request.method == 'POST':
        team_member.delete()
        return redirect('team_member_list')
    return render(request, 'team_member_delete.html', {'team_member': team_member})

# List
def team_member_list(request):
    team_members = TeamMember.objects.all()
    return render(request, 'team_member_list.html', {'team_members': team_members})

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    projects = Project.objects.filter(created_by=team)
    team_members = TeamMember.objects.filter(team=team)

    context = {
        'team': team,
        'projects': projects,
        'team_members': team_members
    }

    return render(request, 'team_detail.html', context)

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return redirect('index')
    return render(request, 'registration/register.html', {'form': form})