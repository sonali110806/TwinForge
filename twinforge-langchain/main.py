from prompts import prompt
from agent import run_agent

def main():
    # input data
    data = {"metric": "CPU usage spike"}

    # create prompt
    final_prompt = prompt.format(metric=data["metric"])

    # run agent (IMPORTANT: pass argument)
    result = run_agent(final_prompt)

    # output
    print("\n=== RESULT ===")
    print(result)

if __name__ == "__main__":
    main()
