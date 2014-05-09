# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.contenttypes.models import ContentType
from .models import Category, News
from .forms import NewsForm
# Use our mixin to allow only some users make actions
from places_core.mixins import LoginRequiredMixin

class CategoryListView(ListView):
    """
    Categories for place's blog
    """
    model = Category
    context_object_name = 'categories'
    
class CategoryDetailView(DetailView):
    """
    Show category info
    """
    model = Category
    
class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    Create new category
    """
    model = Category
    fields = ['name', 'description']

class NewsListView(ListView):
    """
    News index for chosen location
    """
    model = News
    context_object_name = 'entries'
    
class NewsDetailView(DetailView):
    """
    Detailed news page
    """
    model = News

    def get_context_data(self, **kwargs):
        news = super(NewsDetailView, self).get_object()
        content_type = ContentType.objects.get_for_model(news)
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['content_type'] = content_type.pk
        context['title'] = news.title
        return context
    
class NewsCreateView(LoginRequiredMixin, CreateView):
    """
    Create new entry
    """
    model = News
    form_class = NewsForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(NewsCreateView, self).form_valid(form)
