import frontend.app as jarvis_app

class Jarvis:

    def __init__(self):
        self.jarvis = jarvis_app.App()
        self.jarvis.run()


if __name__ == "__main__":
    jarvis = Jarvis()
