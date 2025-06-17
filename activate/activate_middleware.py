from .models import ActivateLog
import httpagentparser  # لتحليل user agent

class ActivateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # تجاهل اللوجات الخاصة بلوحة التحكم
        if 'admin' not in str(request.path):
            user = request.user if request.user.is_authenticated else None

            # الحصول على بيانات user agent
            user_agent_str = request.META.get('HTTP_USER_AGENT', '')
            browser_info = httpagentparser.detect(user_agent_str)
            browser_name = browser_info.get('browser', {}).get('name', 'Unknown')

            # حفظ اللوج في قاعدة البيانات
            try:
                ActivateLog.objects.create(
                    user=user,
                    method=request.method,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    url=request.path,
                    user_agent=user_agent_str,
                    browser_name=browser_name,
                    status='Visited Page'
                )
            except Exception as e:
                # لو فيه أي خطأ في التخزين، اطبعه في الكونسول (أو سجّله في لوجينج لاحقاً)
                print(f"Logging error: {e}")

        return response
