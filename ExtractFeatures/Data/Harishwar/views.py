from django.shortcuts import render
from django.template import RequestContext,loader
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Registration
from django.templatetags.static import static
import reportlab
import json
import hashlib
from email import email
import os
from reportlab.pdfgen import canvas
from django.http import HttpResponse

@csrf_exempt
def register(request):
    template=loader.get_template('registration/register.html')
    context=RequestContext(request)
    return HttpResponse(template.render(context));

def register1(request):
    
    return render(request,'registration/register.html') 

def index(request):
    
    return render(request,'registration/index.html') 

def bigdata(request):
    print 'bigdata'
    return render(request,'registration/bigdata.html') 


@csrf_exempt
def processData(request):
    #if request.method=='POST':
        print request.POST['downloadWpEmail']
        print request.POST.get('downloadWpEmail',False)
        
        #inputToDB=request.body
        #fn = hashlib.md5();
        #fn.update(inputToDB['inputDownloadWpFName'])
        #print fn.digest()
        #print hashlib.md5(inputToDB['first_name']).hexdigest()
        #print hashlib.md5(inputToDB['last_name']).hexdigest()
        #print hashlib.md5(inputToDB['password']).hexdigest()
        
        #a=Registration(first_name=hashlib.md5(inputToDB['inputDownloadWpFName']).hexdigest(),last_name=hashlib.md5(inputToDB['inputDownloadWpLName']).hexdigest(),email=hashlib.sha224(inputToDB['inputDownloadWpEmail']).hexdigest(),phone=inputToDB['phone'],ssn=inputToDB['ssn'],password=hashlib.md5(inputToDB['password']).hexdigest(),cc_number=inputToDB['cc_number'],url=inputToDB['url'])
        a=Registration(first_name=request.POST['downloadWpFName'],last_name=request.POST['downloadWpLName'],email=request.POST['downloadWpEmail'])
        a.save()
        #os.path.join(settings.MEDIA_ROOT, 'a.txt', 'rb').read()
        return render(request,'registration/download.html')
        
        
        
        

#    print request.body
 #   return HttpResponse("Your request is received!!")

