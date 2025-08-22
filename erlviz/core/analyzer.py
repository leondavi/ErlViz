"""
ErlViz Core Analyzer
Analyzes Erlang/OTP projects (like NErlNet and Cowboy) to extract:
- OTP behaviors and their relationships
- Module dependencies
- NIF implementations
- Communication patterns
- Documentation from comments

Copyright (c) 2025 David Leon (leondavi)
Licensed under the MIT License - see LICENSE file for details.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
import ast
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ErlangModule:
    """Represents an Erlang module with its metadata"""
    name: str
    path: str
    behaviors: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)
    documentation: str = ""
    type: str = "module"  # module, behavior, nif, test
    functions: Dict[str, Dict] = field(default_factory=dict)
    nif_functions: List[str] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)

@dataclass 
class NIFModule:
    """Represents a NIF (Native Implemented Function) module"""
    name: str
    erl_path: str
    c_path: Optional[str] = None
    cpp_path: Optional[str] = None
    stub_functions: List[str] = field(default_factory=list)
    native_functions: List[str] = field(default_factory=list)
    documentation: str = ""

@dataclass
class Supervisor:
    """Represents an OTP supervisor and its children"""
    name: str
    path: str
    strategy: str = "one_for_one"
    children: List[Dict] = field(default_factory=list)
    documentation: str = ""

@dataclass
class Application:
    """Represents an OTP application"""
    name: str
    path: str
    description: str = ""
    version: str = ""
    modules: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    mod: Optional[str] = None
    supervisors: List[Supervisor] = field(default_factory=list)

class ErlangAnalyzer:
    """Main analyzer for Erlang/OTP projects"""
    
    def __init__(self, project_path: str, include_external_deps: bool = False, exclude_dirs: List[str] = None):
        self.project_path = Path(project_path)
        self.include_external_deps = include_external_deps
        self.exclude_dirs = exclude_dirs or []
        self.modules: Dict[str, ErlangModule] = {}
        self.nifs: Dict[str, NIFModule] = {}
        self.supervisors: Dict[str, Supervisor] = {}
        self.applications: Dict[str, Application] = {}
        self.dependencies: Dict[str, Set[str]] = {}
        self.communication_patterns: List[Dict] = []
        
    def analyze_project(self) -> Dict[str, Any]:
        """Analyze the entire Erlang project"""
        logger.info(f"Analyzing Erlang project at: {self.project_path}")
        
        # Find all Erlang source files
        erl_files = self._find_erlang_files()
        logger.info(f"Found {len(erl_files)} Erlang files")
        
        # Analyze each module
        for erl_file in erl_files:
            self._analyze_module(erl_file)
            
        # Find and analyze NIFs
        self._analyze_nifs()
        
        # Analyze rebar configuration
        self._analyze_rebar_config()
        
        # Analyze application files
        self._analyze_app_files()
        
        # Extract communication patterns
        self._analyze_communication_patterns()
        
        return self._build_analysis_result()
    
    def _find_erlang_files(self) -> List[Path]:
        """Find all .erl files in the project"""
        erl_files = []
        
        # Common Erlang source directories
        src_dirs = ['src', 'src_erl', 'apps/*/src', 'lib/*/src']
        
        for pattern in src_dirs:
            for src_dir in self.project_path.glob(pattern):
                if src_dir.is_dir() and not self._is_excluded_dir(src_dir):
                    erl_files.extend(src_dir.glob('**/*.erl'))
                    
        # Also check root directory
        erl_files.extend(self.project_path.glob('*.erl'))
        
        # Filter out files in excluded directories
        filtered_files = []
        for erl_file in erl_files:
            if not self._is_excluded_file(erl_file):
                filtered_files.append(erl_file)
        
        return list(set(filtered_files))  # Remove duplicates
    
    def _is_excluded_dir(self, dir_path: Path) -> bool:
        """Check if a directory should be excluded"""
        dir_name = dir_path.name
        return dir_name in self.exclude_dirs
    
    def _is_excluded_file(self, file_path: Path) -> bool:
        """Check if a file is in an excluded directory"""
        for exclude_dir in self.exclude_dirs:
            if exclude_dir in str(file_path):
                return True
        return False
    
    def _analyze_module(self, file_path: Path) -> None:
        """Analyze a single Erlang module"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            module = self._parse_erlang_module(content, file_path)
            if module:
                self.modules[module.name] = module
                logger.debug(f"Analyzed module: {module.name}")
                
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
    
    def _parse_erlang_module(self, content: str, file_path: Path) -> Optional[ErlangModule]:
        """Parse Erlang module content to extract metadata"""
        lines = content.split('\n')
        module_name = None
        behaviors = []
        exports = []
        imports = []
        dependencies = set()
        functions = {}
        nif_functions = []
        comments = []
        documentation = ""
        
        # Extract module name
        module_match = re.search(r'-module\s*\(\s*([^)]+)\s*\)', content)
        if module_match:
            module_name = module_match.group(1).strip()
        else:
            # Try to infer from filename
            module_name = file_path.stem
            
        # Extract behaviors
        behavior_matches = re.findall(r'-behaviour\s*\(\s*([^)]+)\s*\)', content)
        behaviors.extend([b.strip() for b in behavior_matches])
        
        # Alternative behavior spelling
        behavior_matches = re.findall(r'-behavior\s*\(\s*([^)]+)\s*\)', content)
        behaviors.extend([b.strip() for b in behavior_matches])
        
        # Extract exports
        export_matches = re.findall(r'-export\s*\(\s*\[(.*?)\]\s*\)', content, re.DOTALL)
        for export_match in export_matches:
            exports.extend(self._parse_export_list(export_match))
            
        # Extract imports
        import_matches = re.findall(r'-import\s*\(\s*([^,]+)\s*,\s*\[(.*?)\]\s*\)', content, re.DOTALL)
        for module, funcs in import_matches:
            imports.append(f"{module.strip()}:{funcs.strip()}")
            dependencies.add(module.strip())
            
        # Extract function calls to find dependencies
        call_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*):([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content)
        for module, func in call_matches:
            if module not in ['erlang', 'lists', 'io']:  # Always exclude built-in modules
                dependencies.add(module)
                
        # Extract NIF loading
        if 'erlang:load_nif' in content:
            # Pattern 1: Standard erlang:nif_error pattern
            nif_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*->\s*erlang:nif_error', content)
            nif_functions.extend(nif_matches)
            
            # Pattern 2: exit(nif_library_not_loaded) pattern (common in some projects)
            exit_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*->\s*exit\s*\(\s*nif_library_not_loaded\s*\)', content)
            nif_functions.extend(exit_matches)
            
            # Pattern 3: Functions with just throw/exit/error for NIFs
            throw_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*->\s*(?:throw|exit|error)\s*\([^)]*not[_ ]loaded[^)]*\)', content)
            nif_functions.extend(throw_matches)
            
        # Extract functions with documentation
        function_pattern = r'%%\s*(.*?)\n([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*->'
        func_matches = re.findall(function_pattern, content, re.DOTALL)
        for doc, func_name, args in func_matches:
            functions[func_name] = {
                'args': args.strip(),
                'documentation': doc.strip()
            }
            
        # Extract comments for documentation
        comment_matches = re.findall(r'%%\s*(.*)', content)
        comments = [c.strip() for c in comment_matches if c.strip()]
        
        # Build module documentation from comments
        if comments:
            documentation = '\n'.join(comments[:10])  # First 10 comments
            
        # Determine module type
        module_type = "module"
        if any(b in ['gen_server', 'gen_statem', 'gen_fsm', 'gen_event'] for b in behaviors):
            module_type = "behavior"
        elif any(b == 'supervisor' for b in behaviors):
            module_type = "supervisor"
        elif any(b == 'application' for b in behaviors):
            module_type = "application"
        elif nif_functions:
            module_type = "nif"
        elif file_path.name.endswith('_SUITE.erl') or 'test' in str(file_path).lower():
            module_type = "test"
            
        return ErlangModule(
            name=module_name,
            path=str(file_path),
            behaviors=behaviors,
            exports=exports,
            imports=imports,
            dependencies=dependencies,
            documentation=documentation,
            type=module_type,
            functions=functions,
            nif_functions=nif_functions,
            comments=comments
        )
    
    def _parse_export_list(self, export_str: str) -> List[str]:
        """Parse export list from Erlang module"""
        exports = []
        # Handle both function/arity and simple function exports
        items = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*(?:/\d+)?)', export_str)
        exports.extend(items)
        return exports
    
    def _analyze_nifs(self) -> None:
        """Analyze NIF implementations"""
        for module in self.modules.values():
            if module.nif_functions:
                nif = NIFModule(
                    name=f"{module.name}_nif",
                    erl_path=module.path,
                    stub_functions=module.nif_functions
                )
                
                # Look for corresponding C/C++ files
                c_files = self._find_nif_source_files(module.name)
                if c_files:
                    nif.c_path = c_files.get('c')
                    nif.cpp_path = c_files.get('cpp')
                    nif.native_functions = self._extract_nif_native_functions(c_files)
                    
                self.nifs[nif.name] = nif
    
    def _find_nif_source_files(self, module_name: str) -> Dict[str, str]:
        """Find C/C++ source files for NIF module"""
        files = {}
        
        # Common NIF source directories
        src_dirs = ['c_src', 'src_cpp', 'src_c', 'cpp_src', 'priv', 'src', 'native']
        
        for src_dir_name in src_dirs:
            src_dir = self.project_path / src_dir_name
            if src_dir.exists():
                # Look for files matching module name or similar patterns
                patterns = [
                    f"{module_name}",           # exact match
                    f"{module_name.lower()}",   # lowercase
                    f"{module_name.upper()}",   # uppercase  
                    f"{module_name}NIF",        # with NIF suffix
                    f"{module_name}_nif",       # with _nif suffix
                ]
                
                for pattern in patterns:
                    for ext in ['c', 'cpp', 'cc', 'cxx', 'C']:
                        nif_file = src_dir / f"{pattern}.{ext}"
                        if nif_file.exists():
                            files[ext.lower() if ext.lower() == 'c' else 'cpp'] = str(nif_file)
                
                # Also look for files recursively in subdirectories
                for root in src_dir.rglob('*'):
                    if root.is_file() and root.suffix.lower() in ['.c', '.cpp', '.cc', '.cxx']:
                        stem = root.stem.lower()
                        module_lower = module_name.lower()
                        if (module_lower in stem or stem in module_lower or 
                            stem.replace('_nif', '') == module_lower or
                            stem.replace('nif', '') == module_lower):
                            ext_key = 'c' if root.suffix.lower() == '.c' else 'cpp'
                            if ext_key not in files:  # Don't overwrite exact matches
                                files[ext_key] = str(root)
                        
        return files
    
    def _extract_nif_native_functions(self, c_files: Dict[str, str]) -> List[str]:
        """Extract native function names from C/C++ files"""
        functions = []
        
        for file_path in c_files.values():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Look for ERL_NIF_TERM functions
                func_matches = re.findall(r'ERL_NIF_TERM\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content)
                functions.extend(func_matches)
                
            except Exception as e:
                logger.error(f"Error reading NIF file {file_path}: {e}")
                
        return list(set(functions))
    
    def _analyze_rebar_config(self) -> None:
        """Analyze rebar.config for dependencies"""
        rebar_files = ['rebar.config', 'rebar3.config']
        
        for rebar_file in rebar_files:
            rebar_path = self.project_path / rebar_file
            if rebar_path.exists():
                try:
                    with open(rebar_path, 'r') as f:
                        content = f.read()
                        
                    # Extract dependencies
                    deps_match = re.search(r'\{deps,\s*\[(.*?)\]\}', content, re.DOTALL)
                    if deps_match:
                        deps_str = deps_match.group(1)
                        # Parse dependency tuples
                        dep_matches = re.findall(r'\{([^,}]+)', deps_str)
                        for dep in dep_matches:
                            dep_name = dep.strip(' "\'')
                            if dep_name not in self.dependencies:
                                self.dependencies[dep_name] = set()
                                
                except Exception as e:
                    logger.error(f"Error analyzing {rebar_file}: {e}")
    
    def _analyze_app_files(self) -> None:
        """Analyze .app files for application metadata"""
        app_files = list(self.project_path.glob('**/*.app')) + list(self.project_path.glob('**/*.app.src'))
        
        for app_file in app_files:
            try:
                with open(app_file, 'r') as f:
                    content = f.read()
                    
                app = self._parse_app_file(content, app_file)
                if app:
                    self.applications[app.name] = app
                    
            except Exception as e:
                logger.error(f"Error analyzing {app_file}: {e}")
    
    def _parse_app_file(self, content: str, file_path: Path) -> Optional[Application]:
        """Parse .app file content"""
        # Extract application tuple
        app_match = re.search(r'\{application,\s*([^,]+),\s*\[(.*?)\]\}', content, re.DOTALL)
        if not app_match:
            return None
            
        app_name = app_match.group(1).strip(' "\'')
        app_config = app_match.group(2)
        
        # Extract metadata
        description = ""
        version = ""
        modules = []
        dependencies = []
        mod = None
        
        # Description
        desc_match = re.search(r'\{description,\s*"([^"]+)"', app_config)
        if desc_match:
            description = desc_match.group(1)
            
        # Version
        vsn_match = re.search(r'\{vsn,\s*"([^"]+)"', app_config)
        if vsn_match:
            version = vsn_match.group(1)
            
        # Modules
        modules_match = re.search(r'\{modules,\s*\[(.*?)\]\}', app_config, re.DOTALL)
        if modules_match:
            module_names = re.findall(r"'?([a-zA-Z_][a-zA-Z0-9_]*)'?", modules_match.group(1))
            modules = module_names
            
        # Dependencies
        deps_match = re.search(r'\{applications,\s*\[(.*?)\]\}', app_config, re.DOTALL)
        if deps_match:
            dep_names = re.findall(r"'?([a-zA-Z_][a-zA-Z0-9_]*)'?", deps_match.group(1))
            dependencies = dep_names
            
        # Module callback
        mod_match = re.search(r'\{mod,\s*\{([^,}]+)', app_config)
        if mod_match:
            mod = mod_match.group(1).strip(' "\'')
            
        return Application(
            name=app_name,
            path=str(file_path),
            description=description,
            version=version,
            modules=modules,
            dependencies=dependencies,
            mod=mod
        )
    
    def _analyze_communication_patterns(self) -> None:
        """Analyze communication patterns between modules"""
        patterns = []
        
        for module in self.modules.values():
            # Gen_server calls
            if 'gen_server' in module.behaviors:
                patterns.append({
                    'type': 'gen_server',
                    'module': module.name,
                    'pattern': 'synchronous_calls',
                    'description': f"{module.name} handles synchronous gen_server calls"
                })
                
            # Gen_statem (state machine)
            if 'gen_statem' in module.behaviors:
                patterns.append({
                    'type': 'gen_statem', 
                    'module': module.name,
                    'pattern': 'state_machine',
                    'description': f"{module.name} implements state machine behavior"
                })
                
            # HTTP handlers (Cowboy pattern)
            if any('cowboy' in dep for dep in module.dependencies):
                patterns.append({
                    'type': 'http_handler',
                    'module': module.name,
                    'pattern': 'request_response',
                    'description': f"{module.name} handles HTTP requests"
                })
                
            # NIFs
            if module.nif_functions:
                patterns.append({
                    'type': 'nif',
                    'module': module.name,
                    'pattern': 'native_interface',
                    'description': f"{module.name} interfaces with native code"
                })
                
        self.communication_patterns = patterns
    
    def _filter_dependencies(self, dependencies: Set[str]) -> Set[str]:
        """Filter dependencies based on include_external_deps setting"""
        if self.include_external_deps:
            # Include all dependencies except built-in Erlang modules
            excluded_modules = {
                'erlang', 'lists', 'io', 'string', 'timer', 'ets', 'dets', 
                'mnesia', 'file', 'filename', 'filelib', 'dict', 'sets',
                'queue', 'gb_trees', 'gb_sets', 'binary', 'unicode', 're',
                'crypto', 'ssl', 'inets', 'httpc', 'http_uri', 'uri_string'
            }
            return {dep for dep in dependencies if dep not in excluded_modules}
        else:
            # Only include modules that exist in this project
            project_modules = set(self.modules.keys())
            return {dep for dep in dependencies if dep in project_modules}
    
    def _build_analysis_result(self) -> Dict[str, Any]:
        """Build the final analysis result"""
        # Filter modules and their dependencies based on include_external_deps setting
        filtered_modules = {}
        
        for name, module in self.modules.items():
            # Filter dependencies for this module
            filtered_deps = self._filter_dependencies(module.dependencies)
            
            filtered_modules[name] = {
                'name': module.name,
                'path': module.path,
                'behaviors': module.behaviors,
                'exports': module.exports,
                'dependencies': list(filtered_deps),
                'type': module.type,
                'documentation': module.documentation,
                'functions': module.functions,
                'nif_functions': module.nif_functions
            }
        
        return {
            'project_path': str(self.project_path),
            'modules': filtered_modules,
            'nifs': {name: {
                'name': nif.name,
                'erl_path': nif.erl_path,
                'c_path': nif.c_path,
                'cpp_path': nif.cpp_path,
                'stub_functions': nif.stub_functions,
                'native_functions': nif.native_functions,
                'documentation': nif.documentation
            } for name, nif in self.nifs.items()},
            'applications': {name: {
                'name': app.name,
                'description': app.description,
                'version': app.version,
                'modules': app.modules,
                'dependencies': app.dependencies,
                'mod': app.mod
            } for name, app in self.applications.items()},
            'dependencies': {k: list(v) for k, v in self.dependencies.items()},
            'communication_patterns': self.communication_patterns,
            'statistics': {
                'total_modules': len(self.modules),
                'behavior_modules': len([m for m in self.modules.values() if m.type == 'behavior']),
                'supervisor_modules': len([m for m in self.modules.values() if m.type == 'supervisor']),
                'nif_modules': len(self.nifs),
                'test_modules': len([m for m in self.modules.values() if m.type == 'test']),
                'applications': len(self.applications)
            }
        }

def analyze_erlang_project(project_path: str) -> Dict[str, Any]:
    """Convenience function to analyze an Erlang project"""
    analyzer = ErlangAnalyzer(project_path)
    return analyzer.analyze_project()
