from jarvis.config.settings import settings
import logging
logger = logging.getLogger(__name__)

class Application:
    """Coordinates the startup and lifecycle of the Jarvis application."""
    
    def initialize(self) -> None:
        logger.info("Initializing application...")
    def run(self) -> None:
        logger.info(
            "Application started",
            extra={
                "version": settings.app_version,
                "environment": "development",
            },
        )

    def shutdown(self) -> None:
        logger.info("Shutting down application...")
