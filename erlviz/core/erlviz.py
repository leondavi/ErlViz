"""
ErlViz Main Module
Main orchestrator for Erlang project analysis and visualization

Copyright (c) 2025 David Leon (leondavi)
Licensed under the MIT License - see LICENSE file for details.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from .analyzer import ErlangAnalyzer
from .graph_generator import ErlangGraphGenerator
from .documentation_generator import ErlangDocumentationGenerator
from .repository_manager import RepositoryManager

logger = logging.getLogger(__name__)

class ErlViz:
    """
    Main ErlViz class that orchestrates the analysis of Erlang projects
    """
    
    def __init__(self, cache_dir: str = None, output_dir: str = None):
        self.cache_dir = cache_dir or str(Path.home() / '.erlviz' / 'cache')
        self.output_dir = output_dir or './erlviz_output'
        
        # Initialize components
        self.repo_manager = RepositoryManager(self.cache_dir)
        
        # Create output directory
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # Analysis results
        self.analysis_data: Optional[Dict[str, Any]] = None
        self.graphs: Dict[str, str] = {}
        self.docs: Dict[str, str] = {}
        
    def analyze_repository(self, 
                         repo_url_or_path: str,
                         include_submodules: bool = False,
                         use_cache: bool = True,
                         generate_graphs: bool = True,
                         generate_docs: bool = True,
                         output_format: str = 'png',
                         dpi: int = 300,
                         include_external_deps: bool = False,
                         exclude_dirs: List[str] = None) -> Dict[str, Any]:
        """
        Analyze an Erlang repository and generate documentation and graphs
        
        Args:
            repo_url_or_path: Git repository URL or local path
            include_submodules: Whether to include submodules in analysis
            use_cache: Whether to use cached repository if available
            generate_graphs: Whether to generate visualization graphs
            generate_docs: Whether to generate documentation
            output_format: Output format for graphs (png, svg, pdf)
            dpi: Resolution (DPI) for generated graphs
            include_external_deps: Whether to include external dependencies (default: False, project modules only)
            exclude_dirs: List of directory names to exclude from analysis
            
        Returns:
            Dictionary containing analysis results and file paths
        """
        logger.info(f"Starting ErlViz analysis of: {repo_url_or_path}")
        
        # Handle default exclude_dirs
        if exclude_dirs is None:
            exclude_dirs = []
        
        try:
            # Step 1: Get the repository
            repo_path = self._get_repository_path(repo_url_or_path, use_cache)
            if not repo_path:
                raise ValueError(f"Could not access repository: {repo_url_or_path}")
            
            # Step 2: Analyze repository structure
            repo_structure = self.repo_manager.analyze_repository_structure(repo_path)
            if not repo_structure['is_erlang_project']:
                logger.warning("Repository does not appear to be an Erlang project")
            
            # Step 3: Analyze Erlang code
            logger.info("Analyzing Erlang code...")
            analyzer = ErlangAnalyzer(repo_path, include_external_deps, exclude_dirs)
            self.analysis_data = analyzer.analyze_project()
            
            # Add repository metadata
            self.analysis_data['repository'] = repo_structure
            self.analysis_data['analysis_timestamp'] = datetime.now().isoformat()
            
            # Step 4: Generate graphs
            if generate_graphs:
                logger.info("Generating visualization graphs...")
                self.graphs = self._generate_graphs(output_format, dpi)
            
            # Step 5: Generate documentation
            if generate_docs:
                logger.info("Generating documentation...")
                self.docs = self._generate_documentation()
            
            # Step 6: Save analysis results
            self._save_analysis_results()
            
            # Step 7: Create summary
            summary = self._create_summary()
            
            logger.info("ErlViz analysis completed successfully")
            return summary
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            raise
    
    def _get_repository_path(self, repo_url_or_path: str, use_cache: bool) -> Optional[str]:
        """Get the local path to the repository"""
        path = Path(repo_url_or_path)
        
        # Check if it's a local path
        if path.exists() and path.is_dir():
            logger.info(f"Using local repository: {path}")
            return str(path)
        
        # It's a URL, use repository manager
        return self.repo_manager.get_repository(repo_url_or_path, use_cache)
    
    def _generate_graphs(self, output_format: str, dpi: int = 300) -> Dict[str, str]:
        """Generate all visualization graphs"""
        if not self.analysis_data:
            return {}
        
        graphs_dir = Path(self.output_dir) / 'graphs'
        graph_generator = ErlangGraphGenerator(self.analysis_data, str(graphs_dir))
        
        return graph_generator.generate_all_graphs(output_format, dpi)
    
    def _generate_documentation(self) -> Dict[str, str]:
        """Generate all documentation"""
        if not self.analysis_data:
            return {}
        
        docs_dir = Path(self.output_dir) / 'docs'
        doc_generator = ErlangDocumentationGenerator(self.analysis_data, str(docs_dir))
        
        # Generate markdown documentation
        docs = doc_generator.generate_documentation(self.graphs)
        
        # Also generate HTML versions
        html_docs = doc_generator.generate_html_documentation(docs)
        
        # Combine markdown and HTML docs
        all_docs = {}
        for doc_type, doc_path in docs.items():
            all_docs[f"{doc_type}_md"] = doc_path
            
        for doc_type, doc_path in html_docs.items():
            all_docs[f"{doc_type}_html"] = doc_path
            
        return all_docs
    
    def _save_analysis_results(self) -> None:
        """Save analysis results to JSON file"""
        if not self.analysis_data:
            return
        
        results_file = Path(self.output_dir) / 'analysis_results.json'
        
        # Create a copy for JSON serialization (remove non-serializable objects)
        json_data = self._prepare_for_json(self.analysis_data)
        
        with open(results_file, 'w') as f:
            json.dump(json_data, f, indent=2, default=str)
        
        logger.info(f"Analysis results saved to: {results_file}")
    
    def _prepare_for_json(self, data: Any) -> Any:
        """Prepare data for JSON serialization"""
        if isinstance(data, dict):
            return {k: self._prepare_for_json(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._prepare_for_json(item) for item in data]
        elif isinstance(data, set):
            return list(data)
        elif isinstance(data, Path):
            return str(data)
        else:
            return data
    
    def _create_summary(self) -> Dict[str, Any]:
        """Create analysis summary"""
        if not self.analysis_data:
            return {}
        
        stats = self.analysis_data.get('statistics', {})
        repo_info = self.analysis_data.get('repository', {})
        
        summary = {
            'project_name': repo_info.get('name', 'Unknown'),
            'project_path': self.analysis_data.get('project_path', ''),
            'analysis_timestamp': self.analysis_data.get('analysis_timestamp', ''),
            'output_directory': self.output_dir,
            'statistics': stats,
            'repository_info': repo_info,
            'generated_files': {
                'graphs': self.graphs,
                'documentation': self.docs,
                'analysis_data': str(Path(self.output_dir) / 'analysis_results.json')
            },
            'key_findings': self._extract_key_findings()
        }
        
        return summary
    
    def _extract_key_findings(self) -> Dict[str, Any]:
        """Extract key findings from analysis"""
        if not self.analysis_data:
            return {}
        
        modules = self.analysis_data.get('modules', {})
        nifs = self.analysis_data.get('nifs', {})
        patterns = self.analysis_data.get('communication_patterns', [])
        
        findings = {
            'architecture_type': self._determine_architecture_type(modules, patterns),
            'complexity_indicators': self._calculate_complexity_indicators(modules),
            'otp_compliance': self._assess_otp_compliance(modules),
            'performance_considerations': self._identify_performance_considerations(nifs, patterns),
            'documentation_quality': self._assess_documentation_quality(modules)
        }
        
        return findings
    
    def _determine_architecture_type(self, modules: Dict, patterns: List) -> str:
        """Determine the type of architecture"""
        pattern_types = {p.get('type') for p in patterns}
        
        if 'http_handler' in pattern_types:
            return 'Web Application/API Server'
        elif 'gen_statem' in pattern_types:
            return 'State Machine/Protocol Implementation'
        elif len([m for m in modules.values() if m.get('type') == 'supervisor']) > 2:
            return 'Complex OTP Application'
        elif any(m.get('nif_functions') for m in modules.values()):
            return 'High-Performance/Native Integration'
        else:
            return 'Standard OTP Application'
    
    def _calculate_complexity_indicators(self, modules: Dict) -> Dict[str, Any]:
        """Calculate complexity indicators"""
        total_modules = len(modules)
        total_dependencies = sum(len(m.get('dependencies', [])) for m in modules.values())
        avg_dependencies = total_dependencies / total_modules if total_modules > 0 else 0
        
        behavior_modules = len([m for m in modules.values() if m.get('behaviors')])
        behavior_ratio = behavior_modules / total_modules if total_modules > 0 else 0
        
        return {
            'total_modules': total_modules,
            'average_dependencies_per_module': round(avg_dependencies, 2),
            'behavior_module_ratio': round(behavior_ratio, 2),
            'complexity_level': 'High' if avg_dependencies > 5 else 'Medium' if avg_dependencies > 2 else 'Low'
        }
    
    def _assess_otp_compliance(self, modules: Dict) -> Dict[str, Any]:
        """Assess OTP compliance"""
        otp_behaviors = {'gen_server', 'gen_statem', 'gen_fsm', 'gen_event', 'supervisor', 'application'}
        
        modules_with_behaviors = 0
        custom_behaviors = set()
        
        for module in modules.values():
            behaviors = set(module.get('behaviors', []))
            if behaviors:
                modules_with_behaviors += 1
                custom_behaviors.update(behaviors - otp_behaviors)
        
        total_modules = len(modules)
        compliance_ratio = modules_with_behaviors / total_modules if total_modules > 0 else 0
        
        return {
            'modules_with_otp_behaviors': modules_with_behaviors,
            'compliance_ratio': round(compliance_ratio, 2),
            'custom_behaviors': list(custom_behaviors),
            'compliance_level': 'High' if compliance_ratio > 0.7 else 'Medium' if compliance_ratio > 0.4 else 'Low'
        }
    
    def _identify_performance_considerations(self, nifs: Dict, patterns: List) -> List[str]:
        """Identify performance-related considerations"""
        considerations = []
        
        if nifs:
            considerations.append(f"Uses {len(nifs)} NIF modules for native performance")
        
        statem_count = len([p for p in patterns if p.get('type') == 'gen_statem'])
        if statem_count > 0:
            considerations.append(f"Uses {statem_count} state machines for complex logic")
        
        http_count = len([p for p in patterns if p.get('type') == 'http_handler'])
        if http_count > 0:
            considerations.append(f"HTTP server with {http_count} handler modules")
        
        if not considerations:
            considerations.append("Standard Erlang performance characteristics")
        
        return considerations
    
    def _assess_documentation_quality(self, modules: Dict) -> Dict[str, Any]:
        """Assess documentation quality"""
        total_modules = len(modules)
        documented_modules = len([m for m in modules.values() if m.get('documentation')])
        
        total_functions = sum(len(m.get('functions', {})) for m in modules.values())
        documented_functions = sum(
            len([f for f in m.get('functions', {}).values() if f.get('documentation')])
            for m in modules.values()
        )
        
        module_doc_ratio = documented_modules / total_modules if total_modules > 0 else 0
        function_doc_ratio = documented_functions / total_functions if total_functions > 0 else 0
        
        return {
            'documented_modules': documented_modules,
            'module_documentation_ratio': round(module_doc_ratio, 2),
            'documented_functions': documented_functions,
            'function_documentation_ratio': round(function_doc_ratio, 2),
            'documentation_quality': (
                'Good' if module_doc_ratio > 0.7 and function_doc_ratio > 0.5 
                else 'Fair' if module_doc_ratio > 0.4 or function_doc_ratio > 0.3
                else 'Poor'
            )
        }
    
    def analyze_multiple_projects(self, projects: List[Tuple[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Analyze multiple Erlang projects
        
        Args:
            projects: List of (name, url_or_path) tuples
            **kwargs: Additional arguments passed to analyze_repository
            
        Returns:
            Dictionary with results for each project
        """
        results = {}
        
        for project_name, project_path in projects:
            logger.info(f"Analyzing project: {project_name}")
            
            try:
                # Create project-specific output directory
                project_output_dir = Path(self.output_dir) / project_name
                original_output_dir = self.output_dir
                self.output_dir = str(project_output_dir)
                
                # Analyze project
                result = self.analyze_repository(project_path, **kwargs)
                results[project_name] = result
                
                # Restore original output directory
                self.output_dir = original_output_dir
                
            except Exception as e:
                logger.error(f"Error analyzing {project_name}: {e}")
                results[project_name] = {'error': str(e)}
        
        # Generate comparative analysis
        if len(results) > 1:
            comparison = self._generate_comparative_analysis(results)
            
            # Save comparison
            comparison_file = Path(self.output_dir) / 'project_comparison.json'
            with open(comparison_file, 'w') as f:
                json.dump(comparison, f, indent=2, default=str)
        
        return results
    
    def _generate_comparative_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparative analysis between projects"""
        comparison = {
            'projects': list(results.keys()),
            'comparison_timestamp': datetime.now().isoformat(),
            'metrics': {}
        }
        
        # Extract metrics for comparison
        for metric in ['total_modules', 'behavior_modules', 'nif_modules']:
            comparison['metrics'][metric] = {}
            for project_name, result in results.items():
                if 'error' not in result:
                    stats = result.get('statistics', {})
                    comparison['metrics'][metric][project_name] = stats.get(metric, 0)
        
        return comparison

def analyze_erlang_project(project_path: str, 
                         output_dir: str = None,
                         **kwargs) -> Dict[str, Any]:
    """
    Convenience function to analyze an Erlang project
    
    Args:
        project_path: Path to Erlang project (local or Git URL)
        output_dir: Output directory for results
        **kwargs: Additional arguments for analysis
        
    Returns:
        Analysis summary
    """
    erlviz = ErlViz(output_dir=output_dir)
    return erlviz.analyze_repository(project_path, **kwargs)
