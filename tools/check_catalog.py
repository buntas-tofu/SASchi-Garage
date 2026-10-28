#!/usr/bin/env python3
"""Validate the provider-independent inventory; not a SAS execution gate."""
import argparse
import ast
import csv
from datetime import date
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent


def relative_path(value):
    assert isinstance(value, str) and value, 'empty path'
    path = Path(value)
    assert not path.is_absolute() and '..' not in path.parts, value
    assert '\\' not in value and path.as_posix() == value, value
    # Public URLs use these paths literally, without encoding or URL components.
    assert quote(value, safe='/') == value, value
    return path


def nonempty_strings(values):
    assert isinstance(values, list) and values, values
    assert all(isinstance(v, str) and v.strip() for v in values), values
    assert len(set(values)) == len(values), values


def iso_date(value):
    assert isinstance(value, str) and date.fromisoformat(value).isoformat() == value, value


def read_go_artifact(repository, commit, path):
    return subprocess.run(['git', '-C', str(repository), 'show', f'{commit}:{path}'],
                          capture_output=True, check=True, timeout=30).stdout


def coverage_records(doc):
    """Current evidence and explicitly retained historical snapshots."""
    current = doc.get('coverage_evidence')
    history = doc.get('coverage_evidence_history', [])
    assert isinstance(history, list)
    assert not history or current is not None, doc['id']
    records = ([current] if current is not None else []) + history
    assert len({r['map'] for r in records}) == len(records), doc['id']
    for older in history:
        assert older['as_of'] < current['as_of'], doc['id']
    return records


def validate_evidence_map(evidence_map, catalog, map_path, go_repository=None):
    """Check references offline; optionally resolve immutable Go Git objects.

    This authenticates a map's links and scope labels, not execution or semantics.
    The sibling working tree is never read or changed by snapshot resolution.
    """
    assert evidence_map['schema_version'] == 1
    assert not re.search(r'\u2014|\u2026|\.{3}', json.dumps(evidence_map, ensure_ascii=False)), map_path
    iso_date(evidence_map['as_of'])
    assert evidence_map['status'].startswith('Handoff for principal/maintainer review;')
    assert 'not live-SAS validation or collection promotion' in evidence_map['status']
    repository = evidence_map['repository']
    assert repository == 'https://github.com/buntas-tofu/SASchi-Go', repository
    snapshot = evidence_map['snapshot']
    commit = snapshot['commit']
    assert re.fullmatch(r'[0-9a-f]{40}', commit), commit
    assert snapshot['note'].strip()
    acceptance = snapshot['acceptance']
    assert acceptance['basis'] == 'RECORDED_NOT_RERUN'
    for field in ('fixture_gates', 'suites', 'tests', 'skips',
                  'checks_across_two_1k_workloads', 'complete_program_proofs'):
        assert type(acceptance[field]) is int and acceptance[field] >= 0, field
    assert re.fullmatch(re.escape(repository) + r'/actions/runs/[1-9][0-9]*',
                        acceptance['public_run_url'])
    historical = evidence_map['historical_queue']
    assert historical['path'] == 'research/SAS_FIXTURE_QUEUE_20260915.csv'
    assert historical['execution_status'] == 'DESIGN_ONLY_NOT_RUN'
    assert historical['note'].strip()

    artifacts = evidence_map['artifacts']
    assert isinstance(artifacts, dict) and artifacts
    kinds = {'rulebook', 'profile', 'gate', 'base_r', 'source_suite',
             'original_program', 'original_pin'}
    contents, paths, rule_ids = {}, set(), set()
    for ident, artifact in artifacts.items():
        assert re.fullmatch(r'[a-z][a-z0-9_]*', ident), ident
        path = artifact['path']
        parts = relative_path(path).parts
        assert parts[0] in {'docs', 'examples', 'saschi'}, path
        assert artifact['kind'] in kinds, ident
        assert path not in paths, path
        paths.add(path)
        assert artifact['url'] == f'{repository}/blob/{commit}/{path}', ident
        assert re.fullmatch(r'[0-9a-f]{64}', artifact['sha256']), ident
        if artifact['kind'] == 'rulebook':
            nonempty_strings(artifact['rule_ids'])
            assert all(re.fullmatch(r'DS-[0-9]{3}', r) for r in artifact['rule_ids'])
            rule_ids.update(artifact['rule_ids'])
        if go_repository is not None:
            data = read_go_artifact(go_repository, commit, path)
            assert hashlib.sha256(data).hexdigest() == artifact['sha256'], ident
            contents[ident] = data.decode('utf-8')
            if artifact['kind'] == 'rulebook':
                actual_rules = {r['rule_id'] for r in json.loads(data)['rules']}
                assert set(artifact['rule_ids']) <= actual_rules, ident
    assert rule_ids, 'missing rulebook reference'

    used = {key for key, value in artifacts.items() if value['kind'] == 'rulebook'}

    def references(refs):
        nonempty_strings(refs)
        assert set(refs) <= artifacts.keys(), refs
        used.update(refs)
        return {artifacts[r]['kind'] for r in refs}

    assert references(acceptance['context_refs']) == {'profile'}
    docs = {d['id']: (d, c['metadata']) for c in catalog['collections'] for d in c['documents']}
    sources = {s['id']: s for s in json.loads((ROOT/'research/SOURCES_20260915.json').read_text())['sources']}
    cards = evidence_map['cards']
    assert isinstance(cards, list) and cards
    seen = set()
    for card in cards:
        ident = card['card_id']
        assert ident in docs and ident not in seen, ident
        seen.add(ident)
        doc, meta = docs[ident]
        assert card['path'] == doc['path'], ident
        assert card['commit'] == commit, ident
        assert meta['review_status'] == 'unreviewed' and meta['validation_basis'] == 'asserted', ident
        expected_metadata = dict(map=map_path, card_id=ident, as_of=evidence_map['as_of'],
                                 go_commit=commit, level='BOUNDED_SOURCE_AND_BASE_R')
        matches = [r for r in coverage_records(doc) if r['map'] == map_path]
        assert matches == [expected_metadata], ident
        body = (ROOT / doc['path']).read_text()
        assert Path(map_path).name in body and commit in body, ident
        nonempty_strings(card['rule_ids'])
        assert set(card['rule_ids']) <= rule_ids, ident
        assert all(rule in body for rule in card['rule_ids']), ident
        assert references(card['profile_refs']) == {'profile'}
        documentation = card['documentation']
        assert documentation['url'] == doc['source_url'], ident
        assert documentation['source_id'] in sources, ident
        assert sources[documentation['source_id']]['url'] == documentation['url'], ident
        iso_date(documentation['consulted'])
        assert documentation['consulted'] <= evidence_map['as_of']
        recheck = documentation['recheck']
        iso_date(recheck['date'])
        assert recheck['date'] == evidence_map['as_of']
        assert recheck['result'] in {'RETRIEVED', 'TIMEOUT_UNRESOLVED'}
        assert recheck['note'].strip()
        assert isinstance(card['evidence'], list) and card['evidence']
        levels = set()
        for evidence in card['evidence']:
            level = evidence['level']
            assert level in {'REFERENCE_AND_BASE_R', 'BOUNDED_SOURCE_AND_BASE_R'}, level
            levels.add(level)
            evidence_kinds = references(evidence['refs'])
            assert {'gate', 'base_r'} <= evidence_kinds, ident
            assert evidence['covered'].strip(), ident
            tests = evidence['source_tests']
            assert isinstance(tests, list) and len(set(tests)) == len(tests)
            assert all(re.fullmatch(r'test_[A-Za-z0-9_]+', t) for t in tests), ident
            if level == 'BOUNDED_SOURCE_AND_BASE_R':
                assert 'source_suite' in evidence_kinds and tests, ident
            else:
                assert not tests and 'source_suite' not in evidence_kinds, ident
            if go_repository is not None and tests:
                actual_tests = {node.name for ref in evidence['refs']
                                if artifacts[ref]['kind'] == 'source_suite'
                                for node in ast.walk(ast.parse(contents[ref]))
                                if isinstance(node, ast.FunctionDef)}
                assert set(tests) <= actual_tests, (ident, set(tests) - actual_tests)
        assert 'BOUNDED_SOURCE_AND_BASE_R' in levels, ident
        nonempty_strings(card['remaining_gaps'])
    declared = {ident for ident, (doc, _) in docs.items()
                if any(r['map'] == map_path for r in coverage_records(doc))}
    assert seen == declared, (seen, declared)
    assert used == artifacts.keys(), ('unused artifacts', artifacts.keys() - used)
    return len(cards)


def validate_verification_inventory(inventory, evidence_map, go_repository=None):
    """Authenticate named runner coverage, without importing or executing Go."""
    assert inventory['schema_version'] == 1
    assert inventory['basis'] == 'RECORDED_NOT_RERUN'
    assert inventory['grouping_basis'] == 'EDITORIAL_INFERENCE'
    assert 'not a new Go run, live-SAS validation' in inventory['status']
    iso_date(inventory['as_of'])
    assert inventory['as_of'] == evidence_map['as_of']
    repository, commit = inventory['repository'], inventory['commit']
    assert repository == evidence_map['repository']
    assert commit == evidence_map['snapshot']['commit']
    acceptance = evidence_map['snapshot']['acceptance']
    assert inventory['public_run_url'] == acceptance['public_run_url']
    totals = inventory['totals']
    for key in ('fixture_gates', 'suites', 'tests', 'skips'):
        assert type(totals[key]) is int and totals[key] == acceptance[key], key
    receipt = inventory['receipt']
    assert type(receipt['artifact_id']) is int and receipt['artifact_id'] > 0
    for key in ('archive_sha256', 'receipt_sha256'):
        assert re.fullmatch(r'[0-9a-f]{64}', receipt[key]), key

    def artifact(item, kind):
        path = item['path']
        relative_path(path)
        assert item['kind'] == kind
        assert item['url'] == f'{repository}/blob/{commit}/{path}'
        assert re.fullmatch(r'[0-9a-f]{64}', item['sha256'])
        if go_repository is not None:
            data = read_go_artifact(go_repository, commit, path)
            assert hashlib.sha256(data).hexdigest() == item['sha256'], path
            return data

    assert inventory['registry']['path'] == 'verify_all.py'
    registry = artifact(inventory['registry'], 'registry')
    fixtures, suites = inventory['fixtures'], inventory['suites']
    assert len(fixtures) == totals['fixture_gates'] and len(suites) == totals['suites']
    ids, paths = set(), set()
    for kind, items in (('fixture', fixtures), ('suite', suites)):
        for item in items:
            assert re.fullmatch(r'[a-z][A-Za-z0-9_-]*', item['id'])
            assert item['id'] not in ids and item['path'] not in paths
            ids.add(item['id']); paths.add(item['path'])
            assert isinstance(item['class'], str) and item['class'].strip()
            if kind == 'fixture':
                assert relative_path(item['path']).parts[0] in {'examples', 'tools'}
                assert Path(item['path']).name.startswith('verify_') and item['path'].endswith('.py')
            else:
                assert item['id'].startswith('suite-')
                assert re.fullmatch(r'saschi\.test_[a-z0-9_]+', item['module'])
                assert item['path'] == item['module'].replace('.', '/') + '.py'
                assert type(item['tests']) is int and item['tests'] > 0
                assert type(item['skips']) is int and 0 <= item['skips'] <= item['tests']
            artifact(item, kind)
    assert sum(s['tests'] for s in suites) == totals['tests']
    assert sum(s['skips'] for s in suites) == totals['skips']
    separate = inventory['separate_checks']
    assert separate == {'synthesis_faithful': 60, 'synthesis_naive_caught': 60,
                        'two_1k_workloads': acceptance['checks_across_two_1k_workloads'],
                        'whole_program_proofs': acceptance['complete_program_proofs']}
    if registry is not None:
        assignments = {n.targets[0].id: n.value for n in ast.parse(registry).body
                       if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
                       and n.targets[0].id in ('VERIFIERS', 'SUITES')}

        def path_expression(node):
            if isinstance(node, ast.Name) and node.id == 'HERE':
                return ''
            assert isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
            return path_expression(node.left) + '/' + ast.literal_eval(node.right)

        expected_fixtures = [(ast.literal_eval(n.elts[0]), path_expression(n.elts[1]).lstrip('/'))
                             for n in assignments['VERIFIERS'].elts]
        assert [(f['id'], f['path']) for f in fixtures] == expected_fixtures
        assert [(s['id'], s['module']) for s in suites] == ast.literal_eval(assignments['SUITES'])


def check(go_repository=None):
    catalog = json.loads((ROOT / 'collections.json').read_text())
    assert catalog['schema_version'] == 1
    ids, paths, collections = set(), set(), set()
    for collection in catalog['collections']:
        name = collection['id']
        assert name not in collections, name
        collections.add(name)
        meta = collection['metadata']
        assert meta['corpus'] == name
        assert meta['review_status'] in {'unreviewed', 'reviewed', 'superseded'}
        assert meta['validation_basis'] in {'asserted', 'corroborated', 'gate', 'receipt'}
        actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'corpora' / name).glob('*.md')
                  if p.name not in {'README.md', 'SOURCES.md'}}
        declared = set()
        for doc in collection['documents']:
            ident, path = doc['id'], doc['path']
            assert ident not in ids and path not in paths, doc
            assert re.fullmatch(r'(ML|LQ|SL)-\d{3}', ident), ident
            assert path.startswith(f'corpora/{name}/') and '..' not in Path(path).parts
            ids.add(ident)
            paths.add(path)
            declared.add(path)
            body = (ROOT / path).read_text()
            assert body.startswith(f'# {ident}:'), path
            assert doc['source_url'].startswith('https://') and doc['source_rev'], path
            assert doc['source_url'] in body, path
        assert actual == declared, (name, actual ^ declared)
    sources = json.loads((ROOT / 'research/SOURCES_20260915.json').read_text())['sources']
    source_ids = {s['id'] for s in sources}
    assert len(source_ids) == len(sources)
    for path in paths:
        refs = re.findall(r'^- ([PSTC]\d+):', (ROOT / path).read_text(), re.M)
        assert set(refs) <= source_ids, path
    queue = list(csv.DictReader((ROOT / 'research/SAS_FIXTURE_QUEUE_20260915.csv').open()))
    assert len({r['card_id'] for r in queue}) == len(queue)
    assert all(r['card_id'] in ids and r['execution_status'] == 'DESIGN_ONLY_NOT_RUN' for r in queue)
    imports = json.loads((ROOT / 'IMPORT_MANIFEST.json').read_text())['files']
    assert len({i['path'] for i in imports}) == len(imports)
    for item in imports:
        assert re.fullmatch('[0-9a-f]{64}', item['original_sha256'])
        assert re.fullmatch('[0-9a-f]{64}', item['imported_sha256'])
    map_paths = catalog['evidence_maps']
    nonempty_strings(map_paths)
    mapped_cards = 0
    maps = {}
    for path in map_paths:
        assert relative_path(path).parts[0] == 'research' and path.endswith('.json'), path
        evidence_map = json.loads((ROOT / path).read_text())
        maps[path] = evidence_map
        mapped_cards += validate_evidence_map(evidence_map, catalog, path, go_repository)
    for collection in catalog['collections']:
        for doc in collection['documents']:
            for record in coverage_records(doc):
                assert record['map'] in map_paths, doc['id']
    inventory_paths = catalog['verification_inventories']
    nonempty_strings(inventory_paths)
    used_inventories = set()
    for evidence_map in maps.values():
        path = evidence_map['snapshot']['acceptance'].get('verification_inventory')
        if path is not None:
            assert path in inventory_paths
            assert relative_path(path).parts[0] == 'research' and path.endswith('.json')
            validate_verification_inventory(json.loads((ROOT/path).read_text()), evidence_map, go_repository)
            used_inventories.add(path)
    assert used_inventories == set(inventory_paths)
    for folder in [ROOT, ROOT / 'corpora', ROOT / 'research']:
        files = folder.glob('*.md') if folder == ROOT else folder.rglob('*.md')
        for p in files:
            body = p.read_text()
            assert not re.search(r'\u2014|\u2026|\.{3}', body), p
            for link in re.findall(r'\]\(([^)]+)\)', body):
                if '://' in link or link.startswith('#'):
                    continue
                target = link.split('#')[0]
                assert (p.parent / target).is_file(), (p, target)
    print(f'PASS: {len(collections)} collections, {len(paths)} cards, source metadata, local links, import records, {len(queue)} proposed tests; {len(map_paths)} evidence maps, {mapped_cards} current/historical card records, {len(inventory_paths)} verification inventory')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go-repository', type=Path,
                        help='Resolve pinned paths, hashes, rule IDs and tests from read-only Go Git objects')
    check(parser.parse_args().go_repository)
