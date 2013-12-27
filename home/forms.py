from django import forms

from home.models import Resume

class ResumeDropForm(forms.ModelForm):
    class Meta:
    	model = Resume
    	fields = ['name', 'email', 'year', 'resume']