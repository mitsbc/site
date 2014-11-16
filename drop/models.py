from django.db import models
import hashlib, random, mimetypes, datetime
from django.core.exceptions import ValidationError
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils import timezone

if datetime.date.today().month > 6:
	SENIOR = datetime.date.today().year + 1
else:
	SENIOR = datetime.date.today().year
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
	return "drop/resumes/{0}/{1}/{2}.pdf".format(instance.year, hashlib.sha1("SBC"+instance.email).hexdigest(), instance.name)

def get_book_path(instance, filename):
	subdir = '-'.join([x.slug for x in instance.events.all()])
	return "drop/books/{0}/{1}/{2}-{1}.pdf".format(instance.industry, subdir, instance.year)

class DropEvent(models.Model):

	name = models.CharField(max_length=100)
	description = models.TextField()
	slug = models.SlugField(max_length=100)
	ends = models.DateTimeField(default=timezone.now() + datetime.timedelta(days=7))

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(DropEvent, self).save(*args, **kwargs)

	def html_description(self):
		return '<p>' + '</p><p>'.join(self.description.split("\n")) + '</p>'

	def __unicode__(self):
		return self.name

class Resume(models.Model):

	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=200)
	year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=FRESHMAN)
	resume = models.FileField(upload_to=get_resume_path)
	industry = models.IntegerField(max_length=1, choices=TYPE_CHOICES, default=CONSULTING, verbose_name="Industry")
	unique_hash = models.CharField(max_length=100, verbose_name="Student Identifier", unique=True)
	event =  models.ForeignKey(DropEvent, verbose_name="Event")

	def path(self):
		return settings.MEDIA_ROOT + "drop/resumes/{0}/{1}/{2}.pdf".format(self.year, self.unique_hash, self.name)

	def url(self):
		return self.resume.url
		# return reverse('resume',kwargs={'year':self.year, 'unique_hash':self.unique_hash})

	def industry_nice(self):
		return TYPE_CHOICES[self.industry][1]

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.unique_hash = hashlib.sha1("SBC{}{}{}".format(self.email, TYPE_CHOICES[self.industry][1], self.event.pk)).hexdigest()
		super(Resume, self).save(*args, **kwargs)

class ResumeBook(models.Model):
	year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=FRESHMAN)
	industry = models.IntegerField(max_length=1, choices=TYPE_CHOICES, default=CONSULTING, verbose_name="Industry")
	book = models.FileField(upload_to=get_book_path, blank=True, null=True)
	events = models.ManyToManyField(DropEvent)
	resumes = models.ManyToManyField(Resume, blank=True, null=True)

	def url(self):
		return self.book.url
		# return reverse('book', kwargs={'industry': self.industry, 'year': self.year, 'name': slug})

	def path(self):
		subdir = '-'.join([x.slug for x in self.events.all()])
		return settings.MEDIA_ROOT + "drop/books/{0}/{1}/{2}-{1}.pdf".format(self.industry, subdir, self.year)

	def clean(self):
		super(ResumeBook, self).clean()
		if bool(self.book) and mimetypes.guess_type(self.book.name)[0] != "application/pdf":
			raise ValidationError('Resume book must be a PDF.')

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
		super(Company, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name
