from jarvis.app import Application
from jarvis.core.logging import setup_logging


def main() -> None:
    setup_logging()

    app = Application()

    app.initialize()
    app.run()


if __name__ == "__main__":
    main()