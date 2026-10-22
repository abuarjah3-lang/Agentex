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

# تخصيص التصميم والشعار الجديد عبر CSS متقدم
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #007A5E 0%, #004d3a 100%); color: white; font-weight: bold; border-radius: 10px; border: none; padding: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button:hover { background: linear-gradient(135deg, #004d3a 0%, #003326 100%); color: white; }
    
    /* تصميم شعار احترافي مخصص */
    .brand-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
    }
    .brand-icon {
        background: linear-gradient(135deg, #007A5E, #00F5D4);
        color: white;
        width: 45px;
        height: 45px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0, 122, 94, 0.3);
    }
    .brand-text h2 {
        margin: 0;
        font-size: 22px;
        color: #1f2937;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .brand-text p {
        margin: 0;
        font-size: 11px;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي مع الشعار الجديد
with st.sidebar:
    st.markdown("""
        <div class="brand-logo">
            <div class="brand-icon">⚡</div>
            <div class="brand-text">
                <h2>Agentex</h2>
                <p>Autonomous Engine</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    lang = st.selectbox("🌐 Choose Language / اختر اللغة", ["العربية", "English"])
    
    st.markdown("---")
    if lang == "العربية":
        st.subheader("حالة شبكة الوكلاء")
        st.markdown("🟢 **Master Orchestrator:** متصل")
        st.markdown("🟢 **Legal Agent:** متصل")
        st.markdown("🟢 **Financial Agent:** متصل")
        st.markdown("🟢 **Operations Agent:** متصل")
        st.markdown("---")
        st.info("💡 منصة Agentex الذكية لأتمتة تأسيس الأعمال في دبي.")
    else:
        st.subheader("Agents Status")
        st.markdown("🟢 **Master Orchestrator:** Online")
        st.markdown("🟢 **Legal Agent:** Online")
        st.markdown("🟢 **Financial Agent:** Online")
        st.markdown("🟢 **Operations Agent:** Online")
        st.markdown("---")
        st.info("💡 Agentex: Autonomous AI platform for business setup in Dubai.")

# الواجهة الرئيسية مع الشعار البصري
if lang == "العربية":
    st.markdown("""
        <div class="brand-logo" style="margin-bottom: 20px;">
            <div class="brand-icon" style="width: 55px; height: 55px; font-size: 28px;">⚡</div>
            <div class="brand-text">
                <h2 style="font-size: 28px;">Agentex | دبي</h2>
                <p style="font-size: 13px;">المنصة المستقلة لتأسيس الأعمال والامتثال الذكي</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["💬 مساعد Agentex الذكي", "📊 لوحة متابعة المعاملات (Live Dashboard)"])
    
    with tab1:
        st.markdown("### كيف يمكن لشبكة وكلاء Agentex مساعدتك اليوم؟")
        st.markdown("اكتب طلبك بلغتك الطبيعية (مثال: *أريد تأسيس شركة تقنية في دبي، وفتح حساب بنكي*).")

        if "messages_ar" not in st.session_state:
            st.session_state.messages_ar = []

        for message in st.session_state.messages_ar:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("اكتب طلبك هنا..."):
            st.session_state.messages_ar.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                steps = [
                    "🔄 **Master Agent:** تحليل الطلب وتوزيع المهام على وكلاء Agentex...",
                    "⚖️ **Legal Agent:** التحقق من شروط التراخيص التجارية بدبي...",
                    "💰 **Financial Agent:** حساب التكاليف وجهات فتح الحسابات البنكية...",
                    "📄 **Operations Agent:** إعداد مسودة عقد التأسيس والمستندات...",
                    "✨ **النتيجة النهائية:** تم تجهيز حزمة التأسيس بنجاح!"
                ]
                for step in steps:
                    message_placeholder.markdown(step)
                    time.sleep(0.7)
                
                final_response = """
### 📋 تقرير تأسيس الشركة من Agentex:
1. **النشاط المقترح:** شركة خدمات تقنية ونظم معلومات (منطقة حرّة دبي).
2. **الرخصة المتوافقة:** رخصة تجارية رقمية معتمدة من دبي ديجيتال.
3. **التكلفة التقديرية:** ~14,000 درهم إماراتي.
4. **الخطوة القادمة:** المصادقة الرقمية للهوية وإصدار الرخصة فورياً.
                """
                message_placeholder.markdown(final_response)
                st.session_state.messages_ar.append({"role": "assistant", "content": final_response})

    with tab2:
        st.markdown("### 📊 لوحة أداء وكلاء Agentex")
        col1, col2, col3 = st.columns(3)
        col1.metric("الشركات المؤسسة", "184 شركة", "+18 هذا الأسبوع")
        col2.metric("متوسط وقت الإنجاز", "3.8 دقائق", "-50% أسرع")
        col3.metric("معدل دقة الامتثال", "99.9%", "ممتاز")
        
        st.markdown("---")
        st.markdown("#### الطلبات النشطة عبر المنصة:")
        df = pd.DataFrame({
            "رقم الطلب": ["#AG-501", "#AG-502", "#AG-503", "#AG-504"],
            "اسم المستثمر": ["شريف حمدان", "خالد المنصوري", "مارك جونسون", "ليليان سميث"],
            "نوع الشركة": ["ذكاء اصطناعي", "تجارة إلكترونية", "استشارات مالية", "تسويق رقمي"],
            "الوكيل المسؤول": ["Legal Agent", "Financial Agent", "Operations Agent", "Master Agent"],
            "الحالة": ["مكتمل 🟢", "قيد التدقيق 🟡", "بانتظار المستندات 🟠", "مكتمل 🟢"]
        })
        st.dataframe(df, use_container_width=True)

else:
    st.markdown("""
        <div class="brand-logo" style="margin-bottom: 20px;">
            <div class="brand-icon" style="width: 55px; height: 55px; font-size: 28px;">⚡</div>
            <div class="brand-text">
                <h2 style="font-size: 28px;">Agentex Platform</h2>
                <p style="font-size: 13px;">Dubai Autonomous Business & Compliance Orchestrator</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["💬 Agentex AI Assistant", "📊 Live Transactions Dashboard"])
    
    with tab1:
        st.markdown("### How can Agentex assist you today?")
        st.markdown("Type your request in natural language (e.g., *I want to setup a tech startup in Dubai and open a bank account*).")

        if "messages_en" not in st.session_state:
            st.session_state.messages_en = []

        for message in st.session_state.messages_en:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Type your request here..."):
            st.session_state.messages_en.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                steps = [
                    "🔄 **Master Agent:** Analyzing request and delegating tasks...",
                    "⚖️ **Legal Agent:** Verifying Dubai Department of Economy licenses...",
                    "💰 **Financial Agent:** Calculating setup costs and banking options...",
                    "📄 **Operations Agent:** Drafting MOA and incorporation documents...",
                    "✨ **Final Result:** Setup package prepared successfully!"
                ]
                for step in steps:
                    message_placeholder.markdown(step)
                    time.sleep(0.7)
                
                final_response = """
### 📋 Agentex Company Setup Report:
1. **Suggested Activity:** IT & Tech Services (Dubai Free Zone).
2. **Compatible License:** Verified Digital Commercial License.
3. **Estimated Cost:** ~14,000 AED (Inclusive of government fees).
4. **Next Step:** Digital ID verification & instant license issuance.
                """
                message_placeholder.markdown(final_response)
                st.session_state.messages_en.append({"role": "assistant", "content": final_response})

    with tab2:
        st.markdown("### 📊 Agentex Agents Performance")
        col1, col2, col3 = st.columns(3)
        col1.metric("Registered Companies", "184", "+18 this week")
        col2.metric("Avg. Execution Time", "3.8 mins", "-50% vs Traditional")
        col3.metric("Compliance Accuracy", "99.9%", "Optimal")
        
        st.markdown("---")
        st.markdown("#### Active Platform Requests:")
        df = pd.DataFrame({
            "Request ID": ["#AG-501", "#AG-502", "#AG-503", "#AG-504"],
            "Investor Name": ["Sharif Hamdan", "Khaled Al Mansoori", "Mark Johnson", "Lilian Smith"],
            "Company Type": ["AI & Software", "E-Commerce", "Financial Advisory", "Digital Marketing"],
            "Active Agent": ["Legal Agent", "Financial Agent", "Operations Agent", "Master Agent"],
            "Status": ["Completed 🟢", "Under Review 🟡", "Pending Docs 🟠", "Completed 🟢"]
        })
        st.dataframe(df, use_container_width=True)
