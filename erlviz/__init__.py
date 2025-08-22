"""
ErlViz - Erlang Project Analyzer and Visualizer

A comprehensive tool for analyzing Erlang/OTP projects to generate:
- Dependency graphs and communication diagrams
- Documentation from code comments
- NIF analysis and visualization
- OTP behavior patterns analysis

Supports both local repositories and GitHub URLs.
"""

from .core.erlviz import ErlViz, analyze_erlang_project
from .core.analyzer import ErlangAnalyzer
from .core.graph_generator import ErlangGraphGenerator
from .core.documentation_generator import ErlangDocumentationGenerator
from .core.repository_manager import RepositoryManager

__version__ = "1.0.0"
__author__ = "ErlViz Development Team"
__description__ = "Erlang OTP Behavior Visualization Tool"

__all__ = [
    'ErlViz',
    'analyze_erlang_project',
    'ErlangAnalyzer',
    'ErlangGraphGenerator', 
    'ErlangDocumentationGenerator',
    'RepositoryManager'
]
