# Registry

- `SKILLS_REGISTRY.json`: سجل مولد من ملفات `SKILL.md`، ويستخدم المسار كمعرف ثابت عند تكرار الاسم.
- `SOURCES_MANIFEST.json`: مصادر upstream وحالة النقل وحقول المراجعة.
- `COMPATIBILITY_MATRIX.json`: مسارات الاكتشاف المقترحة وحالة التحقق لكل أداة.

شغّل `scripts/build-registry` بعد تحديث metadata، ثم `scripts/validate-skills` قبل Commit.
