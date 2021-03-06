from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
import datetime, json, pytz, dateutil.parser

from home.models import Menu, Widget, SliderItem, CalendarItem, Member, MemberList, ContactGroup, BlogPost
from home.forms import SubscriberForm, ContactMessageForm
from django.utils import timezone


def preprocess_context():
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['STATIC_VERSION'] = settings.STATIC_VERSION
	return context

def set_timezone(request):
	if request.method == 'POST':
		request.session['django_timezone'] = request.POST['timezone']
	elif request.method == 'GET' and request.GET.get('timezone'):
		request.session['django_timezone'] = request.GET.get('timezone')
	return render(request, 'home/timezone.html', {'timezones': pytz.common_timezones})

def index(request):
	context = preprocess_context()
	context['slider_items'] =  SliderItem.objects.all()
	context['calendar_items'] =  CalendarItem.objects.order_by('time').filter(time__gt=timezone.now())[:4]
	context['left_widget'] =  Widget.objects.get(name="left")
	context['right_widget'] =  Widget.objects.get(name="right")
	return render(request, 'home/index.html', context)

def not_found_view(request):
	context = preprocess_context()
	return HttpResponseNotFound(render_to_string('home/404.html', context))

def blog(request):
	context = preprocess_context()
	context['posts'] =  BlogPost.objects.all()
	return render(request, 'home/blog.html', context)

def author(request, slug):
	context = preprocess_context()
	person = get_object_or_404(Member, name=slug.replace("-"," "))
	context['posts'] =  BlogPost.objects.filter(author=person)
	return render(request, 'home/blog.html', context)

def post(request, slug):
	context = preprocess_context()
	context['post'] = get_object_or_404(BlogPost, slug=slug)
	return render(request, 'home/post.html', context)

def about(request):
	context = preprocess_context()
	return render(request, 'home/about.html', context)

def events_all(request):
	context = preprocess_context()
	context['calendar_items'] =  CalendarItem.objects.order_by('time').filter(time__gt=timezone.now())[:3]
	context['gcal_url'] =  settings.GCAL_URL
	return render(request, 'home/events.html', context)

def events_json(request):
	items = []
	try:
		start = dateutil.parser.parse(request.GET.get('start'))
		end = dateutil.parser.parse(request.GET.get('end'))
		calendar_items = CalendarItem.objects.order_by('time').filter(time__gt=start,time__lt=end)
	except AttributeError:
		calendar_items = CalendarItem.objects.order_by('time').filter(time__gt=timezone.now(),time__lt=timezone.now() + datetime.timedelta(weeks=4))
	for c in calendar_items:
		items.append(c.to_dict(request))
	return HttpResponse(json.dumps(items), mimetype='application/json')

def event(request, slug):
	context = preprocess_context()
	context['item'] = get_object_or_404(CalendarItem, slug=slug)
	return render(request, 'home/event.html', context)

def contact(request):
	context = preprocess_context()
	context['contact_groups'] = ContactGroup.objects.all()
	if request.method == 'POST':
		form = ContactMessageForm(request.POST)
		if form.is_valid():
			form.save()
			context["submitted"] = True
			context["name"] = form.cleaned_data.get("name")
			context["group"] = str(form.cleaned_data.get("group"))
	else:
		form = ContactMessageForm()
	context["form"] = form
	return render(request, 'home/contact.html', context)

def subscribe(request):
	context = preprocess_context()
	if request.method == 'POST':
		form = SubscriberForm(request.POST)
		if form.is_valid():
			form.save()
			context["subscribed"] = True
			context["email"] = form.cleaned_data.get("email")
			context["name"] = form.cleaned_data.get("name")
	else:
		form = SubscriberForm(initial={'email': request.GET.get('email')})
	context["form"] = form
	return render(request, 'home/subscribe.html', context)

def custom_exec_sort(title, name):
	if name == 'exec':
		ranking = {'president': 0, 'co-president': 1, 'vice president': 2, 'md of': 3}
	else:
		ranking = {'md of': 0}
	if 'md of' in title:
		title = 'md of'
	return ranking[title] if title in ranking else len(ranking)

def members_by_name(request, name):
	context = preprocess_context()
	members = get_object_or_404(MemberList, name=name)
	context['title'] = members.title
	context['member'] =  list(sorted(members.member.all(), key=lambda x: custom_exec_sort(x.title.lower(), name)))
	return render(request, 'home/members.html', context)

def members_by_year(request, year):
	context = preprocess_context()
	context['title'] = "Class of %s" % year
	context['member'] =  Member.objects.filter(year=year)
	return render(request, 'home/members.html', context)
