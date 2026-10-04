import requests
import streamlit as st

# قراءة مفتاح الربط بأمان من إعدادات ستريملت
api_key = st.secrets["GEMINI_API_KEY"]

# إعدادات الصفحة
st.set_page_config(page_title="Manarat Al-Nashia", page_icon="🏮", layout="centered")

# تصميم الواجهة والألوان
st.markdown("""
<style>
.stApp { background-color: #0b1d3a; color: #ffffff; }
h1 { color: #ffb703 !important; text-align: center; }
p { text-align: center; color: #e0e0e0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>منارة الناشئة 🏮</h1>", unsafe_allow_html=True)
st.markdown("<p>مرشدك الإيماني الموثوق من المصادر الرسمية (القرآن والسنة)</p>", unsafe_allow_html=True)

# نظام التوجيه الصارم لضمان الاعتماد على المصادر ومنع الإجابة من الذاكرة العشوائية
SYSTEM_INSTRUCTION = """You are "Manarat Al-Nashia" (منارة الناشئة), an Islamic educational assistant for children and teens (9-15).
CRITICAL RULES:
1. Rely ONLY on authentic Islamic sources (Quran, Sahih Al-Bukhari, Sahih Muslim, approved APIs like QuranEnc and HadeethEnc).
2. You MUST include the exact source/reference clearly at the end of every answer (e.g., [Quran - سورة الإخلاص] or [HadeethEnc - صحيح البخاري]).
3. If unsure or if the source is not verified, kindly state that you found no reliable source and refer the child to a parent or teacher.
4. Keep the style warm, encouraging, and under 150 words."""

def ask_gemini(user_message):
    # رابط الاتصال المباشر والثابت v1 (الذي يمنع خطأ 404 نهائياً)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser Question: {user_message}"
    
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
            return answer
        else:
            return f"عذراً يا بطل، حدث خطأ في الخادم (رمز الخطأ: {response.status_code})"
    except Exception as e:
        return f"عذراً، حدث خطأ في الاتصال: {e}"

# إدارة المحادثة
if "chat" not in st.session_state:
    st.session_state.chat = []

for role, text in st.session_state.chat:
    st.chat_message(role).write(text)

q = st.chat_input("اكتب سؤالك الديني يا بطل...")
if q:
    st.chat_message("user").write(q)
    st.session_state.chat.append(("user", q))
    
    with st.spinner("المنارة تتحقق من المصادر الشرعية..."):
        ans = ask_gemini(q)
        
    st.session_state.chat.append(("assistant", ans))
    st.chat_message("assistant").write(ans)
