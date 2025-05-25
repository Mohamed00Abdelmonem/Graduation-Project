from gtts import gTTS
import os

text = """
مشروع تخرجي هو تطبيق ويب تم تطويره باستخدام إطار Django.
يهدف المشروع إلى تحويل النصوص إلى صوت باستخدام بايثون.
"""

tts = gTTS(text=text, lang='ar')
tts.save("project_description.mp3")

# لتشغيل الملف مباشرة (في ويندوز)
os.system("start project_description.mp3")
