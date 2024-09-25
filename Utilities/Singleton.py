class Singleton:
    _instance : "Singleton" = None

    def __new__(cls) -> "Singleton":
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
    
class SingletonMeta(Singleton):
    def test(self):
        pass