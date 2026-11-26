# مخطط تقرير الاختبار

استخدم هذا الهيكل في Markdown أو JSON. لا تملأ أي حقل بأدلة غير موجودة.

```json
{
  "run": {
    "project": "string",
    "environment": "staging|preview|localhost",
    "commit": "string|null",
    "started_at": "string",
    "tools": ["string"],
    "browser_profiles": ["isolated-test-profile"]
  },
  "coverage": {
    "anonymous_user": "not_run|partial|complete",
    "authenticated_customer": "not_run|partial|complete",
    "edge_cases": "not_run|partial|complete",
    "api_integrations": "not_run|partial|complete",
    "accessibility_visual": "not_run|partial|complete",
    "performance": "not_run|partial|complete",
    "security": "not_run|partial|complete"
  },
  "findings": [
    {
      "id": "F-001",
      "title": "string",
      "perspective": "anonymous|customer|exploratory|api|accessibility|visual|performance|security",
      "status": "confirmed|failed|inconclusive|blocked",
      "severity": "critical|high|medium|low|info",
      "route": "string",
      "steps": ["string"],
      "expected": "string",
      "actual": "string",
      "evidence": ["path-or-url"],
      "reproduction": "string",
      "confidence": "high|medium|low",
      "candidate_regression_test": false,
      "owner_or_next_action": "string"
    }
  ],
  "deterministic_tests": {
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "artifacts": ["html-report|trace|video|logs"]
  },
  "release_decision": "pass|fail|manual_review|blocked",
  "risks_and_gaps": ["string"]
}
```

## قواعد التقرير

لا تخلط بين `failed` الذي يعني أن اختبارًا حتميًا لم يحقق assertion وبين `inconclusive` الذي يعني أن الوكيل لم يملك دليلًا كافيًا. اربط كل عيب مؤكد بدليل قابل لإعادة الإنتاج. أظهر الأدوار التي لم تعمل أو حجبتها المصادقة. سجّل الأدوات والإصدارات حتى يمكن إعادة التشغيل. لا تعرض الأسرار أو بيانات الاعتماد أو tokens في الأدلة أو السجلات.
