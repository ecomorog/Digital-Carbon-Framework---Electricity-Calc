import logging

logger = logging.getLogger("electricity")
logger.setLevel(logging.WARNING)
_handler = logging.StreamHandler()
_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
_handler.setFormatter(_formatter)
logger.addHandler(_handler)


computation_logger = logging.getLogger("electricity.computation")
computation_logger.propagate = False
computation_logger.setLevel(logging.WARNING)
_handler = logging.StreamHandler()
_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
)
_handler.setFormatter(_formatter)
computation_logger.addHandler(_handler)
