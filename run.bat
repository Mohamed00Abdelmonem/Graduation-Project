@echo off
cd /d "D:\Projects-Django\Managment-library-MET"

REM تفعيل البيئة الافتراضية
call venv\Scripts\activate

REM الدخول لمجلد المشروع
cd venv\src

REM تشغيل السيرفر في نافذة جديدة
start cmd /k "call ..\Scripts\activate && py manage.py runserver"

REM انتظار 3 ثواني
timeout /t 3 >nul

REM فتح المتصفح
start http://127.0.0.1:8000
