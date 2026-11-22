import copy
import json
import unittest
from pathlib import Path
from experiments.strata.validate_run import validate
ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / 'runs' / 'STRATA-002-GEOMETRY-AUDIT-2026-11-09.json'
class StrataRunValidatorTests(unittest.TestCase):
 def setUp(self): self.record=json.loads(RECORD.read_text(encoding='utf-8'))
 def test_historical_record_validates(self): self.assertTrue(validate(self.record))
 def test_missing_dimension_rejected(self):
  r=copy.deepcopy(self.record); r['strata_runner_output']['report']['dimensions']=[x for x in r['strata_runner_output']['report']['dimensions'] if x['dimension']!='held_out_predictive_evaluation']
  with self.assertRaisesRegex(ValueError,'missing required'): validate(r)
 def test_duplicate_dimension_rejected(self):
  r=copy.deepcopy(self.record); d=r['strata_runner_output']['report']['dimensions']; d.append(copy.deepcopy(d[0]))
  with self.assertRaisesRegex(ValueError,'unique'): validate(r)
 def test_invalid_status_rejected(self):
  r=copy.deepcopy(self.record); r['strata_runner_output']['report']['dimensions'][0]['status']='maybe'
  with self.assertRaisesRegex(ValueError,'valid status'): validate(r)
if __name__=='__main__': unittest.main()
