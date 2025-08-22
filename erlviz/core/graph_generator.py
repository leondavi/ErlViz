"""
ErlViz Graph Generator
Creates dependency graphs and communication diagrams for Erlang projects

Copyright (c) 2025 David Leon (leondavi)
Licensed under the MIT License - see LICENSE file for details.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import graphviz
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import logging

logger = logging.getLogger(__name__)

class ErlangGraphGenerator:
    """Generates various graphs for Erlang project analysis"""
    
    def __init__(self, analysis_data: Dict[str, Any], output_dir: str):
        self.data = analysis_data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create NetworkX graph
        self.graph = nx.DiGraph()
        self._build_graph()
        
    def _build_graph(self) -> None:
        """Build NetworkX graph from analysis data"""
        modules = self.data.get('modules', {})
        
        # Add module nodes
        for module_name, module_info in modules.items():
            node_type = module_info.get('type', 'module')
            behaviors = module_info.get('behaviors', [])
            
            # Determine node properties
            color = self._get_node_color(node_type, behaviors)
            shape = self._get_node_shape(node_type)
            
            self.graph.add_node(
                module_name,
                type=node_type,
                behaviors=behaviors,
                color=color,
                shape=shape,
                documentation=module_info.get('documentation', ''),
                exports=module_info.get('exports', []),
                nif_functions=module_info.get('nif_functions', [])
            )
            
        # Add dependency edges
        for module_name, module_info in modules.items():
            dependencies = module_info.get('dependencies', [])
            for dep in dependencies:
                if dep in modules:  # Only internal dependencies
                    self.graph.add_edge(module_name, dep, relation='calls')
                    
        # Add NIF relationships
        nifs = self.data.get('nifs', {})
        for nif_name, nif_info in nifs.items():
            erl_module = self._get_module_from_path(nif_info.get('erl_path', ''))
            if erl_module:
                # Add NIF node if it has C/C++ implementation
                if nif_info.get('c_path') or nif_info.get('cpp_path'):
                    self.graph.add_node(
                        nif_name,
                        type='nif_impl',
                        color='orange',
                        shape='box',
                        native_functions=nif_info.get('native_functions', [])
                    )
                    self.graph.add_edge(erl_module, nif_name, relation='nif')
    
    def _get_node_color(self, node_type: str, behaviors: List[str]) -> str:
        """Get color for node based on type and behaviors"""
        if node_type == 'application':
            return 'lightblue'
        elif node_type == 'supervisor':
            return 'lightgreen'
        elif 'gen_server' in behaviors:
            return 'yellow'
        elif 'gen_statem' in behaviors:
            return 'orange'
        elif node_type == 'nif':
            return 'red'
        elif node_type == 'test':
            return 'lightgray'
        else:
            return 'white'
    
    def _get_node_shape(self, node_type: str) -> str:
        """Get shape for node based on type"""
        shapes = {
            'application': 'house',
            'supervisor': 'diamond',
            'behavior': 'ellipse',
            'nif': 'box',
            'test': 'triangle',
            'module': 'ellipse'
        }
        return shapes.get(node_type, 'ellipse')
    
    def _get_module_from_path(self, path: str) -> str:
        """Extract module name from file path"""
        if path:
            return Path(path).stem
        return ""
    
    def generate_dependency_graph(self, format: str = 'png', dpi: int = 300) -> str:
        """Generate module dependency graph"""
        logger.info("Generating dependency graph")
        
        # Create Graphviz graph
        dot = graphviz.Digraph(comment='Erlang Module Dependencies')
        dot.attr(rankdir='TB', size='12,8', dpi=str(dpi))
        dot.attr('node', fontname='Arial', fontsize='10')
        dot.attr('edge', fontname='Arial', fontsize='8')
        
        # Add nodes by type in clusters
        self._add_clustered_nodes(dot)
        
        # Add edges
        for edge in self.graph.edges(data=True):
            source, target, attrs = edge
            relation = attrs.get('relation', 'calls')
            
            edge_style = {
                'calls': {'color': 'blue', 'style': 'solid'},
                'nif': {'color': 'red', 'style': 'dashed', 'label': 'NIF'},
                'supervises': {'color': 'green', 'style': 'bold'}
            }
            
            style = edge_style.get(relation, {'color': 'black'})
            dot.edge(source, target, **style)
        
        # Save graph
        output_path = self.output_dir / f'dependency_graph.{format}'
        dot.render(str(output_path.with_suffix('')), format=format, cleanup=True)
        
        return str(output_path)
    
    def _add_clustered_nodes(self, dot: graphviz.Digraph) -> None:
        """Add nodes grouped by type in clusters"""
        modules_by_type = {}
        
        for node, attrs in self.graph.nodes(data=True):
            node_type = attrs.get('type', 'module')
            if node_type not in modules_by_type:
                modules_by_type[node_type] = []
            modules_by_type[node_type].append((node, attrs))
        
        # Define cluster styles
        cluster_styles = {
            'application': {'label': 'Applications', 'color': 'lightblue', 'style': 'filled'},
            'supervisor': {'label': 'Supervisors', 'color': 'lightgreen', 'style': 'filled'},
            'behavior': {'label': 'OTP Behaviors', 'color': 'lightyellow', 'style': 'filled'},
            'nif': {'label': 'NIFs', 'color': 'lightcoral', 'style': 'filled'},
            'nif_impl': {'label': 'NIF Implementations', 'color': 'orange', 'style': 'filled'},
            'test': {'label': 'Tests', 'color': 'lightgray', 'style': 'filled'},
            'module': {'label': 'Modules', 'color': 'white', 'style': 'filled'}
        }
        
        for node_type, nodes in modules_by_type.items():
            if len(nodes) > 1:  # Only create cluster if more than one node
                cluster_style = cluster_styles.get(node_type, {})
                with dot.subgraph(name=f'cluster_{node_type}') as cluster:
                    cluster.attr(**cluster_style)
                    
                    for node, attrs in nodes:
                        self._add_node_to_graph(cluster, node, attrs)
            else:
                # Add single nodes directly
                for node, attrs in nodes:
                    self._add_node_to_graph(dot, node, attrs)
    
    def _add_node_to_graph(self, graph, node: str, attrs: Dict) -> None:
        """Add a single node to the graph with proper styling"""
        node_attrs = {
            'shape': attrs.get('shape', 'ellipse'),
            'fillcolor': attrs.get('color', 'white'),
            'style': 'filled',
            'label': self._create_node_label(node, attrs)
        }
        
        # Special styling for different node types
        node_type = attrs.get('type', 'module')
        if node_type == 'nif_impl':
            node_attrs['shape'] = 'box'
            node_attrs['style'] = 'filled,rounded'
        elif node_type == 'supervisor':
            node_attrs['shape'] = 'diamond'
        elif node_type == 'application':
            node_attrs['shape'] = 'house'
            
        graph.node(node, **node_attrs)
    
    def _create_node_label(self, node: str, attrs: Dict) -> str:
        """Create detailed label for node"""
        label_parts = [node]
        
        behaviors = attrs.get('behaviors', [])
        if behaviors:
            label_parts.append(f"({', '.join(behaviors)})")
            
        nif_functions = attrs.get('nif_functions', [])
        if nif_functions:
            label_parts.append(f"NIFs: {len(nif_functions)}")
            
        native_functions = attrs.get('native_functions', [])
        if native_functions:
            label_parts.append(f"Native: {len(native_functions)}")
            
        return '\\n'.join(label_parts)
    
    def generate_communication_diagram(self, format: str = 'png', dpi: int = 300) -> str:
        """Generate communication pattern diagram"""
        logger.info("Generating communication diagram")
        
        dot = graphviz.Digraph(comment='Erlang Communication Patterns')
        dot.attr(rankdir='LR', size='12,8', dpi=str(dpi))
        dot.attr('node', fontname='Arial', fontsize='10')
        dot.attr('edge', fontname='Arial', fontsize='8')
        
        # Group modules by communication patterns
        patterns = self.data.get('communication_patterns', [])
        pattern_groups = {}
        
        for pattern in patterns:
            pattern_type = pattern.get('type', 'unknown')
            module = pattern.get('module', '')
            
            if pattern_type not in pattern_groups:
                pattern_groups[pattern_type] = []
            pattern_groups[pattern_type].append(pattern)
        
        # Create subgraphs for each pattern type
        for pattern_type, pattern_list in pattern_groups.items():
            with dot.subgraph(name=f'cluster_{pattern_type}') as cluster:
                cluster.attr(
                    label=f'{pattern_type.replace("_", " ").title()} Pattern',
                    color=self._get_pattern_color(pattern_type),
                    style='filled',
                    fillcolor=self._get_pattern_fill_color(pattern_type)
                )
                
                for pattern in pattern_list:
                    module = pattern.get('module', '')
                    cluster.node(
                        f"{module}_{pattern_type}",
                        label=f"{module}\\n{pattern.get('pattern', '')}",
                        shape=self._get_pattern_shape(pattern_type),
                        fillcolor=self._get_pattern_color(pattern_type),
                        style='filled'
                    )
        
        # Add communication arrows
        self._add_communication_edges(dot, patterns)
        
        output_path = self.output_dir / f'communication_diagram.{format}'
        dot.render(str(output_path.with_suffix('')), format=format, cleanup=True)
        
        return str(output_path)
    
    def _get_pattern_color(self, pattern_type: str) -> str:
        """Get color for communication pattern"""
        colors = {
            'gen_server': 'lightblue',
            'gen_statem': 'lightyellow',
            'http_handler': 'lightgreen',
            'nif': 'lightcoral',
            'supervisor': 'lightgray'
        }
        return colors.get(pattern_type, 'white')
    
    def _get_pattern_fill_color(self, pattern_type: str) -> str:
        """Get fill color for pattern cluster"""
        colors = {
            'gen_server': 'aliceblue',
            'gen_statem': 'lightyellow',
            'http_handler': 'honeydew',
            'nif': 'mistyrose',
            'supervisor': 'whitesmoke'
        }
        return colors.get(pattern_type, 'white')
    
    def _get_pattern_shape(self, pattern_type: str) -> str:
        """Get shape for communication pattern"""
        shapes = {
            'gen_server': 'ellipse',
            'gen_statem': 'diamond',
            'http_handler': 'box',
            'nif': 'hexagon',
            'supervisor': 'triangle'
        }
        return shapes.get(pattern_type, 'ellipse')
    
    def _add_communication_edges(self, dot: graphviz.Digraph, patterns: List[Dict]) -> None:
        """Add edges showing communication flows"""
        # This is a simplified version - in reality, we'd analyze actual message flows
        pattern_modules = {}
        for pattern in patterns:
            pattern_type = pattern.get('type', '')
            module = pattern.get('module', '')
            pattern_modules[pattern_type] = pattern_modules.get(pattern_type, []) + [module]
        
        # Add some typical communication flows
        if 'supervisor' in pattern_modules and 'gen_server' in pattern_modules:
            for sup_module in pattern_modules['supervisor']:
                for srv_module in pattern_modules['gen_server']:
                    if sup_module != srv_module:
                        dot.edge(
                            f"{sup_module}_supervisor",
                            f"{srv_module}_gen_server",
                            label='supervises',
                            color='green',
                            style='bold'
                        )
        
        if 'http_handler' in pattern_modules and 'gen_server' in pattern_modules:
            for http_module in pattern_modules['http_handler']:
                for srv_module in pattern_modules['gen_server']:
                    if http_module != srv_module:
                        dot.edge(
                            f"{http_module}_http_handler",
                            f"{srv_module}_gen_server",
                            label='calls',
                            color='blue',
                            style='dashed'
                        )
    
    def generate_behavior_hierarchy(self, format: str = 'png', dpi: int = 300) -> str:
        """Generate OTP behavior hierarchy diagram"""
        logger.info("Generating behavior hierarchy")
        
        dot = graphviz.Digraph(comment='OTP Behavior Hierarchy')
        dot.attr(rankdir='TB', size='10,12', dpi=str(dpi))
        dot.attr('node', fontname='Arial', fontsize='10', shape='box', style='rounded,filled')
        dot.attr('edge', fontname='Arial', fontsize='8')
        
        # Standard OTP behaviors
        otp_behaviors = {
            'application': {'color': 'lightblue', 'level': 0},
            'supervisor': {'color': 'lightgreen', 'level': 1},
            'gen_server': {'color': 'lightyellow', 'level': 2},
            'gen_statem': {'color': 'lightcoral', 'level': 2},
            'gen_event': {'color': 'lightgray', 'level': 2},
            'gen_fsm': {'color': 'lightpink', 'level': 2}
        }
        
        # Add OTP behavior nodes
        for behavior, attrs in otp_behaviors.items():
            dot.node(
                behavior,
                label=behavior.replace('_', '_\\n'),
                fillcolor=attrs['color'],
                rank=str(attrs['level'])
            )
        
        # Add project modules implementing behaviors
        modules = self.data.get('modules', {})
        for module_name, module_info in modules.items():
            behaviors = module_info.get('behaviors', [])
            if behaviors:
                module_color = self._get_node_color(module_info.get('type'), behaviors)
                dot.node(
                    module_name,
                    label=f"{module_name}\\n{', '.join(behaviors)}",
                    fillcolor=module_color,
                    shape='ellipse'
                )
                
                # Connect to implemented behaviors
                for behavior in behaviors:
                    if behavior in otp_behaviors:
                        dot.edge(behavior, module_name, label='implements', color='blue')
        
        # Add hierarchy edges
        dot.edge('application', 'supervisor', label='starts', color='green')
        dot.edge('supervisor', 'gen_server', label='supervises', color='green')
        dot.edge('supervisor', 'gen_statem', label='supervises', color='green')
        dot.edge('supervisor', 'gen_event', label='supervises', color='green')
        
        output_path = self.output_dir / f'behavior_hierarchy.{format}'
        dot.render(str(output_path.with_suffix('')), format=format, cleanup=True)
        
        return str(output_path)
    
    def generate_nif_diagram(self, format: str = 'png', dpi: int = 300) -> str:
        """Generate NIF implementation diagram"""
        logger.info("Generating NIF diagram")
        
        nifs = self.data.get('nifs', {})
        if not nifs:
            logger.info("No NIFs found, skipping NIF diagram")
            return ""
        
        dot = graphviz.Digraph(comment='NIF Implementation Diagram')
        dot.attr(rankdir='LR', size='12,8', dpi=str(dpi))
        dot.attr('node', fontname='Arial', fontsize='10')
        dot.attr('edge', fontname='Arial', fontsize='8')
        
        for nif_name, nif_info in nifs.items():
            erl_module = self._get_module_from_path(nif_info.get('erl_path', ''))
            
            # Add Erlang module node
            if erl_module:
                dot.node(
                    erl_module,
                    label=f"{erl_module}\\n(Erlang)",
                    shape='ellipse',
                    fillcolor='lightyellow',
                    style='filled'
                )
            
            # Add stub functions
            stub_functions = nif_info.get('stub_functions', [])
            if stub_functions:
                stub_label = "\\n".join(stub_functions[:5])  # Limit to first 5
                if len(stub_functions) > 5:
                    stub_label += f"\\n... +{len(stub_functions)-5} more"
                    
                dot.node(
                    f"{nif_name}_stubs",
                    label=f"Stub Functions\\n{stub_label}",
                    shape='box',
                    fillcolor='lightgray',
                    style='filled'
                )
                
                if erl_module:
                    dot.edge(erl_module, f"{nif_name}_stubs", label='exports', color='blue')
            
            # Add native implementation
            c_path = nif_info.get('c_path')
            cpp_path = nif_info.get('cpp_path')
            
            if c_path or cpp_path:
                impl_path = c_path or cpp_path
                impl_lang = 'C' if c_path else 'C++'
                impl_name = Path(impl_path).stem
                
                native_functions = nif_info.get('native_functions', [])
                native_label = "\\n".join(native_functions[:5])  # Limit to first 5
                if len(native_functions) > 5:
                    native_label += f"\\n... +{len(native_functions)-5} more"
                
                dot.node(
                    f"{nif_name}_impl",
                    label=f"{impl_name}\\n({impl_lang})\\n{native_label}",
                    shape='box',
                    fillcolor='lightcoral',
                    style='filled'
                )
                
                if stub_functions:
                    dot.edge(
                        f"{nif_name}_stubs",
                        f"{nif_name}_impl",
                        label='calls native',
                        color='red',
                        style='dashed'
                    )
        
        output_path = self.output_dir / f'nif_diagram.{format}'
        dot.render(str(output_path.with_suffix('')), format=format, cleanup=True)
        
        return str(output_path)
    
    def generate_all_graphs(self, format: str = 'png', dpi: int = 300) -> Dict[str, str]:
        """Generate all available graphs"""
        logger.info("Generating all graphs")
        
        graphs = {}
        
        try:
            graphs['dependency'] = self.generate_dependency_graph(format, dpi)
        except Exception as e:
            logger.error(f"Error generating dependency graph: {e}")
        
        try:
            graphs['communication'] = self.generate_communication_diagram(format, dpi)
        except Exception as e:
            logger.error(f"Error generating communication diagram: {e}")
        
        try:
            graphs['behavior_hierarchy'] = self.generate_behavior_hierarchy(format, dpi)
        except Exception as e:
            logger.error(f"Error generating behavior hierarchy: {e}")
        
        try:
            nif_graph = self.generate_nif_diagram(format, dpi)
            if nif_graph:
                graphs['nif'] = nif_graph
        except Exception as e:
            logger.error(f"Error generating NIF diagram: {e}")
        
        return graphs
