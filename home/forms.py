from django import forms
from home.models import Resume
import mimetypes

class ResumeDropForm(forms.ModelForm):
	class Meta:
		model = Resume
		fields = ['name', 'email', 'year', 'resume']

	def clean_email(self):
		if self.cleaned_data.get("email").split("@")[1].startswith("mit.edu") != True:
			raise forms.ValidationError('You must use an MIT email address')
		if Resume.objects.filter(email=self.cleaned_data.get("email")).count() > 0:
			raise forms.ValidationError('You have already submitted your resume')
		return self.cleaned_data.get("email")

	def clean_resume(self):
		if mimetypes.guess_type(self.cleaned_data.get("resume").name)[0] != "application/pdf":
			print mimetypes.guess_type(self.cleaned_data.get("resume").name)
			raise forms.ValidationError('You must submit your resume as a PDF')
		return self.cleaned_data.get("resume")