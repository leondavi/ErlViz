#!/usr/bin/env python3
"""
ErlViz Test Script
Quick test to verify ErlViz installation and basic functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all core modules can be imported"""
    print("Testing imports...")
    
    try:
        import erlviz
        print("✓ Main package imported successfully")
        
        from erlviz.core.analyzer import ErlangAnalyzer
        print("✓ ErlangAnalyzer imported")
        
        from erlviz.core.graph_generator import ErlangGraphGenerator
        print("✓ ErlangGraphGenerator imported")
        
        from erlviz.core.documentation_generator import ErlangDocumentationGenerator
        print("✓ ErlangDocumentationGenerator imported")
        
        from erlviz.core.repository_manager import RepositoryManager
        print("✓ RepositoryManager imported")
        
        from erlviz.core.erlviz import ErlViz
        print("✓ ErlViz main class imported")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_dependencies():
    """Test that required dependencies are available"""
    print("\nTesting dependencies...")
    
    dependencies = [
        ('git', 'GitPython'),
        ('graphviz', 'Graphviz Python package'),
        ('markdown', 'Markdown package'),
        ('requests', 'Requests package'),
        ('networkx', 'NetworkX package'),
        ('matplotlib', 'Matplotlib package'),
        ('pygments', 'Pygments package')
    ]
    
    all_good = True
    
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            print(f"✓ {description}")
        except ImportError:
            print(f"✗ {description} not found")
            all_good = False
    
    # Test GUI dependencies separately (optional)
    try:
        import PySide6
        print("✓ PySide6 (GUI support)")
    except ImportError:
        print("⚠ PySide6 not found (GUI will not work)")
    
    return all_good

def test_graphviz_system():
    """Test that system Graphviz is installed"""
    print("\nTesting system Graphviz...")
    
    import subprocess
    
    try:
        result = subprocess.run(['dot', '-V'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Graphviz system installation: {result.stderr.strip()}")
            return True
        else:
            print("✗ Graphviz system installation not found")
            return False
    except FileNotFoundError:
        print("✗ Graphviz 'dot' command not found in PATH")
        return False

def test_basic_functionality():
    """Test basic ErlViz functionality"""
    print("\nTesting basic functionality...")
    
    try:
        from erlviz import ErlViz
        
        # Create ErlViz instance
        erlviz = ErlViz(output_dir='./test_output')
        print("✓ ErlViz instance created")
        
        # Test analyzer
        from erlviz.core.analyzer import ErlangAnalyzer
        analyzer = ErlangAnalyzer('.')
        print("✓ ErlangAnalyzer instance created")
        
        # Test repository manager
        from erlviz.core.repository_manager import RepositoryManager
        repo_manager = RepositoryManager()
        print("✓ RepositoryManager instance created")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("ErlViz Installation Test")
    print("="*60)
    
    tests = [
        ("Core imports", test_imports),
        ("Dependencies", test_dependencies), 
        ("System Graphviz", test_graphviz_system),
        ("Basic functionality", test_basic_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! ErlViz is ready to use.")
        print("\nNext steps:")
        print("1. Activate virtual environment: source venv/bin/activate")
        print("2. Run GUI: python main.py")
        print("3. Or try CLI: python main.py --cli https://github.com/ninenines/cowboy")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("- Install missing Python packages: pip install <package>")
        print("- Install system Graphviz: brew install graphviz (macOS)")
        print("- Check virtual environment activation")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
