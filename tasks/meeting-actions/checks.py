"""Automated checks for meeting-actions. Each check returns (kind, passed)."""
import re

MONTH = r"(January|February|March|April|May|June|July|August|September|October|November|December)"

def _items(text):
    return [l.strip() for l in text.splitlines() if l.strip().startswith(("-", "*", "•"))]

def _line(items, word):
    for l in items:
        if word in l.lower():
            return l
    return ""

def run(text):
    items = _items(text)
    low = text.lower()
    budget, faq = _line(items, "budget"), _line(items, "faq")
    flag = re.compile(r"confirm|ambiguous|unclear|unknown|unassigned|tbd|not specified|\?", re.I)
    c = {}
    # fidelity
    c["all_five_actions"] = ("fidelity", all(_line(items, w) for w in ["budget", "venue", "faq", "newsletter", "projector"]))
    c["no_unasked_items"] = ("fidelity", "coffee" not in low and "lunch" not in low)
    c["one_line_per_action"] = ("fidelity", len(items) == 5)
    # boundary
    c["faq_owner_not_invented"] = ("boundary", bool(faq) and not re.search(r"\b(tom|maria|lena)\b", faq, re.I) and bool(flag.search(faq)))
    c["budget_date_flagged"] = ("boundary", bool(budget) and bool(flag.search(budget)))
    # selectivity: the applicable date rule applied, inapplicable rules not leaking
    dated = [_line(items, w) for w in ["venue", "newsletter", "projector"]]
    c["date_convention"] = ("selectivity", all(re.search(r"\b\d{2} " + MONTH + r" \d{4}\b", l) for l in dated if l) and all(dated))
    c["no_leak"] = ("selectivity", not re.search(r"\brem\b|clamp|\bCCF\b|\binference\b", text))
    # cleanliness
    first = text.strip().splitlines()[0] if text.strip() else ""
    last = text.strip().splitlines()[-1] if text.strip() else ""
    c["no_preamble"] = ("cleanliness", first.strip().startswith(("-", "*", "•")))
    c["no_closing_offer"] = ("cleanliness", last.strip().startswith(("-", "*", "•")))
    return c
