from django.shortcuts import render
from .models import GraduationProject
from django.views import generic


class ProjectDetail(generic.DetailView):
    model = GraduationProject
    template_name = "project_detail.html"