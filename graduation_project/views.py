from django.shortcuts import render
from .models import GraduationProject
from django.views import generic
from django.contrib.auth.decorators import login_required
class ProjectDetail(generic.DetailView):
    model = GraduationProject
    template_name = "project_detail.html"



@login_required(login_url='/accounts/login/')
def like_post(request, id):
    if request.method == "POST":
        instance = GraduationProject.objects.get(id=id)
        if not instance.likes.filter(id=request.user.id).exists():
            instance.likes.add(request.user)
            instance.save() 
            return render( request, 'partials/likes_area.html', context={'object':instance})
        else:
            instance.likes.remove(request.user)
            instance.save() 
            return render( request, 'partials/likes_area.html', context={'object':instance})    