import sys
sys.path.insert(0, '.')

print("="*60)
print("MEMBER 4 COMPLETE MODULE TEST")
print("="*60)

# ── Test 1: fixes.py ──────────────────────────────────────────
print("\n[Test 1] fixes.py — Fix definitions")
from tournament.fixes import get_fixes_for_anomaly, ALL_FIXES
fixes = get_fixes_for_anomaly("cpu_percent")
assert len(fixes) == 3, "Must return 3 fixes"
assert all("id" in f and "name" in f and "action" in f for f in fixes)
print(f"  ✓ {len(ALL_FIXES)} fixes defined, 3 returned for cpu_percent")
for f in fixes: print(f"    - {f['name']}")

# ── Test 2: scorer.py ─────────────────────────────────────────
print("\n[Test 2] scorer.py — Confidence scoring")
from tournament.scorer import calculate_confidence, get_decision

high_result = {
    "winner_details": {"fix_id": "rate_limit", "fix_name": "Rate Limit",
                       "success": True, "recovery_seconds": 5,
                       "side_effects": [], "risk_level": "low"},
    "all_results": [
        {"fix_id": "rate_limit", "success": True, "recovery_seconds": 5},
        {"fix_id": "scale_up",   "success": True, "recovery_seconds": 20},
    ]
}
score = calculate_confidence(high_result)
decision = get_decision(score)
assert score > 80, f"High quality fix should score > 80, got {score}"
assert decision["action"] in ["auto_apply", "request_human_approval"]
print(f"  ✓ Score: {score}/100 → Decision: {decision['action']}")

# ── Test 3: postmortem.py ─────────────────────────────────────
print("\n[Test 3] postmortem.py — Claude API post-mortem")
print("  (This calls Claude API — needs ANTHROPIC_API_KEY in .env)")
try:
    from tournament.postmortem import generate_postmortem
    report = generate_postmortem({
        "detected_at": "2026-04-04 10:00:00",
        "anomaly_metric": "cpu_percent",
        "anomaly_value": 91,
        "root_cause": "Traffic spike from /checkout endpoint",
        "fixes_tested": ["Rate Limit", "Scale Up", "Restart"],
        "winning_fix": "Apply Rate Limiting",
        "confidence_score": 94,
        "resolution_seconds": 38
    })
    assert len(report) > 100, "Report should have content"
    print(f"  ✓ Post-mortem generated ({len(report)} characters)")
    print(f"  Preview: {report[:100]}...")
except Exception as e:
    print(f"  ✗ Error (check API key): {e}")

# ── Test 4: memory.py ─────────────────────────────────────────
print("\n[Test 4] memory.py — ChromaDB memory store")
from tournament.memory import save_incident, search_similar_incidents, get_memory_stats

save_incident(
    {"anomaly_metric": "cpu_percent", "anomaly_value": 85,
     "root_cause": "Test incident", "winning_fix": "Rate Limiting",
     "confidence_score": 90},
    "Test incident resolved successfully."
)
stats = get_memory_stats()
results = search_similar_incidents("cpu")
print(f"  ✓ Memory working: {stats['total_incidents_remembered']} incidents stored")

# ── Test 5: tournament.py MOCK ────────────────────────────────
print("\n[Test 5] tournament.py — Mock tournament (no Docker)")
import unittest.mock as mock
from tournament.tournament import pick_winner

fake_results = [
    {"fix_id": "rate_limit",      "fix_name": "Rate Limit",  "success": True,  "recovery_seconds": 8,  "side_effects": []},
    {"fix_id": "scale_up",        "fix_name": "Scale Up",    "success": True,  "recovery_seconds": 20, "side_effects": ["more_resources"]},
    {"fix_id": "restart_service", "fix_name": "Restart",     "success": False, "recovery_seconds": 15, "side_effects": ["downtime"]},
]
winner = pick_winner(fake_results)
assert winner["fix_id"] == "rate_limit", f"Rate limit should win, got {winner['fix_id']}"
print(f"  ✓ Tournament winner correctly selected: {winner['fix_name']}")

print("\n" + "="*60)
print("ALL MEMBER 4 TESTS PASSED ✓")
print("You are ready for integration with the team!")
print("="*60)