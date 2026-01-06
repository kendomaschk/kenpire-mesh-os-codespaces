"""
🌟 KenPire Mesh OS - Production Package
Military-grade cognitive infrastructure for enterprise applications

Version: 2.0.0
License: Enterprise
Author: KenPire Systems
"""

__version__ = "2.0.0"
__author__ = "KenPire Systems"
__license__ = "Enterprise"

# Core imports
from .core.smart_cards import SmartNarrativeCard, SmartCardOrchestrator
from .core.ai_orchestration import TrifectaCoordinator
from .core.security import SecurityHardening
from .core.mesh import MeshOrchestrator

# Server and utilities
from .server import create_app, run_server
from .utils import (
    json_utils,
    id_utils,
    time_utils,
    validation_utils,
    config_utils,
    default_cache,
    setup_logging,
)

# Core classes for easy import
__all__ = [
    # Core classes
    "SmartNarrativeCard",
    "SmartCardOrchestrator",
    "TrifectaCoordinator",
    "SecurityHardening",
    "MeshOrchestrator",
    # Server
    "create_app",
    "run_server",
    # Utilities
    "json_utils",
    "id_utils",
    "time_utils",
    "validation_utils",
    "config_utils",
    "default_cache",
    "setup_logging",
]

# Package metadata
__package_info__ = {
    "name": "kenpire",
    "version": __version__,
    "description": "Military-grade cognitive infrastructure for enterprise applications",
    "author": __author__,
    "license": __license__,
    "python_requires": ">=3.8",
    "keywords": ["ai", "orchestration", "mesh", "cognitive", "enterprise"],
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
}


def get_version():
    """Get package version"""
    return __version__


def get_info():
    """Get package information"""
    return __package_info__.copy()
