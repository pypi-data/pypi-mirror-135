"""
Taktile Client
"""
__version__ = "1.0.0"

from .config import arrow_available

if arrow_available:
    from taktile_client.arrow import ArrowClient

# pylint: disable-next=wrong-import-position, wrong-import-order
from taktile_client.rest import RestClient
