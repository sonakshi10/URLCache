from django.shortcuts import render, get_object_or_404
from links.models import Link
from links.forms import LinkForm
import requests
from bs4 import BeautifulSoup
from taggit.models import Tag
from django.template.defaultfilters import slugify

# Create your views here.
def link_list(request):
	links = Link.objects.all()
	atags = Link.tags.all()
	form = LinkForm(request.POST)
	if(form.is_valid()):
		newlink = form.save(commit=False)
		page = requests.get(newlink.url)
		soup = BeautifulSoup(page.content, 'html5lib')
		title_box = soup.find("title",attrs = {})
		title = title_box.text.strip()
		images=soup.findAll('img')
		if len(images) == 0:
			newlink.image_url="https://dummyimage.com/vga"
		if len(images) >= 2:
			newlink.image_url=images[1]['src']
		# print(images[0]['src'])
		else:
			newlink.image_url=images[0]['src']
		newlink.title=title
		
		newlink.save()
		form.save_m2m()
	
	context = {
		'tag':"All",
		'links': links,
		'tags':	atags,
		'form': form,
	}
	return render(request,'links/link_list.html',context)

def tagged(request,slug):
	tag = get_object_or_404(Tag,slug=slug)
	atags = Link.tags.all()
	links=Link.objects.filter(tags=tag)
	form = LinkForm(request.POST)
	if(form.is_valid()):
		newlink = form.save(commit=False)
		page = requests.get(newlink.url)
		soup = BeautifulSoup(page.content, 'html5lib')
		title_box = soup.find("title",attrs = {})
		title = title_box.text.strip()
		images=soup.findAll('img')
		if len(images) == 0:
			newlink.image_url="https://dummyimage.com/vga"
		if len(images) >= 2:
			newlink.image_url=images[1]['src']
		# print(images[0]['src'])
		else:
			newlink.image_url=images[0]['src']
		newlink.title=title
		
		newlink.save()
		form.save_m2m()
	context = {
		'tag':tag,
		'tags':atags,
		'links':links,
		'form': form,
   	}
	return render(request, 'links/link_list.html', context)
