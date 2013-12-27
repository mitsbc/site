from django.db import models
import datetime
from django.template import defaultfilters

# Create your models here.
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
	time = models.DateTimeField("Date and Time",default=datetime.datetime.now())
	location = models.CharField(max_length=200)
	link = models.URLField(max_length=200,null=True,blank=True)
	new_page = models.BooleanField("Open in new page")
	def __unicode__(self):
		return "%s (%s at %s)" % (self.name,self.location, defaultfilters.date(self.time, 'fA \o\\n l F d, Y'))

class Widget(models.Model):
	name = models.CharField(max_length=200,null=True)
	title = models.CharField(max_length=200)
	contents = models.TextField(max_length=1000)
	def __unicode__(self):
		return self.title

class Member(models.Model):
	name = models.CharField(max_length=200)
	title = models.CharField(max_length=200,null=True,blank=True)
	email = models.EmailField(max_length=200)
	department = models.CharField(max_length=200,null=True,blank=True)
	year = models.IntegerField()
	img_height = models.PositiveIntegerField("Image height")
	img_width = models.PositiveIntegerField("Image width")
	image = models.ImageField(upload_to="home/member_images/",height_field="img_height",width_field="img_width")
	def __unicode__(self):
		return self.name

class Subscriber(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)
	def __unicode__(self):
		return self.name

class MemberList(models.Model):
	name = models.CharField(max_length=200)
	title = models.CharField(max_length=200,null=True,blank=True)
	member = models.ManyToManyField(Member, related_name='member')
	def __unicode__(self):
		return self.name
