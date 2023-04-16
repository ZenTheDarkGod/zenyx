import pip

def require(package):
    try:
        return __import__(package)
    except ImportError:
        pip.main(['install', package])
    return __import__(package)
