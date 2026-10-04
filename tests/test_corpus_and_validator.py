import json
import subprocess
import sys
import unittest

import yaml

from helpers import CORPUS, EXAMPLE_BUNDLE, ROOT, TOOLS
from pwb.corpus import run

VALIDATOR = TOOLS / "validate_bundle.py"


class CorpusTests(unittest.TestCase):
    def test_corpus_passes(self):
        results = run(CORPUS)
        failed = [(label, detail) for status, label, detail in results if status == "fail"]
        self.assertEqual(failed, [])
        self.assertGreater(len(results), 60)

    def test_example_bundle_validates(self):
        proc = subprocess.run([sys.executable, str(VALIDATOR), str(EXAMPLE_BUNDLE), "--quiet"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout)


class SchemaFilesTests(unittest.TestCase):
    def test_schemas_parse_and_declare_draft(self):
        for f in (ROOT / "schemas").glob("*.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            self.assertEqual(data["$schema"], "https://json-schema.org/draft/2020-12/schema", f)

    def test_tool_self_assessment_validates(self):
        sys.path.insert(0, str(TOOLS))
        import validate_bundle  # noqa: WPS433
        v = validate_bundle.Validator(ROOT / "schemas")
        data = yaml.safe_load((TOOLS / "wiki-commons.yaml").read_text(encoding="utf-8"))
        errors = []
        schema = v.load("self-assessment.schema.json")
        v.validate(data, schema, schema, "self-assessment", errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
