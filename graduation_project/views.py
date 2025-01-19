from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.conf import settings 
from django.db.models import Q, Count
from .models import GraduationProject, Category
from accounts.models import UserProfile




def ProjectList(request):
    # Get filter parameters from the request
    category_id = request.GET.get('category')
    doctor_id = request.GET.get('doctor')
    graduation_year = request.GET.get('graduation_year')

    # Start with all accepted projects
    projects = GraduationProject.objects.filter(status='accepted')

    # Apply filters
    if category_id and category_id != 'all':
        projects = projects.filter(category_id=category_id)
    if doctor_id:
        projects = projects.filter(doctor_id=doctor_id)
    if graduation_year:
        projects = projects.filter(graduation_year=graduation_year)

    # Fetch all categories for the sidebar
    categories = Category.objects.all()

    # Fetch the top 10 doctors with the most projects (only accepted projects)
    doctors = UserProfile.objects.filter(is_doctor=True).annotate(
        book_count=Count('user__doctor_projects', filter=Q(user__doctor_projects__status='accepted'))
    ).order_by('-book_count')[:10]

    # Fetch the latest 10 accepted projects for the main section
    projects_main = GraduationProject.objects.filter(status='accepted').order_by('-id')[:10]
    count_books = projects_main.count()

    # Check if the request is from HTMX
    if request.headers.get('HX-Request'):
        # Render only the project list for HTMX requests
        return render(request, "partials/project_list.html", {
            "projects": projects,
        })
    else:
        # Render the full page for regular requests
        return render(request, "projects.html", {
            "projects_main": projects_main,
            "count_books": count_books,
            "projects": projects,
            "categories": categories,
            "doctors": doctors,
        })
    





class ProjectDetail(generic.DetailView):
    model = GraduationProject
    template_name = "project_detail.html"

    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj




class AddProject(UserPassesTestMixin, generic.CreateView):
    model = GraduationProject
    fields = "__all__"  # Use this or form_class, but not both
    template_name = "add_project.html"
    success_url = '/'  # Use reverse_lazy for success URL

    def form_valid(self, form):
        # Set the leader and status before saving the form
        form.instance.leader = self.request.user.profile
        form.instance.status = 'pending'  # Set status to pending
        response = super().form_valid(form)

        # Send email notification to the leader
        send_mail(
            'Project Submitted',
            'Your project has been submitted and is awaiting admin approval.',
            'mmohamedabdelm@gmail.com',
            [self.request.user.email],
            fail_silently=False,
        )

        return response  # Return the response after sending the email

    def test_func(self):
        # Only allow access if the user is a leader
        return self.request.user.profile.is_leader







def approve_project(request, project_id):
    project = get_object_or_404(GraduationProject, id=project_id)
    project.status = 'accepted'  # تغيير حالة المشروع لـ "مقبول"
    user = request.user
    project.save()

    # إرسال إيميل للقائد
    send_mail(
        'تم قبول المشروع',
        f'تم قبول مشروعك "{project.title}".',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    messages.success(request, f'تم قبول مشروعك "{project.title}".')
    return redirect(request.META.get('HTTP_REFERER', '/'))






def reject_project(request, project_id):
    project = get_object_or_404(GraduationProject, id=project_id)
    project.status = 'rejected'  # تغيير حالة المشروع لـ "مرفوض"
    user = request.user
    project.save()

    # إرسال إيميل للقائد
    send_mail(
        'تم رفض المشروع',
        f'تم رفض مشروعك "{project.title}".',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    messages.success(request, f'تم رفض مشروعك "{project.title}".')
    return redirect(request.META.get('HTTP_REFERER', '/'))





def pending_projects(request):
    pending_projects = GraduationProject.objects.filter(status='pending')
    return render(request, 'pending_projects.html', {'projects': pending_projects})






# class AddProject(UserPassesTestMixin, generic.CreateView):
#     model = GraduationProject
#     fields = "__all__"
#     template_name = "add_project.html"
#     success_url = '/'  # Replace "home" with your desired success URL

#     def test_func(self):
#         # Only allow access if the user is a leader
#         return self.request.user.profile.is_leader

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