from django.db import models
import datetime, hashlib, random, mimetypes
from django.template import defaultfilters
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.conf import settings

class Resume(models.Model):
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

	def get_resume_path(instance, filename):
		return "ine/resumes/{0}/{1}/{2}.pdf".format(instance.year, hashlib.sha1(instance.email).hexdigest(), instance.name)

	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=200)
	year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=FRESHMAN)
	resume = models.FileField(upload_to=get_resume_path)

	def __unicode__(self):
		return self.name

class ResumeBook(models.Model):
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

	def get_book_path(instance, filename):
		return "ine/books/{0}/{1}.pdf".format(instance._type, instance.year)

	def url(self):
		return reverse('book',kwargs={'_type':self._type, 'year':self.year})

	def path(self):
		return settings.MEDIA_ROOT+"ine/books/{0}/{1}.pdf".format(self._type, self.year)

	def clean(self):
		super(ResumeBook, self).clean()
		if mimetypes.guess_type(self.book.name)[0] != "application/pdf":
			raise ValidationError('Resume book must be a PDF.')

	year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=FRESHMAN)
	_type = models.IntegerField(max_length=1, choices=TYPE_CHOICES, default=CONSULTING, verbose_name="Industry")
	book = models.FileField(upload_to=get_book_path)

	def __unicode__(self):
		return "{0} {1} Resume Book".format(self.year, self.TYPE_CHOICES[self._type][1])

class Company(models.Model):
	
	class Meta:
		verbose_name_plural = "Companies"

	CONSULTING = 0
	FINANCE = 1
	ENGINEERING = 2

	TYPE_CHOICES = (
	    (CONSULTING, 'Consulting'),
	    (FINANCE, 'Finance'),
	    (ENGINEERING, 'Engineering'),
	)

	name = models.CharField(max_length=100)
	contact_name = models.CharField(max_length=100, null=True, blank=True)
	contact_email = models.EmailField(max_length=100, null=True, blank=True)
	_type = models.IntegerField(max_length=1, choices=TYPE_CHOICES, default=CONSULTING, verbose_name="Industry")
	_hash = models.CharField(max_length=100, verbose_name="Company Identifier")

	def save(self):
		self._hash = hashlib.sha1("INE"+self.name+str(random.randint(0,100))).hexdigest()
		super(Company, self).save()

	def __unicode__(self):
		return self.name
