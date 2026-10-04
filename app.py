import requests
import streamlit as st

# سحب المفتاح من إعدادات ستريملت
api_key = st.secrets.get("GEMINI_API_KEY", "").strip()

st.set_page_config(page_title="Manarat Al-Nashia", page_icon="🏮", layout="centered")

SYSTEM_INSTRUCTION = """You are "Manarat Al-Nashia" (منارة الناشئة), an Islamic educational assistant for children and teens (9-15).
CRITICAL RULES:
1. Rely ONLY on authentic Islamic sources (Quran, Sahih Al-Bukhari, Sahih Muslim, approved APIs like QuranEnc).
2. You MUST include the exact source/reference clearly at the end of every answer (e.g., [Quran] or [HadeethEnc]).
3. LANGUAGE: reply strictly in the language of the child's last message.
4. If unsure, kindly state that you found no reliable source and refer the child to a teacher.
5. Keep the style warm, encouraging, and under 150 words."""

def ask_gemini(user_message):
    if not api_key:
        return "خطأ: لم يتم ضبط المفتاح في إعدادات Secrets.", False
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser Question: {user_message}"
    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"], True
        else:
            return f"عذراً، حدث خطأ في الخادم (الرمز: {response.status_code})", False
    except Exception as e:
        return f"عذراً، حدث خطأ في الاتصال: {e}", False

# إعدادات الواجهة واللغات
T = {
 "ar": dict(title="منارة الناشئة 🏮", tag="مرشدك الإيماني الموثوق من المصادر الرسمية", ph="اكتب سؤالك الديني...",
            guest="ضيف", reg="سجّل اسمك", nick="اسم مستعار", stars="نجومك", learned="معلومات تعلمتها", 
            think="المنارة تبحث...", note="أنا مساعد آلي أجيب من مصادر معتمدة.", mode="الدخول"),
 "en": dict(title="Manarat Al-Nashia 🏮", tag="Your trusted faith guide", ph="Ask your question...",
            guest="Guest", reg="Sign your name", nick="Nickname", stars="Your stars", learned="Things learned", 
            think="Searching sources...", note="I am an AI assistant.", mode="Entry"),
}

lang = "ar" if st.sidebar.radio("اللغة / Language", ["العربية", "English"]) == "العربية" else "en"
t = T[lang]

st.markdown(f"<style>.stApp {{ direction: {'rtl' if lang=='ar' else 'ltr'}; }} h1 {{ color: #ffb703; text-align: center; }}</style>", unsafe_allow_html=True)

ss = st.session_state
ss.setdefault("chat", []); ss.setdefault("stars", 0)

mode = st.sidebar.radio(t["mode"], [t["guest"], t["reg"]])
name = st.sidebar.text_input(t["nick"], max_chars=20) if mode == t["reg"] else ""
st.sidebar.markdown(f"### ⭐ {t['stars']}: {ss.stars}")

st.markdown(f"<h1>{t['title']}</h1><p style='text-align:center'>{t['tag']}</p>", unsafe_allow_html=True)
if name: st.markdown(f"🏮 **{name}**")
st.info(t["note"])

for role, text in ss.chat:
    st.chat_message(role).write(text)

q = st.chat_input(t["ph"])
if q:
    st.chat_message("user").write(q)
    ss.chat.append(("user", q))
    with st.spinner(t["think"]):
        ans, success = ask_gemini(q)
    ss.chat.append(("assistant", ans))
    st.chat_message("assistant").write(ans)
    if success: ss.stars += 1
