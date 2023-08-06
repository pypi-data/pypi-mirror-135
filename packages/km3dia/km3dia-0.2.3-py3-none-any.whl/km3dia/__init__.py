from pkg_resources import get_distribution, DistributionNotFound

version = get_distribution(__name__).version

from .core import DBManager
from .DOM_integration_summary import DOMIntegrationSummary
