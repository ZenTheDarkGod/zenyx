
import src.zenyx as zenyx
import tests.databank as db

def test_one():
    zenyx.pyon.debugf(__file__)
    assert zenyx.pyon.deep_serialize(db.demo_obj) == {'param': [{'param': {'test': 0}, 'PYON_TYPE': 'test'}, 'asd'], 'PYON_TYPE': 'test'}, "Deep Serialize"

test_one()