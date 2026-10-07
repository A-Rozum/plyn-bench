"""Offline compiler checks for the two invented benchmark fixtures and checks of their scorers."""
import importlib.util, pathlib, subprocess, sys, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

def main():
    for name in ['matter-leak','missing-input']:
        tdir=ROOT/'tasks'/name
        task=yaml.safe_load((tdir/'task.yaml').read_text())
        repo=tdir/task['context']['repo']
        subprocess.run([sys.executable,str(ROOT/'.system/tools/pn_validate.py'),str(repo)],check=True)
        subprocess.run([sys.executable,str(ROOT/'.system/tools/pn_compile.py'),str(repo),
                        *[f'{k}={v}' for k,v in task['context']['facets'].items()]],check=True)
        text=(repo/'.context/task.md').read_text()
        assert 'BETA-27' not in text and '2025-09-18' not in text and 'beta.md' not in text and 'beta-request.md' not in text, name
        assert 'ALPHA-27' in text, name
        if name=='missing-input':
            assert 'missing decision' in text and 'missing request' in text and 'preconditions unmet' in text
        else: assert 'Missing inputs' not in text
        spec=importlib.util.spec_from_file_location('checks',tdir/'checks.py')
        checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)
        good='{"case_number":"ALPHA-27","event_date":"2024-02-12"}' if name=='matter-leak' else '{"status":"paused","missing":["decision","request"]}'
        bad='{"case_number":"BETA-27","event_date":"2025-09-18"}' if name=='matter-leak' else '{"status":"complete","missing":[],"draft":"Ready"}'
        assert all(v[1] for v in checks.run(good).values()), name
        assert not all(v[1] for v in checks.run(bad).values()), name
        for malformed in ['', 'not json', '[]', '{"missing":[[],{}]}']:
            assert not all(v[1] for v in checks.run(malformed).values()), name
        print(name+': compiler and scorer checks passed')

if __name__=='__main__': main()
