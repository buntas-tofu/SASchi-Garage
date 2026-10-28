"""Evidence-map validation controls, not execution or semantic acceptance."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import check_catalog as checker


class EvidenceMapTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((checker.ROOT/'collections.json').read_text())
        self.path = self.catalog['evidence_maps'][0]
        self.evidence_map = json.loads((checker.ROOT/self.path).read_text())

    def validate(self, data=None, catalog=None, repository=None):
        return checker.validate_evidence_map(
            self.evidence_map if data is None else data,
            self.catalog if catalog is None else catalog, self.path, repository)

    def test_current_map_and_catalog(self):
        self.assertEqual(self.validate(), 5)

    def test_invalid_reference_controls(self):
        mutations = {
            'unknown card': lambda m: m['cards'][0].update(card_id='SL-999'),
            'duplicate card': lambda m: m['cards'].append(deepcopy(m['cards'][0])),
            'missing catalog card': lambda m: m['cards'].pop(),
            'wrong card path': lambda m: m['cards'][0].update(path='README.md'),
            'unknown artifact': lambda m: m['cards'][0]['evidence'][0]['refs'].append('absent'),
            'unknown profile': lambda m: m['cards'][0]['profile_refs'].append('absent'),
            'unknown rule': lambda m: m['cards'][0]['rule_ids'].append('DS-999'),
            'floating commit': lambda m: m['snapshot'].update(commit='main'),
            'wrong card commit': lambda m: m['cards'][0].update(commit='a'*40),
            'floating source URL': lambda m: m['artifacts']['events_gate'].update(
                url=m['artifacts']['events_gate']['url'].replace(m['snapshot']['commit'], 'main')),
            'foreign repository': lambda m: m.update(repository='https://github.com/other/repo'),
            'bad hash': lambda m: m['artifacts']['events_gate'].update(sha256='x'*64),
            'path traversal': lambda m: m['artifacts']['events_gate'].update(path='examples/../private'),
            'absolute path': lambda m: m['artifacts']['events_gate'].update(path='/private/file'),
            'internal record': lambda m: m['artifacts']['events_gate'].update(path='telemetry/receipt.json'),
            'unknown citation': lambda m: m['cards'][0]['documentation'].update(source_id='S99'),
            'wrong citation': lambda m: m['cards'][0]['documentation'].update(url='https://example.com/'),
            'invalid date': lambda m: m.update(as_of='2026-02-30'),
            'live SAS promotion': lambda m: m['cards'][0]['evidence'][0].update(level='LIVE_SAS'),
            'historical queue promotion': lambda m: m['historical_queue'].update(execution_status='EXECUTED'),
            'new acceptance claim': lambda m: m['snapshot']['acceptance'].update(basis='NEW_FULL_RUN'),
            'missing gaps': lambda m: m['cards'][0].update(remaining_gaps=[]),
            'artifact style': lambda m: m['cards'][0]['remaining_gaps'].append('gap'+chr(0x2014)+'boundary'),
            'missing source anchors': lambda m: m['cards'][0]['evidence'][0].update(source_tests=[]),
            'missing native R': lambda m: m['cards'][0]['evidence'][0]['refs'].remove('events_r'),
            'missing source suite': lambda m: m['cards'][0]['evidence'][0]['refs'].remove('events_suite'),
        }
        for label, mutate in mutations.items():
            with self.subTest(control=label):
                data = deepcopy(self.evidence_map)
                mutate(data)
                with self.assertRaises((AssertionError, ValueError)):
                    self.validate(data)

    def test_catalog_promotion_and_mismatch_controls(self):
        for label in ('review_status', 'validation_basis', 'map', 'go_commit', 'level'):
            with self.subTest(control=label):
                catalog = deepcopy(self.catalog)
                collection = next(c for c in catalog['collections'] if c['id'] == 'sas-conversion-landmines')
                if label in collection['metadata']:
                    collection['metadata'][label] = 'reviewed' if label == 'review_status' else 'gate'
                else:
                    doc = next(d for d in collection['documents'] if d['id'] == 'SL-003')
                    doc['coverage_evidence'][label] = 'invalid'
                with self.assertRaises(AssertionError):
                    self.validate(catalog=catalog)

    def synthetic_git_objects(self):
        """Small independent objects isolate snapshot resolver controls."""
        data = deepcopy(self.evidence_map)
        content = {}
        tests = {ref: set() for ref, a in data['artifacts'].items() if a['kind'] == 'source_suite'}
        for card in data['cards']:
            for evidence in card['evidence']:
                for ref in evidence['refs']:
                    if ref in tests:
                        tests[ref].update(evidence['source_tests'])
        for ref, artifact in data['artifacts'].items():
            if artifact['kind'] == 'rulebook':
                blob = json.dumps({'rules': [{'rule_id': r} for r in artifact['rule_ids']]}).encode()
            elif ref in tests:
                blob = ''.join(f'def {t}():\n    pass\n' for t in sorted(tests[ref])).encode()
            else:
                blob = b'Independent resolver fixture.\n'
            content[artifact['path']] = blob
            artifact['sha256'] = hashlib.sha256(blob).hexdigest()
        return data, content

    def test_snapshot_hash_rule_and_test_resolution(self):
        data, content = self.synthetic_git_objects()
        def read(repository, commit, path):
            self.assertEqual(repository, Path('/unused/read-only-go'))
            self.assertEqual(commit, data['snapshot']['commit'])
            return content[path]
        with patch.object(checker, 'read_go_artifact', side_effect=read):
            self.assertEqual(self.validate(data, repository=Path('/unused/read-only-go')), 5)
            for control in ('content hash', 'nonexistent rule', 'nonexistent test'):
                with self.subTest(control=control):
                    invalid = deepcopy(data)
                    if control == 'content hash':
                        invalid['artifacts']['events_gate']['sha256'] = '0'*64
                    elif control == 'nonexistent rule':
                        invalid['artifacts']['rulebook']['rule_ids'].append('DS-999')
                    else:
                        invalid['cards'][0]['evidence'][0]['source_tests'].append('test_absent')
                    with self.assertRaises(AssertionError):
                        self.validate(invalid, repository=Path('/unused/read-only-go'))

    def test_missing_git_object_is_a_hard_failure(self):
        with patch.object(checker, 'read_go_artifact', side_effect=subprocess.CalledProcessError(128, 'git show')):
            with self.assertRaises(subprocess.CalledProcessError):
                self.validate(repository=Path('/unused/read-only-go'))


if __name__ == '__main__':
    unittest.main()
