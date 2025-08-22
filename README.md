# ErlViz - Erlang Project Analyzer and Visualizer

ErlViz is a comprehensive Python-based tool that analyzes Erlang/OTP projects to generate dependency graphs, communication diagrams, and documentation. Providing deep insights into OTP behaviors, module dependencies, and communication patterns.

## Features

### 🔍 **Deep Analysis**
- **OTP Behavior Detection**: Automatically identifies `gen_server`, `gen_statem`, `supervisor`, `application`, and custom behaviors
- **Module Dependencies**: Maps internal and external dependencies between modules
- **Communication Patterns**: Analyzes message flows and communication patterns
- **NIF Analysis**: Identifies Native Implemented Functions and their C/C++ implementations

### 📊 **Rich Visualizations**
- **Dependency Graphs**: Module dependency relationships with clustering by behavior type
- **Communication Diagrams**: Visual representation of message flows and patterns
- **Behavior Hierarchy**: OTP supervision trees and behavior implementations
- **NIF Integration Maps**: Erlang-to-native code interfaces

### 📚 **Documentation Generation**
- **Module Documentation**: Extracted from code comments and function signatures
- **API Reference**: Comprehensive function documentation
- **Behavior Analysis**: Detailed OTP behavior usage patterns
- **Architecture Overview**: High-level project structure analysis

### 🌐 **Flexible Input**
- **Local Repositories**: Analyze local Erlang projects
- **GitHub Integration**: Direct analysis from GitHub URLs
- **Submodule Support**: Optional inclusion of Git submodules
- **Multiple Formats**: PNG, SVG, PDF output for graphs

## Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/ErlViz.git
cd ErlViz

# Run setup script (creates virtualenv and installs dependencies)
python setup.py
```

### 2. Install System Dependencies

**Graphviz** is required for graph generation:

```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# CentOS/RHEL
sudo yum install graphviz

# Windows
# Download from https://graphviz.org/download/
```

### 3. Activate Virtual Environment

```bash
# Unix/Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

## Usage

### GUI Mode (Recommended)

Launch the PySide6-based graphical interface:

```bash
python main.py
```

The GUI provides:
- Repository input (local path or GitHub URL)
- Analysis options configuration
- Real-time progress monitoring
- Interactive result viewing
- Graph and documentation export

### CLI Mode

Analyze projects from the command line:

```bash
# Analyze a local project
python main.py --cli /path/to/erlang/project

# Analyze a GitHub repository
python main.py --cli https://github.com/leondavi/NErlNet

# Customize output options
python main.py --cli https://github.com/ninenines/cowboy \
    --output ./cowboy_analysis \
    --format svg \
    --include-submodules \
    --verbose
```

#### CLI Options

```
--cli PROJECT_PATH          Run in CLI mode with specified project
--output DIR                Output directory (default: ./erlviz_output)
--format {png,svg,pdf}      Graph output format (default: png)
--no-graphs                 Skip graph generation
--no-docs                   Skip documentation generation
--include-submodules        Include Git submodules
--no-cache                  Disable repository caching
--verbose                   Enable verbose logging
```

## Example Projects

### NErlNet Analysis
```bash
python main.py --cli https://github.com/leondavi/NErlNet
```

NErlNet is a sophisticated distributed machine learning framework that demonstrates:
- Complex OTP supervision trees
- State machine implementations (`gen_statem`)
- HTTP API handling with Cowboy
- NIF integration for performance-critical operations
- Multi-application architecture

### Cowboy Analysis
```bash
python main.py --cli https://github.com/ninenines/cowboy
```

Cowboy is a clean HTTP server framework showcasing:
- Standard OTP application patterns
- Protocol handler behaviors
- Clean module organization
- Extensive examples and tests

## Architecture

ErlViz is built with a modular architecture:

```
erlviz/
├── core/                   # Core analysis engine
│   ├── analyzer.py         # Erlang code analysis
│   ├── graph_generator.py  # Graph generation
│   ├── documentation_generator.py  # Doc generation
│   ├── repository_manager.py       # Git repository handling
│   └── erlviz.py          # Main orchestrator
├── gui/                    # PySide6 GUI application
│   ├── main_window.py     # Main application window
│   └── __init__.py
└── __init__.py            # Package initialization
```

### Core Components

1. **ErlangAnalyzer**: Parses Erlang source files to extract:
   - Module metadata and behaviors
   - Function exports and documentation
   - Dependencies and imports
   - NIF implementations

2. **ErlangGraphGenerator**: Creates visualizations using Graphviz:
   - Dependency graphs with behavior clustering
   - Communication pattern diagrams
   - NIF integration maps
   - OTP behavior hierarchies

3. **ErlangDocumentationGenerator**: Generates comprehensive docs:
   - Markdown and HTML formats
   - Module and API references
   - Behavior analysis reports
   - Architecture overviews

4. **RepositoryManager**: Handles Git operations:
   - Repository cloning and caching
   - Submodule management
   - GitHub integration

## Output Structure

ErlViz generates a comprehensive analysis output:

```
erlviz_output/
├── docs/                   # Generated documentation
│   ├── README.md          # Project overview
│   ├── modules.md         # Module documentation
│   ├── behaviors.md       # OTP behavior analysis
│   ├── nifs.md           # NIF documentation
│   ├── communication.md   # Communication patterns
│   ├── dependencies.md    # Dependency analysis
│   ├── api.md            # API reference
│   └── *.html            # HTML versions
├── graphs/                # Generated graphs
│   ├── dependency_graph.png
│   ├── communication_diagram.png
│   ├── behavior_hierarchy.png
│   └── nif_diagram.png
└── analysis_results.json  # Raw analysis data
```

## Development

### Project Structure

The project follows Python best practices with clear separation of concerns:

- **Core Logic**: Pure Python analysis and generation logic
- **GUI Layer**: PySide6-based user interface  
- **CLI Interface**: Command-line tools for automation
- **Configuration**: JSON-based configuration management

### Adding New Features

1. **New Analysis Types**: Extend `ErlangAnalyzer` with additional parsing logic
2. **New Visualizations**: Add methods to `ErlangGraphGenerator`
3. **New Documentation**: Extend `ErlangDocumentationGenerator`
4. **GUI Enhancements**: Modify `main_window.py` and related components

### Testing

```bash
# Run with example projects
python main.py --cli https://github.com/ninenines/cowboy --verbose

# Test specific components
python -c "from erlviz import ErlangAnalyzer; print('Import successful')"
```

## Configuration

Create custom configurations in `config/`:

```json
{
  "output_format": "png",
  "generate_graphs": true,
  "generate_docs": true,
  "include_submodules": false,
  "cache_dir": "~/.erlviz/cache",
  "graph_options": {
    "dpi": 300,
    "rankdir": "TB"
  }
}
```

## Troubleshooting

### Common Issues

1. **Graphviz not found**: Install system Graphviz package
2. **PySide6 import error**: Install with `pip install PySide6`
3. **Git authentication**: Use HTTPS URLs or configure SSH keys
4. **Large repositories**: Enable caching and use `--no-submodules`

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
python main.py --cli <project> --verbose
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Quick start for contributors:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Third Party Licenses

ErlViz uses several open source libraries. See [NOTICE](NOTICE) file for complete attribution.

## Acknowledgments

- **NErlNet**: Example of complex Erlang ML framework
- **Cowboy**: Clean OTP application example  
- **Graphviz**: Graph visualization engine
- **PySide6**: GUI framework
- **Erlang/OTP**: The language and platform we analyze
- **Open Source Community**: For the amazing tools that make this possible
