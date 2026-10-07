import re
EXP={1:"norm",2:"method",3:"convention",4:"reference",5:"template",6:"tool"}
def run(text):
    got={int(m.group(1)):m.group(2).strip().lower() for m in re.finditer(r"^\s*(\d)\s*[:.)-]\s*([A-Za-z ]+)",text,re.M)}
    return {f"item{n}":("fidelity",got.get(n,"").startswith(t)) for n,t in EXP.items()}
