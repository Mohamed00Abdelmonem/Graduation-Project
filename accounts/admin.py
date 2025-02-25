from django.contrib import admin
from .models import UserProfile, Experience

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'address', 'national_id', 'is_leader')  
    search_fields = ('user', 'full_name', 'national_id',  'phone_number' )

# ___________________________________________________________________________________


admin.site.register(Experience)







# ___________________________________________________________________________________

# this for what's show permessions in admin panel 
# عشان الموظف ميظهرش له ان هو يدي صلاحيات 

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# نموذج مخصص لإضافة المستخدمين
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # حدد الحقول المطلوبة فقط

# كلاس إداري مخصص
class CustomUserAdmin(BaseUserAdmin):
    # نموذج لإضافة المستخدمين
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')  # الحقول المطلوبة
        }),
    )

    # تخصيص الحقول المعروضة عند تعديل المستخدم
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)  # الحصول على الحقول الافتراضية
        
        if not request.user.is_superuser:  # إذا لم يكن المستخدم Superuser
            # إزالة 'groups' و 'user_permissions'
            fieldsets = [
                (name, {'fields': [field for field in options['fields'] if field not in ('is_staff', 'is_superuser','groups', 'user_permissions')]})
                for name, options in fieldsets
            ]
        
        return fieldsets

    # تخصيص القائمة المعروضة بناءً على صلاحيات المستخدم الحالي
    def get_list_display(self, request):
        if not request.user.is_superuser:  # إذا المستخدم ليس Superuser
            return ('username', 'is_active', 'is_staff')
        return ('username', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

    # تخصيص الفلاتر بناءً على صلاحيات المستخدم الحالي
    def get_list_filter(self, request):
        if not request.user.is_superuser:  # إذا المستخدم ليس Superuser
            return ('is_staff', 'is_active')
        return ('is_staff', 'is_superuser', 'is_active')

# تسجيل الكلاس الإداري المخصص
admin.site.unregister(User)  # إلغاء تسجيل الكلاس الافتراضي
admin.site.register(User, CustomUserAdmin)  # تسجيل الكلاس المخصص
