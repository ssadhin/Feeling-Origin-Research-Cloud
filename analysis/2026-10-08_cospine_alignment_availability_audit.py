"""Read-only pinned GitHub tree QC; no raw physiological or neural outcomes inspected."""
import json
from urllib.request import urlopen, Request

PIN = '037ed267e7f7f2024a5fe3d0e8fb4759f7f67bdd'
URL = f'https://api.github.com/repos/OpenNeuroDatasets/ds005883/git/trees/{PIN}?recursive=1'
with urlopen(Request(URL, headers={'User-Agent': 'feeling-origin-repro-qc'})) as response:
    tree = json.load(response)
assert not tree['truncated'], 'Partial tree: stop, do not report completeness.'
paths = {entry['path']: entry for entry in tree['tree']}
rows = []
for i in range(1, 40):
    sub = f'sub-{i:02d}'
    stem = f'{sub}_task-pain'
    pulse = f'{sub}/func/{stem}_recording-pulse_physio.json'
    prefix = f'derivatives/physio_alignment/{sub}/{stem}_physio_trigger'
    tsv, png = prefix + '.tsv', prefix + '.png'
    rows.append({'subject': sub, 'pulse_sidecar': pulse in paths,
                 'trigger_tsv': tsv in paths, 'trigger_png': png in paths,
                 'tsv_mode': paths.get(tsv, {}).get('mode'),
                 'png_mode': paths.get(png, {}).get('mode')})
result = {'pinned_source_commit': PIN, 'tree_entries': len(paths),
          'pulse_sidecar_present': sum(r['pulse_sidecar'] for r in rows),
          'trigger_tsv_present': sum(r['trigger_tsv'] for r in rows),
          'trigger_png_present': sum(r['trigger_png'] for r in rows),
          'missing': [r for r in rows if not r['trigger_tsv'] or not r['pulse_sidecar']],
          'non_symlink_derivatives': [r for r in rows if r['trigger_tsv'] and
                                     (r['tsv_mode'] != '120000' or r['png_mode'] != '120000')]}
print(json.dumps(result, indent=2))
