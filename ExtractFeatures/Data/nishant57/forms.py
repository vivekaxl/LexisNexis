from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, 
		help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Category

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, 
		help_text="Please enter the title of the page.")
	url = forms.URLField(max_length=200, 
		help_text="Please enter the url of the page.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0) 

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		if url and not (url.startswith('http://') or url.startswith('https://')):
			url = 'http://' + url
			cleaned_data['url'] = url

		return cleaned_data

	class Meta:
		model = Page
		fields = ('title', 'url', 'views')

class UserForm(forms.ModelForm):
	username = forms.CharField(help_text="Please enter your username")
	email = forms.URLField(help_text="Please enter your email address")
	password = forms.CharField(widget=forms.PasswordInput(), help_text="Please choose a password")


	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	 website = forms.URLField(help_text="Please enter your website")
	 picture = forms.ImageField(help_text="Select a profile picute.")
	
	 class Meta:
		model = UserProfile
		fields = ('website', 'picture')
