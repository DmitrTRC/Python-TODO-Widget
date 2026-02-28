import logging
from rich.logging import RichHandler

def setup_logger(name="TodoWidget"):
    """Configures and returns a rich, beautiful logger."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )
    logger = logging.getLogger(name)
    return logger

logger = setup_logger()
