from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class TaskForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)    
    description = forms.CharField(max_length=255, required=False)
    status = forms.CharField(max_length=50, required=False, initial='pending')
    priority = forms.CharField(max_length=50, required=False, initial='medium')
    owner = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    assignee = forms.ModelChoiceField(queryset=User.objects.all(), required=False, empty_label="None")
    created_at = forms.DateTimeField(required=False, initial=forms.fields.now)
    due_date = forms.DateTimeField(required=False, initial=None)
    completed = forms.BooleanField(required=False, initial=False) 


        
class ArticleUpdateForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=100, required=False)
    body = forms.CharField(max_length=100, required=False)
    tagList = forms.Field(required=False)
    
# class Task(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     status = models.CharField(max_length=50, default='pending')
#     priority = models.CharField(max_length=50, default='medium')
#     owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tasks')
#     assignee = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
#     created_at = models.DateTimeField(auto_now_add=True)
#     due_date = models.DateTimeField(null=True, blank=True)
#     completed = models.BooleanField(default=False)