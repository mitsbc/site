from django.http import HttpResponse
from django.shortcuts import render
import datetime
from django.utils import timezone

from ine.models import Resume, Company, ResumeBook
from home.models import Menu
from ine.forms import ResumeDropForm, CompanyLoginForm


def ine(request):
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	if request.method == 'POST':
		form = ResumeDropForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			context["submitted"] = True
	else:
		form = ResumeDropForm()
	context["form"] = form
	return render(request, 'ine/ine.html', context)

def ine_admin(request):
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	if request.method == 'POST':
		form = CompanyLoginForm(request.POST)
		if form.is_valid():
			request.session["company"] = form.cleaned_data.get("_hash")
			request.session["type"] = form.cleaned_data.get("type")
	else:
		form = CompanyLoginForm()
	if request.session.get("company") != None:
		try:
			context['company'] = Company.objects.get(_hash=request.session.get("company"))
			context['books'] = ResumeBook.objects.filter(_type=context['company']._type)
		except Company.DoesNotExist:
			request.session.pop("company")
	context["form"] = form
	return render(request, 'ine/ine_admin.html', context)

def book(request, _type, year):
	_type = int(_type)
	year = int(year)
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	if request.session.get("company") != None:
		try:
			company = Company.objects.get(_hash=request.session.get("company"))
			if company._type == _type:
				book = ResumeBook.objects.get(_type=_type, year=year)
				pdf = open(book.path(),"r")
				response = HttpResponse(pdf,content_type='application/pdf')
				response["Pragma"] = "Public"
				response["Cache-Control"] = "must-revalidate, post-check=0, pre-check=0"
				if "MSIE" in request.META['HTTP_USER_AGENT']:
					response["X-Download-Options"] = "noopen"
					response["X-Content-Type-Options"] = "nosniff"
				response['Content-Disposition'] = 'inline; filename="{0}"'.format(str(book))
				response['Content-Transfer-Encoding'] = 'binary'
				response['Content-Length'] = str(book.book.size)
				return response
		except Company.DoesNotExist:
			pass
	return render(request, 'ine/ine_error.html', context)