from django.http import HttpResponse
from django.shortcuts import render
import datetime
from django.utils import timezone

from ine.models import Resume, Company, ResumeBook
from home.models import Menu
from ine.forms import ResumeDropForm, CompanyLoginForm


def ine_drop(request):
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	if request.method == 'POST':
		form = ResumeDropForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			context["submitted"] = True
			context["name"] = form.cleaned_data.get("name")
	else:
		form = ResumeDropForm()
	context["form"] = form
	return render(request, 'ine/ine_drop.html', context)

def ine_admin(request):
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	if request.method == 'POST':
		form = CompanyLoginForm(request.POST)
		if form.is_valid():
			request.session["company"] = form.cleaned_data.get("unique_hash")
			request.session["type"] = form.cleaned_data.get("type")
	else:
		form = CompanyLoginForm()
	if request.session.get("company") != None:
		try:
			context['company'] = Company.objects.get(unique_hash=request.session.get("company"))
			context['books'] = ResumeBook.objects.filter(industry=context['company'].industry)
		except Company.DoesNotExist:
			request.session.pop("company")
	context["form"] = form
	return render(request, 'ine/ine_admin.html', context)

def ine_resumes(request):
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	if Resume.objects.all().count() > 0:
		context['resumes'] = Resume.objects.all()
		context['prefix'] = "All"
		return render(request, 'ine/ine_resumes.html', context)
	else:
		return render(request, 'ine/resume_error.html', context)

def ine_resumes_by_year(request, year):
	year = int(year)
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	if Resume.objects.filter(year=year).count() > 0:
		context['resumes'] = Resume.objects.filter(year=year)
		context['prefix'] = "Class of {0} ".format(year)
		return render(request, 'ine/ine_resumes.html', context)
	else:
		return render(request, 'ine/resume_error.html', context)

def ine_resumes_by_industry(request, industry):
	industry = int(industry)
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	context['resumes'] = Resume.objects.filter(industry=industry)
	try:
		context['prefix'] = Resume.objects.get(industry=industry).industry_nice
	except Resume.DoesNotExist:
		return render(request, 'ine/resume_error.html', context)
	return render(request, 'ine/ine_resumes.html', context)

def book(request, industry, year):
	industry = int(industry)
	year = int(year)
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	if request.session.get("company") != None:
		try:
			company = Company.objects.get(unique_hash=request.session.get("company"))
			if company.industry == industry:
				book = ResumeBook.objects.get(industry=industry, year=year)
				pdf = open(book.path(),"r")
				response = HttpResponse(pdf,content_type='application/pdf')
				response["Pragma"] = "Public"
				response["Cache-Control"] = "must-revalidate, post-check=0, pre-check=0"
				if "MSIE" in request.META['HTTP_USER_AGENT']:
					response["X-Download-Options"] = "noopen"
					response["X-Content-Type-Options"] = "nosniff"
				response['Content-Disposition'] = 'inline; filename="{0}.pdf"'.format(str(book))
				response['Content-Transfer-Encoding'] = 'binary'
				response['Content-Length'] = str(book.book.size)
				return response
		except Company.DoesNotExist:
			pass
	return render(request, 'ine/ine_error.html', context)

def resume(request, year, unique_hash):
	year = int(year)
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	try:
		resume = Resume.objects.get(unique_hash=unique_hash,year=year)
		pdf = open(resume.path(),"r")
		response = HttpResponse(pdf,content_type='application/pdf')
		response["Pragma"] = "Public"
		response["Cache-Control"] = "must-revalidate, post-check=0, pre-check=0"
		if "MSIE" in request.META['HTTP_USER_AGENT']:
			response["X-Download-Options"] = "noopen"
			response["X-Content-Type-Options"] = "nosniff"
		response['Content-Disposition'] = 'inline; filename="{0}.pdf"'.format(str(resume))
		response['Content-Transfer-Encoding'] = 'binary'
		response['Content-Length'] = str(resume.resume.size)
		return response
	except Resume.DoesNotExist:
		pass
	return render(request, 'ine/resume_error.html', context)