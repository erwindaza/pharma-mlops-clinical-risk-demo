import logging
import sys
from dataclasses import dataclass


@dataclass
class ServiceMetrics:
    prediction_count: int = 0


service_metrics = ServiceMetrics()


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=level,
        stream=sys.stdout,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
