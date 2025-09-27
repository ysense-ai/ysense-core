# core/__init__.py
"""
YSense Platform v2.0 Core Module
"""

from .mcp_integration import YSenseMCPServer, YSenseMCPClient, initialize_mcp

__version__ = "2.0.0"
__all__ = ["YSenseMCPServer", "YSenseMCPClient", "initialize_mcp"]
