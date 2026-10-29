"""Inventory provenance and negative controls; no Go or SAS execution."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import check_catalog as checker


class VerificationInventoryTests(unittest.TestCase):
    def setUp(self):
        catalog = json.loads((checker.ROOT/'collections.json').read_text())
        self.map = json.loads((checker.ROOT/catalog['evidence_maps'][0]).read_text())
        self.inventory = json.loads((checker.ROOT/catalog['verification_inventories'][0]).read_text())

    def validate(self, inventory=None, mapping=None, repository=None):
        checker.validate_verification_inventory(
            self.inventory if inventory is None else inventory,
            self.map if mapping is None else mapping, repository)

    def test_complete_inventory(self):
        self.validate()
        self.assertEqual(len(self.inventory['fixtures']), 50)
        self.assertEqual(len(self.inventory['suites']), 40)
        self.assertEqual(sum(s['tests'] for s in self.inventory['suites']), 755)

    def test_bad_provenance_and_counts_refuse(self):
        controls = {
            'floating commit': lambda d: d.update(commit='main'),
            'wrong repository': lambda d: d.update(repository='https://example.com'),
            'wrong run': lambda d: d.update(public_run_url='https://example.com'),
            'new execution claim': lambda d: d.update(basis='NEW_RUN'),
            'unlabeled grouping': lambda d: d.update(grouping_basis='OFFICIAL_SAS_CLASSES'),
            'wrong date': lambda d: d.update(as_of='2026-10-27'),
            'wrong total': lambda d: d['totals'].update(tests=1),
            'wrong suite count': lambda d: d['suites'][0].update(tests=1),
            'hidden skip': lambda d: d['suites'][0].update(skips=1),
            'bad receipt hash': lambda d: d['receipt'].update(receipt_sha256='x'*64),
            'bad artifact ID': lambda d: d['receipt'].update(artifact_id=True),
            'missing gate': lambda d: d['fixtures'].pop(),
            'missing suite': lambda d: d['suites'].pop(),
            'synthesis counted as workload': lambda d: d['separate_checks'].update(two_1k_workloads=99),
        }
        for name, mutate in controls.items():
            data = deepcopy(self.inventory); mutate(data)
            with self.subTest(control=name), self.assertRaises((AssertionError, ValueError)):
                self.validate(data)

    def test_ambiguous_or_internal_paths_refuse(self):
        for value in ('telemetry/receipt.json', 'examples/../private.py', '/private.py',
                      'examples/verify_x.py?raw=1', 'examples/verify_x.py#other',
                      'examples/verify%20x.py'):
            data = deepcopy(self.inventory)
            item = data['fixtures'][0]
            item.update(path=value, url=f"{data['repository']}/blob/{data['commit']}/{value}")
            with self.subTest(path=value), self.assertRaises(AssertionError):
                self.validate(data)

    def test_duplicate_and_module_controls(self):
        for kind in ('duplicate ID', 'duplicate path', 'bad module', 'bad kind'):
            data = deepcopy(self.inventory)
            if kind == 'duplicate ID': data['fixtures'][1]['id'] = data['fixtures'][0]['id']
            elif kind == 'duplicate path': data['fixtures'][1]['path'] = data['fixtures'][0]['path']
            elif kind == 'bad module': data['suites'][0]['module'] = 'os.system'
            else: data['fixtures'][0]['kind'] = 'suite'
            with self.subTest(control=kind), self.assertRaises(AssertionError):
                self.validate(data)

    def test_snapshot_registry_and_hash_controls(self):
        data = deepcopy(self.inventory); mapping = deepcopy(self.map)
        data['fixtures'] = data['fixtures'][:2]; data['suites'] = data['suites'][:2]
        data['totals'] = dict(fixture_gates=2, suites=2, tests=48, skips=0)
        mapping['snapshot']['acceptance'].update(data['totals'])
        registry = b'VERIFIERS = [("rounding_n", HERE / "examples" / "verify_rounding.py"), ("rounding_n_R", HERE / "examples" / "verify_rounding_r.py")]\nSUITES = [("suite-parser", "saschi.test_parser"), ("suite-rules", "saschi.test_rules")]\n'
        objects = {'verify_all.py': registry}
        for item in data['fixtures'] + data['suites']:
            objects[item['path']] = b'# Independent snapshot fixture.\n'
        for item in [data['registry']] + data['fixtures'] + data['suites']:
            item['sha256'] = hashlib.sha256(objects[item['path']]).hexdigest()
        with patch.object(checker, 'read_go_artifact', side_effect=lambda repo, commit, path: objects[path]):
            self.validate(data, mapping, Path('/unused/go'))
            for control in ('fixture order', 'suite order', 'content hash'):
                invalid = deepcopy(data)
                if control == 'fixture order': invalid['fixtures'].reverse()
                elif control == 'suite order': invalid['suites'].reverse()
                else: invalid['registry']['sha256'] = '0'*64
                with self.subTest(control=control), self.assertRaises(AssertionError):
                    self.validate(invalid, mapping, Path('/unused/go'))


if __name__ == '__main__':
    unittest.main()
