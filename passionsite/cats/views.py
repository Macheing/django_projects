
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from cats.models import Breed, Cat


# Create your views here.

# MainView of cats app.
class CatList(LoginRequiredMixin, View):
    def get(self, request):
        breed_count = Breed.objects.all().count()
        catList = Cat.objects.all()

        context = {'breed_count': breed_count, 'cat_list': catList}
        return render(request, 'cats/cat_list.html', context)

# CatView of cats app.
class CatView(LoginRequiredMixin, View):
    def get(self, request):
        breed = Breed.objects.all()
        context = {'breed_list': breed}
        return render(request, 'cats/breed_list.html', context)


# 1: Using Generic View, Model Approach; easy way of making views.
# CatCreate view
class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

# CatUpdate view
class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

# CatDelete view
class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

# BreedCreate view
class BreedCreate(LoginRequiredMixin, CreateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

# BreedUpdate view
class BreedUpdate(LoginRequiredMixin, UpdateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

# BreedDelete view
class BreedDelete(LoginRequiredMixin, DeleteView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

