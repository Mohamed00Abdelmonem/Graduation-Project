from django.shortcuts import render, redirect
from .models import GraduationProject
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin



class ProjectDetail(generic.DetailView):
    model = GraduationProject
    template_name = "project_detail.html"


class AddProject(UserPassesTestMixin, generic.CreateView):
    model = GraduationProject
    fields = "__all__"
    template_name = "add_project.html"
    success_url = '/'  # Replace "home" with your desired success URL

    def test_func(self):
        # Only allow access if the user is a leader
        return self.request.user.profile.is_leader

    # def handle_no_permission(self):
    #     # Redirect users who don't pass the test_func
    #     return redirect("permission_denied")  # Replace with your desired permission denied URL or view





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