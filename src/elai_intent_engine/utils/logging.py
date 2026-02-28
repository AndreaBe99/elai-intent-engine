import sys

from loguru import logger


def configure_logging(log_dir: str = "logs", rotation: str = "10 MB") -> None:
    """
    Configure loguru sinks for the application.

    Two sinks are set up:
    - **Console**: coloured, human-readable output sent to stderr.
    - **File**: structured JSON logs with automatic rotation and retention,
        written to ``{log_dir}/api.log``.

    Args:
        log_dir: Directory where rotating log files are stored.
        rotation: Rotation trigger — size string (``"10 MB"``) or time string
            (``"1 day"``). Loguru interprets both automatically.
    """
    # Remove the default loguru sink so we fully control the configuration.
    logger.remove()

    # Console sink
    logger.add(
        sys.stderr,
        level="DEBUG",
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
            "{exception}"
        ),
        backtrace=True,
        diagnose=True,
    )

    # File sink
    logger.add(
        f"{log_dir}/api.log",
        level="INFO",
        rotation=rotation,  # rotate when the file reaches this size
        retention="30 days",  # keep rotated files for 30 days
        compression="gz",  # compress rotated files to save space
        serialize=True,  # write structured JSON — easy to ship to
        #   any log aggregator (ELK, Loki, etc.)
        backtrace=True,
        diagnose=False,  # avoid leaking sensitive locals to disk
        enqueue=True,  # thread-safe / async-safe writes
    )
