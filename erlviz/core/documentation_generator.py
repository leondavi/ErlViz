"""
ErlViz Documentation Generator
Generates markdown documentation from Erlang project analysis
"""

import markdown
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ErlangDocumentationGenerator:
    """Generates comprehensive documentation for Erlang projects"""
    
    def __init__(self, analysis_data: Dict[str, Any], output_dir: str):
        self.data = analysis_data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_documentation(self, graph_paths: Dict[str, str] = None) -> Dict[str, str]:
        """Generate complete documentation suite"""
        logger.info("Generating documentation")
        
        docs = {}
        
        # Main project overview
        docs['overview'] = self._generate_project_overview(graph_paths)
        
        # Module documentation
        docs['modules'] = self._generate_module_documentation()
        
        # Behavior documentation  
        docs['behaviors'] = self._generate_behavior_documentation()
        
        # NIF documentation
        if self.data.get('nifs'):
            docs['nifs'] = self._generate_nif_documentation()
        
        # Communication patterns
        docs['communication'] = self._generate_communication_documentation()
        
        # Dependencies
        docs['dependencies'] = self._generate_dependency_documentation()
        
        # API reference
        docs['api'] = self._generate_api_reference()
        
        return docs
    
    def _generate_project_overview(self, graph_paths: Dict[str, str] = None) -> str:
        """Generate main project overview documentation"""
        project_path = self.data.get('project_path', '')
        project_name = Path(project_path).name if project_path else 'Erlang Project'
        
        stats = self.data.get('statistics', {})
        
        content = f"""# {project_name} - ErlViz Analysis

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Project Overview

**Location**: `{project_path}`

### Statistics

- **Total Modules**: {stats.get('total_modules', 0)}
- **Behavior Modules**: {stats.get('behavior_modules', 0)}
- **Supervisor Modules**: {stats.get('supervisor_modules', 0)}
- **NIF Modules**: {stats.get('nif_modules', 0)}
- **Test Modules**: {stats.get('test_modules', 0)}
- **Applications**: {stats.get('applications', 0)}

## Architecture Overview

This Erlang/OTP project follows standard OTP design principles with the following key components:

"""
        
        # Add applications info
        applications = self.data.get('applications', {})
        if applications:
            content += "### Applications\n\n"
            for app_name, app_info in applications.items():
                content += f"- **{app_name}** v{app_info.get('version', 'unknown')}\n"
                content += f"  - {app_info.get('description', 'No description')}\n"
                deps = app_info.get('dependencies', [])
                if deps:
                    content += f"  - Dependencies: {', '.join(deps)}\n"
                content += "\n"
        
        # Add communication patterns summary
        patterns = self.data.get('communication_patterns', [])
        if patterns:
            content += "### Communication Patterns\n\n"
            pattern_counts = {}
            for pattern in patterns:
                pattern_type = pattern.get('type', 'unknown')
                pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
            
            for pattern_type, count in pattern_counts.items():
                content += f"- **{pattern_type.replace('_', ' ').title()}**: {count} modules\n"
            content += "\n"
        
        # Add graphs if available
        if graph_paths:
            content += "## Visualizations\n\n"
            for graph_type, graph_path in graph_paths.items():
                graph_name = graph_type.replace('_', ' ').title()
                content += f"### {graph_name}\n\n"
                content += f"![{graph_name}]({Path(graph_path).name})\n\n"
        
        # Save to file
        overview_path = self.output_dir / 'README.md'
        with open(overview_path, 'w') as f:
            f.write(content)
            
        return str(overview_path)
    
    def _generate_module_documentation(self) -> str:
        """Generate detailed module documentation"""
        content = "# Module Documentation\n\n"
        
        modules = self.data.get('modules', {})
        
        # Group modules by type
        modules_by_type = {}
        for module_name, module_info in modules.items():
            module_type = module_info.get('type', 'module')
            if module_type not in modules_by_type:
                modules_by_type[module_type] = []
            modules_by_type[module_type].append((module_name, module_info))
        
        # Generate documentation for each type
        for module_type, module_list in modules_by_type.items():
            content += f"## {module_type.replace('_', ' ').title()} Modules\n\n"
            
            for module_name, module_info in sorted(module_list):
                content += f"### {module_name}\n\n"
                
                # Basic info
                content += f"**File**: `{module_info.get('path', '')}`\n\n"
                
                # Behaviors
                behaviors = module_info.get('behaviors', [])
                if behaviors:
                    content += f"**Behaviors**: {', '.join(behaviors)}\n\n"
                
                # Documentation from comments
                documentation = module_info.get('documentation', '')
                if documentation:
                    content += f"**Description**:\n{documentation}\n\n"
                
                # Exports
                exports = module_info.get('exports', [])
                if exports:
                    content += f"**Exported Functions**: {', '.join(exports[:10])}"
                    if len(exports) > 10:
                        content += f" ... (+{len(exports)-10} more)"
                    content += "\n\n"
                
                # Functions with documentation
                functions = module_info.get('functions', {})
                if functions:
                    content += "**Functions**:\n\n"
                    for func_name, func_info in functions.items():
                        args = func_info.get('args', '')
                        doc = func_info.get('documentation', '')
                        content += f"- `{func_name}({args})`"
                        if doc:
                            content += f" - {doc}"
                        content += "\n"
                    content += "\n"
                
                # NIFs
                nif_functions = module_info.get('nif_functions', [])
                if nif_functions:
                    content += f"**NIF Functions**: {', '.join(nif_functions)}\n\n"
                
                # Dependencies
                dependencies = module_info.get('dependencies', [])
                if dependencies:
                    content += f"**Dependencies**: {', '.join(dependencies)}\n\n"
                
                content += "---\n\n"
        
        # Save to file
        modules_path = self.output_dir / 'modules.md'
        with open(modules_path, 'w') as f:
            f.write(content)
            
        return str(modules_path)
    
    def _generate_behavior_documentation(self) -> str:
        """Generate OTP behavior documentation"""
        content = "# OTP Behavior Analysis\n\n"
        
        modules = self.data.get('modules', {})
        
        # Group by behavior
        behavior_modules = {}
        for module_name, module_info in modules.items():
            behaviors = module_info.get('behaviors', [])
            for behavior in behaviors:
                if behavior not in behavior_modules:
                    behavior_modules[behavior] = []
                behavior_modules[behavior].append((module_name, module_info))
        
        if not behavior_modules:
            content += "No OTP behaviors found in this project.\n"
        else:
            content += "This project implements the following OTP behaviors:\n\n"
            
            for behavior, module_list in sorted(behavior_modules.items()):
                content += f"## {behavior}\n\n"
                content += self._get_behavior_description(behavior) + "\n\n"
                
                content += f"**Implementing Modules** ({len(module_list)}):\n\n"
                
                for module_name, module_info in sorted(module_list):
                    content += f"### {module_name}\n\n"
                    
                    # Documentation
                    documentation = module_info.get('documentation', '')
                    if documentation:
                        content += f"{documentation}\n\n"
                    
                    # Key functions for this behavior
                    functions = module_info.get('functions', {})
                    callback_functions = self._get_behavior_callbacks(behavior, functions)
                    
                    if callback_functions:
                        content += "**Callback Functions**:\n\n"
                        for func_name, func_info in callback_functions.items():
                            content += f"- `{func_name}({func_info.get('args', '')})`"
                            doc = func_info.get('documentation', '')
                            if doc:
                                content += f" - {doc}"
                            content += "\n"
                        content += "\n"
                    
                    content += "---\n\n"
        
        # Save to file
        behaviors_path = self.output_dir / 'behaviors.md'
        with open(behaviors_path, 'w') as f:
            f.write(content)
            
        return str(behaviors_path)
    
    def _get_behavior_description(self, behavior: str) -> str:
        """Get description for OTP behavior"""
        descriptions = {
            'gen_server': 'Generic server behavior for implementing stateful server processes with synchronous and asynchronous calls.',
            'gen_statem': 'Generic state machine behavior for implementing finite state machines with complex state transitions.',
            'gen_fsm': 'Generic finite state machine behavior (deprecated, use gen_statem instead).',
            'gen_event': 'Generic event handler behavior for implementing event managers with multiple handlers.',
            'supervisor': 'Supervisor behavior for implementing fault-tolerant supervision trees.',
            'application': 'Application behavior for implementing OTP applications with start/stop lifecycle management.',
            'ranch_protocol': 'Ranch protocol behavior for implementing network protocol handlers.',
            'cowboy_handler': 'Cowboy HTTP handler behavior for processing HTTP requests.',
            'cowboy_websocket': 'Cowboy WebSocket handler behavior for WebSocket connections.',
            'cowboy_rest': 'Cowboy REST handler behavior for implementing RESTful APIs.'
        }
        return descriptions.get(behavior, f'Custom behavior: {behavior}')
    
    def _get_behavior_callbacks(self, behavior: str, functions: Dict) -> Dict:
        """Get callback functions for specific behavior"""
        callback_patterns = {
            'gen_server': ['init', 'handle_call', 'handle_cast', 'handle_info', 'terminate', 'code_change'],
            'gen_statem': ['init', 'callback_mode', 'handle_event', 'terminate', 'code_change'],
            'supervisor': ['init'],
            'application': ['start', 'stop'],
            'cowboy_handler': ['init', 'handle'],
            'cowboy_rest': ['init', 'allowed_methods', 'content_types_provided', 'content_types_accepted']
        }
        
        patterns = callback_patterns.get(behavior, [])
        callbacks = {}
        
        for func_name, func_info in functions.items():
            if any(pattern in func_name for pattern in patterns):
                callbacks[func_name] = func_info
                
        return callbacks
    
    def _generate_nif_documentation(self) -> str:
        """Generate NIF documentation"""
        content = "# Native Implemented Functions (NIFs)\n\n"
        
        nifs = self.data.get('nifs', {})
        
        if not nifs:
            content += "No NIFs found in this project.\n"
        else:
            content += "This project implements the following Native Implemented Functions:\n\n"
            
            for nif_name, nif_info in sorted(nifs.items()):
                content += f"## {nif_name}\n\n"
                
                # Paths
                erl_path = nif_info.get('erl_path', '')
                c_path = nif_info.get('c_path', '')
                cpp_path = nif_info.get('cpp_path', '')
                
                content += f"**Erlang Module**: `{erl_path}`\n"
                if c_path:
                    content += f"**C Implementation**: `{c_path}`\n"
                if cpp_path:
                    content += f"**C++ Implementation**: `{cpp_path}`\n"
                content += "\n"
                
                # Stub functions
                stub_functions = nif_info.get('stub_functions', [])
                if stub_functions:
                    content += "**Stub Functions** (Erlang side):\n\n"
                    for func in stub_functions:
                        content += f"- `{func}()` - Placeholder function that calls native implementation\n"
                    content += "\n"
                
                # Native functions
                native_functions = nif_info.get('native_functions', [])
                if native_functions:
                    content += "**Native Functions** (C/C++ side):\n\n"
                    for func in native_functions:
                        content += f"- `{func}()` - Native implementation\n"
                    content += "\n"
                
                # Documentation
                documentation = nif_info.get('documentation', '')
                if documentation:
                    content += f"**Description**:\n{documentation}\n\n"
                
                content += "---\n\n"
        
        # Save to file
        nifs_path = self.output_dir / 'nifs.md'
        with open(nifs_path, 'w') as f:
            f.write(content)
            
        return str(nifs_path)
    
    def _generate_communication_documentation(self) -> str:
        """Generate communication patterns documentation"""
        content = "# Communication Patterns\n\n"
        
        patterns = self.data.get('communication_patterns', [])
        
        if not patterns:
            content += "No specific communication patterns identified.\n"
        else:
            content += "This project uses the following communication patterns:\n\n"
            
            # Group by pattern type
            patterns_by_type = {}
            for pattern in patterns:
                pattern_type = pattern.get('type', 'unknown')
                if pattern_type not in patterns_by_type:
                    patterns_by_type[pattern_type] = []
                patterns_by_type[pattern_type].append(pattern)
            
            for pattern_type, pattern_list in sorted(patterns_by_type.items()):
                content += f"## {pattern_type.replace('_', ' ').title()}\n\n"
                content += self._get_pattern_description(pattern_type) + "\n\n"
                
                content += f"**Modules using this pattern** ({len(pattern_list)}):\n\n"
                
                for pattern in sorted(pattern_list, key=lambda p: p.get('module', '')):
                    module = pattern.get('module', '')
                    description = pattern.get('description', '')
                    content += f"- **{module}**: {description}\n"
                
                content += "\n---\n\n"
        
        # Save to file
        communication_path = self.output_dir / 'communication.md'
        with open(communication_path, 'w') as f:
            f.write(content)
            
        return str(communication_path)
    
    def _get_pattern_description(self, pattern_type: str) -> str:
        """Get description for communication pattern"""
        descriptions = {
            'gen_server': 'Synchronous request-response pattern with state management. Clients send requests and wait for responses.',
            'gen_statem': 'State machine pattern with event-driven state transitions. Handles complex stateful logic.',
            'http_handler': 'HTTP request-response pattern. Handles incoming HTTP requests and returns responses.',
            'nif': 'Native interface pattern. Bridges Erlang code with C/C++ implementations for performance-critical operations.',
            'supervisor': 'Supervision pattern. Monitors and restarts child processes to provide fault tolerance.',
            'websocket': 'Bidirectional communication pattern over WebSocket connections.',
            'pubsub': 'Publish-subscribe pattern for event broadcasting to multiple subscribers.'
        }
        return descriptions.get(pattern_type, f'Custom communication pattern: {pattern_type}')
    
    def _generate_dependency_documentation(self) -> str:
        """Generate dependency documentation"""
        content = "# Dependencies\n\n"
        
        # External dependencies
        dependencies = self.data.get('dependencies', {})
        if dependencies:
            content += "## External Dependencies\n\n"
            content += "This project depends on the following external libraries:\n\n"
            
            for dep_name, dep_modules in sorted(dependencies.items()):
                content += f"- **{dep_name}**"
                if dep_modules:
                    content += f" (used by: {', '.join(dep_modules)})"
                content += "\n"
            content += "\n"
        
        # Internal module dependencies
        modules = self.data.get('modules', {})
        internal_deps = {}
        
        for module_name, module_info in modules.items():
            module_deps = module_info.get('dependencies', [])
            internal_module_deps = [dep for dep in module_deps if dep in modules]
            if internal_module_deps:
                internal_deps[module_name] = internal_module_deps
        
        if internal_deps:
            content += "## Internal Module Dependencies\n\n"
            content += "Dependencies between project modules:\n\n"
            
            for module_name, deps in sorted(internal_deps.items()):
                content += f"- **{module_name}** depends on: {', '.join(deps)}\n"
            content += "\n"
        
        # Applications
        applications = self.data.get('applications', {})
        if applications:
            content += "## Application Dependencies\n\n"
            
            for app_name, app_info in sorted(applications.items()):
                app_deps = app_info.get('dependencies', [])
                if app_deps:
                    content += f"- **{app_name}** depends on: {', '.join(app_deps)}\n"
            content += "\n"
        
        # Save to file
        deps_path = self.output_dir / 'dependencies.md'
        with open(deps_path, 'w') as f:
            f.write(content)
            
        return str(deps_path)
    
    def _generate_api_reference(self) -> str:
        """Generate API reference documentation"""
        content = "# API Reference\n\n"
        
        modules = self.data.get('modules', {})
        
        # Only document modules with exported functions
        api_modules = {}
        for module_name, module_info in modules.items():
            exports = module_info.get('exports', [])
            functions = module_info.get('functions', {})
            if exports or functions:
                api_modules[module_name] = module_info
        
        if not api_modules:
            content += "No public API functions documented.\n"
        else:
            content += "Public API functions in this project:\n\n"
            
            for module_name, module_info in sorted(api_modules.items()):
                content += f"## {module_name}\n\n"
                
                # Module description
                documentation = module_info.get('documentation', '')
                if documentation:
                    content += f"{documentation}\n\n"
                
                # Exported functions
                exports = module_info.get('exports', [])
                functions = module_info.get('functions', {})
                
                if exports:
                    content += "### Exported Functions\n\n"
                    
                    for export in sorted(exports):
                        content += f"#### `{export}`\n\n"
                        
                        # Try to find function documentation
                        func_name = export.split('/')[0]  # Remove arity
                        if func_name in functions:
                            func_info = functions[func_name]
                            args = func_info.get('args', '')
                            doc = func_info.get('documentation', '')
                            
                            if args:
                                content += f"**Arguments**: `{args}`\n\n"
                            if doc:
                                content += f"**Description**: {doc}\n\n"
                        
                        content += "---\n\n"
                
                content += "\n"
        
        # Save to file
        api_path = self.output_dir / 'api.md'
        with open(api_path, 'w') as f:
            f.write(content)
            
        return str(api_path)
    
    def generate_html_documentation(self, docs: Dict[str, str]) -> Dict[str, str]:
        """Convert markdown documentation to HTML"""
        html_docs = {}
        
        md = markdown.Markdown(extensions=['tables', 'toc', 'codehilite'])
        
        for doc_type, doc_path in docs.items():
            if doc_path and Path(doc_path).exists():
                try:
                    with open(doc_path, 'r') as f:
                        md_content = f.read()
                    
                    html_content = md.convert(md_content)
                    
                    # Wrap in HTML template
                    html_full = self._create_html_template(
                        title=f"{doc_type.title()} - ErlViz Documentation",
                        content=html_content
                    )
                    
                    html_path = self.output_dir / f"{doc_type}.html"
                    with open(html_path, 'w') as f:
                        f.write(html_full)
                    
                    html_docs[doc_type] = str(html_path)
                    
                except Exception as e:
                    logger.error(f"Error converting {doc_type} to HTML: {e}")
        
        return html_docs
    
    def _create_html_template(self, title: str, content: str) -> str:
        """Create HTML template for documentation"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
        }}
        h1 {{
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
            margin-top: 30px;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Consolas', monospace;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .toc {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 10px 0;
        }}
        hr {{
            border: none;
            height: 1px;
            background-color: #bdc3c7;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>"""
