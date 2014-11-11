from django import forms
from drop.models import Resume, Company
import mimetypes

class ResumeDropForm(forms.ModelForm):
	class Meta:
		model = Resume
		fields = ['name', 'industry','email', 'year', 'resume']

	def clean_email(self):
		if self.cleaned_data.get("email").split("@")[1].startswith("mit.edu") != True:
			raise forms.ValidationError('You must use an MIT email address.')
		resumes = Resume.objects.filter(email=self.cleaned_data.get("email"), industry=self.cleaned_data.get("industry"), event=self.cleaned_data.get("event"))
		if resumes.count() > 0:
			raise forms.ValidationError('You have already submitted your resume for this event and industry.')
		return self.cleaned_data.get("email")

	def clean_resume(self):
		if mimetypes.guess_type(self.cleaned_data.get("resume").name)[0] != "application/pdf":
			raise forms.ValidationError('You must submit your resume as a PDF.')
		return self.cleaned_data.get("resume")

class CompanyLoginForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = ['unique_hash']

	def clean_unique_hash(self):
		if Company.objects.filter(unique_hash=self.cleaned_data.get("unique_hash")).count() == 0:
			raise forms.ValidationError('That company identifier was not found in our records.')
		return self.cleaned_data.get("unique_hash")
