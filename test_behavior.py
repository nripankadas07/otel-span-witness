import copy,json,unittest
from pathlib import Path
import otel_span_witness as m

class Behavior(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((Path(__file__).parent/'example.json').read_text())
    def bad(self):
        with self.assertRaises(m.InputError):m.analyze(self.d)
    def test_unknown_field_rejected(self):
        self.d['unknown']=True;self.bad()

    def test_overlapping_children_union(self):
        r=m.analyze(self.d);p=r['spans'][0];self.assertEqual(p['clipped_direct_child_union_ns'],70);self.assertEqual(p['uncovered_by_direct_children_ns'],30);self.assertEqual(r['findings'],[])
    def test_missing_parent_capture_finding(self):
        self.d['spans']=self.d['spans'][1:];self.assertEqual(m.analyze(self.d)['findings'][0]['kind'],'parents_not_in_capture')
    def test_cycles_reported_once(self):
        self.d['spans'][0]['parent_span_id']='2'*16;r=m.analyze(self.d);self.assertEqual(sum(x['kind']=='parent_cycle' for x in r['findings']),1)
    def test_self_cycle(self):
        self.d['spans'][0]['parent_span_id']='1'*16;self.assertEqual(m.analyze(self.d)['findings'][0]['kind'],'parent_cycle')
    def test_async_child_not_a_validation_failure(self):
        self.d['spans'][1].update(start_ns=90,end_ns=120);r=m.analyze(self.d);self.assertEqual(r['findings'],[]);self.assertTrue(r['timeline_annotations'])
    def test_clipping_bounds(self):
        self.d['spans'][1].update(start_ns=0,end_ns=200);r=m.analyze(self.d);self.assertEqual(r['spans'][0]['clipped_direct_child_union_ns'],100)
    def test_same_span_id_across_traces_allowed(self):
        self.d['spans'][1].update(trace_id='2'*32,parent_span_id=None);self.assertEqual(len(m.analyze(self.d)['spans']),3)
    def test_duplicate_identity_rejected(self):
        self.d['spans']*=2;self.bad()
    def test_zero_id_rejected(self):
        self.d['spans'][0]['trace_id']='0'*32;self.bad()
    def test_uppercase_id_rejected(self):
        self.d['spans'][0]['trace_id']='A'*32;self.bad()
    def test_negative_duration_rejected(self):
        self.d['spans'][0]['end_ns']=-1;self.bad()
    def test_reversed_time_rejected(self):
        self.d['spans'][1]['end_ns']=0;self.bad()

if __name__ == '__main__':unittest.main()
