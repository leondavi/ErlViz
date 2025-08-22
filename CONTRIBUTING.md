# Contributing to ErlViz

Thank you for your interest in contributing to ErlViz! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment for all contributors.

## How to Contribute

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/ErlViz.git
cd ErlViz
```

### 2. Set Up Development Environment

```bash
# Run the setup script
python3 setup.py

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 4. Make Your Changes

- Follow the existing code style
- Add docstrings to new functions and classes
- Include type hints where appropriate
- Update documentation if needed

### 5. Test Your Changes

```bash
# Run the test installation script
python test_installation.py

# Test with sample repositories
python main.py --cli https://github.com/ninenines/cowboy

# Test the GUI
python main.py
```

### 6. Commit and Push

```bash
git add .
git commit -m "Add: brief description of changes"
git push origin feature/your-feature-name
```

### 7. Create Pull Request

- Open a pull request on GitHub
- Provide a clear description of changes
- Reference any related issues

## Development Guidelines

### Code Style

- Use Python 3.8+ features
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Keep functions focused and concise

### Documentation

- Add docstrings to all public functions and classes
- Update README.md for new features
- Include usage examples where helpful

### Testing

- Test with different Erlang project structures
- Verify both CLI and GUI functionality
- Test on different operating systems when possible

### Architecture

ErlViz is organized in layers:

```
main.py                    # Entry point (CLI/GUI)
├── erlviz/
│   ├── core/             # Core analysis logic
│   │   ├── analyzer.py   # Erlang code analysis
│   │   ├── graph_generator.py  # Graph creation
│   │   ├── documentation_generator.py  # Doc generation
│   │   └── repository_manager.py  # Git operations
│   └── gui/              # PySide6 GUI
│       └── main_window.py
```

## Types of Contributions

### Bug Reports

- Use GitHub Issues
- Provide clear reproduction steps
- Include environment details (OS, Python version)
- Attach sample project if possible

### Feature Requests

- Use GitHub Issues with "enhancement" label
- Describe the use case clearly
- Explain why the feature would be valuable

### Code Contributions

#### High Priority Areas

- **Erlang Parser Improvements**: Better parsing of complex syntax
- **Visualization Enhancements**: New graph types or improved layouts
- **Documentation Features**: Better extraction from code comments
- **Performance Optimizations**: Faster analysis of large projects
- **Platform Support**: Better Windows/Linux compatibility

#### Good First Issues

- Adding new OTP behavior types
- Improving error messages
- Adding configuration options
- Documentation improvements

## License

By contributing to ErlViz, you agree that your contributions will be licensed under the MIT License. All contributions must be your own work or properly attributed if using others' work under compatible licenses.

## Getting Help

- Create an issue for questions
- Check existing issues and documentation first
- Be specific about your environment and use case

Thank you for contributing to ErlViz!
