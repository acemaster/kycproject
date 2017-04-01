from django.shortcuts import render
from main.models import *
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home(request):
	return render(request,'homepage/index.html',{})

def signup(request):
	response={}
	if request.method == 'POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		username = request.POST['email']
		email = request.POST['email']
		password1 = request.POST['password']
		password2 = request.POST['confirm_password']

		if password1!=password2:
			response['message'] = "Password does not match"
			return render(request,'main/site/signup.djt',response)

		user = User()
		user.first_name = firstname
		user.last_name = lastname
		user.username = username
		user.email = email
		user.set_password(password1)
		try:
			user.save()
			response['message'] = "Successfully Registered"
			p = UserProfile()
			p.user = user
			p.phone = request.POST['phone']
			p.country = request.POST['country']
			p.father_name = request.POST['fname']
			p.address = request.POST['address']
			p.dob = request.POST['dob']
			p.native_lang = request.POST['native_lang']
			p.lang = request.POST['lang']
			p.save()
			return render(request,'main/site/login.djt',response)
		except Exception,e:
			print str(e)
			response['message'] = "username already exist"
			return render(request,'main/site/signup.djt',response)
	return render(request,'main/site/signup.djt')

def signin(request):
	response={}
	if request.user.is_authenticated():
	    return HttpResponseRedirect('/')
	if request.method == "POST":
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return HttpResponseRedirect('/main/dashboard/')
	    else:
	        response['message']='User is not registered / Password Incorrect' 
	return render(request,'main/site/login.djt',response)

def signout(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/main/signin/')
def uploadpaper(request):
	if request.method == 'POST':
		if request.FILES:
			b = UploadIdentification()
			b.user = request.user
			b.identification_doc = request.FILES['identificationdoc']
			b.save()
			return HttpResponseRedirect('/main/dashboard/')
	return render(request,'main/site/uploadprint.djt',{})

@login_required(login_url='/main/signin/')
def dashboard(request):
	response = {}
	docs = UploadIdentification.objects.filter(user=request.user)
	response['docs']=docs
	if request.user.is_superuser:
		response['users'] = UserProfile.objects.all()
		response['applications'] = UploadIdentification.objects.all()
		response['accepted']=UploadIdentification.objects.filter(is_accepted=1).count()
		response['rejected']=UploadIdentification.objects.filter(is_accepted=2).count()
		response['waiting']=UploadIdentification.objects.filter(is_accepted=0).count()
		return render(request,'main/site/admin-dashboard.djt',response)
	return render(request,'main/site/dashboard.djt',response)

@login_required(login_url='/main/signin/')
def viewuser(request,uid):
	response = {}
	p =UserProfile.objects.get(id=uid)
	if request.method == 'POST':
		p.user.first_name = request.POST['firstname']
		p.user.last_name = request.POST['lastname']
		p.user.save()
		p.phone = request.POST['phone']
		p.country = request.POST['country']
		p.father_name = request.POST['fname']
		p.address = request.POST['address']
		p.native_lang = request.POST['native_lang']
		p.lang = request.POST['lang']
		p.save()
		return HttpResponseRedirect('/main/viewuser/'+str(p.id))
	response['profile'] = p
	response['docs']= UploadIdentification.objects.filter(user=p.user)
	return render(request,'main/site/viewuser.djt',response)

@login_required(login_url='/main/signin/')
def viewapplication(request,aid):
	response = {}
	doc = UploadIdentification.objects.get(id=aid)
	if request.method == 'POST':
		doc.reason_to_reject = request.POST['rtoreject']
		doc.reason_to_move = request.POST['rtomove']
		doc.applicant_score = request.POST['score']
		if request.POST['status'] == 'Accepted':
			doc.is_accepted = 1
		elif request.POST['status'] == 'Rejected':
			doc.is_accepted = 2
		doc.save()
		return HttpResponseRedirect('/main/viewapplication/'+str(doc.id))
	response['doc'] = doc
	response['profileid']= doc.user.userprofile.id
	return render(request,'main/site/viewapplication.djt',response)
