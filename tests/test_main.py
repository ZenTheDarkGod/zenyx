import zenyx
import databank as db


def test_one():
    zenyx.pyon.debug.init(__file__)
    print(zenyx.pyon.deep_serialize(db.demo_obj))
    assert zenyx.pyon.deep_serialize(db.demo_obj) == {
        "param": [{"param": {"test": [10, 10]}, "@class": "test"}, "asd"],
        "@class": "test",
    }, "Deep Serialize"