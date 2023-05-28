from django import forms

class PostForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'What s on your mind, zahidul'}))
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'transparent-input'}))

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'What s on your mind, zahidul'}))
