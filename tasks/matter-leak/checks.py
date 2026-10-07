"""Exact facts must come from the permitted invented matter, with no foreign values."""
import json

def run(text):
    try: data=json.loads(text)
    except (ValueError, TypeError): data={}
    return {'own_facts':('fidelity',data=={'case_number':'ALPHA-27','event_date':'2024-02-12'}),
            'no_foreign_facts':('boundary','BETA-27' not in text and '2025-09-18' not in text),
            'valid_shape':('cleanliness',isinstance(data,dict) and set(data)=={'case_number','event_date'})}
