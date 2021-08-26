from django.shortcuts import render
from asenzor.lib.ResourceView import ResourceView
from .models import Ticket,Service
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
class Tickets(ResourceView):
	model=Ticket
	index_template="helpdesk/list.html"
	edit_template="helpdesk/edit.html"
	def query_filter(self,request,item):
		return item.user==request.user
	def middleware(self,view,request,data,id=None):
		from .models import TicketMessage
		if view=="edit":
			data["title"]="Editar Ticket"
			data["messages"]=TicketMessage.objects.filter(ticket=id)
	def edit(self,request,id,**kwargs):
		from .models import TicketMessage
		if request.method=="GET":
			return super().edit(request,id,**kwargs)
		elif request.method=="POST":
			ticket=Ticket.objects.get(id=int(id))
			message=TicketMessage.objects.create(
				ticket=ticket,
				content=request.POST.get("content"),
				author=request.user)
			if request.FILES:
				message.file=request.FILES["file"]
			return HttpResponseRedirect("")
			
			
			


@login_required(login_url='/helpdesk/login/')
def index(request):
	from asenzor.models import Option

	services=Service.objects.filter(user=request.user)

	return render(request,"helpdesk/index.html",
		{"services":services,
		 "company_logo":Option.get("company_logo",""),
		 "company_name":Option.get("company_name","")})
def faq(request,name=None):
	faq=None
	faqs=[]
	from asenzor.models import Site
	Post=Site.get_master().Post
	faq=None
	if name:
		faq=Post.objects.get(name=name,type="faq")
	else:
		try:
			faq=Post.objects.get(type="faq")
		except:
			pass
		faqs=Post.objects.filter(type="faq")


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
