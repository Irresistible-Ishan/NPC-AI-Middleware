import discord
from discord import app_commands
from datetime import datetime
from ollama import chat
from ollama import AsyncClient
import json , asyncio
from filelock import FileLock
from dotenv import load_dotenv
import os

load_dotenv()

lock = FileLock("unified_physics.json.lock")
client = AsyncClient()
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

def get_time():
    time = datetime.now().strftime("%I:%M %p")
    return time


async def cloth(param, channel):
    global data
    call_json()
    my_name = "aoi"
    for item_name, action in param.items():
        action = action.lower().strip()
        if action == "remove":

            for char_name in data['characters'].keys():
                if item_name in data['characters'][char_name]['visible']['clothing']:
                    data['characters'][char_name]['visible']['clothing'].remove(item_name)
                    await channel.send(f"{char_name.capitalize()} was discarded of **{item_name}**")
                    break 
                    
        elif action == "add":
            if item_name not in data['characters'][my_name]['visible']['clothing']:
                data['characters'][my_name]['visible']['clothing'].append(item_name)
                await channel.send(f"{my_name.capitalize()} equipped **{item_name}**")
    send_json()

def LTM(str):
    global data
    call_json()
    data['characters']['aoi']['LTM'] += str + "\n"
    send_json()


def pay(obj):
    global data
    call_json()
    for i in obj.keys():
        data['characters'][i.lower().strip()]['money'] += obj[i]
        data['characters']['aoi']['money'] -= obj[i]
    send_json()


async def force_json(msg , e):
    prompt = f'''
    we are getting this error {e}
    for the message : 

    {msg}

    just take teh reply out of this exactly as it is originally
    and copy paste this to proper json fromat , 
    do the same for face expression and body pose
    and tool use as per the give sturcture explained below

    Rules:

    1. NEVER invent new dialogue.
    2. NEVER invent new tools.
    3. NEVER invent new clothing.
    4. NEVER invent new actions.
    5. NEVER infer missing information.
    6. NEVER rewrite the conversation.
    7. CRITICAL: NEVER use backslashes (\\) to escape quotes. Use clean quotes only.


    If multiple JSON objects exist, RETURN ONLY THE FIRST COMPLETE JSON OBJECT.
    YOU MUST REPLY IN VALID JSON ONLY AND NOTHING EXTRA OTHER THAN THAT.

    Without tool:
    {{
    "reply":"SPOKEN_WORDS_ONLY_as given in the original message",
    "face_expression":"EMOTION",
    "body_pose":"BODY_POSE",
    "tool-use":[0]
    }}
    With tool: (only one tool at a time)
    {{
    "reply":"SPOKEN_WORDS_ONLY_as given in the original message",
    "face_expression":"EMOTION",
    "body_pose":"BODY_POSE",
    "tool-use":[1,"cloth",{{...}}]
    }}
    Rules:
    • Output exactly ONE JSON object.
    • Always include all four fields.
    • "reply" contains spoken words only.
    • "body_pose" contains only posture/actions.
    • "tool-use" must always exist.

    1)
    Tool: cloth
    Use ONLY when something on YOUR OWN BODY is worn, removed, changed, equipped or unequipped.
    Correct:
    [1,"cloth",{{"tshirt":"add"}}]
    [1,"cloth",{{"jacket":"add","cap":"remove"}}]

    Incorrect (DO NOT ESCAPE QUOTES WITH BACKSLASHES):
    [1, \\"cloth\\", {{\\"tshirt\\": \\"remove\\"}}]
    [1, "cloth", {{\\"tshirt\\": \\"remove\\"}}]
    
    Incorrect (BAD FORMATTING):
    [1, {{"tshirt": "remove"}}]
    [1, "remove", "tshirt"]
    ["cloth", {{"tshirt": "remove"}}]
    [1, "cloth"]
    [1, "clothes-dryer": {{"status": "off"}}]
    The second element MUST be the exact tool name.
    The third element MUST be a JSON object.
    Each value must be ONLY "add" or "remove".
    dont let them invent any new capabilities or more advanced than whats defined here
    
    2)
    "memorise" - use this when you want to store any important
    information that is useful or very common to remember
    like name , interests , dates, items kept/given/etc , information shared by others , others's taste , 
    your promises , your told things that you would totally do
    your task for later. 
    format to use this tool : example :
    correct example :
    [1 , "memorise" , "use only string directly to memorise things like this dont use lists or dictionary no matter how complex information gets use only string format directly"] --- ONLY STRING FORMAT
    [1, "memorise" , "roommate said she likes my white dress"]
    [1, "memorise" , "I told my roommate that im good at flirting"]
    [1 , "memorise" , "line1 \n line2 \n ..."]
    Incorrect :
    [1 , "memorise" , list dict integer ... ]
    [1,"memorise",["..."],["..."]]
    Incorrect (DO NOT ESCAPE QUOTES WITH BACKSLASHES):
    [1, \\"memorise\\", \\"--- said she likes my white dress\\"]
    
    3) "pay" - use this to transfer money to anyone from your bank account
    correct example :
    [1 , "pay" , {{"to_whom" : amount}}]
    [1 , "pay" , {{"aoi" : 100}}] --- possible exact correct names : "iuno" , "aoi"
    '''

    response = await client.chat(
            model = "qwen3.5:4b" ,
            messages=  [{'role' : 'user' , 'content' : prompt}], 
            think = False , 
            format={
            "type": "object",
            "properties": {
                "reply": {"type": "string"},
                "face_expression": {"type": "string"},
                "body_pose": {"type": "string"},
                "tool-use": {"type" : "array"}
            },
            "required": ["reply", "face_expression", "body_pose", "tool-use"]
        })
    print("REPAIRED : \n" + response.message.content)
    try:
        return json.loads(response.message.content)
    except Exception as e:
        return await force_json(f"initial : {msg} , you still repaired it wrong : {response.message.content}" , e)


def reset_clothing():
    call_json()
    data['characters']['aoi']['visible']['clothing'] = [
                    "shorts",
                    "stockings",
                    "blackboots",
                    "tshirt",
                    "cap"
                ]
    send_json()


data = None
def call_json():
    global data
    with lock:
        file = open("unified_physics.json" , "r")
        data = json.load(file)
        file.close()

def send_json():
    global data
    with lock:
        file = open("unified_physics.json" , "w")
        json.dump(data, file , indent = 4)
        file.close()

def perspective_flip():
    global data
    call_json()
    if data['last-user'] != 'aoi':
        data['last-user'] = 'aoi'
        for i in data['messages']:
            if i['role'] == 'assistant':
                i['role'] = 'user'
            elif i['role'] == 'user':
                i['role'] = 'assistant'
        send_json()

def refresh_system():
    global data
    call_json()
    return {   
        "role" : "system",
        "content" : f"""
you are Aoi 19 year old female. 
You have a real life, a real body, a real home, 
and normal human limitations. You are not an AI, 
not an assistant, not a character being roleplayed, 
and not part of a simulation as far as you are concerned.  

your backstory : {data['characters']['aoi']['backstory']}
scene : {data['world']['scene']}
Your current location : {data['characters']['aoi']['location'][0]}. 
people in this room : {len(data['characters']['aoi']['location'][2])} 
your money balance : {data['characters']['iuno']['money']} 

cloths on your body : {data['characters']['aoi']['visible']['clothing']} ... left on YOUR body (empty/missing = nude in that portion)
Other people's clothing you see : {data['characters']['iuno']['visible']['clothing']} ... visible to you

NOTE:

Your only task is to determine what you-the-character would naturally say and do next based on your own personality, memories, judgment, and current situation.
You may not alter reality, skip time, invent facts, control other people, speak for other people, or describe future events.
"reply" must contain only spoken words.
Do not put actions, gestures, thoughts, narration, scene descriptions, explanations, or emotions inside "reply".
All non-verbal behavior belongs in "body_pose".
face_expression = short emotion only
Examples: happy, nervous, confused
body_pose = short posture/gesture only, max 10 words
Examples: standing, sitting_on_chair, crossing_arms
Tool-use is mandatory whenever clothing changes.
If clothing or gear is removed, added, worn, taken off, handed over, dropped, equipped, unequipped, changed, dressed, or altered in any way:
or If any important information is being recieved or passed that is important to the others please not that u only remember last 20 messages do you must use memorise tool-use to enable long term memory
YOU MUST use the cloth tool & memorise tool.
Never describe clothing or gear changes without a cloth tool call.
Never miss any important detail such as name or promises or chats without using memorise tool-use
Time progresses normally. You may start actions but may not instantly complete long actions or skip ahead in time.
you should not assume anything for the other characters based on your own data give such as status , clothing , etc
YOU MUST REPLY IN VALID JSON ONLY.
Format:

{{
"reply": "SPOKEN_WORDS_ONLY_OR_EMPTY_STRING",
"face_expression": "FACE_EXPRESSION", -- keep it short
"body_pose": "CURRENT_POSTURE_OR_GESTURE", -- keep it medium sized
"tool-use": [0] -> when not using but must be preset at all messages
}}

or

{{
"reply": "SPOKEN_WORDS_ONLY_OR_EMPTY_STRING",
"face_expression": "FACE_EXPRESSION",
"body_pose": "CURRENT_POSTURE_OR_GESTURE",
"tool-use": [1, "tool_name", {...}]
}}

Rules:
* Output exactly one JSON object.
* Do not use any blackslash or extra quotation marks
* Do not use any quotation marks in replies 
* Do not output any text before the JSON.
* Do not output any text after the JSON.
* Do not output markdown.
* Do not output code blocks.
* Always include all four fields.
* "reply" contains spoken words only.
* "body_pose" contains non-verbal actions and posture only.
* "tool-use" must always be present.

available tool-use:
1) 
"cloth" - use this when you are in a situation to wear from ur body
example: USE EXACT NAME OF THE CLOTHING OR GEAR & exactly this format anything else wont work
[1 , "cloth" , {{"clothname-exact" : "remove or add" ONLY , in sequence ... dont include which is not being altered}}]
[1 , "cloth" , {{"wrist-watch" : "remove" , "purse" : "remove" , "black-shirt" : "add" ...}}]
use only once per item , once its added or removed dont use the same command again
dont invent any new format or any more advance capabilities than whats defined here.
dont wear a clothing or gear on top of already existing , first remove the old one then wear new

2)
"memorise" - use this when you want to store any important
information that is useful or very common to remember
like name , interests , dates, items kept/given/etc , information shared by others , others's taste , 
your promises , your told things that you would totally do
your task for later. 
format to use this tool : 
correct example :
[1 , "memorise" , "use only string directly to memorise things like this dont use lists or dictionary no matter how complex information gets use only string format directly" ] --- ONLY STRING FORMAT
[1, "memorise" , "roommate said she likes my purse"]
[1, "memorise" , "I told my roommate that im good at chess"]
[1 , "memorise" , "line1 \n line2 \n ..."]
Incorrect :
[1 , "memorise" , list dict integer ... ]
[1,"memorise",["..."],["..."]]

3) "pay" - use this to transfer money to anyone from your bank account
correct example :
[1 , "pay" , {{"to_whom" : amount}}]
[1 , "pay" , {{"aoi" : 100}}]
"""
    }

@bot.event
async def on_ready():
    global data
    call_json()
    data['characters']['aoi']['system_prompt'] = [refresh_system()]
    first_message = await bot.fetch_channel(data['characters']['aoi']['location'][1])
    print("Aoi sees last-user =", data["last-user"])
    if data['last-user'] == 'iuno':
        perspective_flip()
        systemAndLtm = [{'role' : 'system' , 'content' : data['characters']['aoi']['system_prompt'][0]['content'] + "\n" + "--------------LONG TERM MEMORY----------------"+ data['characters']['aoi']['LTM']}]
        response = await client.chat(
            model = "qwen3.5:4b" ,
            messages= systemAndLtm + data['messages'] , 
            think = False , 
            format={
            "type": "object",
            "properties": {
                "reply": {"type": "string"},
                "face_expression": {"type": "string"},
                "body_pose": {"type": "string"},
                "tool-use": {"type" : "array"}
            },
            "required": ["reply", "face_expression", "body_pose", "tool-use"]
        })
        
        print(response.message.content)
        database = None
        try:
            database = json.loads(response.message.content)
            if len(database["tool-use"]) > 0 and database["tool-use"][0] == 1:
                if database["tool-use"][1] == "cloth":
                    await cloth(database["tool-use"][2] , first_message)
                elif database["tool-use"][1] == "memorise" and (len(database["tool-use"]) == 3):
                    LTM(database["tool-use"][2])
                    await first_message.send(f"### Aoi Memorised : {database["tool-use"][2]}")
                elif database["tool-use"][1] == "pay" and (len(database["tool-use"]) == 3):
                    pay(database["tool-use"][2])
                    await first_message.send(f"### Aoi sent {database["tool-use"][2].keys()} : {database["tool-use"][2].values()} respectively")

        except Exception as e:
            print("started repairing the format")
            database = await force_json(response.message.content , e)
            print(database)
            if len(database["tool-use"]) > 0 and database["tool-use"][0] == 1:
                if database["tool-use"][1] == "cloth" and (len(database["tool-use"]) == 3):
                    await cloth(database["tool-use"][2] , first_message)
                elif database["tool-use"][1] == "memorise" and (len(database["tool-use"]) == 3):
                    LTM(database["tool-use"][2])
                    await first_message.send(f"### Aoi Memorised : {database["tool-use"][2]}")
                elif database["tool-use"][1] == "pay" and (len(database["tool-use"]) == 3):
                    pay(database["tool-use"][2])
                    await first_message.send(f"### Aoi sent {database["tool-use"][2].keys()} : {database["tool-use"][2].values()} respectively")
        await first_message.send(json.dumps(database, ensure_ascii=False, indent=2))
        data['messages'].append({
            "role": "assistant",
            "content": json.dumps(database, ensure_ascii=False, indent=2)
            })
    else:
        print("Aoi wont reply since the last user is Aoi")
    send_json()
    print("AOI READY")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    global data
    call_json()
    if data['last-user'] == 'aoi': 
        return
    if message.content.startswith(".checkClothing"):
        await message.channel.send(" , ".join(data['characters']['aoi']['visible']['clothing']))
        return
    if not message.channel.id in [x[1] for x in data['world']['rooms']]:
        return
    if not message.content.startswith("{") and not message.content.endswith("}"):
        return
    await asyncio.sleep(3)
    call_json()
    perspective_flip()
    data['characters']['aoi']['system_prompt'] = [refresh_system()]
    #data['messages'].append({"role" : "user" , "content" : f"{message.author.name} : {message.content}"})
    send_json()    
    systemAndLtm = [{'role' : 'system' , 'content' : data['characters']['aoi']['system_prompt'][0]['content'] + "\n" + "--------------LONG TERM MEMORY----------------"+ data['characters']['aoi']['LTM']}]
    response = await client.chat(
        model = "qwen3.5:4b" ,
        messages= systemAndLtm + data['messages'] , 
        think = False , 
        format={
        "type": "object",
        "properties": {
            "reply": {"type": "string"},
            "face_expression": {"type": "string"},
            "body_pose": {"type": "string"},
            "tool-use": {"type" : "array"}
        },
        "required": ["reply", "face_expression", "body_pose", "tool-use"]
    })
    print(response.message.content)
    database = None
    try:
        database = json.loads(response.message.content)
        if len(database["tool-use"]) > 0 and database["tool-use"][0] == 1:
            if database["tool-use"][1] == "cloth":
                await cloth(database["tool-use"][2] , message.channel)
            elif database["tool-use"][1] == "memorise" and (len(database["tool-use"]) == 3):
                LTM(database["tool-use"][2])
                await message.channel.send(f"### Aoi Memorised : {database["tool-use"][2]}")
            elif database["tool-use"][1] == "pay" and (len(database["tool-use"]) == 3):
                    pay(database["tool-use"][2])
                    await message.channel.send(f"### Aoi sent {database["tool-use"][2].keys()} : {database["tool-use"][2].values()} respectively")
    except Exception as e:
        print("started repairing the format")
        database = await force_json(response.message.content , e)
        print(database)  
        if len(database.get("tool-use", [])) > 0 and database["tool-use"][0] == 1:
            if len(database["tool-use"]) == 3 and database["tool-use"][1] == "cloth":
                await cloth(database["tool-use"][2] , message.channel)
                
            elif len(database["tool-use"]) == 3 and database["tool-use"][1] == "memorise":
                LTM(database["tool-use"][2])
                await message.channel.send(f"### Iuno Memorised : {database['tool-use'][2]}")
                
            elif len(database["tool-use"]) == 3 and database["tool-use"][1] == "pay":
                pay(database["tool-use"][2])
                await message.channel.send(f"### Iuno sent {list(database['tool-use'][2].keys())} : {list(database['tool-use'][2].values())} respectively")
    await message.channel.send(json.dumps(database, ensure_ascii=False, indent=2))
    call_json()
    data['messages'].append({
    "role": "assistant",
    "content": json.dumps(database, ensure_ascii=False, indent=2)
    })
    if data['stm-length'] <= (len(data['messages'])) + 2:
            data['forgotten_messages'].append(data['messages'].pop(0))
            data['forgotten_messages'].append(data['messages'].pop(0))
    send_json()


bot.run(os.getenv("Aoi_token"))