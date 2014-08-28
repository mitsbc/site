from django.db import models
import hashlib, random, mimetypes, datetime, requests, os, errno
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files import File
from django.template.defaultfilters import slugify

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

def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else:
    	raise

def get_resume_path(instance, filename):
	return "drop/resumes/{0}/{1}/{2}.pdf".format(instance.year, hashlib.sha1("SBC"+instance.email).hexdigest(), instance.name)

def get_book_path(instance, filename):
	return "drop/books/{0}/{1}.pdf".format(instance.industry, instance.year)

class DropEvent(models.Model):

	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(DropEvent, self).save()

	def __unicode__(self):
		return self.name

class Resume(models.Model):

	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=200)
	year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=FRESHMAN)
	resume = models.FileField(upload_to=get_resume_path)
	industry = models.IntegerField(max_length=1, choices=TYPE_CHOICES, default=CONSULTING, verbose_name="Industry")
	unique_hash = models.CharField(max_length=100, verbose_name="Student Identifier")

	def path(self):
		return settings.MEDIA_ROOT+"drop/resumes/{0}/{1}/{2}.pdf".format(self.year, self.unique_hash, self.name)

	def url(self):
		return settings.CF_URL + self.resume.path[len(settings.PROJECT_PATH):]
		# return reverse('resume',kwargs={'year':self.year, 'unique_hash':self.unique_hash})

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
		return settings.CF_URL + self.book.path[len(settings.PROJECT_PATH):]
		# return reverse('book', kwargs={'industry': self.industry, 'year': self.year, 'name': slug})

	def path(self):
		return settings.MEDIA_ROOT+"drop/books/{0}/{1}.pdf".format(self.industry, self.year)

	def clean(self):
		super(ResumeBook, self).clean()
		if self.book and mimetypes.guess_type(self.book.name)[0] != "application/pdf":
			raise ValidationError('Resume book must be a PDF.')

	def save(self, *args, **kwargs):
		if not self.book:
			import pdf, time
			resumes = [x.path() for x in Resume.objects.filter(year=self.year, industry=self.industry)]
			for resume_loc in resumes:
				mkdir_p('/'.join(resume_loc.split('/')[:-1]))
				r = requests.get(self.url())
				with open(resume_loc, 'wb') as f:
					for chunk in r.iter_content():
						f.write(chunk)
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
