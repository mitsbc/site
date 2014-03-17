from django.db import models
import datetime, hashlib, random, mimetypes
from django.template import defaultfilters
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files import File

SENIOR = 2014
JUNIOR = SENIOR + 1
SOPHOMORE = SENIOR + 2
FRESHMAN = SENIOR + 3

YEAR_CHOICES = (
    (FRESHMAN, 'Freshman'),
    (SOPHOMORE, 'Sophomore'),
    (JUNIOR, 'Junior'),
    (SENIOR, 'Senior'),
)

CONSULTING = 0
FINANCE = 1
ENGINEERING = 2

TYPE_CHOICES = (
    (CONSULTING, 'Consulting'),
    (FINANCE, 'Finance'),
    (ENGINEERING, 'Engineering'),
)

def get_resume_path(instance, filename):
	return "ine/resumes/{0}/{1}/{2}.pdf".format(instance.year, hashlib.sha1("SBC"+instance.email).hexdigest(), instance.name)

def get_book_path(instance, filename):
	return "ine/books/{0}/{1}.pdf".format(instance.industry, instance.year)

class Resume(models.Model):

	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=200)
	year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=FRESHMAN)
	resume = models.FileField(upload_to=get_resume_path)
	industry = models.IntegerField(max_length=1, choices=TYPE_CHOICES, default=CONSULTING, verbose_name="Industry")
	unique_hash = models.CharField(max_length=100, verbose_name="Student Identifier")

	def path(self):
		return settings.MEDIA_ROOT+"ine/resumes/{0}/{1}/{2}.pdf".format(self.year, self.unique_hash, self.name)

	def url(self):
		return reverse('resume',kwargs={'year':self.year, 'unique_hash':self.unique_hash})

	def industry_nice(self):
		return TYPE_CHOICES[self.industry][1]

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.unique_hash = hashlib.sha1("SBC"+self.email).hexdigest()
		super(Resume, self).save()

class ResumeBook(models.Model):

	year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=FRESHMAN)
	industry = models.IntegerField(max_length=1, choices=TYPE_CHOICES, default=CONSULTING, verbose_name="Industry")
	book = models.FileField(upload_to=get_book_path,blank=True)

	def url(self):
		return reverse('book',kwargs={'industry':self.industry, 'year':self.year})

	def path(self):
		return settings.MEDIA_ROOT+"ine/books/{0}/{1}.pdf".format(self.industry, self.year)

	def clean(self):
		super(ResumeBook, self).clean()
		if self.book and mimetypes.guess_type(self.book.name)[0] != "application/pdf":
			raise ValidationError('Resume book must be a PDF.')

	def save(self, *args, **kwargs):
		if not self.book:
			import pdf, time
			resumes = [x.path() for x in Resume.objects.filter(year=self.year, industry=self.industry)]
			tmpfile = "/tmp/" + str(time.time()) + ".pdf"
			pdf.merge(resumes, tmpfile)
			with open(tmpfile, 'r') as f:
				self.book.save(get_book_path(self,tmpfile), File(f))
		super(ResumeBook, self).save()

	def industry_nice(self):
		return TYPE_CHOICES[self.industry][1]

	def __unicode__(self):
		return "{0} {1} Resume Book".format(self.year, self.industry_nice())

class Company(models.Model):
	
	class Meta:
		verbose_name_plural = "Companies"

	name = models.CharField(max_length=100)
	contact_name = models.CharField(max_length=100, null=True, blank=True)
	contact_email = models.EmailField(max_length=100, null=True, blank=True)
	industry = models.IntegerField(max_length=1, choices=TYPE_CHOICES, default=CONSULTING, verbose_name="Industry")
	unique_hash = models.CharField(max_length=100, verbose_name="Company Identifier")

	def save(self, *args, **kwargs):
		self.unique_hash = hashlib.sha1("INE"+self.name+str(random.randint(0,100))).hexdigest()
		super(Company, self).save()

	def __unicode__(self):
		return self.name
