# app module
class App:
    def __init__(self, **kwargs):
        pass

    def run(self):
        # Simulate run: just call build and exit
        if hasattr(self, 'build'):
            self.build()
        return 0
