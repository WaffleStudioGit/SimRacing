from .assetto import AssettoSource
from .beamng import BeamNGSource
from .demo import DemoSource
from .forza import ForzaSource

SOURCES = {
    "forza": ForzaSource,
    "beamng": BeamNGSource,
    "assetto": AssettoSource,
    "demo": DemoSource,
}

__all__ = [
    "AssettoSource",
    "BeamNGSource",
    "DemoSource",
    "ForzaSource",
    "SOURCES",
]
