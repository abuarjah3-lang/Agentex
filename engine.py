"""Agentex 0.2 — explicit rules, evidence snapshots, and scenario arithmetic.

No legal eligibility inference, live retrieval, licensing or external action.
"""
from dataclasses import dataclass, asdict, replace
from datetime import date, datetime, timezone
from hashlib import sha256
import json
import math

VERSION = "0.2.0"
REVIEW_DATE = "2026-10-22"
REVIEW_INTERVAL_DAYS = 30  # Product review policy, not a statutory expiry.

def bi(ar, en):
    return {"ar": ar, "en": en}

SOURCES = {
    "S1": {
        "title": "Invest in Dubai — Mainland companies",
        "url": "https://www.investindubai.gov.ae/en/business-setup/mainland-companies",
        "checked": REVIEW_DATE,
        "type": bi("بوابة حكومية", "Government portal"),
        "summary": bi("تعرّف البوابة بمسار تأسيس شركة في البر الرئيسي لمن يستهدف العمل داخل الإمارات أو خارج المناطق الحرة.", "The portal describes mainland formation for businesses targeting UAE trade or a location outside free zones."),
        "limit": bi("لا يثبت هذا المصدر أهلية نشاط محدد أو رسومه.", "Does not establish eligibility or fees for a specific activity."),
    },
    "S2": {
        "title": "Meydan Free Zone — Company setup cost breakdown",
        "url": "https://www.meydanfz.ae/blog/meydan-free-zone-company-setup-cost-breakdown",
        "checked": REVIEW_DATE,
        "type": bi("مصدر مباشر من مقدم الخدمة", "Provider primary source"),
        "summary": bi("تعلن ميدان بداية سعرية 12,500 درهم تشمل الرخصة ومكتبًا مرنًا وحتى ثلاث مجموعات أنشطة؛ تخصيص التأشيرات ومعالجتها والإضافات منفصلة.", "Meydan advertises a starting package of AED 12,500 with a licence, flexi-desk and up to three activity groups; visa allocation, processing and add-ons are separate."),
        "limit": bi("سعر ابتدائي منشور وليس عرض سعر لحالتك؛ يلزم تأكيد النشاط والإجمالي والتجديد والضرائب.", "An advertised starting price, not a quote for your case; confirm activity, total, renewal and taxes."),
    },
    "S3": {
        "title": "Invest in Dubai — Business activity search",
        "url": "https://app.invest.dubai.ae/search-business-activities",
        "checked": REVIEW_DATE,
        "type": bi("أداة حكومية للبحث", "Government search tool"),
        "summary": bi("أداة للبحث باسم النشاط أو رقمه. التطبيق لا يستعلم منها آليًا.", "Search by activity name or number. This app does not query this tool automatically."),
        "limit": bi("رابط للمتابعة فقط؛ لم تُطابق رموز أنشطة المستخدم في هذه النسخة.", "Follow-up link only; user activity codes are not matched in this release."),
    },
}

LABELS = {
    "software": bi("تطوير برمجيات / SaaS", "Software / SaaS"),
    "it": bi("استشارات تقنية", "IT consulting"),
    "digital": bi("خدمات رقمية", "Digital services"),
    "other": bi("نشاط آخر", "Other activity"),
    "international": bi("عملاء خارج الإمارات", "International clients"),
    "uae": bi("عملاء داخل الإمارات", "UAE clients"),
    "both": bi("داخل الإمارات وخارجها", "UAE and international"),
    "flexi": bi("مكتب مرن", "Flexi-desk"),
    "private": bi("مكتب خاص", "Private office"),
    "unknown": bi("لم أحدد بعد", "Not decided"),
    "meydan": bi("ميدان — مسار منطقة حرة", "Meydan — free-zone route"),
    "mainland": bi("دبي — مسار البر الرئيسي", "Dubai — mainland route"),
    "base": bi("الباقة / الرخصة الأساسية", "Base package / licence"),
    "visa": bi("التأشيرات: تخصيص ومعالجة ورسوم مرتبطة", "Visas: allocation, processing and related fees"),
    "office": bi("المقر للسنة الأولى / الترقية", "First-year premises / upgrade"),
    "other_cost": bi("رسوم إضافية وضرائب وخدمات لازمة", "Additional fees, taxes and required services"),
    "renewal": bi("التجديد للسنة الثانية — منفصل عن مجموع السنة الأولى", "Year-two renewal — excluded from year-one subtotal"),
}

@dataclass(frozen=True)
class Profile:
    description: str = ""
    activity: str = "software"
    budget: float = 25000
    visas: int = 0
    office: str = "flexi"
    market: str = "international"
    founders: int = 1
    regulated: bool = False
    confirmed_scope: bool = False

def fingerprint(profile, assumptions):
    return sha256(json.dumps({"profile": asdict(profile), "assumptions": assumptions}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]

def source_state(source, today):
    try:
        age = (today - date.fromisoformat(source["checked"])).days
        return "review_due" if age < 0 or age > REVIEW_INTERVAL_DAYS else "snapshot"
    except (KeyError, ValueError, TypeError):
        return "review_due"

def validate(profile, assumptions):
    if profile.activity not in ("software", "it", "digital", "other"):
        raise ValueError("Invalid activity")
    if profile.office not in ("flexi", "private", "unknown") or profile.market not in ("international", "uae", "both", "unknown"):
        raise ValueError("Invalid profile option")
    if not isinstance(profile.description, str) or len(profile.description) > 2000:
        raise ValueError("Description too long")
    if not math.isfinite(profile.budget) or profile.budget < 0 or profile.budget > 1e9:
        raise ValueError("Invalid budget")
    if type(profile.visas) is not int or not 0 <= profile.visas <= 100:
        raise ValueError("Invalid visa count")
    if type(profile.founders) is not int or not 1 <= profile.founders <= 100:
        raise ValueError("Invalid founder count")
    for route, values in assumptions.items():
        if route not in ("meydan", "mainland") or not isinstance(values, dict):
            raise ValueError("Invalid route")
        for key, value in values.items():
            if key not in ("base", "visa", "office", "other_cost", "renewal"):
                raise ValueError("Invalid cost key")
            if value is not None and (isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or not 0 <= value <= 1e9):
                raise ValueError("Invalid cost value")

def analyse(profile, assumptions=None, today=None, sources=None):
    assumptions = assumptions or {}
    today = today or date.today()
    sources = SOURCES if sources is None else sources
    validate(profile, assumptions)
    events, questions, routes = [], [], []
    def event(code, ar, en, refs=(), level="review", kind="rule"):
        events.append({"code": code, "text": bi(ar, en), "sources": list(refs), "level": level, "kind": kind})
    if not profile.description.strip():
        questions.append(bi("صف الخدمة التي ستبيعها ولمن.", "Describe the service you will sell and to whom."))
    if not profile.confirmed_scope:
        questions.append(bi("أكد تصنيف نشاطك؛ الوصف الحر لا يُصنّف آليًا في هذا الإصدار.", "Confirm your activity classification; free text is not automatically classified in this release."))
    if profile.office == "unknown":
        questions.append(bi("هل تحتاج مكتبًا خاصًا أم مكتبًا مرنًا؟", "Do you need a private office or a flexi-desk?"))
    if profile.market == "unknown":
        questions.append(bi("هل عملاؤك داخل الإمارات أم خارجها؟", "Are your clients in the UAE or abroad?"))
    blocked = profile.activity == "other" or profile.regulated
    if blocked:
        event("SCOPE", "هذه الحالة خارج نطاق النسخة؛ يلزم تصنيف متخصص قبل مقارنة المسارات.", "This case is outside this release's scope; obtain specialist classification before route comparison.", level="blocked")
    if questions:
        event("INTAKE", "توجد معلومات ناقصة؛ أكمل الأسئلة قبل المقارنة.", "Information is missing; answer the questions before comparison.", level="blocked")
    if blocked or questions:
        status = "out_of_scope" if blocked else "needs_input"
    else:
        status = "preliminary"
        event("ACTIVITY", "لم تُؤكّد أهلية النشاط أو رمزه لدى أي جهة؛ تحقق قبل الاختيار.", "Activity eligibility and codes are unconfirmed for every route; verify before selecting.", ("S3",))
        if profile.market in ("uae", "both"):
            event("MARKET", "أضف مسار البر الرئيسي للمناقشة، وتحقق من شروط خدمة العملاء داخل الإمارات لكل خيار؛ هذا لا يستبعد المناطق الحرة.", "Discuss the mainland route and verify conditions for serving UAE clients for each option; this does not exclude free zones.", ("S1",), kind="planning_inference")
        if profile.founders > 1:
            event("FOUNDERS", "تعدد المؤسسين يحتاج تأكيد متطلبات المساهمين وأي رسوم إضافية بعرض مكتوب.", "Multiple founders require confirmation of shareholder requirements and any added fees in a written quote.", kind="planning_inference")
        for route_id in ("meydan", "mainland"):
            values = assumptions.get(route_id, {})
            rows, notes = [], []
            src = "S2" if route_id == "meydan" else "S1"
            evidence_ok = src in sources and source_state(sources[src], today) == "snapshot"
            if not evidence_ok:
                event("FRESHNESS_" + route_id, "مصدر المسار يحتاج مراجعة؛ لن نعتمد سعرًا منشورًا قديمًا في الحساب.", "This route's source needs review; stale published prices will not be used in calculations.", (src,))
            def add(key, amount, origin, ref=None):
                rows.append({"key": key, "label": LABELS[key], "amount": amount, "origin": origin, "source": ref})
            base = values.get("base")
            if base is not None:
                add("base", base, "user_estimate")
            elif route_id == "meydan" and evidence_ok:
                add("base", 12500, "published_start", "S2")
            else:
                add("base", None, "unknown")
            if profile.visas:
                add("visa", values.get("visa"), "user_estimate" if values.get("visa") is not None else "unknown")
                if route_id == "meydan":
                    notes.append(bi("الباقة الأساسية لا تغطي تخصيص التأشيرات ومعالجتها؛ يلزم عرض مناسب لعدد التأشيرات.", "The base package excludes visa allocation and processing; request a quote for your visa count."))
                    event("VISA_GAP", "احتياج التأشيرات لا تغطيه البداية السعرية المنشورة لميدان.", "The advertised Meydan starting price does not cover the requested visa needs.", ("S2",))
            if profile.office == "private" or route_id == "mainland":
                add("office", values.get("office"), "user_estimate" if values.get("office") is not None else "unknown")
            elif route_id == "meydan":
                notes.append(bi("المكتب المرن ضمن الوصف المنشور؛ أكّد إدراجه في عرضك، خصوصًا إن استبدلت السعر بتقديرك.", "A flexi-desk is described in the published package; confirm inclusion in your quote, especially if you replace the base price."))
            add("other_cost", values.get("other_cost"), "user_estimate" if values.get("other_cost") is not None else "unknown")
            subtotal = sum(row["amount"] for row in rows if row["amount"] is not None)
            unknowns = [row["key"] for row in rows if row["amount"] is None]
            gap = profile.budget - subtotal
            budget_state = "exceeds" if gap < 0 else "unresolved"
            if gap < 0:
                event("BUDGET_" + route_id, "المجموع الجزئي لهذا المسار يتجاوز الميزانية، قبل استكمال البنود الناقصة.", "This route's subtotal exceeds the budget before unresolved items are added.", level="conflict", kind="calculation")
            routes.append({"id": route_id, "name": LABELS[route_id], "rows": rows, "subtotal": subtotal, "unknowns": unknowns, "budget_gap": gap, "budget_state": budget_state, "renewal": values.get("renewal"), "notes": notes, "sources": [src, "S3"], "eligibility": "unconfirmed"})
    tasks = [
        {"id":"T1", "label":bi("تأكيد النشاط ورمزه وأهليته لدى الجهة", "Confirm activity code and eligibility with the authority"), "depends":[], "source":"S3"},
        {"id":"T2", "label":bi("طلب عرض مكتوب: سنة أولى وتجديد وتأشيرات ومقر وضرائب", "Request a written quote: year one, renewal, visas, premises and taxes"), "depends":["T1"], "source":None},
        {"id":"T3", "label":bi("مقارنة العروض وتأكيد النواقص مع مختص", "Compare quotes and resolve gaps with a specialist"), "depends":["T2"], "source":None},
        {"id":"T4", "label":bi("طلب قائمة المستندات الرسمية من الجهة المختارة", "Obtain the official document checklist from the selected authority"), "depends":["T3"], "source":None},
    ] if status == "preliminary" else []
    return {"version": VERSION, "case_id": fingerprint(profile, assumptions), "generated_at": datetime.now(timezone.utc).isoformat(), "as_of": today.isoformat(), "profile": asdict(profile), "assumptions": assumptions, "status":status, "questions":questions, "routes":routes, "events":events, "tasks":tasks, "sources":sources, "source_states":{k:source_state(v,today) for k,v in sources.items()}, "review_policy_days":REVIEW_INTERVAL_DAYS}

def scenario(profile, assumptions, budget, visas, office, **kwargs):
    """Invalidate dependent totals when quantities/configuration change."""
    adjusted = {route: dict(values) for route, values in assumptions.items()}
    for values in adjusted.values():
        if visas != profile.visas:
            values["visa"] = None
            values["base"] = None
            values["other_cost"] = None
            values["renewal"] = None
        if office != profile.office:
            values["office"] = None
            values["base"] = None
            values["other_cost"] = None
            values["renewal"] = None
    return analyse(replace(profile, budget=budget, visas=visas, office=office), adjusted, **kwargs)
