import streamlit as st
import time
import pandas as pd

# إعدادات الصفحة
st.set_page_config(
    page_title="Agentex - Dubai Autonomous Business Orchestrator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم عبر CSS لهوية Agentex
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #007A5E; color: white; font-weight: bold; border-radius: 8px; }
    .stButton>button:hover { background-color: #005c47; color: white; }
    .agent-box { padding: 15px; border-radius: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي (Sidebar)
with st.sidebar:
    st.title("⚡ Agentex")
    st.caption("Dubai AI Agents Championship Prototype")
    st.markdown("---")
    st.subheader("حالة شبكة الوكلاء (Offline Mode)")
    
    st.markdown("🟢 **Master Orchestrator:** متصل")
    st.markdown("🟢 **Legal & Compliance Agent:** متصل")
    st.markdown("🟢 **Financial & Tax Agent:** متصل")
    st.markdown("🟢 **Operations & Docs Agent:** متصل")
    
    st.markdown("---")
    st.info("💡 منصة Agentex مصممة لأتمتة تأسيس الأعمال في دبي عبر شبكة وكلاء أذكياء.")

# الواجهة الرئيسية
st.title("⚡ Agentex | دبي")
st.subheader("المنصة الذكية المستقلة لتأسيس الأعمال والامتثال في دبي")
st.markdown("---")

# التبويبات
tab1, tab2 = st.tabs(["💬 مساعد Agentex الذكي", "📊 لوحة متابعة المعاملات (Live Dashboard)"])

with tab1:
    st.markdown("### كيف يمكن لشبكة وكلاء Agentex مساعدتك اليوم؟")
    st.markdown("اكتب طلبك بلغتك الطبيعية (مثال: *أريد تأسيس شركة تقنية في دبي، وفتح حساب بنكي، واستخراج التراخيص*).")

    # حفظ رسائل المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # إدخال المستخدم
    if prompt := st.chat_input("اكتب طلبك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # محاكاة عمل شبكة الوكلاء
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            steps = [
                "🔄 **Master Agent:** تحليل الطلب وتوزيع المهام على وكلاء Agentex المختصين...",
                "⚖️ **Legal Agent:** التحقق من شروط التراخيص التجارية في دبي (دائرة الاقتصاد والسياحة)...",
                "💰 **Financial Agent:** حساب التكاليف التقديرية وجهات فتح الحسابات البنكية المناسبة...",
                "📄 **Operations Agent:** إعداد مسودة عقد التأسيس والمستندات المطلوبة...",
                "✨ **النتيجة النهائية:** تم تجهيز حزمة التأسيس بنجاح!"
            ]
            
            for step in steps:
                message_placeholder.markdown(step)
                time.sleep(0.8)
            
            final_response = f"""
### تقرير تأسيس الشركة من Agentex:
1. **النشاط المقترح:** شركة خدمات تقنية ونظم معلومات (منطقة حرّة دبي).
2. **الرخصة المتوافقة:** رخصة تجارية رقمية معتمدة.
3. **التكلفة التقديرية:** ~14,000 درهم إماراتي (تشمل كافة الرسوم الحكومية).
4. **الخطوة القادمة:** المصادقة الرقمية للهوية وإصدار رخصة Agentex فورياً.

*ملاحظة: هذا رد تجريبي من الـ Prototype المحلي لنظام Agentex.*
            """
            message_placeholder.markdown(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})

with tab2:
    st.markdown("### نظرة عامة على أداء وكلاء Agentex والشركات المسجلة")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("الشركات المؤسسة عبر Agentex", "184 شركة", "+18 هذا الأسبوع")
    col2.metric("متوسط وقت الإنجاز", "3.8 دقائق", "-50% مقارنة بالأنظمة التقليدية")
    col3.metric("معدل دقة الامتثال", "99.9%", "ممتاز")
    
    st.markdown("---")
    st.markdown("#### حالة الطلبات النشطة عبر المنصة:")
    
    df = pd.DataFrame({
        "رقم الطلب": ["#AG-501", "#AG-502", "#AG-503", "#AG-504"],
        "اسم المستثمر": ["شريف حمدان", "خالد المنصوري", "مارك جونسون", "ليليان سميث"],
        "نوع الشركة": ["ذكاء اصطناعي وبرمجيات", "تجارة إلكترونية", "استشارات مالية", "تسويق رقمي"],
        "الوكيل المسؤول": ["Legal Agent", "Financial Agent", "Operations Agent", "Master Agent"],
        "الحالة": ["مكتمل 🟢", "قيد التدقيق 🟡", "بانتظار المستندات 🟠", "مكتمل 🟢"]
    })
    
    st.dataframe(df, use_container_width=True)