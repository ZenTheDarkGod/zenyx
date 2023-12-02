
import zenyx
import databank as db

def test_one():
    zenyx.pyon.debug(__file__)
    assert zenyx.pyon.deep_serialize(db.demo_obj) == {'param': [{'param': {'test': 0}, 'PYON_TYPE': 'test'}, 'asd'], 'PYON_TYPE': 'test'}, "Deep Serialize"
