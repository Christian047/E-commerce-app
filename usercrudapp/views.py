from itertools import product
from django.shortcuts import render, HttpResponse, redirect, get_list_or_404, get_object_or_404
from django. views.generic import View, UpdateView
from base.models import *
from django.contrib.auth.mixins import LoginRequiredMixin


# # Create your views here.

# categories = Category.objects.all()

        

# class Pendingpage(LoginRequiredMixin, View):
#     login_url = 'login'
#     def get(self, request, pk):
#         pending_products = get_object_or_404(Product, pk=pk)
#         if request.user.is_staff:
#             pending_products = Product.objects.filter(status='pending')
#         else:
#             pending_products = Product.objects.filter(author=request.user, status='pending')

#         return render(request, 'base/pendingpage.html', {'pending_products': pending_products})
    

#     def post(self, request, pk):
#         pending_products = get_object_or_404(Product, pk=pk) 
#         if request.user.is_staff:
#             try:
#                 pending_products = get_object_or_404(Product, pk=pk)    
#                 if request.POST.get('approve'):
#                     pending_products.status = 'approved'
#                     pending_products.save()
#             except: pending_products = None 

#         context =  {
#             'pending_products': pending_products
#             }      

#         return redirect('base/pendingpage.html', context=context, pk=pk)
    


# class ApprovePost(LoginRequiredMixin, View):
#     login_url = 'login'
#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             'product': product,
#         }
#         return render(request, 'base/penapprove.html', context=context)

#     def post(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         product.status = 'approved'
#         product.save()
#         return redirect('store')
    

# class UnapprovePost(LoginRequiredMixin, View):
#     login_url = 'login'
#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             'product': product,
#         }
#         return render(request, 'base/unapprove.html', context=context)

#     def post(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         product.status = 'pending'
#         product.save()
#         return redirect('store')

class Pendingpage(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        if request.user.is_staff:
            pending_products = Product.objects.filter(status='pending')
        else:
            pending_products = Product.objects.filter(author=request.user, status='pending')

        return render(request, 'base/pendingpage.html', {'pending_products': pending_products})

    def post(self, request, pk):
        pending_product = get_object_or_404(Product, pk=pk)

        if request.user.is_staff:
            if request.POST.get('approve'):
                pending_product.status = 'approved'
                pending_product.save()
            elif request.POST.get('unapprove'):
                pending_product.status = 'pending'  # You can set it to any status you prefer
                pending_product.save()

        return redirect('base:pendingpage', pk=pk)
    
