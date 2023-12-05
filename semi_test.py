
import src.zenyx as tzenyx
import tests.databank as db

def test_one():
    
    c: list = []
    
    tzenyx.pyon.debug.init(__file__)
    
    x = tzenyx.pyon.deep_serialize(db.demo_obj)
    y = tzenyx.pyon.deep_parse(x)
    
    z = tzenyx.pyon.deep_serialize(y)
    
    print(f"Z: {z}\nZ as JSON: {tzenyx.pyon.dumps(z)}")
    

test_one()