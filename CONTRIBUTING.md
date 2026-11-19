# المساهمة

قبل إضافة أو تحديث مهارة، اقرأ `00-MASTER/SECURITY_POLICY.md` و`00-MASTER/WORKFLOW_POLICY.md`. ضع كل مهارة داخل المجموعة المناسبة، وحافظ على `SKILL.md` صالحاً بواجهة YAML تحتوي `name` و`description`.

انسخ المجلد المساعد كاملاً، ولا تشغل سكربتات المصدر أثناء التحقق. حدّث `registry/SOURCES_MANIFEST.json` بمصدر محدد وحالة Commit/Tag وترخيص بعد مراجعة المصدر. بعد التغيير شغّل:

```bash
python scripts/build_registry.py
python scripts/validate-skills
python -m unittest discover -s tests -p 'test_*.py' -v
```

لا تستبدل تعديلاً محلياً بنسخة upstream دون فرق ومراجعة. اشرح في Pull Request ما الذي تغير، وما المهارات أو المصادر المتأثرة، وما فحوص التحقق التي نجحت.
