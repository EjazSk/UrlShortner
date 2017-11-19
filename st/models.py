from django.db import models
from django.contrib.auth.models import User

import string
import random
# Create your models here.
def shortcodeGenerator(length=6, chars=string.ascii_lowercase + string.digits+ string.ascii_uppercase):
	code=''
	#print(range(0,length-1))
	for x in range(0,length):
		code+=random.choice(chars)
	exists= Shortner.objects.filter(shortcode=code).exists()
	if exists:
		shortcodeGenerator()

	return code	


class Shortner(models.Model):
	user              = models.ForeignKey(User,null=True)
	url_field         = models.CharField(max_length=300)
	shortcode         = models.CharField(max_length=6,blank=True , null = True)
	created	          = models.DateTimeField(auto_now_add=True)
	updated           = models.DateTimeField(auto_now=True)
	count             = models.IntegerField(default=0)
	# browser	  		  = models.CharField(max_length=300,blank=True,null=True)
	# browser_version	  = models.CharField(max_length=300,blank=True,null=True)
	# os                = models.CharField(max_length=300,blank=True,null=True)
	# os_version        = models.CharField(max_length=300,blank=True,null=True)
	# device            = models.CharField(max_length=300,blank=True,null=True)
	# device_brand      = models.CharField(max_length=300,blank=True,null=True)
	# device_model      = models.CharField(max_length=300,blank=True,null=True)
	# is_mobile         = models.NullBooleanField()
	# is_tablet         = models.NullBooleanField()
	# is_touch_capable  = models.NullBooleanField()
	# is_pc             = models.NullBooleanField()
	# is_bot            = models.NullBooleanField()
	class Meta:
		unique_together = (('user', 'url_field'),)

	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == "":
			self.shortcode = shortcodeGenerator()
		#print(self.request.user)	
		# if not "http" in self.url:
		# 	self.url = "http://" + self.url
		super(Shortner, self).save(*args, **kwargs)



	def __str__(self):
		return(str(self.url_field))

	def get_short_url(self):
		return 'http://127.0.0.1:8000/%s' %(self.shortcode)


class Analytic(models.Model):
	url               = models.ForeignKey(Shortner,related_name='analytic',on_delete=models.CASCADE,) 
	browser	  		  = models.CharField(max_length=300,blank=True,null=True)
	browser_version	  = models.CharField(max_length=300,blank=True,null=True)
	os                = models.CharField(max_length=300,blank=True,null=True)
	os_version        = models.CharField(max_length=300,blank=True,null=True)
	device            = models.CharField(max_length=300,blank=True,null=True)
	device_brand      = models.CharField(max_length=300,blank=True,null=True)
	device_model      = models.CharField(max_length=300,blank=True,null=True)
	is_mobile         = models.NullBooleanField()
	is_tablet         = models.NullBooleanField()
	is_touch_capable  = models.NullBooleanField()
	is_pc             = models.NullBooleanField()
	is_bot            = models.NullBooleanField()


	def __str__(self):
		return(str('Analytics of %s')%(self.url))





# class Analytics(models.Model):
# 	url       = models.OneToOneField(Shortner)
# 	count     = models.IntegerField(default=0)
# 	timestamp = models.DateTimeField(auto_now_add=True)

# 	# def save(self, *args, **kwargs):
# 	# 	self.count+=1
# 	# 	super(Shortner, self).save(*args, **kwargs)