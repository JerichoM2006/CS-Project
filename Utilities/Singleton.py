# Singleton design pattern ensures only one instance of a class exists
class Singleton:
    # Class variable to hold the single instance of the class
    _instance : "Singleton" = None

    # Override __new__ method to create a single instance of the class
    def __new__(cls) -> "Singleton":
        # Check if an instance of the class already exists
        if not cls._instance:
            # If no instance exists, create a new instance
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance