# main.py

from postmortem import analyze_issue
from agent import AI_Agent
from confidence import calculate_confidence
from prompts import get_prompt
from tournament import submit_to_tournament
from fixes import generate_fixes

import logging

# -----------------------
# Logging setup
# -----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting AI agent system...")

    # Step 1: Detect problem using postmortem analysis
    issue_data = analyze_issue()
    logging.info(f"Issue detected: {issue_data}")

    # Step 2: Prepare prompt for AI agent
    prompt = get_prompt(issue_data)
    logging.info(f"Generated prompt for agent: {prompt}")

    # Step 3: Initialize AI agent
    agent = AI_Agent(prompt)
    decision = agent.decide()
    logging.info(f"Agent decision: {decision}")

    # Step 4: Generate possible fixes based on decision
    fixes = generate_fixes(decision)
    logging.info(f"Generated fixes: {fixes}")

    # Step 5: Calculate confidence scores for each fix
    scored_fixes = []
    for fix in fixes:
        confidence_score = calculate_confidence(fix, issue_data)
        scored_fixes.append({'fix': fix, 'confidence': confidence_score})
    logging.info(f"Scored fixes: {scored_fixes}")

    # Step 6: Submit top fixes to tournament / evaluation system
    top_fixes = sorted(scored_fixes, key=lambda x: x['confidence'], reverse=True)
    submit_to_tournament(top_fixes)
    logging.info("Top fixes submitted to tournament successfully.")

    logging.info("AI agent system run completed.")

if __name__ == "__main__":
    main()


        
           
        
    

