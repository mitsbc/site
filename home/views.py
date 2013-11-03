from django.http import HttpResponse
from django.template import RequestContext, loader

from home.models import Menu,MenuItem,Widget,SliderItem

def index(request):
	template = loader.get_template('home/index.html')
	context = RequestContext(request, {
		'test': "db var",
	})
	return HttpResponse(template.render(context))