from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,MessegesForm,FeedbackForm
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

User = get_user_model()

# # Create your views here

def chat_view(request, product_id,user_id):
    product = Product.objects.get(id=product_id)
    qs1 = Messeges.objects.prefetch_related('user','accepter').filter(product=product,user=request.user.id)
    qs2 = Messeges.objects.prefetch_related('user','accepter').filter(product=product,accepter=request.user.id)
    messeges = qs1.union(qs2).order_by('date_create')
    form = MessegesForm(request.POST or None)
    if form.is_valid():
        new_disput = form.save(commit=False)
        text = form.cleaned_data['text']
        new_disput.text = text
        new_disput.user = request.user
        if request.user == product.user:
            new_disput.accepter = messeges.first().user
        else:
            new_disput.accepter = product.user
        new_disput.product = product
        new_disput.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'chat-2.html', {'product':product,'messeges':messeges,'form': form})

def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product.html', {'product': product})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'details.html', {'product': product})

def feedback_view(request, product_id):
    form = FeedbackForm(request.POST or None, request.FILES or None)
    product = get_object_or_404(Product, id=product_id)
    if form.is_valid():
        new_feed = form.save(commit=False)
        text = form.cleaned_data['text']
        adv = form.cleaned_data['adv']
        disadv = form.cleaned_data['disadv']
        files = form.cleaned_data['files']
        rating = form.cleaned_data['rating']
        user = User.objects.get(id = request.user.id)
        new_feed.user = user
        new_feed.text = text
        new_feed.adv = adv
        new_feed.files = files
        new_feed.rating= rating
        new_feed.product= product
        new_feed.save()
        return HttpResponseRedirect(f'../product/{product_id}')
    context = {
        'form': form,
        'product':product
    }
    return render(request, 'review.html', context)


