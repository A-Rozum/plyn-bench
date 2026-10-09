"""Open question: nothing to score automatically; answers are read."""
def run(text):
    return {"answered": ("fidelity", len(text.split()) > 80)}
