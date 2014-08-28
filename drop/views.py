from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from drop.models import Resume, Company, ResumeBook, DropEvent
from home.models import Menu
from drop.forms import ResumeDropForm, CompanyLoginForm
import datetime

def preprocess_context(name):
	context = {}
	context['top_menu'] =  Menu.objects.get(name="top")
	context['today'] = datetime.date.today()
	context['event'] = get_object_or_404(DropEvent, slug=name)
	return context

def drop_drop(request, name):
	context = preprocess_context(name)
	if request.method == 'POST':
		form = ResumeDropForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			context["submitted"] = True
			context["name"] = form.cleaned_data.get("name")
	else:
		form = ResumeDropForm()
	context["form"] = form
	return render(request, 'drop/drop.html', context)

def drop_admin(request, name):
	context = preprocess_context(name)
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
	return render(request, 'drop/admin.html', context)

def drop_resumes(request, name):
	if request.session.get("company") == None:
		return redirect('drop_admin')
		context = preprocess_context(name)
	if Resume.objects.all().count() > 0:
		context['resumes'] = Resume.objects.all()
		context['prefix'] = "All"
		return render(request, 'drop/resumes.html', context)
	else:
		return render(request, 'drop/resume_error.html', context)

def drop_resumes_by_year(request, name, year):
	if request.session.get("company") == None:
		return redirect('drop_admin')
	year = int(year)
	context = preprocess_context(name)
	if Resume.objects.filter(year=year).count() > 0:
		context['resumes'] = Resume.objects.filter(year=year)
		context['prefix'] = "Class of {0} ".format(year)
		return render(request, 'drop/resumes.html', context)
	else:
		return render(request, 'drop/resume_error.html', context)

def drop_resumes_by_industry(request, name, industry):
	if request.session.get("company") == None:
		return redirect('drop_admin')
	industry = int(industry)
	context = preprocess_context(name)
	context['resumes'] = Resume.objects.filter(industry=industry)
	try:
		context['prefix'] = Resume.objects.get(industry=industry).industry_nice
	except Resume.DoesNotExist:
		return render(request, 'drop/resume_error.html', context)
	return render(request, 'drop/resumes.html', context)

def book(request, name, industry, year):
	if request.session.get("company") == None:
		return redirect('drop_admin')
	industry = int(industry)
	year = int(year)
	context = preprocess_context(name)
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
				response['Content-Disposition'] = 'inldrop; filename="{0}.pdf"'.format(str(book))
				response['Content-Transfer-Encoding'] = 'binary'
				response['Content-Length'] = str(book.book.size)
				return response
		except Company.DoesNotExist:
			pass
	return render(request, 'drop/error.html', context)

def resume(request, name, year, unique_hash):
	if request.session.get("company") == None:
		return redirect('drop_admin')
	year = int(year)
	context = preprocess_context(name)
	try:
		resume = Resume.objects.get(unique_hash=unique_hash,year=year)
		pdf = open(resume.path(),"r")
		response = HttpResponse(pdf,content_type='application/pdf')
		response["Pragma"] = "Public"
		response["Cache-Control"] = "must-revalidate, post-check=0, pre-check=0"
		if "MSIE" in request.META['HTTP_USER_AGENT']:
			response["X-Download-Options"] = "noopen"
			response["X-Content-Type-Options"] = "nosniff"
		response['Content-Disposition'] = 'inldrop; filename="{0}.pdf"'.format(str(resume))
		response['Content-Transfer-Encoding'] = 'binary'
		response['Content-Length'] = str(resume.resume.size)
		return response
	except Resume.DoesNotExist:
		pass
	return render(request, 'drop/resume_error.html', context)
