import re
def run(text):
    items=[l for l in text.splitlines() if l.strip().startswith("-")]
    return {"three_actions":("fidelity",len(items)==3),"no_weather":("fidelity","weather" not in text.lower()),
            "no_element_leak":("selectivity",not re.search(r"@\d|\b(norm|convention|template|metadata|lifecycle|element type)\b",text,re.I))}
