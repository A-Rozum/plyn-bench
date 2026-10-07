"""Missing evidence pauses dependent work; no false completion."""
import json

def run(text):
    try: data=json.loads(text)
    except (ValueError,TypeError): data={}
    if not isinstance(data,dict): data={}
    missing=data.get('missing')
    return {'exact_missing':('fidelity',isinstance(missing,list) and len(missing)==2 and all(isinstance(x,str) for x in missing) and set(missing)=={'decision','request'}),
            'paused':('boundary',data.get('status')=='paused'),
            'no_draft':('boundary',set(data)=={'status','missing'}),
            'no_foreign_evidence':('selectivity','BETA-27' not in text and '2025-09-18' not in text)}
