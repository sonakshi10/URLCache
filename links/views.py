from django.shortcuts import render, get_object_or_404, redirect
from links.models import Link
from django.http import HttpResponse, HttpResponseRedirect
from links.forms import LinkForm
import requests
from bs4 import BeautifulSoup
from taggit.models import Tag
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
@login_required
def link_list(request):
    links = Link.objects.filter(author=request.user)
    # atags = Link.tags.all()
    atags = Tag.objects.filter(link__author=request.user).distinct()
    # print(a)
    form = LinkForm(request.POST)
    context = {
        "author": request.user.username,
        "tag": "All",
        "links": links,
        "tags": atags,
        "form": form,
    }
    if form.is_valid():
        newlink = form.save(commit=False)
        page = requests.get(newlink.url)
        soup = BeautifulSoup(page.content, "html5lib")
        title_box = soup.find("title", attrs={})
        title = title_box.text.strip()
        images = soup.findAll("img")
        if len(images) == 0:
            newlink.image_url = "https://dummyimage.com/vga"
        elif len(images) >= 2:
            newlink.image_url = images[1]["src"]
        # print(images[0]['src'])
        else:
            newlink.image_url = images[0]["src"]
        newlink.title = title
        newlink.author = request.user
        newlink.save()
        form.save_m2m()
        return HttpResponseRedirect("/", context)

    return render(request, "links/link_list.html", context)


@login_required
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    atags = Tag.objects.filter(link__author=request.user).distinct()
    links = Link.objects.filter(author=request.user).filter(tags=tag)
    form = LinkForm(request.POST)
    context = {
        "author": request.user.username,
        "tag": tag,
        "tags": atags,
        "links": links,
        "form": form,
    }
    if form.is_valid():
        newlink = form.save(commit=False)
        page = requests.get(newlink.url)
        soup = BeautifulSoup(page.content, "html5lib")
        title_box = soup.find("title", attrs={})
        title = title_box.text.strip()
        images = soup.findAll("img")
        if len(images) == 0:
            newlink.image_url = "https://dummyimage.com/vga"
        elif len(images) >= 2:
            newlink.image_url = images[1]["src"]
        # print(images[0]['src'])
        else:
            newlink.image_url = images[0]["src"]
        newlink.title = title
        newlink.author = request.user
        newlink.save()
        form.save_m2m()
        return HttpResponseRedirect("/", context)

    return render(request, "links/link_list.html", context)


def sign_up(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("/accounts/logout/")
    return render(request, "registration/sign_up.html", {"form": form})


def link_remove(request, pk):
    link = get_object_or_404(Link, auto_increment_id=pk)
    link.delete()
    return redirect("link_list")

