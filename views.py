from django.shortcuts import render
from asenzor.lib.ResourceView import ResourceView
from .models import Ticket,Service
from django.contrib.auth.decorators import login_required
# Create your views here.
class Tickets(ResourceView):
	model=Ticket
	filter={"user":lambda request,instance: request.user==instance.user}
	index_template="helpdesk/list.html"
	edit_template="helpdesk/edit.html"


@login_required(login_url='/helpdesk/login/')
def index(request):
	services=Service.objects.filter(user=request.user)
	return render(request,"helpdesk/index.html",
		{"services":services})
def faq(request,name=None):
	faq=None
	faqs=[]
	if name:
		faq=Faq.objects.get(name=name)
	else:
		faqs=Faq.objects.all()

	return render(request,"helpdesk/faq.html",{
		"faq":faq,
		"faqs":faqs})

def login(request):
	from django.conf import settings
	from django.contrib.auth import authenticate,login

	if request.method=="POST":

		user = authenticate(
			username=request.POST.get("username"), 
			password=request.POST.get("password"))
		if user:
			request.user=user
			login(request, user)
			return HttpResponseRedirect(settings.HELPDESK_URL)
	else:
		return render(request,"helpdesk/login.html",{
			"LOGOUT_REDIRECT_URL":settings.HELPDESK_REDIRECT_URL
			})