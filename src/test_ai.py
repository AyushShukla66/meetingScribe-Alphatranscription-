from services.ai_engine import generate_executive_brief

transcript = """
Ravi will complete the firewall upgrade by Friday.

Priya will prepare the RBI compliance report.

Decision:
Approve new branch opening in Indore.

Risk:
Delay in CBS integration.
"""

print(generate_executive_brief(transcript))