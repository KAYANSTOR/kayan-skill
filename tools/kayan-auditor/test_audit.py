import tempfile, unittest, json
from pathlib import Path
from audit import audit,reports
class AuditTests(unittest.TestCase):
    def test_catalog(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"repo"; root.mkdir()
            for n in ("a","b"):
                p=root/n;p.mkdir();(p/"SKILL.md").write_text("---\nname: demo\ndescription: Flutter demo\n---\nAlways commit changes.\n[bad](missing.md)\n",encoding="utf-8")
            p=root/"c";p.mkdir();(p/"SKILL.md").write_text("---\nname: c\ndescription: demo\n---\nNever commit changes.\n",encoding="utf-8")
            before={p:p.read_bytes() for p in root.rglob("SKILL.md")}
            r=audit(root,.55);self.assertEqual(r["read_count"],3)
            self.assertTrue({"exact-duplicate","duplicate-name","broken-link","potential-conflict"}<={x["kind"] for x in r["findings"]})
            out=Path(d)/"out";reports(r,out)
            self.assertEqual(json.loads((out/"audit.json").read_text())["skill_count"],3)
            self.assertTrue((out/"audit.html").exists())
            self.assertEqual(before,{p:p.read_bytes() for p in root.rglob("SKILL.md")})
    def test_duplicate_yaml(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/"SKILL.md").write_text("---\nname: a\nname: b\ndescription: test\n---\n")
            self.assertTrue(any(f["kind"]=="frontmatter" for f in audit(p)["findings"]))
if __name__=="__main__":
    unittest.main()
