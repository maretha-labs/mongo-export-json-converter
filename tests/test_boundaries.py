import json
import tempfile
import unittest
from pathlib import Path
from src.json_processor import process_ndjson

class BoundaryTests(unittest.TestCase):
    def test_filters_unsupported_types_and_preserves_ids_without_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dest = Path(tmp)/'input', Path(tmp)/'output'
            src.write_text('\n'.join(json.dumps(x) for x in [
                {'ecm:primaryType':'Other','af:name':'excluded'},
                {'ecm:primaryType':'Policy','ecm:parentId':'keep','af:name':'included'}]))
            process_ndjson(src, dest, {}, '2026-09-10T00:00:00Z')
            rows=[json.loads(x) for x in dest.read_text().splitlines()]
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]['ecm:parentId'],'keep')
            self.assertEqual(rows[0]['true:name'],'included')
    def test_refuses_same_path_without_truncating_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'input';src.write_text('original')
            with self.assertRaises(FileExistsError):process_ndjson(src,src,{})
            self.assertEqual(src.read_text(),'original')
    def test_refuses_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            src,dest=Path(tmp)/'input',Path(tmp)/'output'
            src.write_text('');dest.write_text('previous output')
            with self.assertRaises(FileExistsError):process_ndjson(src,dest,{})
            self.assertEqual(dest.read_text(),'previous output')
