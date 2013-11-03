from django.db import models

# Create your models here.
class Menu(models.Model):
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class MenuItem(models.Model):
	menus = models.ManyToManyField(Menu, related_name='Menus') #same item, multiple menus
	text = models.CharField(max_length=200)
	link = models.URLField(max_length=200)
	new_page = models.BooleanField("Open in new page")
	def __unicode__(self):
		return self.text	


class SliderItem(models.Model):
	text = models.CharField(max_length=200)
	link = models.URLField(max_length=200)
	new_page = models.BooleanField("Open in new page")
	image = models.ImageField(upload_to="slider_images/")
	def __unicode__(self):
		return self.text

class Widget(models.Model):
	title = models.CharField(max_length=200)
	contents = models.TextField(max_length=1000)
	def __unicode__(self):
		return self.title