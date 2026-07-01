from jarvis.config.settings import settings

class Application:
    """Coordinates the startup and lifecycle of the Jarvis application."""

    def initialize(self) -> None:
        print("Initializing..")

    def run(self) -> None:
        print("Running..")
        
        print(settings.app_name)

        print(settings.app_version)

        print(settings.default_model)

        print(settings.debug)


    def shutdown(self) -> None:
        print("Shutting down..")
