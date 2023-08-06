"""PATHOS being core."""
import sys


try:
    import can
    import canopen

    # PCAN on darwin patch
    if sys.platform.startswith('darwin'):
        from being.can.pcan_darwin_patch import patch_pcan_on_darwin
        patch_pcan_on_darwin()
except ModuleNotFoundError:
    pass


__author__ = 'atheler'
__version__ = '0.3.4'
