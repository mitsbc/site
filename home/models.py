from django.db import models
import datetime, os
from django.template import defaultfilters
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify

class Person(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)
	class Meta:
		abstract = True
	def __unicode__(self):
		return self.name

class Menu(models.Model):
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class MenuItem(models.Model):
	menus = models.ManyToManyField(Menu, related_name='menuitems') #same item, multiple menus
	text = models.CharField(max_length=200)
	link = models.URLField(max_length=200,null=True,blank=True)
	page = models.CharField(max_length=200,null=True,blank=True)
	new_page = models.BooleanField("Open in new page")
	def __unicode__(self):
		return self.text	


class SliderItem(models.Model):
	text = models.CharField(max_length=200)
	link = models.URLField(max_length=200,null=True,blank=True)
	new_page = models.BooleanField("Open in new page")
	img_height = models.PositiveIntegerField("Slider image height")
	img_width = models.PositiveIntegerField("Slider image width")
	image = models.ImageField(upload_to="home/slider_images/",height_field="img_height",width_field="img_width")
	def __unicode__(self):
		return self.text

class CalendarItem(models.Model):
	name = models.CharField(max_length=200)
	time = models.DateTimeField("Date and Time",default=timezone.now())
	location = models.CharField("Building",max_length=200)
	link = models.URLField(max_length=200,null=True,blank=True)
	new_page = models.BooleanField("Open in new page")
	description = models.TextField()

	def url(self,request):
		return request.build_absolute_uri(reverse('event',kwargs={'pk': self.pk}))

	def to_dict(self,request):
		obj = {}
		obj["id"] = self.pk
		obj["title"] = self.name
		obj["start"] = str(self.time)
		obj["url"] = self.url(request)
		return obj

	def get_location(self):
		return reverse('event',kwargs={'pk': self.pk})

	def __unicode__(self):
		return "%s (%s at %s)" % (self.name,self.location, defaultfilters.date(timezone.localtime(self.time), 'fA \o\\n l F d, Y'))

class Widget(models.Model):
	name = models.CharField(max_length=200,null=True)
	title = models.CharField(max_length=200)
	contents = models.TextField(max_length=1000)
	def __unicode__(self):
		return self.title

class Member(Person):
	title = models.CharField(max_length=200,null=True,blank=True)
	department = models.CharField(max_length=200,null=True,blank=True)
	year = models.IntegerField()
	img_height = models.PositiveIntegerField("Image height")
	img_width = models.PositiveIntegerField("Image width")
	image = models.ImageField(upload_to=get_filename,height_field="img_height",width_field="img_width",blank=True,default='home/member_images/placeholder.png')

	def get_filename(instance, filename):
		ext = filename.split('.')[-1]
		slug = slugify(instance.name)
		filename = ('%s.%s' % (slug, ext)).lower()
		return filename

	def save(self, *args, **kwargs):
		if not self.image:
			self.image.save('placeholder.png',File('home/member_images/placeholder.png'))
		elif os.path.exists(self.image.path):
			os.remove(self.image.path)
		super(Member, self).save() 

class ContactGroup(Person):
	description = models.CharField(max_length=200)
	def __unicode__(self):
		return self.description

class Subscriber(Person):
	date = models.DateField("Subscribed On",auto_now_add=True)

	def save(self, *args, **kwargs):
		import ssh
		ssh.subscribe(self.email)
		super(Subscriber, self).save()

class ContactMessage(Person):
	group =  models.ForeignKey(ContactGroup,verbose_name="Department",default=ContactGroup.objects.get(name="Exec").pk)
	phone = models.CharField("Phone Number",max_length=200,blank=True,null=True)
	message = models.TextField()
	subscribe = models.BooleanField("Subscribe To List", default=True)
	date = models.DateField("Contacted On",auto_now_add=True)

	def save(self, *args, **kwargs):
		from django.core.mail import EmailMultiAlternatives
		import html

		subject = 'MIT SBC Inquiry from ' + self.name
		from_email = self.email
		to_email = self.group.email
		html_body = self.message
		text_body = html.strip_tags(html_body)
		msg = EmailMultiAlternatives(subject, text_body, from_email, [to_email])
		msg.attach_alternative(html_body, "text/html")
		msg.send()
		if self.subscribe and Subscriber.objects.filter(email=self.email).count() == 0:
			Subscriber.objects.create(name=self.name,email=self.email)
		super(ContactMessage, self).save()

	def get_message_html(self):
		return self.message

	get_message_html.allow_tags = True
	get_message_html.short_description = 'Message'

class MemberList(models.Model):
	name = models.CharField(max_length=200)
	title = models.CharField(max_length=200,null=True,blank=True)
	member = models.ManyToManyField(Member, related_name='member')

	def get_location(self):
		return reverse('members_by_name',kwargs={'list': self.name})

	def __unicode__(self):
		return self.name
