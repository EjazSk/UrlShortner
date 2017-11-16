from django.shortcuts import render, get_object_or_404
from .models import Shortner,Analytic
from .forms import ShortnerForm
from django.http import HttpResponseRedirect
from .utils import get_client_ip
#from __future__ import unicode_literals
from user_agents import parse
# Create your views here.

def home(request):
	form = ShortnerForm(request.POST)
	context={'form':form}
	template='home.html'
	if form.is_valid():
		form.save(commit=False)
		new_url=form.cleaned_data.get('url_field')
		print(new_url)
		obj,created = Shortner.objects.get_or_create(url_field=new_url)
		print(obj)
		context={'form':form, 'object':obj}
		if created:
			template='success.html'
		else:
			template='exists.html'
			


	
	return render(request,template,context)


def ShortnerView(request,shortcode=None):
	qs = get_object_or_404(Shortner,shortcode=shortcode)
	qs.count+=1
	qs.save()
	#print('the ip is' +str(get_client_ip(request)))
	rs = get_object_or_404(Shortner,url_field=url)
	

	ua_string = request.META['HTTP_USER_AGENT']
	user_agent = parse(ua_string)

	# Accessing user agent's browser attributes
	rs.browser = user_agent.browser.family  # returns 'Mobile Safari'
	rs.browser_version = user_agent.browser.version_string   # returns '5.1'



	# Accessing user agent's operating system properties
	rs.os = user_agent.os.family  # returns 'iOS'
	rs.os_version = user_agent.os.version_string  # returns '5.1'

	# Accessing user agent's device properties
	rs.device = user_agent.device.family  # returns 'iPhone'
	rs.device_brand = str(user_agent.device.brand) # returns 'Apple'
	rs.device_model=str(user_agent.device.model) # returns 'iPhone'

	
	rs.is_mobile= user_agent.is_mobile # returns True
	rs.is_tablet= user_agent.is_tablet # returns False
	rs.is_touch_capable = user_agent.is_touch_capable # returns False
	rs.is_pc = user_agent.is_pc # returns False
	rs.is_bot= user_agent.is_bot # returns False
	rs.save()
	


	return HttpResponseRedirect(qs.url_field)

