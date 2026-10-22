"""Escaped, standalone report; browser Print can save as PDF."""
from html import escape
import json
from engine import LABELS

def export_json(result):
    return json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False).encode("utf-8")

def html_report(result, lang="ar"):
    ar = lang == "ar"
    def t(a,b): return a if ar else b
    def e(value): return escape(str(value), quote=True)
    def money(value): return t("غير محسوم", "Unresolved") if value is None else f"{value:,.0f} AED"
    p = result["profile"]
    body = f'<h1>AGENTEX <small>v{e(result["version"])}</small></h1><h2>{t("ملف قرار التأسيس الأولي", "Preliminary formation decision file")}</h2>'
    body += f'<p>{e(result["case_id"])} · {e(result["generated_at"])}</p>'
    body += f'<aside>{t("تخطيط أولي بقواعد معلنة ومصادر محفوظة. ليس ترخيصًا أو تحققًا قانونيًا. المقارنة محدودة بمسارين ولا تثبت الأفضل أو الأرخص. المجموع جزئي وليس تكلفة نهائية.", "Preliminary planning using explicit rules and saved sources. Not licensing or legal verification. Two routes only, with no best/cheapest claim. Subtotals are not final costs.")}</aside>'
    body += f'<h3>{t("المشروع", "Project")}</h3><p>{e(p["description"])}</p><ul>'
    for key in ("activity", "market", "office"):
        body += f'<li>{e(LABELS[p[key]][lang])}</li>'
    body += f'<li>{t("الميزانية", "Budget")}: {money(p["budget"])}</li><li>{t("التأشيرات", "Visas")}: {p["visas"]}</li><li>{t("المؤسسون", "Founders")}: {p["founders"]}</li></ul>'
    for q in result["questions"]: body += f'<p>{e(q[lang])}</p>'
    for r in result["routes"]:
        body += f'<h3>{e(r["name"][lang])}</h3><table><tr><th>{t("البند", "Item")}</th><th>{t("المبلغ", "Amount")}</th><th>{t("أساس القيمة", "Basis")}</th></tr>'
        origins = {"user_estimate":t("تقدير المستخدم", "User estimate"), "published_start":t("بداية سعرية منشورة [S2]", "Published starting price [S2]"), "unknown":t("غير محسوم", "Unresolved")}
        for row in r["rows"]:
            body += f'<tr><td>{e(row["label"][lang])}</td><td>{money(row["amount"])}</td><td>{origins[row["origin"]]}</td></tr>'
        priced = any(row["amount"] is not None for row in r["rows"])
        body += f'</table><p><b>{t("المجموع الجزئي", "Partial subtotal")}: {money(r["subtotal"] if priced else None)}</b> · {t("بنود غير محسومة", "Unresolved items")}: {len(r["unknowns"])}</p>'
        body += f'<p>{t("التجديد منفصل", "Renewal separate")}: {money(r["renewal"])}</p>'
        body += f'<p>{t("أهلية النشاط غير مؤكدة؛ كفاية الميزانية غير مثبتة.", "Activity eligibility is unconfirmed; budget sufficiency is not established.")}</p>'
        for n in r["notes"]: body += f'<p>{e(n[lang])}</p>'
    body += f'<h3>{t("سجل القرار", "Decision record")}</h3><ul>'
    for ev in result["events"]: body += f'<li><b>{e(ev["code"])}</b>: {e(ev["text"][lang])} {e(" ".join(ev["sources"]))}</li>'
    body += f'</ul><h3>{t("الخطوات التالية — غير منفذة", "Next steps — not executed")}</h3><ol>'
    for task in result["tasks"]: body += f'<li>{e(task["label"][lang])}</li>'
    body += f'</ol><h3>{t("المصادر", "Sources")}</h3>'
    for sid, s in result["sources"].items():
        body += f'<p><b>{e(sid)} — {e(s["title"])}</b><br><a href="{e(s["url"])}">{e(s["url"])}</a><br>{e(s["summary"][lang])}<br>{e(s["limit"][lang])}<br>{t("تاريخ المراجعة", "Reviewed")}: {e(s["checked"])} · {e(result["source_states"][sid])}</p>'
    body += f'<p>{t("تحتاج المصادر مراجعة بعد 30 يومًا وفق سياسة المنتج، وقد تتغير قبل ذلك. التقرير لا يجري تحققًا حيًا.", "Product policy flags sources for review after 30 days; they may change sooner. This report does not perform live verification.")}</p>'
    return ('<!doctype html><html lang="'+lang+'" dir="'+('rtl' if ar else 'ltr')+'"><meta charset="utf-8"><title>Agentex decision file</title><style>body{font:16px/1.8 Arial,sans-serif;color:#142c3b;max-width:1000px;margin:40px auto;padding:24px}h1{color:#087f6f}small{font-size:14px}aside{background:#edf6f4;padding:18px;border-inline-start:4px solid #087f6f}table{width:100%;border-collapse:collapse}td,th{padding:10px;border:1px solid #d4e2df;text-align:start}a{overflow-wrap:anywhere}h3{margin-top:30px}@media print{body{margin:0;padding:0;font-size:12px}table{break-inside:avoid}h3{break-after:avoid}}</style>'+body+'</html>').encode('utf-8')
