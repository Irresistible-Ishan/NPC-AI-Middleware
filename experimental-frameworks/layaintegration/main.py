# test run for laya model 

from ollama import chat
from ollama import AsyncClient
import json , asyncio
from filelock import FileLock
from dotenv import load_dotenv
import os
from datetime import datetime
from laya import Router

router = Router() 
load_dotenv()
client = AsyncClient()

def get_time():
    time = datetime.now().strftime("%I:%M %p")
    return time
"""
response = client.chat(
            model = "jaahas/qwen3.5-uncensored:4b " ,
            messages=  [{'role' : 'user' , 'content' : "hello"}], 
            think = False)
"""
# ------------ laya testing ---------------


state = "Hi, we were billed twice for March. Please refund the duplicate today or we will cancel our plan."
questions = {
    "department": {"type": "choice", "instructions": "Which department should handle this?",
                   "criteria": {"billing": "invoices, payments, refunds",
                                "technical": "bugs, outages, system errors",
                                "other": "everything else"}},
    "urgency": {"type": "score", "instructions": "How urgent is this?",
                "criteria": ["not urgent", "soon", "blocking"]},
    "churn_risk": {"type": "noul", "instructions": "Does the user threaten to cancel or leave?"},
}

result = router.predict(state, questions)
print(result["answers"]["department"]["choice"])  # billing
print(result["answers"]["churn_risk"]["noul"])    # probability the answer is yes
print(result["routing"]["model"])                 # english


