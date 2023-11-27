import pip

def require(package):
    try:
        return __import__(package)
    except ImportError:
        pip.main(['install', package])
    try:
        return __import__(package)
    except:
        print(f"Pakcage \"{package}\" couldn't be installed, as a resoult require couldn't import it :(")
