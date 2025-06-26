from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings 
from django.db.models import Q, Count
from .models import GraduationProject, Category, Review, ProjectImages
from accounts.models import UserProfile
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import GraduationProject, ProjectImages
from .forms import GraduationProjectForm




from django.contrib.auth import get_user_model
User = get_user_model()


# ___________________________________________________________________________________



# @cache_page(60 * 5)
def ProjectList(request):
    # Get search query and filter parameters
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    doctor_id = request.GET.get('doctor')
    graduation_year = request.GET.get('graduation_year')

    # Start with all accepted projects
    projects = GraduationProject.objects.filter(status='accepted').order_by('-created_at')
    projects_count = GraduationProject.objects.filter(status='accepted').count()
    projects_count = GraduationProject.objects.filter(status='accepted').count()
    

    # Apply search query (if provided)
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |  # Search by title
            Q(description__icontains=search_query)  # Search by description
        )

    # Apply filters (if provided)
    if category_id and category_id != 'all':
        projects = projects.filter(category_id=category_id)
    if doctor_id:
        projects = projects.filter(doctor_id=doctor_id)
    if graduation_year:
        projects = projects.filter(graduation_year=graduation_year)



   # Pagination
    page = request.GET.get('page', 1)  # Get the current page number from the request
    paginator = Paginator(projects, 8)  # Show 10 projects per page
    try:
        paginated_projects = paginator.page(page)
    except PageNotAnInteger:
        paginated_projects = paginator.page(1)  # If page is not an integer, deliver first page
    except EmptyPage:
        paginated_projects = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page



    # Fetch all categories for the sidebar
    categories = Category.objects.all()

    # Fetch the top 10 doctors with the most projects (only accepted projects)
    doctors = UserProfile.objects.filter(is_doctor=True).annotate(
        book_count=Count('user__doctor_projects', filter=Q(user__doctor_projects__status='accepted'))
    ).order_by('-book_count')[:10]

    # Check if the request is from HTMX
    if request.headers.get('HX-Request'):
        # Render only the project list for HTMX requests
        return render(request, "partials/project_list.html", {
            "projects": projects,
        })
    else:
        # Render the full page for regular requests
        return render(request, "projects.html", {
            "projects": projects,
            "projects_count": projects_count,
            "projects": paginated_projects,
            "categories": categories,
            "doctors": doctors,
        })
    


# ___________________________________________________________________________________



def project_detail(request, slug):
    # Get the current project
    current_project = get_object_or_404(GraduationProject, slug=slug)
    
    # Increment the view count for the current project
    current_project.view_count += 1
    current_project.save()

    # Get related projects in the same category, excluding the current project
    related_projects = GraduationProject.objects.filter(
        category=current_project.category
    ).exclude(id=current_project.id)[:5]  # Limit to 5 related projects (optional)

    # Render the template with context
    return render(request, 'project_detail.html', {
        'object': current_project,
        'related_projects': related_projects,
    })


# __________________________________________________________________________________

@login_required

def add_review(request, slug):
        project = GraduationProject.objects.get(slug=slug)
        comments = request.POST['comments']
        
        Review.objects.create(
            project=project,
            comments=comments,
            reviewer=request.user
        )

        return redirect(f'/project/book/{project.slug}')

# ___________________________________________________________________________________



@login_required
def delete_review(request, slug, review_id):
    project = get_object_or_404(GraduationProject, slug=slug)
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)

    if request.method == 'POST':
        review.delete()
        return redirect(f'/project/book/{project.slug}')

    # If accessed via GET, redirect back to the project detail page
    return redirect('project:detail', slug=project.slug)



# __________________________________________________________________________________


class AddProject(UserPassesTestMixin, generic.CreateView):
    model = GraduationProject
    form_class = GraduationProjectForm

    template_name = "add_project.html"
    success_url = '/'  # Use reverse_lazy for success URL

    def form_valid(self, form):
        # Check if the leader has already added a project
        existing_project = GraduationProject.objects.filter(author=self.request.user).exists()
        if existing_project:
            messages.error(self.request, 'لقد قمت بإضافة مشروع واحد بالفعل، لا يمكنك إضافة أكثر من مشروع.')
            return self.form_invalid(form)

        # Set the author and status before saving the form
        form.instance.author = self.request.user
        form.instance.status = 'pending'  # Set status to pending

        # Save the form and get the project instance
        project = form.save()  # Save the form first to get the project instance

       # Handle uploaded images
        images = self.request.FILES.getlist('images')

        for image in images:
            ProjectImages.objects.create(project=project, image=image)

        # Send email notification to the leader
        # Prepare context for email
        context = {
            'user': self.request.user,
            'project': project,
        }

        # Render email content
        html_content = render_to_string('emails/new_project.html', context)
        text_content = strip_tags(html_content)

        # Send the email
        email = EmailMultiAlternatives(
            subject='مشروع تخرج جديد للمراجعة',
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.request.user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        messages.success(self.request, 'تم إرسال المشروع بنجاح! سيتم مراجعته من قبل المشرف.')

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the success_create_project page only if the form is valid
        return reverse('project:success_create_project')

    def test_func(self):
        # Only allow access if the user is a leader
        return self.request.user.profile.is_leader
    

# ___________________________________________________________________________________

class UpdateProject(UserPassesTestMixin, generic.UpdateView):
    model = GraduationProject
    fields = [
        'title', 'title_ar', 'description', 'sub_description', 'graduation_year', 
        'category', 'doctor', 'students', 'supervisors', 'book_pdf', 'images', 'video'
    ]
    template_name = "update_project.html"
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['project'] = project  # ⬅️ مهم جدًا للـ slug في التمبلت
        context['existing_images'] = project.project_image.all()
        
        if project.book_pdf:
            context['existing_book_pdf'] = project.book_pdf.url
        if project.video:
            context['existing_video'] = project.video.url
            
        return context

    def form_valid(self, form):
        project = form.save()

        new_images = self.request.FILES.getlist('project_images')
        for image in new_images:
            ProjectImages.objects.create(project=project, image=image)

        project.status = 'pending'
        project.save()


        
        # Prepare context for email
        context = {
            'user': self.request.user,
            'project': project,
        }       # إنشاء محتوى البريد من قالب HTML
        html_content = render_to_string('emails/project_updated.html', context)
        text_content = strip_tags(html_content)

        # إرسال البريد
        email = EmailMultiAlternatives(
            subject='تم تعديل مشروع التخرج الخاص بك',
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.request.user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()


        # Add a success message to be displayed on the same page
        messages.success(self.request, 'تم تحديث المشروع بنجاح! سيتم مراجعته من قبل المشرف.')

        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.author or self.request.user.is_staff

# حذف صورة
@login_required
def delete_project_image(request, project_slug, image_id):
    image = get_object_or_404(
        ProjectImages,
        id=image_id,
        project__slug=project_slug,
        project__author=request.user
    )
    image.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


# ______________________________________________________________


def delete_proejct(request, slug):
    project = GraduationProject.objects.get(slug=slug)
    project.delete()
    return redirect('profile')



# _________________________________________________________




def approve_project(request, project_id):
    # التحقق من أن المستخدم موظف (is_staff)
    if not request.user.is_staff:
        messages.error(request, 'غير مصرح لك بتنفيذ هذا الإجراء.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # جلب المشروع بناءً على ID
    project = get_object_or_404(GraduationProject, id=project_id)

   
    # التحقق من وجود author و email
    if not project.author or not hasattr(project.author, 'email') or not project.author.email:
        messages.error(request, 'لا يمكن إرسال بريد إلكتروني لأن البريد الإلكتروني للقائد غير متوفر.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # تغيير حالة المشروع لـ "مقبول"
    project.status = 'accepted'
    project.save()

    # تحديد البيانات الأساسية
    subject = 'تم قبول مشروعك'
    to_email = [project.author.email]  # البريد الإلكتروني للقائد

    # إنشاء النصوص (HTML وPLAIN)
    context = {
        'project_title': project.title,
        'approval_date': project.updated_at.strftime('%Y-%m-%d'),
        'project_url': request.build_absolute_uri(project.get_absolute_url()),
    }

    # استخدم قالب HTML للإيميل
    html_content = render_to_string('emails/approve_project_email.html', context)
    text_content = strip_tags(html_content)  # نسخة نصية بسيطة من الإيميل

    # إنشاء الرسالة
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=to_email
    )
    email.attach_alternative(html_content, "text/html")  # إضافة النسخة HTML
    email.send()

    # إضافة رسالة نجاح للمشرف
    messages.success(request, f'تم قبول مشروع "{project.title}" بنجاح.')

    # إعادة التوجيه إلى الصفحة السابقة أو الرئيسية
    return redirect(request.META.get('HTTP_REFERER', '/'))
# ___________________________________________________________________________________


def reject_project(request, project_id):
    # جلب المشروع بناءً على ID
    project = get_object_or_404(GraduationProject, id=project_id)

   

    # التحقق من وجود author و email
    if not project.author or not hasattr(project.author, 'email') or not project.author.email:
        messages.error(request, 'لا يمكن إرسال بريد إلكتروني لأن البريد الإلكتروني للقائد غير متوفر.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    # تغيير حالة المشروع لـ "مرفوض"
    project.status = 'rejected'
    project.save()
    project.delete()
    # تحديد البيانات الأساسية
    subject = 'تم رفض مشروعك'
    to_email = [project.author.email]  # البريد الإلكتروني للقائد

    # إنشاء النصوص (HTML وPLAIN)
    context = {
        'project_title': project.title,
    }

    # استخدم قالب HTML للإيميل
    html_content = render_to_string('emails/reject_project_email.html', context)
    text_content = strip_tags(html_content)  # نسخة نصية بسيطة من الإيميل

    # إنشاء الرسالة
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=to_email
    )
    email.attach_alternative(html_content, "text/html")  # إضافة النسخة HTML
    email.send()

    # إضافة رسالة نجاح للمشرف
    messages.success(request, f'تم رفض مشروع "{project.title}" بنجاح.')

    # إعادة التوجيه إلى الصفحة السابقة أو الرئيسية
    return redirect(request.META.get('HTTP_REFERER', '/'))



# ___________________________________________________________________________________


def temporary_reject_project(request, project_id):
    # جلب المشروع بناءً على ID
    project = get_object_or_404(GraduationProject, id=project_id)

    

    # جلب سبب الرفض من النموذج
    rejection_reason = request.POST.get('rejection_reason', 'لم يتم تحديد سبب')

    # التحقق من وجود author و email
    if not project.author or not hasattr(project.author, 'email') or not project.author.email:
        messages.error(request, 'لا يمكن إرسال بريد إلكتروني لأن البريد الإلكتروني للقائد غير متوفر.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # تغيير حالة المشروع لـ "مرفوض مؤقتًا"
    project.status = 'temporary_rejection'
    project.save()
    
    # تحديد البيانات الأساسية
    subject = 'تم رفض مشروعك مؤقتًا'
    to_email = [project.author.email]  # البريد الإلكتروني للقائد

    # إنشاء النصوص (HTML وPLAIN)
    context = {
        'project_title': project.title,
        'rejection_reason': rejection_reason,
    }

    # استخدم قالب HTML للإيميل
    html_content = render_to_string('emails/temporary_reject_email.html', context)
    text_content = strip_tags(html_content)  # نسخة نصية بسيطة من الإيميل

    # إنشاء الرسالة
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=to_email
    )
    email.attach_alternative(html_content, "text/html")  # إضافة النسخة HTML
    email.send()

    # إضافة رسالة نجاح للمشرف
    messages.success(request, f'تم رفض مشروع "{project.title}" بنجاح مؤقتًا.')

    # إعادة التوجيه إلى الصفحة السابقة أو الرئيسية
    return redirect(request.META.get('HTTP_REFERER', '/'))


# _______________________________________________________


def pending_projects(request):
    # Get the status filter from the request (default to 'pending' if not provided)
    status_filter = request.GET.get('status', 'pending')
    search_query = request.GET.get('search', '')

    # Filter projects based on the selected status
    if status_filter == 'all':
        pending_projects = GraduationProject.objects.filter(status__in=['pending', 'temporary_rejection'])
    elif status_filter == 'temporary_rejection':
        pending_projects = GraduationProject.objects.filter(status='temporary_rejection')
    else:
        pending_projects = GraduationProject.objects.filter(status='pending')

    # Filter projects by title if search query is provided
    if search_query:
        pending_projects = pending_projects.filter(title__icontains=search_query)

    # Pagination
    page = request.GET.get('page', 1)  # Get the current page number from the request
    paginator = Paginator(pending_projects, 15)  # Show 15 projects per page
    try:
        paginated_projects = paginator.page(page)
    except PageNotAnInteger:
        paginated_projects = paginator.page(1)  # If page is not an integer, deliver first page
    except EmptyPage:
        paginated_projects = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page

    # Pass the filtered projects, status filter, and search query to the template
    return render(request, 'pending_projects.html', {
        'projects': paginated_projects,
        'status_filter': status_filter,
        'search_query': search_query,
    })


# _______________________________________________________________________




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
        


# ___________________________________________________________________________________
