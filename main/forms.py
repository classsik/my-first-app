from .models import Comment, Course, Module
from django import forms
from django.forms.models import inlineformset_factory

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

ModuleFormSet = inlineformset_factory(Course, Module, fields=['title', 'description'],  extra=2, can_delete=True) 
