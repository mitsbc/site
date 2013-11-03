from django.db import models

# Create your models here.
class Menu(models.Model):
	name = models.CharField(max_length=200)

class MenuItem(models.Model):
	menus = models.ManyToManyField(Menu) #same item, multiple menus
	text = models.CharField(max_length=200)
	link = models.URLField(max_length=200)
	new_page = models.BooleanField()


class SliderItem(models.Model):
	text = models.CharField(max_length=200)
	link = models.URLField(max_length=200)
	new_page = models.BooleanField()
	image = models.ImageField(upload_to="slider_images/")

class Widget(models.Model):
	title = models.CharField(max_length=200)
	contents = models.TextField(max_length=1000)