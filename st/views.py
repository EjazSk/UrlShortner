from django.shortcuts import render, get_object_or_404
from .models import Shortner,Analytic
from .forms import ShortnerForm
from django.http import HttpResponseRedirect,HttpResponse
from .utils import get_client_ip
#from __future__ import unicode_literals
from user_agents import parse
from django.contrib.auth.decorators import login_required
from registration.models import RegistrationProfile  
from django.core.exceptions import MultipleObjectsReturned
# Create your views here.


from django.http import JsonResponse

@login_required(login_url='/accounts/login/')
def home(request):
	form = ShortnerForm(request.POST or None)
	context={'form':form}
	template='home.html'
	if form.is_valid():
		form.user=request.user
		#print(form.user)
		form.save(commit=False)
		

		new_url=form.cleaned_data.get('url_field')
		#print(new_url)
		try:

			obj,created = Shortner.objects.get_or_create(url_field=new_url,user=request.user)
			print(obj.url_field)
			context={'form':form, 'object':obj}
			if created:
				qs=Shortner.objects.filter(url_field=obj.url_field).first()
				#qs = get_object_or_404(Shortner,url_field=obj.url_field,user=None)
				qs.user=request.user
				qs.save()
				template='success.html'
			else:
				template='exists.html'
		
		except MultipleObjectsReturned:
			obj= Shortner.objects.filter(url_field=new_url).first()
			context={'ojects':obj}
			print(context)
			print('here is context')
			#print(Shortner.objects.filter(url_field=obj.url_field).first())
			template='exists.html'
	
	return render(request,template,context)

@login_required(login_url='/accounts/login/')
def ShortnerView(request,shortcode=None):
	qs = get_object_or_404(Shortner,shortcode=shortcode)
	qs.count+=1
	#print(qs.url_field)
	qs.save()
	#print('the ip is' +str(get_client_ip(request)))
	analytic_obj = Analytic()
	

	ua_string = request.META['HTTP_USER_AGENT']
	user_agent = parse(ua_string)



	# artist = Artist.objects.get(id=1)  
	# newMp3 = Mp3(title="sth", artist=artist)

	analytic_obj.url=Shortner.objects.get(id=qs.id)
	#analytic_obj.url= qs.url_field

	# Accessing user agent's browser attributes
	analytic_obj.browser = user_agent.browser.family  # returns 'Mobile Safari'
	analytic_obj.browser_version = user_agent.browser.version_string   # returns '5.1'



	# Accessing user agent's operating system properties
	analytic_obj.os = user_agent.os.family  # returns 'iOS'
	analytic_obj.os_version = user_agent.os.version_string  # returns '5.1'

	# Accessing user agent's device properties
	analytic_obj.device = user_agent.device.family  # returns 'iPhone'
	analytic_obj.device_brand = str(user_agent.device.brand) # returns 'Apple'
	analytic_obj.device_model=str(user_agent.device.model) # returns 'iPhone'

	
	analytic_obj.is_mobile= user_agent.is_mobile # returns True
	analytic_obj.is_tablet= user_agent.is_tablet # returns False
	analytic_obj.is_touch_capable = user_agent.is_touch_capable # returns False
	analytic_obj.is_pc = user_agent.is_pc # returns False
	analytic_obj.is_bot= user_agent.is_bot # returns False
	analytic_obj.save()
	
	print('here')
	print(qs.url_field)
	return HttpResponseRedirect(qs.url_field)


@login_required(login_url='/accounts/login/')
def analytic_view_graph(request,id=None):
	obj=get_object_or_404(Shortner,id=id)
	# >>> Entry.objects.filter(blog__name='Beatles Blog')

	analytic = Analytic.objects.filter(url=obj)
	

	print(obj)
	print(analytic)
	context={'object':obj,'analytic':analytic}

	return render(request,'graphview.html',context)


@login_required(login_url='/accounts/login/')
def get_data(request, *args, **kwargs):
	name=['ajaz','ganesh','alex','max']
	rating=[10,10,8,7]
	data = {
		"labels": name,
		"default":rating,
	}
	return JsonResponse(data) # http response

@login_required(login_url='/accounts/login/')
def my_shortened_urls(request):


	qs=Shortner.objects.filter(user=request.user)


	context={'qs':qs}	
	return render(request,'myurls.html',context)	



@login_required(login_url='/accounts/login/')
def analytic_view_table(request,id=None):
	obj=get_object_or_404(Shortner,id=id,user=request.user)
	analytic = Analytic.objects.filter(url=obj)
	context={'object':obj,'analytic':analytic}
	return render(request,'tableview.html',context)

