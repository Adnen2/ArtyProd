from django import forms
from .models import Project, ContactMessage, Service,Portfolio,Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class ContactForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your message...'}))

    class Meta:
        model = ContactMessage
        fields = ('message',)



class ProjectForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title...'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter project description...'}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    github_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Github link...'}))
    website_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter website link...'}))
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = Project
        fields = ('title', 'description', 'image', 'github_link', 'website_link', 'services')

    
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mr-3', 'placeholder': 'Add comment','rows': 3, 'size': 50}))
    def __init__(self, *args, **kwargs):
        portfolio_id = kwargs.pop('portfolio_id', None)
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        self.fields['portfolio'].initial = portfolio_id
        self.fields['project'].initial = project_id
        self.fields['portfolio'].widget = forms.HiddenInput()
        self.fields['project'].widget = forms.HiddenInput()

    class Meta:
        model = Comment
        fields = ['project', 'portfolio', 'content']

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your first name...'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter last name...'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your Email...'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name' , 'email' )