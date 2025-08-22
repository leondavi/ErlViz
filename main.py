#!/usr/bin/env python3
"""
ErlViz Main Entry Point
Launch the ErlViz GUI application for analyzing Erlang projects

Copyright (c) 2025 David Leon (leondavi)
Licensed under the MIT License - see LICENSE file for details.
"""

import sys
import os
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for ErlViz"""
    parser = argparse.ArgumentParser(
        description="ErlViz - Erlang Project Analyzer and Visualizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Launch GUI
  python main.py --cli /path/to/erlang/project    # Analyze project via CLI
  python main.py --cli https://github.com/user/repo # Analyze GitHub repo via CLI
        """
    )
    
    parser.add_argument(
        '--cli', 
        metavar='PROJECT_PATH',
        help='Run in CLI mode, analyze specified project path or Git URL'
    )
    
    parser.add_argument(
        '--output', '-o',
        metavar='OUTPUT_DIR',
        default='./erlviz_output',
        help='Output directory for analysis results (default: ./erlviz_output)'
    )
    
    parser.add_argument(
        '--format',
        choices=['png', 'svg', 'pdf'],
        default='png',
        help='Output format for graphs (default: png)'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        choices=[72, 96, 150, 300, 600, 1200],
        default=300,
        help='Resolution (DPI) for generated graphs (default: 300)'
    )
    
    parser.add_argument(
        '--no-graphs',
        action='store_true',
        help='Skip graph generation'
    )
    
    parser.add_argument(
        '--no-docs',
        action='store_true', 
        help='Skip documentation generation'
    )
    
    parser.add_argument(
        '--include-submodules',
        action='store_true',
        help='Include Git submodules in analysis'
    )
    
    parser.add_argument(
        '--include-external-deps',
        action='store_true',
        help='Include external dependencies in analysis (default: project modules only)'
    )
    
    parser.add_argument(
        '--exclude-dirs',
        nargs='*',
        default=[],
        help='Directories to exclude from analysis (e.g., --exclude-dirs test tests _build)'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable repository caching'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    import logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if args.cli:
        # CLI mode
        return run_cli_analysis(args)
    else:
        # GUI mode
        return run_gui()

def run_cli_analysis(args):
    """Run ErlViz in CLI mode"""
    try:
        from erlviz import ErlViz
        
        print(f"ErlViz - Analyzing: {args.cli}")
        print(f"Output directory: {args.output}")
        
        # Create ErlViz instance
        erlviz = ErlViz(output_dir=args.output)
        
        # Run analysis
        result = erlviz.analyze_repository(
            args.cli,
            include_submodules=args.include_submodules,
            use_cache=not args.no_cache,
            generate_graphs=not args.no_graphs,
            generate_docs=not args.no_docs,
            output_format=args.format,
            dpi=args.dpi,
            include_external_deps=args.include_external_deps,
            exclude_dirs=args.exclude_dirs
        )
        
        # Print summary
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        
        project_name = result.get('project_name', 'Unknown')
        stats = result.get('statistics', {})
        
        print(f"Project: {project_name}")
        print(f"Total Modules: {stats.get('total_modules', 0)}")
        print(f"Behavior Modules: {stats.get('behavior_modules', 0)}")
        print(f"NIF Modules: {stats.get('nif_modules', 0)}")
        print(f"Output Directory: {result.get('output_directory', 'Unknown')}")
        
        # List generated files
        generated_files = result.get('generated_files', {})
        
        graphs = generated_files.get('graphs', {})
        if graphs:
            print(f"\nGenerated Graphs ({len(graphs)}):")
            for graph_type, graph_path in graphs.items():
                print(f"  - {graph_type}: {graph_path}")
        
        docs = generated_files.get('documentation', {})
        if docs:
            print(f"\nGenerated Documentation ({len(docs)}):")
            for doc_type, doc_path in docs.items():
                print(f"  - {doc_type}: {doc_path}")
        
        # Key findings
        key_findings = result.get('key_findings', {})
        if key_findings:
            print(f"\nKey Findings:")
            arch_type = key_findings.get('architecture_type', 'Unknown')
            print(f"  - Architecture: {arch_type}")
            
            complexity = key_findings.get('complexity_indicators', {})
            complexity_level = complexity.get('complexity_level', 'Unknown')
            print(f"  - Complexity: {complexity_level}")
            
            otp_compliance = key_findings.get('otp_compliance', {})
            compliance_level = otp_compliance.get('compliance_level', 'Unknown')
            print(f"  - OTP Compliance: {compliance_level}")
        
        print("\nAnalysis completed successfully!")
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

def run_gui():
    """Run ErlViz in GUI mode"""
    try:
        from erlviz.gui import main as gui_main
        return gui_main()
    except ImportError as e:
        print(f"Error: GUI dependencies not available: {e}")
        print("Please install PySide6: pip install PySide6")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
