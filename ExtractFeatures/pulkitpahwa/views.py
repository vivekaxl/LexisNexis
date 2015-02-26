from django.http import HttpResponse
from django.template import Context,Template
from django.template.loader import get_template
from django.shortcuts import render
from django.views.generic import CreateView
from coke.models import Notice,Academic,Parent_Information,facultie,committee_member

def gallery(request) :
	a = get_template("gallery.html")
	w = Notice.objects.all()
	c =Context({'title':"sitemap",'w':w})
	html = a.render(c)
	return HttpResponse(html)

def contact(request):
	a = get_template("contact.html")
	w = Notice.objects.all()
	c = Context({'title':"Contact Us",'w':w})
	html = a.render(c)
	return HttpResponse(html)

def home(request) :
	a = get_template("index.html")
	w = Notice.objects.all()
	c =Context({'title':"sitemap",'w':w})
	html = a.render(c)
	return HttpResponse(html)


def gallery(request) :
	a = get_template("gallery.html")
	w = Notice.objects.all()
	c =Context({'title':"sitemap",'w':w})
	html = a.render(c)
	return HttpResponse(html)

def alumni(request) :
	a = get_template("alumni.html")
	w = Notice.objects.all()
	c =Context({'title':"sitemap",'w':w})
	html = a.render(c)
	return HttpResponse(html)


def about(request) :
	a = get_template("about.html")
	w = Notice.objects.all()
	c =Context({'title':"sitemap",'w':w})
	html = a.render(c)
	return HttpResponse(html)

def fac(request):
	a = get_template("faculty.html")
	fac = facultie.objects.all()
	w = Notice.objects.all()
	text = Parent_Information.objects.all()
	c = Context({'w':w,'fac':fac})
	html = a.render(c)
	return HttpResponse(html)

def com(request):
	a = get_template("commitee-member.html")
	com = committee_member.objects.all()
	w = Notice.objects.all()
	c = Context({'w':w,'com':com})
	html = a.render(c)
	return HttpResponse(html)

def parent(request) :
	a = get_template("parent.html")
	w = Notice.objects.all()
	text = Parent_Information.objects.all()
	for i in text :
		text = i.info
	c =Context({'title':"sitemap",'w':w,'text':text})
	html = a.render(c)
	return HttpResponse(html)

def academics(request) :
	a = get_template("academics.html")
	text = Academic.objects.all()
	for i in text :
		text = i.list
	w = Notice.objects.all()
	c =Context({'title':"sitemap",'text':text,'w':w})
	html = a.render(c)
	return HttpResponse(html)

def achievements(request) :
	a = get_template("alumni.html")
	w = Notice.objects.all()
	c =Context({'title':"sitemap",'w':w})
	html = a.render(c)
	return HttpResponse(html)


def activities(request) :
	a = get_template("activities.html")
	w = Notice.objects.all()
	c =Context({'title':"sitemap",'w':w})
	html = a.render(c)
	return HttpResponse(html)


def facilities(request) :
	a = get_template("facilities.html")
	w = Notice.objects.all()
	c =Context({'title':"sitemap",'w':w})
	html = a.render(c)
	return HttpResponse(html)

