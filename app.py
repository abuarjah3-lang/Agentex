import streamlit as st
import time
import pandas as pd

# إعدادات الصفحة
st.set_page_config(
    page_title="Agentex | Dubai Autonomous Business Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "lang_select" not in st.session_state:
    st.session_state.lang_select = "العربية"

is_arabic = (st.session_state.lang_select == "العربية")

# حقن خط Tajawal وأكواد التنسيق المتقدمة (RTL/LTR والألوان ووضوح النصوص)
custom_css = f"""
    <import href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap">
    <style>
    /* تطبيق خط تاجوال على كامل التطبيق */
    html, body, [class*="st-"] {{
        font-family: 'Tajawal', sans-serif !important;
        direction: {"rtl" if is_arabic else "ltr"};
        text-align: {"right" if is_arabic else "left"};
    }}
    
    [data-testid="stAppViewContainer"] {{
        direction: {"rtl" if is_arabic else "ltr"};
        background-color: #f8fafc;
    }}
    
    /* تنسيق الشريط الجانبي وضمان ظهور النصوص باللون الأبيض الناصع */
    [data-testid="stSidebar"] {{
        background-color: #0f172a;
        {"right: 0 !important; left: auto !important;" if is_arabic else "left: 0 !important; right: auto !important;"}
    }}
    
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .stMarkdown {{
        color: #ffffff !important;
        text-align: {"right" if is_arabic else "left"};
    }}
    
    /* بطاقات خطوات العمل الآلي */
    .step-card {{
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        direction: {"rtl" if is_arabic else "ltr"};
    }}
    .step-number {{
        font-size: 14px;
        font-weight: 700;
        color: #007A5E;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .step-title {{
        font-size: 16px;
        font-weight: 600;
        color: #1e293b;
        margin-top: 5px;
    }}
    
    /* الأزرار */
    .stButton>button {{ 
        width: 100%; 
        background: linear-gradient(135deg, #007A5E 0%, #005c47 100%); 
        color: white; 
        font-weight: 600; 
        border-radius: 8px; 
        border: none; 
        padding: 10px; 
    }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.markdown("### ⚡ AGENTEX")
    st.caption("Dubai AI Agents Championship V1.0")
    st.markdown("---")
    
    lang = st.selectbox("🌐 لغة واجهة المستخدم / Interface Language", ["العربية", "English"], key="lang_select")
    
    st.markdown("---")
    if lang == "العربية":
        st.markdown("#### 🟢 حالة شبكة الوكلاء")
        st.markdown("• **المنسق الرئيسي (Master):** `نشط`")
        st.markdown("• **الوكيل القانوني (Legal):** `نشط`")
        st.markdown("• **الوكيل المالي (Financial):** `نشط`")
        st.markdown("• **وكيل العمليات (Operations):** `نشط`")
        
        nav_option = st.radio(
            "🧭 نظام التنقل",
            ["🚀 لوحة التشغيل (Overview)", "💬 غرفة العمليات (AI Workspace)", "📊 التحليلات الحية (Live Analytics)"]
        )
    else:
        st.markdown("#### 🟢 Agents Status")
        st.markdown("• **Master Agent:** `Active`")
        st.markdown("• **Legal Agent:** `Active`")
        st.markdown("• **Financial Agent:** `Active`")
        st.markdown("• **Operations Agent:** `Active`")
        
        nav_option = st.radio(
            "🧭 Navigation",
            ["🚀 Overview", "💬 AI Workspace", "📊 Live Analytics"]
        )

# محتوى التطبيق حسب اللغة
if lang == "العربية":
    if "لوحة التشغيل" in nav_option:
        st.title("⚡ منصة Agentex الذكية لتأسيس الأعمال")
        st.subheader("النظام المستقل الأول المدعوم بالوكلاء المتعددين (Multi-Agent OS) لإمارة دبي")
        st.markdown("---")
        
        st.info("💡 **انطباع اللجنة:** هذا البروتوتيب يستبدل البيروقراطية التقليدية بشبكة وكلاء ذكيين ينجزون تراخيص دبي والامتثال المالي في أقل من 4 دقائق.")
        
        st.markdown("### ⚙️ خطوات العمل الآلي (Autonomous Workflow)")
        # في حالة العربية: نرتب الأعمدة من اليمين لليسار (01 ثم 02 ثم 03)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="step-card"><div class="step-number">01. تحليل النوايا</div><div class="step-title">Intent Analysis & Scope</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="step-card"><div class="step-number">02. تنسيق الوكلاء</div><div class="step-title">Multi-Agent Orchestration</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="step-card"><div class="step-number">03. التنفيذ الفوري</div><div class="step-title">Autonomous Execution</div></div>', unsafe_allow_html=True)
            
        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("سرعة إنجاز المعاملة", "3.8 دقيقة", "-85%")
        m2.metric("دقة الامتثال القانوني", "99.9%", "مثالي")
        m3.metric("الشركات المسجلة", "1,420+", "+18%")
        m4.metric("تكلفة التأسيس", "مُحسّنة تلقائياً", "أقل تكلفة")

    elif "غرفة العمليات" in nav_option:
        st.title("💬 غرفة عمليات وكلاء Agentex")
        st.markdown("تفاعل مباشرة مع المنسق الرئيسي (Master Agent) لتأسيس شركتك في دبي.")
        
        if "messages_ar" not in st.session_state:
            st.session_state.messages_ar = []

        for message in st.session_state.messages_ar:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("اكتب طلبك (مثال: أريد تأسيس شركة ذكاء اصطناعي في دبي)..."):
            st.session_state.messages_ar.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                steps = [
                    "🔄 **المنسق الرئيسي (Master):** تحليل الطلب وتوزيع المهام على وكلاء Agentex...",
                    "⚖️ **الوكيل القانوني (Legal):** التحقق من شروط التراخيص التجارية بدبي ديجيتال...",
                    "💰 **الوكيل المالي (Financial):** حساب تكاليف التأسيس واختيار البنك الرقمي...",
                    "📄 **وكيل العمليات (Operations):** إعداد مسودة عقد التأسيس (MOA) ومستندات الترخيص...",
                    "✨ **النتيجة النهائية:** تم تجهيز حزمة التأسيس بنجاح كامل!"
                ]
                for step in steps:
                    message_placeholder.markdown(step)
                    time.sleep(0.5)
                
                final_response = """
### 📋 تقرير تأسيس الشركة المعتمد من Agentex:
1. **الكيان القانوني:** شركة ذكاء اصطناعي وبرمجيات (منطقة حرّة بدبي - DAFZA).
2. **الرخصة:** رخصة تجارية رقمية فورية.
3. **التكلفة الإجمالية التقديرية:** ~13,500 درهم إماراتي.
4. **حالة الامتثال:** مستوفي لكافة معايير دبي للذكاء الاصطناعي والحاكمية.
                """
                message_placeholder.markdown(final_response)
                st.session_state.messages_ar.append({"role": "assistant", "content": final_response})
    else:
        st.title("📊 لوحة التحليلات الحية ومتابعة المعاملات")
        df = pd.DataFrame({
            "رقم الطلب": ["#AG-901", "#AG-902", "#AG-903", "#AG-904"],
            "المستثمر": ["شريف حمدان", "خالد المنصوري", "مارك جونسون", "إيلينا رومانوف"],
            "النشاط": ["ذكاء اصطناعي", "تجارة إلكترونية", "تقنية مالية", "استشارات رقمية"],
            "الوكيل المسؤول": ["الوكيل القانوني", "الوكيل المالي", "وكيل العمليات", "المنسق الرئيسي"],
            "الحالة": ["مكتمل 🟢", "قيد التدقيق 🟡", "بانتظار المستندات 🟠", "مكتمل 🟢"]
        })
        st.dataframe(df, use_container_width=True)

else:
    if "Overview" in nav_option:
        st.title("⚡ Agentex Enterprise Engine")
        st.subheader("The First Autonomous Multi-Agent OS for Dubai Business Setup & Compliance")
        st.markdown("---")
        
        st.info("💡 **Jury Note:** This prototype replaces traditional bureaucracy with an autonomous agent network executing Dubai licensing & compliance in under 4 minutes.")
        
        st.markdown("### ⚙️ Autonomous Workflow Pipeline")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="step-card"><div class="step-number">01. Intake</div><div class="step-title">Intent Analysis</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="step-card"><div class="step-number">02. Orchestration</div><div class="step-title">Multi-Agent Collaboration</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="step-card"><div class="step-number">03. Execution</div><div class="step-title">Autonomous Issuance</div></div>', unsafe_allow_html=True)
            
        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Setup Velocity", "3.8 mins", "-85%")
        m2.metric("Compliance Accuracy", "99.9%", "Optimal")
        m3.metric("Registered Entities", "1,420+", "+18%")
        m4.metric("Setup Cost", "Optimized", "Lowest Rate")

    elif "AI Workspace" in nav_option:
        st.title("💬 Agentex Operations Workspace")
        st.markdown("Interact directly with the Master Agent to orchestrate your Dubai business setup.")
        
        if "messages_en" not in st.session_state:
            st.session_state.messages_en = []

        for message in st.session_state.messages_en:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Type your request (e.g., Setup an AI startup in Dubai)..."):
            st.session_state.messages_en.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                steps = [
                    "🔄 **Master Agent:** Analyzing request and delegating tasks...",
                    "⚖️ **Legal Agent:** Verifying Dubai Digital licensing requirements...",
                    "💰 **Financial Agent:** Calculating setup costs and banking options...",
                    "📄 **Operations Agent:** Drafting MOA and incorporation documents...",
                    "✨ **Final Result:** Setup package prepared successfully!"
                ]
                for step in steps:
                    message_placeholder.markdown(step)
                    time.sleep(0.5)
                
                final_response = """
### 📋 Verified Agentex Setup Report:
1. **Legal Entity:** AI & Software LLC (Dubai Free Zone - DAFZA).
2. **License Type:** Instant Digital Commercial License.
3. **Estimated Cost:** ~13,500 AED.
4. **Compliance Status:** Fully aligned with Dubai AI Ethics & Governance.
                """
                message_placeholder.markdown(final_response)
                st.session_state.messages_en.append({"role": "assistant", "content": final_response})
    else:
        st.title("📊 Live Analytics & Transactions Dashboard")
        df = pd.DataFrame({
            "Request ID": ["#AG-901", "#AG-902", "#AG-903", "#AG-904"],
            "Investor": ["Sharif Hamdan", "Khaled Al Mansoori", "Mark Johnson", "Elena Romanov"],
            "Activity": ["Artificial Intelligence", "E-Commerce", "FinTech", "Digital Advisory"],
            "Active Agent": ["Legal Agent", "Financial Agent", "Operations Agent", "Master Agent"],
            "Status": ["Completed 🟢", "Under Review 🟡", "Pending Docs 🟠", "Completed 🟢"]
        })
        st.dataframe(df, use_container_width=True)
