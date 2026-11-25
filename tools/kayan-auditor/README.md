# Kayan Skill Auditor
Read-only static analysis of SKILL.md files, registry, source metadata and support scripts. Never executes skill code. Requires Python 3.10+.
```sh
python -m pip install -r tools/kayan-auditor/requirements.txt
python -m unittest discover -s tools/kayan-auditor -p 'test_*.py'
python tools/kayan-auditor/audit.py . --out ../kayan-audit
```
Output must be outside the repository. HTML, JSON and Markdown reports are generated. Exit 2 means no skills or incomplete reads; --fail-on-high optionally gates confirmed high findings. Similarity, policy conflicts, license and dependency indicators require human review; no upstream legal verification is performed. CI runs on main pushes, PRs, manual dispatch and Mondays 02:15 UTC. Download reports from Actions artifacts (30 days). No automatic commits. The CI integration excludes its own directory and common dependency directories from scanning and omits raw command excerpts from risk findings to reduce exposure.
