import sys
import time
from pathlib import Path

prject_path = Path(__file__).resolve().parents[2]

if str(prject_path) not in sys.path:
    sys.path.insert(0, str(prject_path))

from backend.agent import run_agent

def main():
    # Test 1: Testing tool selection via natural language
    prompt = "send a mail to kondurupriyanka80@gmail.com saying iam fine here and how are you add somehing nice."
    print(f"User: {prompt}")

    response = run_agent(prompt=prompt)
    print(f"EndoAgent : {response}")

if __name__ == "__main__":
    main()    
    