import os
import sys

# Ensure backend root is in sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from scripts.generate_role_benchmarks import ROLES_DATA

print("AUDIT OF ALL 16 ROLES IN generate_role_benchmarks.py:")
print("-" * 80)
for r in ROLES_DATA:
    onets = [s for s in r.get("sources", []) if "onetonline" in s]
    syn_count = len(r.get("skill_synonyms", {}))
    crit_count = len(r.get("critical_skills", []))
    bonus_count = len(r.get("bonus_skills", []))
    print(f"Role: {r['role']:<30} | Crit: {crit_count:2d} | Bonus: {bonus_count:2d} | Synonyms: {syn_count:2d} | O*NET: {onets}")
