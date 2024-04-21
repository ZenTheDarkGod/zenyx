
import src.zenyx as zenyx
import sys
import tests.databank as db

def test_one():
    zenyx.pyon.debug.init(__file__)
    print(zenyx.pyon.deep_serialize(db.demo_obj))

test_one()