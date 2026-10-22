from dataclasses import asdict
import streamlit as st
from engine import Profile, SOURCES, LABELS, VERSION, analyse, scenario
from reporting import html_report, export_json
from ai_assist import explain, AssistError

st.set_page_config(page_title="Agentex | Business decision studio", page_icon="◈", layout="wide")
st.session_state.setdefault("language", "ar")
with st.sidebar:
    st.markdown("## ◈ AGENTEX")
    lang = st.selectbox("اللغة / Language", ["ar", "en"], format_func=lambda x: "العربية" if x == "ar" else "English", key="language")
ar = lang == "ar"
def t(a,b): return a if ar else b
def label(key): return LABELS[key][lang]
def money(value): return t("غير محسوم", "Unresolved") if value is None else f"{value:,.0f} AED"
direction = "rtl" if ar else "ltr"
st.markdown("""<style>
[data-testid="stAppViewContainer"]{background:#f4f7f6}
[data-testid="stMainBlockContainer"]{max-width:1220px;padding-top:2rem}
[data-testid="stSidebar"]{background:#102d34}
[data-testid="stSidebar"] .stMarkdown{color:#ecf6f2}
h1,h2,h3{color:#153a41;letter-spacing:-.025em}
.hero{background:#102d34;color:#fff;padding:36px;border-radius:20px;margin-bottom:24px}
.hero h1{color:white;font-size:2.4rem;margin:12px 0}
.hero p{color:#cfdfdc;font-size:1.05rem;max-width:780px}
.eyebrow{color:#83d6bd;letter-spacing:.12em;font:700 12px Arial}
.pill{display:inline-block;background:#e7f3ee;color:#12614d;border-radius:20px;padding:5px 14px;font-size:13px}
[data-testid="stMetric"]{background:white;border:1px solid #dfe9e4;border-radius:14px;padding:18px}
.stButton>button[kind="primary"]{background:#087f6f;border-color:#087f6f}
.stDownloadButton>button{border-radius:9px}
@media(max-width:600px){.hero{padding:22px}.hero h1{font-size:1.9rem}}
</style>""" + f"<style>[data-testid='stMain']{{direction:{direction};text-align:{'right' if ar else 'left'}}}[data-testid='stSidebar']{{direction:{direction}}}input,textarea{{direction:{direction}}}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(t("**من الفكرة إلى قرار مبرر**", "**From an idea to an informed decision**"))
    page = st.radio(t("مساحة العمل", "Workspace"), ["home", "project", "compare", "whatif", "evidence"], format_func=lambda x: {
        "home":t("البداية", "Start here"), "project":t("ملف المشروع", "Project brief"),
        "compare":t("المقارنة وخطة العمل", "Compare & plan"), "whatif":t("مختبر ماذا لو؟", "What-if lab"),
        "evidence":t("المصادر وسجل القرار", "Evidence & decisions")}[x], key="page")
    st.markdown("---")
    st.markdown(t("**وضع التخطيط المحلي**\n\nقواعد وحسابات فعلية، مع مصادر محفوظة. الشرح بالنموذج اختياري.", "**Local planning mode**\n\nActual rules and calculations with saved sources. Model explanation is optional."))
    st.caption("v" + VERSION)
    if st.button(t("مسح بيانات الجلسة", "Clear this session")):
        for k in list(st.session_state):
            if k not in ("language", "page"): del st.session_state[k]
        st.rerun()

def load_example(name):
    examples = {
        "solo":Profile("خدمة تطوير برمجيات للشركات / Software development for businesses", "software", 25000, 0, "flexi", "international", 1, False, True),
        "team":Profile("استشارات تقنية لفريق يحتاج تأشيرتين / IT consultancy with two visas", "it", 18000, 2, "private", "both", 2, False, True),
        "outside":Profile("منصة خدمات مالية / Financial services platform", "other", 50000, 1, "flexi", "uae", 1, True, True),
    }
    st.session_state.profile = asdict(examples[name])
    st.session_state.assumptions = {}
    st.session_state.result = analyse(examples[name])
    st.session_state.is_example = True
    for key in list(st.session_state):
        if key.startswith(("brief_", "estimate_", "what_", "ai_text_")):
            del st.session_state[key]

def current_result():
    if "profile" not in st.session_state: return None
    # Re-evaluate freshness on rerun; no cached green status across dates.
    result = analyse(Profile(**st.session_state.profile), st.session_state.get("assumptions", {}))
    st.session_state.result = result
    return result

def require_result():
    result = current_result()
    if result is None:
        st.info(t("ابدأ بملف المشروع، أو حمّل مثالًا من صفحة البداية.", "Start with a project brief, or load an example from Start here."))
        st.stop()
    if st.session_state.get("is_example"):
        st.info(t("هذه بيانات مثال تجريبي، وليست معاملة حقيقية.", "These are demonstration inputs, not a real transaction."))
    return result

def gates(result):
    if result["status"] == "out_of_scope":
        st.error(t("الحالة خارج نطاق النسخة. نحتاج مراجعة متخصصة قبل مقارنة المسارات.", "Outside this release's scope. Specialist review is needed before comparing routes."))
    for q in result["questions"]: st.warning(q[lang])
    return result["status"] == "preliminary"

def render_route(route):
    st.subheader(route["name"][lang])
    st.caption(t("خيار للنقاش — أهلية النشاط لم تُؤكّد", "Option for discussion — activity eligibility is unconfirmed"))
    origins = {"published_start":t("بداية سعرية [S2]", "Published starting price [S2]"), "user_estimate":t("تقدير المستخدم", "User estimate"), "unknown":t("يحتاج تسعيرًا", "Needs pricing")}
    st.table([{t("البند", "Item"): row["label"][lang], t("المبلغ", "Amount"):money(row["amount"]), t("الأساس", "Basis"):origins[row["origin"]]} for row in route["rows"]])
    priced = any(row["amount"] is not None for row in route["rows"])
    st.metric(t("المجموع الجزئي فقط", "Partial subtotal only"), money(route["subtotal"] if priced else None))
    if route["budget_state"] == "exceeds":
        st.error(t("يتجاوز الميزانية بمقدار ", "Over budget by ") + money(-route["budget_gap"]))
    else:
        st.warning(t("كفاية الميزانية غير مثبتة. المتبقي بعد البنود المحسوبة: ", "Budget sufficiency is not established. Remaining after priced items: ") + money(route["budget_gap"]))
    st.caption(t("بنود غير محسومة: ", "Unresolved items: ") + str(len(route["unknowns"])) + " · " + t("التجديد: ", "Renewal: ") + money(route["renewal"]))
    for note in route["notes"]: st.caption(note[lang])

if page == "home":
    st.markdown('<div class="hero"><div class="eyebrow">AGENTEX / DECISION STUDIO</div><h1>'+t("ابدأ مشروعك بقرار أوضح.", "Start your business with a clearer decision.")+'</h1><p>'+t("افهم احتياجات مشروعك، وقارن مسارين للتأسيس في دبي، واكشف ما ينقص ميزانيتك قبل اتخاذ الخطوة التالية.", "Understand your project, compare two Dubai formation routes, and uncover budget gaps before your next step.")+'</p></div>', unsafe_allow_html=True)
    a,b,c = st.columns(3)
    a.metric(t("مسارات في النسخة", "Routes in this release"), "2")
    b.metric(t("مصادر محفوظة", "Saved sources"), str(len(SOURCES)))
    c.metric(t("بياناتك الأساسية", "Core planning data"), t("داخل الجلسة", "Session only"))
    st.markdown(t("### جرّب اختلاف الحالات", "### See how different cases behave"))
    for col, key, title, detail in zip(st.columns(3), ["solo", "team", "outside"], [t("مؤسس مستقل", "Solo founder"), t("فريق واحتياجات إضافية", "A team with additional needs"), t("نشاط يحتاج مختصًا", "A specialist activity")], [t("برمجيات، دون تأشيرات، مكتب مرن.", "Software, no visas, flexi-desk."), t("تأشيرتان ومكتب خاص وميزانية محدودة.", "Two visas, private office, limited budget."), t("خدمات مالية خارج النطاق التجريبي.", "Financial services outside the pilot scope.")]):
        with col:
            with st.container(border=True):
                st.subheader(title)
                st.write(detail)
                if st.button(t("تحميل المثال", "Load example"), key="demo_"+key):
                    load_example(key)
                    st.success(t("تم التحميل. افتح «المقارنة وخطة العمل» من القائمة.", "Loaded. Open Compare & plan from the menu."))
    st.info(t("النطاق: برمجيات واستشارات تقنية وخدمات رقمية غير متخصصة تنظيميًا. المقارنة أولية، وليست مسحًا لكل خيارات دبي أو توصية بالأرخص.", "Scope: software, IT consulting and digital services without specialist regulatory needs. This is a preliminary comparison, not an exhaustive Dubai market search or a cheapest-route recommendation."))
    with st.expander(t("ما الذي تفعله هذه النسخة؟", "What does this release do?")):
        st.write(t("تنفّذ جمع بيانات منظمًا، وقواعد نطاق وتعارض، وحسابات تكلفة وسيناريوهات، وتصدر تقريرًا مرتبطًا بمصادر. لا تُصدر رخصًا، ولا ترسل طلبات، ولا تُثبت الامتثال. لا توجد شبكة وكلاء مستقلة في هذه النسخة.", "Runs structured intake, scope and conflict rules, cost arithmetic and scenarios, and exports a source-linked report. It does not issue licences, submit applications or verify compliance. This release is not an autonomous multi-agent network."))

elif page == "project":
    st.title(t("ملف المشروع", "Your project brief"))
    st.write(t("نحتاج معلومات تغير القرار، دون أسماء شخصية أو وثائق هوية.", "Provide decision-relevant details without personal names or identity documents."))
    p = Profile(**st.session_state.get("profile", asdict(Profile())))
    with st.form("brief"):
        description = st.text_area(t("ما الخدمة التي ستبيعها ولمن؟", "What service will you sell, and to whom?"), value=p.description, max_chars=2000, key="brief_description")
        left,right = st.columns(2)
        with left:
            activity = st.selectbox(t("النشاط المبدئي", "Initial activity"), ["software","it","digital","other"], index=["software","it","digital","other"].index(p.activity), format_func=label, key="brief_activity")
            budget = st.number_input(t("ميزانية التأسيس للسنة الأولى — درهم", "Year-one formation budget — AED"), min_value=0.0, max_value=100000000.0, value=float(p.budget), step=1000.0, key="brief_budget")
            visas = st.number_input(t("عدد التأشيرات المطلوبة", "Required visa count"), min_value=0, max_value=100, value=p.visas, key="brief_visas")
        with right:
            market = st.selectbox(t("موقع العملاء", "Client market"), ["international","uae","both","unknown"], index=["international","uae","both","unknown"].index(p.market), format_func=label, key="brief_market")
            office = st.selectbox(t("احتياج المقر", "Workspace need"), ["flexi","private","unknown"], index=["flexi","private","unknown"].index(p.office), format_func=label, key="brief_office")
            founders = st.number_input(t("عدد المؤسسين", "Founder count"), min_value=1, max_value=100, value=p.founders, key="brief_founders")
        regulated = st.checkbox(t("يتضمن نشاطي خدمات مالية أو صحية أو تعليمية أو نشاطًا قد يحتاج موافقات متخصصة، أو لست متأكدًا", "My activity includes finance, healthcare, education or may require specialist approvals, or I am unsure"), value=p.regulated, key="brief_regulated")
        confirmed = st.checkbox(t("أؤكد التصنيف أعلاه؛ أعلم أن التطبيق لا يصنّف الوصف الحر أو يتحقق من رمز النشاط آليًا", "I confirm this classification; the app does not automatically classify free text or verify activity codes"), value=p.confirmed_scope, key="brief_confirmed")
        submit = st.form_submit_button(t("حفظ وتحليل المشروع", "Save & analyse brief"), type="primary")
    if submit:
        profile = Profile(description,activity,budget,int(visas),office,market,int(founders),regulated,confirmed)
        st.session_state.profile = asdict(profile)
        # Quotes depend on the full brief; avoid silently carrying over old estimates.
        st.session_state.assumptions = {}
        st.session_state.is_example = False
        for key in list(st.session_state):
            if key.startswith(("estimate_", "what_", "ai_text_")): del st.session_state[key]
        result = analyse(profile)
        st.session_state.result = result
        if gates(result): st.success(t("حُفظ المشروع. افتح المقارنة وخطة العمل. أُعيد ضبط تقديرات التكاليف لتجنب استخدام تقديرات لحالة سابقة.", "Saved. Open Compare & plan. Cost estimates were reset to avoid reusing quotes for a previous case."))

elif page == "compare":
    st.title(t("المقارنة وخطة العمل", "Compare & plan"))
    result = require_result()
    if not gates(result): st.stop()
    st.caption(t("المقارنة محايدة بين مسارين فقط؛ لا يوجد تصنيف «الأفضل» أو «الأرخص».", "A neutral two-route comparison; neither is labelled best or cheapest."))
    for col, route in zip(st.columns(2), result["routes"]):
        with col:
            with st.container(border=True): render_route(route)
    with st.expander(t("أدخل تقديراتك أو أرقام عروض الأسعار", "Enter your estimates or quoted figures")):
        st.caption(t("هذه مدخلات مستخدم غير متحقق منها. اترك الخانة فارغة للمجهول، واكتب 0 فقط إن تأكدت من عدم وجود تكلفة. أدخل مجموع رسوم التأشيرات للعدد المطلوب. وزّع قيمة العرض على البنود دون تكرار؛ لا تدخل قيمة باقة شاملة ثم تضف تكاليفها مرة أخرى.", "These are unverified user inputs. Leave unknowns blank; use 0 only for confirmed zero cost. Enter the total visa-related cost for your requested count. Split quotes into non-overlapping items; do not enter an all-inclusive base plus its components again."))
        with st.form("estimates"):
            raw = {}
            for col,rid in zip(st.columns(2), ["meydan","mainland"]):
                with col:
                    st.write(label(rid))
                    raw[rid] = {}
                    for key in ("base","visa","office","other_cost","renewal"):
                        if key == "visa" and result["profile"]["visas"] == 0:
                            raw[rid][key] = ""
                            continue
                        if key == "office" and rid == "meydan" and result["profile"]["office"] == "flexi":
                            raw[rid][key] = ""
                            continue
                        old = st.session_state.get("assumptions",{}).get(rid,{}).get(key)
                        raw[rid][key] = st.text_input(label(key), value="" if old is None else str(old), key=f"estimate_{rid}_{key}", max_chars=16)
            saved = st.form_submit_button(t("تحديث الحسابات", "Update calculations"))
        if saved:
            try:
                values = {rid:{k:None if not value.strip() else float(value.replace(",", "").strip()) for k,value in row.items()} for rid,row in raw.items()}
                analyse(Profile(**st.session_state.profile),values)
                st.session_state.assumptions = values
                st.rerun()
            except ValueError:
                st.error(t("استخدم أرقامًا موجبة أو صفرًا، أو اترك الحقل فارغًا. القيم غير المحدودة غير مقبولة.", "Use non-negative finite numbers, or leave the field blank."))
    st.subheader(t("قائمة الخطوات التالية", "Your next steps"))
    st.caption(t("قائمة متابعة شخصية؛ التعليم لا يثبت إنجاز معاملة لدى جهة رسمية.", "Personal checklist; ticking a box does not establish completion with an authority."))
    for task in result["tasks"]:
        dep = " → ".join(task["depends"])
        st.checkbox(task["id"]+" · "+task["label"][lang]+(" ("+dep+")" if dep else ""), key="task_"+result["case_id"]+task["id"])
    st.subheader(t("ملف القرار", "Decision file"))
    a,b=st.columns(2)
    a.download_button(t("تنزيل التقرير للطباعة", "Download printable report"), html_report(result,lang), file_name="Agentex-decision-"+result["case_id"]+".html", mime="text/html")
    b.download_button(t("تنزيل البيانات وسجل القرار", "Download data & decision record"), export_json(result), file_name="Agentex-case-"+result["case_id"]+".json", mime="application/json")
    st.caption(t("افتح التقرير في المتصفح واختر طباعة لحفظه PDF. التقرير يسرد الخطوات بوصفها غير منفذة.", "Open the report in a browser and print to PDF. It lists next steps as not executed."))
    with st.expander(t("شرح اختياري بالذكاء الاصطناعي", "Optional AI explanation")):
        st.caption(t("يرسل نسخة من ملف المشروع والحسابات والمصادر إلى OpenAI عند الضغط فقط. قد تترتب تكلفة على حساب API. لا يدخل الشرح غير المتحقق منه في التقرير المعتمد على القواعد.", "Sends the project brief, calculations and source summaries to OpenAI only when clicked. Your API account may incur charges. The unverified explanation is kept out of the rules-based report."))
        # Never expose a public app owner's key: user supplies a per-session key.
        api_key=st.text_input(t("مفتاح API الخاص بك — للجلسة فقط", "Your API key — session only"),type="password",key="api_key")
        model=st.text_input(t("اسم النموذج المتاح في حسابك", "Model name available in your account"),key="api_model",max_chars=150)
        consent=st.checkbox(t("أوافق على إرسال هذه البيانات وتشغيل طلب API من حسابي", "I agree to send these data and run an API request on my account"),key="api_consent")
        if st.button(t("إنشاء شرح لهذا الملف", "Explain this case"),disabled=not(api_key and model and consent)):
            with st.spinner(t("جارٍ إعداد الشرح…", "Preparing explanation…")):
                try: st.session_state["ai_text_"+result["case_id"]+result["as_of"]+lang]=explain(result,lang,api_key,model)
                except AssistError:
                    st.error(t("تعذر الحصول على شرح مكتمل. راجع المفتاح والنموذج والرصيد والاتصال. بقيت الحسابات الأصلية دون تغيير.", "A complete explanation could not be obtained. Check key, model, credits and connection. Original calculations are unchanged."))
        text=st.session_state.get("ai_text_"+result["case_id"]+result["as_of"]+lang)
        if text:
            st.warning(t("شرح مولّد غير متحقق منه؛ راجع الأرقام والمصادر في التقرير.", "Unverified generated explanation; check the report's figures and sources."))
            st.text(text)  # No active external links or HTML from model output.

elif page == "whatif":
    st.title(t("مختبر ماذا لو؟", "What-if lab"))
    result=require_result()
    if not gates(result): st.stop()
    p=Profile(**st.session_state.profile)
    st.write(t("جرّب تغيير الاحتياجات دون تعديل ملفك الأصلي. التقديرات المتأثرة بالتغيير تُلغى وتعود إلى «غير محسوم».", "Explore changes without editing your original brief. Estimates affected by a change are cleared and become unresolved."))
    a,b,c=st.columns(3)
    budget=a.number_input(t("الميزانية البديلة", "Alternative budget"),min_value=0.0,max_value=100000000.0,value=float(p.budget),step=1000.0,key="what_budget")
    visas=b.number_input(t("عدد التأشيرات البديل", "Alternative visa count"),min_value=0,max_value=100,value=p.visas,key="what_visas")
    office=c.selectbox(t("المقر البديل", "Alternative workspace"),["flexi","private"],index=["flexi","private"].index(p.office),format_func=label,key="what_office")
    alternative=scenario(p,st.session_state.get("assumptions",{}),budget,int(visas),office)
    if visas!=p.visas or office!=p.office:
        st.info(t("تغيرت متطلبات الباقة؛ أُلغيت تقديرات الباقة والإضافات والتجديد المتأثرة. لا تعتبر انخفاض المجموع الجزئي توفيرًا مثبتًا.", "Package needs changed; affected base, add-on and renewal estimates were cleared. A lower partial subtotal is not proven savings."))
    st.table([{t("المسار", "Route"):old["name"][lang],t("المجموع الجزئي الأصلي", "Original subtotal"):money(old["subtotal"]),t("المجموع الجزئي البديل", "Alternative subtotal"):money(new["subtotal"]),t("بنود مجهولة أصلًا / بديلًا", "Unknown items original / alternative"):f'{len(old["unknowns"])} / {len(new["unknowns"])}',t("المتبقي البديل قبل النواقص", "Alternative remainder before unknowns"):money(new["budget_gap"])} for old,new in zip(result["routes"],alternative["routes"])])
    st.download_button(t("تنزيل تقرير السيناريو البديل", "Download alternative scenario"),html_report(alternative,lang),file_name="Agentex-scenario.html",mime="text/html")

else:
    st.title(t("المصادر وسجل القرار", "Evidence & decisions"))
    st.info(t("هذه مصادر محفوظة راجعناها في 22 أكتوبر 2026، وليست قراءة مباشرة عند كل استخدام. تنبيه المراجعة بعد 30 يومًا سياسة منتج وليس ضمانًا لصلاحية المعلومات خلالها.", "These saved sources were reviewed on 22 October 2026, not fetched on every use. A 30-day review flag is product policy, not a guarantee that information remains current."))
    result=current_result()
    for sid,source in SOURCES.items():
        with st.container(border=True):
            st.markdown("**"+sid+" · "+source["title"]+"**")
            st.write(source["summary"][lang])
            st.caption(source["limit"][lang])
            st.caption(source["type"][lang]+" · "+source["checked"])
            if result and result["source_states"][sid]=="review_due": st.warning(t("يحتاج مراجعة جديدة", "Needs a new review"))
            st.link_button(t("فتح المصدر", "Open source"),source["url"])
    if result:
        st.subheader(t("سجل القرار للحالة الحالية", "Current case decision record"))
        for ev in result["events"]:
            with st.container(border=True):
                st.write("**"+ev["code"]+"** · "+ev["text"][lang])
                st.caption(ev["kind"]+" · "+(", ".join(ev["sources"]) or t("قاعدة داخلية / مدخلات المستخدم", "Internal rule / user input")))

st.markdown("---")
st.caption(t("Agentex · نموذج تخطيط تجريبي · تطوير شريف حمدان عرجه · ليس جهة ترخيص أو شريكًا حكوميًا معتمدًا.", "Agentex · Planning prototype · Sharif Hamdan Arjah · Not a licensing authority or an accredited government partner."))
