from django.http import HttpResponse
from django.shortcuts import render
import datetime
from django.utils import timezone

from home.models import Menu,MenuItem,Widget,SliderItem,CalendarItem,Member,MemberList

def index(request):
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['slider_items'] =  SliderItem.objects.all()
	context['calendar_items'] =  CalendarItem.objects.all().order_by('time').exclude(time__lt=timezone.now())[:3]
	context['left_widget'] =  Widget.objects.get(name="left")
	context['right_widget'] =  Widget.objects.get(name="right")
	return render(request, 'home/index.html', context)

def about(request):
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	return render(request, 'home/about.html', context)

def members(request, list):
	context = {}
	context['members'] =  MemberList.objects.get(name=list)
	return render(request, 'home/members.html', context)