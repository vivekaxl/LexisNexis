
############################ IMPORTS ###########################
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.bing_search import run_query
from datetime import datetime

############################ ISSUES ############################
#
# cat_list not working in any view except index

############################ VIEWS #############################

def encode_url(str):
	return str.replace(' ', '_')

def decode_url(str):
	return str.replace('_', ' ')

def get_category_list():
	cat_list = Category.objects.all()	

	for cat in cat_list:
		cat.url = encode_url(cat.name)

	return cat_list

cat_list = get_category_list() # Global variable, many views are using this.

def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	for category in category_list:
		category.url = category.name.replace(' ', '_')
	page_list = Page.objects.order_by('-views')[:5]
	request.session.set_test_cookie()

### Sessions

	if request.session.get('last_visit'):
		last_visit_time = request.session.get('last_visit')
		visits = request.session.get('visits', 0)
		a = 1   # Variables a and b to test behavior of the code.
		b = 5

		if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 2:
			request.session['visits'] = visits + 1
			request.session['last_visit'] = str(datetime.now())
			b = 2

	else:
			request.session['last_visit'] = str(datetime.now())
			request.session['visits'] = 1
			b = 3
			a = 4
	

	return render(request, 'rango/index.html', {'categories': category_list, 'page_list':page_list, 'a':a, 'b':b, 'cat_list':cat_list, })

### Cookies 

#	visits = int(request.COOKIES.get('visits','0'))
#
#	if 'last_visit' in request.COOKIES:
#		last_visit = request.COOKIES['last_visit']
#		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
#
#		if (datetime.now() - last_visit_time).seconds > 2:
#			response.set_cookie('visits', visits+1)
#			response.set_cookie('last_visit', datetime.now())
#
#	else: 
#		response.set_cookie('last_visit', datetime.now())
#
#	return response



def about(request):
	if request.session.get('visits'):
		visits = request.session.get('visits')
	
	else: visits= 256
	return render(request, 'rango/about.html', {'visits': visits, 'cat_list':cat_list, })
	

def category(request, category_name_url):
	category_name = category_name_url.replace('_', ' ')
	page_list = Page.objects.filter( category__name = category_name )

	context_dict = {'category_name_url':category_name_url,'category_name': category_name, 'page_list': page_list, 'cat_list':cat_list }

	if request.method == 'POST':
		query = request.POST['query'].strip
		if query:
			result_list = run_query(query)
			context_dict['result_list'] = result_list
		

	return render(request, 'rango/category.html', context_dict)


########################## Forms ##############################

def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()
	return render(request, 'rango/add_category.html', {'form':form, 'cat_list':cat_list, })

def add_page(request, category_name_url):
	category_name = category_name_url.replace('_', ' ')
	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			page = form.save(commit=False)
			
			try:
				cat = Category.objects.get(name=category_name)
				page.category = cat
			except Category.DoesNotExist:
				return render(context, 'rango/add_category', {})
			page.views = 0
			page.save()
			return category(request, category_name_url)
		else:
			print form.errors

	else:
		form = PageForm()
	return render(request, 'rango/add_page.html', {'category_name_url':category_name_url, 'category_name':category_name ,'form':form, 'cat_list':cat_list, })
	
def register(request):
	registered = False

	## Testing cookies
	if request.session.test_cookie_worked():
		print ">>>>> Test cookie worked!"
	#	request.session.delete_test_cookie()
	## Testing cookies
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()
			registered = True

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'rango/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered': registered, 'cat_list':cat_list, })


def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("Your Rango account is disabled.")

		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	
	else:
		return render(request, 'rango/login.html', {'cat_list':cat_list, })
		
@login_required
def restricted(request):
	return render(request, 'rango/restricted.html', {'cat_list':cat_list, })
	
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')

#def search(request):
#	cat_list = get_category_list() 
#	result_list = []
#
#	if request.method == 'POST':
#		query = request.POST['query'].strip()
#
#		if query:
#			result_list = run_query(query)
#	
#	return render(request, 'rango/search.html', {'result_list':result_list, 'cat_list':cat_list, })


