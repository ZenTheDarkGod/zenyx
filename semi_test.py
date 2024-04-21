
import src.zenyx as zenyx
import sys
import tests.databank as db

def test_one():
    zenyx.pyon.debug.init(__file__)
    myobj = zenyx.pyon.deep_parse(zenyx.pyon.deep_serialize(db.demo_obj))
    print(myobj)
    myobj.param = 'asd'
    print(myobj)
    print((zenyx.pyon.deep_serialize(myobj)))


test_one()