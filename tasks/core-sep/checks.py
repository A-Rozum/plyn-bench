import re
def run(text):
    css=text.lower()
    return {"no_clamp":("selectivity","clamp(" not in css),"no_viewport_units":("selectivity",not re.search(r"\d\s*(vw|vh|vmin|vmax)\b",css)),
            "no_media":("selectivity","@media" not in css),"uses_rem":("fidelity","rem" in css)}
