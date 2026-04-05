import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def generate_postmortem(incident_data: dict) -> str:
    """Generate post-mortem — tries Gemini first, template as backup"""

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""Write a short IT incident post-mortem report.
Keep under 200 words. Sections: SUMMARY, ROOT CAUSE, FIX APPLIED, PREVENTION

Problem: {incident_data.get('anomaly_metric')} at {incident_data.get('anomaly_value')}%
Root cause: {incident_data.get('root_cause')}
Fix applied: {incident_data.get('winning_fix')}
Confidence: {incident_data.get('confidence_score')}%
Fixed in: {incident_data.get('resolution_seconds', 45)} seconds"""

            response = model.generate_content(prompt)
            report = response.text
            _save_report(report)
            print("[PostMortem] ✓ Generated using Gemini (FREE)")
            return report

        except Exception as e:
            print(f"[PostMortem] Gemini error: {e} — using template")

    # Fallback — no API needed at all
    return generate_postmortem_template(incident_data)


def generate_postmortem_template(incident_data: dict) -> str:
    """Template version — works with ZERO API keys"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"""
INCIDENT POST-MORTEM — TwinForge
Generated: {now}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY
Incident auto-detected and resolved by TwinForge.
No human intervention required.

ROOT CAUSE
Metric    : {incident_data.get('anomaly_metric', 'Unknown')}
Value     : {incident_data.get('anomaly_value', '?')}%
Cause     : {incident_data.get('root_cause', 'System anomaly detected')}

FIX APPLIED
Fix used  : {incident_data.get('winning_fix', 'Unknown')}
Confidence: {incident_data.get('confidence_score', 0)}%
Time taken: {incident_data.get('resolution_seconds', 45)} seconds
Auto fixed: {'YES — zero human needed' if incident_data.get('confidence_score', 0) >= 85 else 'Human approved'}

PREVENTION
1. Monitor {incident_data.get('anomaly_metric', 'metrics')} proactively
2. Auto-scaling configured for high traffic
3. This fix pattern saved to TwinForge memory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    _save_report(report)
    print("[PostMortem] ✓ Generated using template (no API needed)")
    return report


def _save_report(report: str):
    os.makedirs("postmortems", exist_ok=True)
    filename = f"postmortems/INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(report)
    print(f"[PostMortem] Saved: {filename}")


def get_all_postmortems() -> list:
    reports = []
    os.makedirs("postmortems", exist_ok=True)
    for f in sorted(os.listdir("postmortems")):
        if f.endswith(".txt"):
            with open(f"postmortems/{f}") as file:
                reports.append({"filename": f, "content": file.read()})
    return reports


# ─── TEST ─────────────────────────────────────────────────────
if __name__ == "__main__":
    test_data = {
        "anomaly_metric": "cpu_percent",
        "anomaly_value": 92,
        "root_cause": "Traffic spike on /checkout",
        "winning_fix": "Apply Rate Limiting",
        "confidence_score": 94,
        "resolution_seconds": 42
    }
    report = generate_postmortem(test_data)
    print("\n" + "="*50)
    print(report)