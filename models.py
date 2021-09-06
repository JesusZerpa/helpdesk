from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
from datetime import datetime
# Create your models here.
class Theme(models.Model):
	name=models.CharField("Nombre",max_length=250,unique=True)
	image=models.FileField("Archivo",upload_to="helpdesk/images/")
	decription=models.TextField("Descripcion")


class Package(models.Model):
	name=models.CharField("Nombre",max_length=250)
	codename=models.CharField("Codigo",max_length=250,unique=True)
	description=models.TextField("Descripcion")
	options=JSONField("Opciones")

class Template(models.Model):
	CURRENCY=[
		("usd","Dolar"),
		("eur","Euro"),
	]
	RECURRENCY=[
		("hour","Por Hora"),
		("day","Diario"),
		("15-31","Quience y ultimo"),
		("month","Mensual"),
		("3-month","Trimestral"),
		("6-month","Semestral"),
		("year","Anual"),
	]
	price=models.IntegerField("Precio")
	currency=models.CharField("Moneda",
		max_length=250,
		choices=CURRENCY,default="usd")
	recurrency=models.CharField("Recurrencia",max_length=250,
		help_text="Ciclo de facturacion ",
		choices=RECURRENCY,default="month")
	package=models.ForeignKey(Package,on_delete=models.CASCADE)
	def __str__(self):
		return f"Template[{self.id}]:{self.package.codename}"

class Service(models.Model):
	"""
	Es el servicio el cual estara asignado a un usuario
	por defecto el nombre del servicio es el nombre de 

	su plantilla dado que el servicio esta asignado al usuario
	un mismo servicio puede tener diferente precio dependiendo 
	del usuario 

	La definicion de precios en la 
	"""
	CURRENCY=[
		("usd","Dolar"),
		("eur","Euro"),
	]
	RECURRENCY=[
		("hour","Por Hora"),
		("day","Diario"),
		("15-31","Quience y ultimo"),
		("month","Mensual"),
		("3-month","Trimestral"),
		("6-month","Semestral"),
		("year","Anual"),
	]
	STATUS=[
		("active","Activo"),
		("suspend","Suspendido"),
		("cancel","Cancelado"),
	]
	price=models.IntegerField("Precio",
		blank=True,null=True,
		default=None)
	currency=models.CharField("Moneda",
		blank=True,null=True,
		max_length=250,
		default=None,
		choices=CURRENCY)
	status=models.CharField("Status",
		max_length=260,
		choices=STATUS,default="active")
	recurrency=models.CharField("Recurrencia",
		max_length=250,
		blank=True,null=True,
		help_text="Ciclo de facturacion ",
		choices=RECURRENCY,
		default=None)
	name=models.CharField("Nombre",max_length=250,blank=True,null=True)
	start_datetime=models.DateTimeField("Fecha inicio")
	suspend_datetime=models.DateTimeField("Tiempo suspendido",blank=True,null=True)
	end_datetime=models.DateTimeField("Fecha Fin",blank=True,null=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	template=models.ForeignKey(Template,on_delete=models.CASCADE)
	decription=models.TextField("Descripcion")


class Plan(models.Model):
	"""
	Grupo de servicios
	"""
	CURRENCY=[
		("usd","Dolar"),
		("eur","Euro"),
	]
	RECURRENCY=[
		("hour","Por Hora"),
		("day","Diario"),
		("15-31","Quience y ultimo"),
		("month","Mensual"),
		("3-month","Trimestral"),
		("6-month","Semestral"),
		("year","Anual"),
	]
	price=models.IntegerField("Precio")
	currency=models.CharField("Moneda",max_length=250)
	recurrency=models.CharField("Recurrencia",max_length=250,
		help_text="Ciclo de facturacion ",
		choices=RECURRENCY)
	decription=models.TextField("Descripcion")
	services=models.ManyToManyField("helpdesk.Service")

class Ticket(models.Model):
	PRIORITY=[("up","Alta"),
	        ("middle","Media"),
	        ("low","Baja")]
	STATUS=[
		("opened","Abierto"),
		("pending","Pendiente"),
		("responding","Respondido"),
		("closed","Cerrado"),
	]
	name=models.CharField("Nombre",max_length=250)
	theme=models.ForeignKey("helpdesk.Theme",on_delete=models.CASCADE)
	open_datetime=models.DateTimeField("Fecha apertura")
	closed_datetime=models.DateTimeField("Fecha cierre",blank=True,null=True)
	priority=models.CharField("Prioridad",max_length=250,choices=PRIORITY)
	status=models.CharField("Estatus",max_length=250,choices=STATUS)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	def __str__(self):
		return f"Ticket[{self.id}]: {self.name} | {self.priority}"

class TicketMessage(models.Model):
	author=models.ForeignKey(User,on_delete=models.CASCADE)
	datetime=models.DateTimeField("Fecha",default=datetime.now)
	ticket=models.ForeignKey("helpdesk.Ticket",on_delete=models.CASCADE)
	content=models.TextField("Contenido",max_length=250,)
	file=models.FileField("Archivo",
		max_length=250,
		upload_to="media/helpdesk/reportes/",
		null=True,blank=True)
