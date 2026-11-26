# مصفوفة أدوات الاختبار الوكيلي

هذه المصفوفة توجيهية وليست ضمانًا للميزات. افتح المصدر الرسمي قبل الاعتماد على قدرة أو خطة أو تكامل.

## Momentic

- الموقع: https://momentic.ai/
- الوثائق: https://momentic.ai/docs/mo
- مناسب لـ: الاستكشاف الوظيفي، bug bash، إعادة إنتاج العيوب، وتحويل النتائج إلى اختبارات YAML وCI.
- multi-agent: توثق المنصة وكيل جلسة يخطط ويوزع التحقيق على Investigators متوازيين، ثم يجمع النتائج ويزيل التكرار.
- الحدود: ليس بديلًا موثقًا لاختبار الحمل أو اختبار الاختراق. نتائج AI غير حتمية وتحتاج assertions ومراجعة.

## TestSprite

- الموقع: https://www.testsprite.com/
- بدء MCP: https://docs.testsprite.com/mcp/getting-started/overview
- دورة الاختبار: https://docs.testsprite.com/web-portal/concepts/testing-lifecycle
- مناسب لـ: قراءة PRD والكود، استكشاف UI وAPI، توليد وتشغيل الاختبارات، الأدلة، تحليل الفشل، CI وMCP.
- multi-agent: مصمم لسير عمل يقوده وكيل برمجي، وتذكر صفحاته تشغيل وكلاء على ميزات متعددة؛ لا تفترض وجود orchestrator عام إلا إذا أثبتته نسخة الوثائق الحالية.
- الحدود: ذكر الأداء والوصول والأمن لا يجعله بديلًا تلقائيًا عن أدوات متخصصة؛ راجع المنهجية والمقاييس قبل الاعتماد.

## Playwright Test Agents

- الوثائق: https://playwright.dev/docs/test-agents
- Playwright: https://playwright.dev/
- الوكلاء: planner للاستكشاف والخطة، generator لتحويل الخطة إلى tests، healer لمعالجة الاختبارات الفاشلة.
- مناسب لـ: اختبارات Playwright قابلة للمراجعة والامتلاك داخل المستودع.
- multi-agent: تقسيم مرحلي موثق، وليس بالضرورة تنفيذًا أفقيًا متوازيًا لوكلاء مستقلين.
- الحدود: لا تنسب له تلقائيًا تغطية أداء أو أمن أو WCAG متخصصة.

## mabl

- الموقع: https://www.mabl.com/
- الاختبارات الوكيلة: https://www.mabl.com/ai-test-automation
- مناسب لـ: الويب والهاتف وAPI، إنشاء من اللغة الطبيعية أو المتطلبات، CI/CD، تحليل الفشل، auto-heal، الوصول، وبعض اختبارات الأداء.
- multi-agent: توصف المنصة بأنها تستخدم وكلاء لإنشاء الاختبارات وتشغيلها وتحليل الفشل وصيانتها؛ آلية تقسيم مهمة مخصصة قد تختلف حسب الخطة.
- الحدود: راجع قيود توليد API والهاتف وشروط auto-heal، ولا تعتبر ممارسات حماية البيانات اختبار أمن للتطبيق.

## BrowserStack AI

- الموقع: https://www.browserstack.com/browserstack-ai
- وكلاء الاختبار: https://www.browserstack.com/test-management/ai-agents
- الوصول: https://www.browserstack.com/accessibility-testing/browserstack-ai
- Percy: https://www.browserstack.com/percy/ai-agents
- مناسب لـ: توليد الحالات، تحليل الفشل، self-healing، WCAG، المراجعة البصرية، وMCP داخل منظومة BrowserStack.
- multi-agent: منظومة وكلاء متخصصة قابلة للتكامل، وليست دليلًا على orchestrator عام متعدد الوكلاء.
- الحدود: الإتاحة تختلف حسب المنتج والخطة. لا تنسب إليها اختبار أداء أو أمن هجومي دون توثيق مباشر.

## QA Wolf

- الموقع: https://www.qawolf.com/
- الوكلاء: https://www.qawolf.com/agents
- أتمتة الاختبار: https://docs.qawolf.com/test-automation
- MCP: https://docs.qawolf.com/qawolf-mcp
- مناسب لـ: استكشاف رحلات المستخدم، توليد كود Playwright/Appium قياسي، التشغيل المتوازي، CI، فيديو وtrace وتحليل الفشل.
- multi-agent: يدعم استدعاء المنصة من وكلاء البرمجة، لكن لا تفترض وجود فريق وكلاء داخلي مخصص دون تحقق.
- الحدود: لا تعتبره أداة WCAG أو أداء أو اختبار اختراق متخصصة.

## Browser Use

- الاختبار: https://browser-use.com/automated-testing
- GitHub: https://github.com/browser-use/browser-use
- وثائق Cloud: https://docs.browser-use.com/cloud/agent/quickstart
- مناسب لـ: طبقة متصفح لوكيل مخصص ينفذ مهامًا باللغة الطبيعية، نماذج، تسجيل دخول، تنزيل واستخراج ونتائج مهيكلة.
- multi-agent: توجد أمثلة لوكلاء متوازين، لكن التنسيق المتخصص للاختبارات يجب بناؤه حول المكتبة.
- الحدود: أتمتة متصفح عامة وليست test runner؛ لا تعتمد على حكم `is_successful` وحده، ولا تعرضها كأداة وصول أو أداء أو أمن.

## أدوات مساندة لا تستبدل بعضها

- Playwright Test: https://playwright.dev/docs/intro — assertions، isolation، traces، parallelism، CI.
- Playwright MCP: https://playwright.dev/docs/getting-started-mcp — تحكم بالمتصفح عبر accessibility snapshots.
- W3C Accessibility Tools: https://www.w3.org/WAI/test-evaluate/tools/list/ — دليل أدوات الوصول، مع ضرورة التقييم البشري.
- Chrome DevTools MCP: استخدم المهارة الموجودة في `02-Architecture-Quality/browser-testing-with-devtools` لفحص DOM وconsole وnetwork والأداء والصورة.
