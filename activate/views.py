

# عرض كل سجلات الدخول في جدول
from django.shortcuts import render
from .models import ActivateLog

def log_list_view(request):
    try:
        # استرجاع جميع السجلات مرتبة من الأحدث إلى الأقدم
        logs = ActivateLog.objects.all().order_by('-created_at')
        return render(request, 'activate/logs_list.html', {"logs": logs})
    except Exception as e:
        # في حالة حدوث خطأ، يتم إظهاره في الصفحة
        return render(request, 'activate/logs_list.html', {"error": str(e)})






# عرض الرسوم البيانية بناءً على عدد مرات الدخول لكل رابط
from collections import Counter
import matplotlib.pyplot as plt
from django.shortcuts import render
from activate.models import ActivateLog
import io, base64

def logs_chart_view(request):
    try:
        # استبعاد السجلات التي لا تحتوي على رابط
        logs = ActivateLog.objects.exclude(url__isnull=True)

        # حساب عدد مرات تكرار كل رابط
        url_counter = Counter(log.url for log in logs if log.url)
        top_urls = url_counter.most_common(5)  # أعلى 5 روابط فقط

        labels = [str(item[0]) for item in top_urls]  # أسماء الروابط
        counts = [item[1] for item in top_urls]       # عدد مرات الدخول

        # إنشاء الرسم البياني
        fig, axs = plt.subplots(1, 2, figsize=(16, 6))  # رسم Pie و Bar في صف واحد

        # رسم Pie Chart
        axs[0].pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
        axs[0].axis('equal')
        axs[0].set_title('Pie Chart: Most Visited URLs')

        # رسم Bar Chart
        axs[1].bar(labels, counts, color='lightblue')
        axs[1].set_title('Bar Chart: Visit Count per URL')
        axs[1].tick_params(axis='x', rotation=45)

        # حفظ الرسم في ذاكرة مؤقتة وتحويله إلى base64 لعرضه في HTML
        buffer = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

        # عرض الصفحة مع البيانات
        return render(request, 'activate/logs_chart.html', {
            'top_logs': top_urls,
            'chart': chart_base64
        })

    except Exception as e:
        # عرض الخطأ إذا حدثت مشكلة أثناء التوليد
        return render(request, 'activate/logs_chart.html', {'error': str(e)})
