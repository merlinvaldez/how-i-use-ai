"""Render sourced vendor cards; submit selection through a host follow-up only."""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import urlsplit


def render(manifest_path, output_path):
    manifest_path, output_path = Path(manifest_path).resolve(), Path(output_path).resolve()
    if manifest_path == output_path:
        raise ValueError('Output must not overwrite the manifest')
    data = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    run_id = data.get('run_id')
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError('run_id must be a nonempty string')
    prospects = data.get('prospects')
    if not isinstance(prospects, list):
        raise ValueError('prospects must be a list')
    ids = [p.get('id') for p in prospects]
    if any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('Prospect IDs must be unique nonempty strings')
    for p in prospects:
        for key in ('company', 'contract', 'agency', 'activity', 'activity_basis'):
            if not isinstance(p.get(key), str) or not p[key].strip():
                raise ValueError(f"{p['id']}: missing {key}")
        for source in p.get('sources', []):
            parsed = urlsplit(source['url'])
            if parsed.scheme not in ('https', 'http') or not parsed.netloc:
                raise ValueError(f"{p['id']}: source must be an HTTP(S) URL")
        detail = p.get('selection_detail', {})
        p.setdefault('documented_services', detail.get('scope') or 'Published services not verified.')
        p.setdefault('awarded_scope', p['contract'] + '. Individual components not verified.')
        p.setdefault('opportunity', detail.get('offer') or 'Service fit not assessed; verify scope before proposing work.')
        p.setdefault('selection_note', detail.get('paid') or p.get('gaps') or 'Paid subcontract availability not verified.')
        p.setdefault('sources', [])
    template = (Path(__file__).resolve().parent.parent/'assets/selector-cards.html').read_text(encoding='utf-8')
    template = template.replace('ROOT_ID', 'primes-' + run_id.encode().hex())
    template = template.replace('REPORT_TITLE', html.escape(data.get('title', 'Awarded vendors & subcontracting opportunities')))
    subtitle = data.get('subtitle') or f"{data.get('seed', '')} | Checked {data.get('checked_at', 'unknown')}"
    template = template.replace('REPORT_SUBTITLE', html.escape(subtitle))
    # Insert arbitrary evidence last so its text cannot modify template placeholders.
    payload = json.dumps(data, ensure_ascii=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    template = template.replace('MANIFEST_PATH', json.dumps(str(manifest_path))).replace('MANIFEST_DATA', payload)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template, encoding='utf-8')
    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest')
    parser.add_argument('output')
    args = parser.parse_args()
    print(render(args.manifest, args.output))
