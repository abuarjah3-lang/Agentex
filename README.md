# Agentex 0.2 — Business Decision Studio

من فكرة مشروع إلى ملف قرار أولي قابل للمراجعة.

Developed for Sharif Hamdan Arjah. This release replaces the static demonstration with an executable, bilingual planning prototype. It is not a deployed licensing service or an autonomous multi-agent system.

## التشغيل

Python 3.10+ (tested with Python 3.12.14).

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

على Streamlit Community Cloud: ارفع **جميع ملفات المشروع** إلى المستودع، واجعل `app.py` ملف التشغيل. لا ترفع مفاتيح API أو ملفات الأسرار. هذه الحزمة لم تنشر تلقائيًا إلى GitHub أو Streamlit.

## جرّب النسخة

1. من «البداية»، حمّل مثال المؤسس المستقل ثم افتح «المقارنة وخطة العمل».
2. جرّب مثال الفريق: تظهر تكاليف التأشيرات والمكتب بوصفها غير محسومة.
3. غيّر الميزانية في «ماذا لو؟»، ثم غيّر عدد التأشيرات: يعاد ضبط التقديرات المتأثرة، ولا يعلن التطبيق توفيرًا وهميًا.
4. جرّب النشاط المالي: تتوقف المقارنة وتظهر الحاجة إلى مراجعة متخصصة.
5. أنشئ ملف مشروعك من الصفحة المخصصة. حفظ ملف المشروع يعيد ضبط تقديرات الأسعار.
6. نزّل تقرير HTML، وافتحه في المتصفح، ثم اختر Print / Save as PDF. لا يحتاج التقرير اتصالًا لعرضه.

## ما نُفّذ

- Structured intake with explicit confirmation of the user-selected activity.
- Scope gates, missing-information prompts and transparent decision rules.
- Neutral comparison of two example routes: Dubai mainland and Meydan Free Zone. This is not a complete market comparison.
- Cost arithmetic separating published starting prices, user estimates and unknowns. Unknown is never treated as confirmed zero.
- Visa/package gaps, budget conflicts and customer-market review prompts.
- What-if scenarios that invalidate estimates when requirements change.
- Saved source summaries, review dates and a 30-day review policy. Expired source prices are removed from calculations; 30 days is not a legal validity period.
- Session-only personal checklist. Check marks are not evidence of official completion and are not exported as such.
- Escaped standalone Arabic/English HTML reports and complete JSON decision records.
- Optional OpenAI explanation with explicit per-session user key and consent. The core planning engine makes no API calls.

## حدود مقصودة ومهمة

هذه النسخة **قواعد وحسابات فعلية**، وليست شبكة وكلاء لغوية. وصف المشروع الحر يُحفظ، لكنه لا يُستخدم لتصنيف النشاط آليًا؛ يعتمد التحليل على الحقول التي يؤكدها المستخدم. لا يُستنتج رمز النشاط أو أهليته لدى جهة الترخيص.

لا تُنفّذ معاملات أو طلبات حكومية، ولا تصدر رخصًا أو عقود تأسيس، ولا تثبت الامتثال أو قبول بنك. لا توجد نسبة دقة أو عدد شركات مسجلة أو زمن إنجاز مزعوم. المصادر محفوظة وليست حية، والأسعار تحتاج تأكيدًا مكتوبًا قبل الاعتماد. حتى عند تعبئة كل البنود، تظل كفاية الميزانية غير مثبتة لأن المدخلات قد تكون تقديرات غير متحقق منها.

مجموع السنة الأولى جزئي؛ التجديد منفصل. لا يمثل المجموع ميزانية تشغيل شاملة تشمل الرواتب والمعيشة والتسويق. تقديرات المقر تخص السنة الأولى. أرقام التأشيرات هي إجمالي التخصيص والمعالجة والرسوم المرتبطة للعدد المطلوب، وليس سعر الفرد. لا تدخل نفس التكلفة في أكثر من بند.

## AI explanation (optional)

In Compare & plan, open the optional explanation panel. Supply your own API key and an available model name, review the data-sharing note and consent, then click Explain. One request is sent to `https://api.openai.com/v1/responses`; the app requests `store:false`, limits output and uses a 45-second timeout. This does not imply zero provider retention; provider account policies still apply.

The project brief, calculations and source summaries are sent. Do not enter personal or confidential data. No API request was made during development. Live model output quality and paid-account connectivity are **not yet validated**. Error and response parsing paths were tested with mocks. The model explanation cannot alter the rule engine and is not included in its report; it is explicitly labelled unverified.

For public demonstrations, keep explanation disabled unless a user intentionally supplies their own key. No shared developer key is read from environment or secrets. API keys are not exported or written by this application. Session state ends when the Streamlit session is discarded; it is not durable storage or a multiuser database.

## Sources reviewed 2026-10-22

- S1: https://www.investindubai.gov.ae/en/business-setup/mainland-companies — general mainland route only.
- S2: https://www.meydanfz.ae/blog/meydan-free-zone-company-setup-cost-breakdown — AED 12,500 advertised starting package; visa allocation, processing and extras separate. Not a personalised quote.
- S3: https://app.invest.dubai.ae/search-business-activities — follow-up search link, not an automated integration.
- OpenAI implementation reference: https://developers.openai.com/api/docs/guides/text

Update the relevant source's `checked` date in `engine.py` only after actually re-reading and validating its supported statements. Do not merely change dates to hide review warnings.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests cover scope gates, missing inputs, unknown costs, budget conflicts, renewal separation, stale/missing sources, scenario invalidation, invalid values, HTML escaping, JSON export, optional API failure/parsing and Streamlit navigation/forms in both languages.

## Before a competitive final submission

1. Validate the problem through interviews with 3–5 founders or formation advisers; document actual pain points and alternatives.
2. Obtain expert review of activity matching, source coverage and quote assumptions. Do not claim legal validation beforehand.
3. Build and evaluate actual evidence retrieval and model-assisted intake against a reviewed test set; preserve current deterministic calculations and scope gates.
4. Expand routes only when reliable, maintained primary sources are available.
5. Measure time saved, correctness and abstention on real cases before publishing performance claims.
6. Produce a short demo showing a normal case, a changed requirement and an honest stop when evidence is missing.

The distinctive product direction is an **evidence-linked decision record with counterfactual planning and conflict detection**. Novelty relative to competitors has not been established by market research.
