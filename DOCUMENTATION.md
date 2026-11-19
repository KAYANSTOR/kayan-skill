# دليل دمج وإدارة كتالوج `kayan-skill`

هذا الدليل يشرح كيف تُكتشف المهارات وتُثبت وتُراجع بأمان مع أدوات التطوير والوكلاء المحليين والسحابيين. الكتالوج مصدر ملفات وتعليمات؛ وجود `SKILL.md` لا يعني أن الأداة ستستدعيه تلقائياً.

## 1. البنية المعتمدة

```text
kayan-skill/
├── 00-MASTER/                 # السياسات المركزية والتوافق والصلاحيات
├── 01-Core-Workflows/         # التخطيط والاختبار والتصحيح والمراجعة
├── 02-Architecture-Quality/   # المعمارية وجودة الكود والأداء والأمان
├── 03-UI-UX-Design/           # UI/UX وFigma وAdobe والحركات
├── 04-Web-Frameworks/         # React وNext وأنماط تركيب الويب
├── 05-AI-Infrastructure/     # البوابات والموجهات وأدوات النماذج
├── 06-Code-Analysis/          # Graphify وتحليل قواعد الكود
├── 07-SEO-Marketing/          # SEO وGEO والمحتوى والتجارة
├── 08-Security-Auditing/     # التدقيق الأمني وSAST والثغرات
├── registry/                  # سجل المهارات والمصادر والتوافق
├── scripts/                   # التثبيت والتحقق والتدقيق والتحديث الآمن
├── tests/                     # اختبارات الكتالوج نفسه
└── .github/workflows/         # تحقق تلقائي عند Push وPull Request
```

كل مهارة أساسية تبدأ من `<skill-path>/SKILL.md` وقد تعتمد على `references/` أو `scripts/` أو `assets/`. انسخ مجلد المهارة كاملاً ولا تنسخ الملف وحده.

## 2. التثبيت الصحيح في مشروع

نفذ الأوامر داخل بيئة التطوير أو الوكيل، وليس على الهاتف. يحافظ المثبت على اسم المجموعة، ولذلك لا يحدث تعارض بين مهارتين لهما الاسم نفسه ولا تنكسر المسارات المذكورة في التقارير.

```bash
set -e
cd /path/to/project
git clone https://github.com/KAYANSTOR/kayan-skill.git /tmp/kayan-skill
python /tmp/kayan-skill/scripts/install-skills --destination .agent/skills --dry-run
python /tmp/kayan-skill/scripts/install-skills --destination .agent/skills
find .agent/skills -type f -name SKILL.md | sort
```

لتثبيت مجموعة محددة:

```bash
python /tmp/kayan-skill/scripts/install-skills \
  --destination .agent/skills \
  --category 01-Core-Workflows \
  --category 02-Architecture-Quality
```

إذا كان `.agent/skills` يحتوي على نسخ سابقة، راجع الفرق أولاً. لا تستخدم `--force` إلا بعد حفظ التغييرات المحلية ومراجعة أن الاستبدال مقصود.

المسارات بعد التثبيت تكون من الشكل التالي:

```text
.agent/skills/01-Core-Workflows/verification-before-completion/SKILL.md
.agent/skills/02-Architecture-Quality/security-and-hardening/SKILL.md
.agent/skills/03-UI-UX-Design/ui/mobile-first-card-ui-architecture/SKILL.md
.agent/skills/08-Security-Auditing/cloudflare/security-audit/SKILL.md
```

## 3. اختيار المهارة من المجموعات الثماني

| المجموعة | استخدمها عندما تحتاج إلى |
| --- | --- |
| `01-Core-Workflows` | عصف ذهني، خطة تنفيذ، TDD، تصحيح منهجي، مراجعة، أو تحقق قبل الإكمال |
| `02-Architecture-Quality` | تصميم معماري، جودة كود، تبسيط، أداء، اختبار متصفح، أو مراجعة أمان عامة |
| `03-UI-UX-Design` | تصميم واجهة، RTL، أنظمة تصميم، Figma/Adobe، حركات وتجربة استخدام |
| `04-Web-Frameworks` | React، Next.js، composition patterns، أو إرشادات واجهات الويب |
| `05-AI-Infrastructure` | بوابة LLM، توجيه نماذج، مزودات، مفاتيح، حدود استخدام، أو OmniRoute |
| `06-Code-Analysis` | بناء رسم بياني معرفي لقاعدة كود أو الاستعلام عن علاقات الملفات |
| `07-SEO-Marketing` | Technical SEO، GEO، E-E-A-T، Schema، Sitemap، محتوى، منافسين أو تجارة إلكترونية |
| `08-Security-Auditing` | SAST، CodeQL، Semgrep، CVSS، threat modeling، سلسلة توريد أو فرز ثغرات |

لا تطلب من الوكيل قراءة الكتالوج كله. اختر مهارة أو مهارتين، واقرأ ملفهما، ثم اذكر نطاق الملفات ونوع المخرج المطلوب.

## 4. سجل المهارات والمصادر

السجل المركزي هو [`registry/SKILLS_REGISTRY.json`](./registry/SKILLS_REGISTRY.json). لكل سجل مسار المهارة ووصفها ومجموعتها وتبعياتها المحتملة وحالة التحقق ومعلومة المصدر. تستخدم المسارات كمعرفات ثابتة عند وجود أسماء مكررة.

- `registry/SOURCES_MANIFEST.json`: المستودعات الأصلية، نوع النقل، وحالة مراجعة Commit/Tag والترخيص.
- `registry/COMPATIBILITY_MATRIX.json`: المسار المقترح وطريقة الاكتشاف وحالة التوافق لكل أداة.
- `scripts/audit-sources`: تقرير الحقول التي تحتاج مراجعة بشرية.

شغّل إعادة بناء السجل بعد إضافة مهارة أو تغيير metadata:

```bash
python scripts/build_registry.py
python scripts/validate-skills
```

لا تُملأ معلومات Commit أو License بالتخمين. راجع المصدر الأصلي، ثم حدّث manifest في نفس التغيير.

## 5. Claude Code وCodex وCursor وGemini وVS Code وAntigravity وManus

المسار المشترك الآمن هو `.agent/skills/`. بعض الإصدارات تدعم الاكتشاف التلقائي وبعضها يحتاج توجيهاً صريحاً؛ راجع [`00-MASTER/AGENT_COMPATIBILITY.md`](./00-MASTER/AGENT_COMPATIBILITY.md) وإصدار الأداة قبل الاعتماد على الاكتشاف.

استخدم رسالة صريحة عند عدم معرفة دعم الأداة:

```text
قبل التنفيذ اقرأ:
.agent/skills/00-MASTER/SECURITY_POLICY.md
.agent/skills/00-MASTER/WORKFLOW_POLICY.md
.agent/skills/02-Architecture-Quality/code-review-and-quality/SKILL.md

حلل الملفات المحددة فقط. أخرج تقريراً وخطة، ولا تعدل أو تثبت أو تعمل Commit.
```

في Manus والوكلاء السحابيين، ثبّت المهارات داخل مساحة العمل المعزولة واترك الهاتف مديراً للموافقة. لا تضع مفاتيح API أو رموز OAuth داخل الكتالوج.

## 6. تكاملات Figma وAdobe

تقع مهارات Figma وAdobe في `03-UI-UX-Design/figma-adobe-tools/`. قبل استخدامها تحقق من MCP أو تكامل التطبيق والمصادقة:

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
claude mcp list
```

قد تختلف أوامر Claude وCursor وGemini حسب الإصدار؛ لا تنقل بيانات الاعتماد إلى Git. اقرأ `03-UI-UX-Design/CONNECTORS.md` والمهارة المطلوبة، ثم اطلب خطة قبل أي تعديل.

## 7. OpenCodeReview وAI Infrastructure

توجد مهارة التفويض في `01-Core-Workflows/alibaba-open-code-review/`. اتبع تعليماتها وتحقق من وجود Node.js قبل التثبيت. أدوات `05-AI-Infrastructure` توثق بوابات وموجهات LLM لكنها لا تمنح مفاتيح أو خدمة مجانية تلقائياً؛ راجع التبعيات والحدود والخصوصية قبل الاتصال بمزود.

## 8. SEO وتحليل الكود والأمان

تحتوي `07-SEO-Marketing/claude-seo/skills/` على مهارات SEO متعددة. اختر `seo-technical` أو `seo-geo` أو `seo-schema` حسب المهمة ولا تفترض أن كل API متاح.

يحتوي `06-Code-Analysis/graphify/` على توثيق Graphify ومسارات الوكلاء. استخدمه لفهم علاقات قاعدة الكود قبل قراءة آلاف الملفات، مع الحفاظ على وضع القراءة فقط.

ابدأ مهام الأمان من `08-Security-Auditing/README.md` ثم اقرأ `00-MASTER/SECURITY_POLICY.md`. نفّذ الفحص فقط على أنظمة مصرح بها، وتعامل مع النتائج كفرضيات تحتاج تحققاً.

## 9. دورة العمل والصلاحيات

1. اقرأ السياسات المركزية ثم نفذ تدقيقاً قراءة فقط.
2. حدد المهارات المطلوبة ونطاق الملفات والأدوات الخارجية.
3. أخرج تقريراً يذكر الملف والسطر والدليل والأثر ودرجة الخطر.
4. اطلب موافقة صريحة قبل التعديل أو التثبيت أو Commit أو Push.
5. نفذ التغيير المحدد فقط وشغّل الاختبارات المناسبة.
6. راجع الفرق وسجّل المهارات المستخدمة.

مهارة `subagent-driven-development` لا تمنح صلاحية Commit. أي عبارة عن Commit داخل مهارة فرعية مشروطة بسياسة المشروع وموافقة المستخدم.

## 10. التحقق وCI

التحقق المركزي لا ينفذ أي سكربت من المهارات؛ يفحص metadata، المسارات، الروابط المحلية، التكرارات، والسجل:

```bash
python scripts/validate-skills
python -m unittest discover -s tests -p 'test_*.py' -v
python -m compileall -q scripts tests
```

يُشغّل GitHub Actions نفس الفحوص عند كل Push وPull Request. لا تُضاف اختبارات تشغّل كوداً من المهارات الخارجية تلقائياً.

## 11. التحديث والإصدارات

`scripts/update-skills --check` يعرض خطة مراجعة فقط. `--apply` مرفوض عمداً؛ لا يُستبدل محتوى محلي بنسخة upstream آلياً. حدّث مهارة واحدة بعد مراجعة فرق المصدر والترخيص والاعتماديات، ثم شغّل المدقق وسجّل التغيير.

الإصدارات موثقة في [`CHANGELOG.md`](./CHANGELOG.md). استخدم SemVer عند إنشاء Tags أو Releases بعد موافقة مالك المستودع.

## 12. استكشاف الأخطاء

إذا لم يجد الوكيل المهارة، تحقق من المسار الكامل ووجود `SKILL.md` ثم اطلب قراءته صراحة. إذا فقدت المراجع، أعد تثبيت مجلد المهارة كاملاً عبر `install-skills`. إذا فشل CI، شغّل `validate-skills --json` واقرأ أول خطأ؛ لا تتجاوز الفحص بإخفاء الرابط أو حذف المرجع دون فهمه.
