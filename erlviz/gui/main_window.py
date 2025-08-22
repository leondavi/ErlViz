"""
ErlViz GUI Application
PySide6-based graphical user interface for ErlViz

Copyright (c) 2025 David Leon (leondavi)
Licensed under the MIT License - see LICENSE file for details.
"""

import sys
import os
import json
import webbrowser
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QProgressBar, QSplitter,
    QTabWidget, QLabel, QFileDialog, QCheckBox, QComboBox,
    QTreeWidget, QTreeWidgetItem, QGroupBox, QGridLayout,
    QScrollArea, QMessageBox, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, QThread, QTimer, Signal, QUrl
from PySide6.QtGui import QFont, QPixmap, QDesktopServices
from PySide6.QtWebEngineWidgets import QWebEngineView

from ..core.erlviz import ErlViz

logger = logging.getLogger(__name__)

class AnalysisWorker(QThread):
    """Worker thread for running ErlViz analysis"""
    
    progress_updated = Signal(str)
    analysis_completed = Signal(dict)
    analysis_failed = Signal(str)
    
    def __init__(self, erlviz: ErlViz, repo_path: str, options: Dict[str, Any]):
        super().__init__()
        self.erlviz = erlviz
        self.repo_path = repo_path
        self.options = options
    
    def run(self):
        """Run the analysis in background thread"""
        try:
            self.progress_updated.emit("Starting analysis...")
            
            result = self.erlviz.analyze_repository(
                self.repo_path,
                include_submodules=self.options.get('include_submodules', False),
                use_cache=self.options.get('use_cache', True),
                generate_graphs=self.options.get('generate_graphs', True),
                generate_docs=self.options.get('generate_docs', True),
                output_format=self.options.get('output_format', 'png'),
                dpi=self.options.get('dpi', 300),
                include_external_deps=self.options.get('include_external_deps', False),
                exclude_dirs=self.options.get('exclude_dirs', [])
            )
            
            self.analysis_completed.emit(result)
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            self.analysis_failed.emit(str(e))

class ProjectOverviewWidget(QWidget):
    """Widget showing project overview information"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Project info
        self.project_info = QLabel("No project analyzed yet")
        self.project_info.setFont(QFont("Arial", 12))
        layout.addWidget(self.project_info)
        
        # Statistics
        stats_group = QGroupBox("Project Statistics")
        stats_layout = QGridLayout()
        
        self.stats_labels = {}
        stats_fields = [
            'total_modules', 'behavior_modules', 'supervisor_modules',
            'nif_modules', 'test_modules', 'applications'
        ]
        
        for i, field in enumerate(stats_fields):
            label = QLabel(field.replace('_', ' ').title() + ":")
            value = QLabel("0")
            value.setFont(QFont("Arial", 10, QFont.Bold))
            
            stats_layout.addWidget(label, i // 2, (i % 2) * 2)
            stats_layout.addWidget(value, i // 2, (i % 2) * 2 + 1)
            
            self.stats_labels[field] = value
            
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Key findings
        self.findings_text = QTextEdit()
        self.findings_text.setMaximumHeight(200)
        self.findings_text.setReadOnly(True)
        
        findings_group = QGroupBox("Key Findings")
        findings_layout = QVBoxLayout()
        findings_layout.addWidget(self.findings_text)
        findings_group.setLayout(findings_layout)
        layout.addWidget(findings_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def update_overview(self, analysis_result: Dict[str, Any]):
        """Update overview with analysis results"""
        # Update project info
        project_name = analysis_result.get('project_name', 'Unknown')
        analysis_time = analysis_result.get('analysis_timestamp', '')
        self.project_info.setText(f"Project: {project_name}\nAnalyzed: {analysis_time}")
        
        # Update statistics
        stats = analysis_result.get('statistics', {})
        for field, label in self.stats_labels.items():
            value = stats.get(field, 0)
            label.setText(str(value))
        
        # Update key findings
        findings = analysis_result.get('key_findings', {})
        findings_text = []
        
        arch_type = findings.get('architecture_type', 'Unknown')
        findings_text.append(f"Architecture: {arch_type}")
        
        complexity = findings.get('complexity_indicators', {})
        complexity_level = complexity.get('complexity_level', 'Unknown')
        findings_text.append(f"Complexity: {complexity_level}")
        
        otp_compliance = findings.get('otp_compliance', {})
        compliance_level = otp_compliance.get('compliance_level', 'Unknown')
        findings_text.append(f"OTP Compliance: {compliance_level}")
        
        doc_quality = findings.get('documentation_quality', {})
        doc_level = doc_quality.get('documentation_quality', 'Unknown')
        findings_text.append(f"Documentation: {doc_level}")
        
        perf_considerations = findings.get('performance_considerations', [])
        if perf_considerations:
            findings_text.append(f"Performance: {'; '.join(perf_considerations)}")
        
        self.findings_text.setText('\n\n'.join(findings_text))

class ModuleTreeWidget(QWidget):
    """Widget showing module hierarchy tree"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['Module', 'Type', 'Behaviors', 'Dependencies'])
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        layout.addWidget(self.tree)
        self.setLayout(layout)
    
    def update_modules(self, analysis_result: Dict[str, Any]):
        """Update module tree with analysis results"""
        self.tree.clear()
        
        modules = analysis_result.get('modules', {})
        
        # Group modules by type
        modules_by_type = {}
        for module_name, module_info in modules.items():
            module_type = module_info.get('type', 'module')
            if module_type not in modules_by_type:
                modules_by_type[module_type] = []
            modules_by_type[module_type].append((module_name, module_info))
        
        # Create tree structure
        for module_type, module_list in sorted(modules_by_type.items()):
            type_item = QTreeWidgetItem(self.tree)
            type_item.setText(0, f"{module_type.title()} Modules ({len(module_list)})")
            type_item.setExpanded(True)
            
            for module_name, module_info in sorted(module_list):
                module_item = QTreeWidgetItem(type_item)
                module_item.setText(0, module_name)
                module_item.setText(1, module_type)
                
                behaviors = module_info.get('behaviors', [])
                module_item.setText(2, ', '.join(behaviors))
                
                dependencies = module_info.get('dependencies', [])
                module_item.setText(3, f"{len(dependencies)} deps")
                
                # Store full module info
                module_item.setData(0, Qt.UserRole, module_info)
        
        # Resize columns
        for i in range(4):
            self.tree.resizeColumnToContents(i)
    
    def on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle double-click on tree item"""
        module_info = item.data(0, Qt.UserRole)
        if module_info:
            self.show_module_details(item.text(0), module_info)
    
    def show_module_details(self, module_name: str, module_info: Dict[str, Any]):
        """Show detailed module information in dialog"""
        dialog = ModuleDetailDialog(module_name, module_info, self)
        dialog.exec()

class ModuleDetailDialog(QDialog):
    """Dialog showing detailed module information"""
    
    def __init__(self, module_name: str, module_info: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.module_name = module_name
        self.module_info = module_info
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle(f"Module Details: {self.module_name}")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        # Module info
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        
        info_content = f"Module: {self.module_name}\n"
        info_content += f"Type: {self.module_info.get('type', 'unknown')}\n"
        info_content += f"Path: {self.module_info.get('path', 'unknown')}\n"
        
        behaviors = self.module_info.get('behaviors', [])
        if behaviors:
            info_content += f"Behaviors: {', '.join(behaviors)}\n"
        
        exports = self.module_info.get('exports', [])
        if exports:
            info_content += f"\nExported Functions ({len(exports)}):\n"
            info_content += '\n'.join(f"  - {exp}" for exp in exports[:20])
            if len(exports) > 20:
                info_content += f"\n  ... and {len(exports) - 20} more"
        
        dependencies = self.module_info.get('dependencies', [])
        if dependencies:
            info_content += f"\n\nDependencies ({len(dependencies)}):\n"
            info_content += '\n'.join(f"  - {dep}" for dep in dependencies)
        
        functions = self.module_info.get('functions', {})
        if functions:
            info_content += f"\n\nDocumented Functions ({len(functions)}):\n"
            for func_name, func_info in functions.items():
                args = func_info.get('args', '')
                doc = func_info.get('documentation', '')
                info_content += f"  - {func_name}({args})"
                if doc:
                    info_content += f": {doc}"
                info_content += "\n"
        
        documentation = self.module_info.get('documentation', '')
        if documentation:
            info_content += f"\n\nModule Documentation:\n{documentation}"
        
        info_text.setText(info_content)
        layout.addWidget(info_text)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

class GraphViewWidget(QWidget):
    """Widget for viewing generated graphs"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.graphs = {}
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Graph selection
        self.graph_combo = QComboBox()
        self.graph_combo.currentTextChanged.connect(self.load_graph)
        layout.addWidget(self.graph_combo)
        
        # Graph display
        self.scroll_area = QScrollArea()
        self.graph_label = QLabel("No graph selected")
        self.graph_label.setAlignment(Qt.AlignCenter)
        self.graph_label.setMinimumSize(400, 300)
        
        self.scroll_area.setWidget(self.graph_label)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)
        
        # Open in external viewer button
        self.open_external_btn = QPushButton("Open in External Viewer")
        self.open_external_btn.clicked.connect(self.open_external)
        self.open_external_btn.setEnabled(False)
        layout.addWidget(self.open_external_btn)
        
        self.setLayout(layout)
    
    def update_graphs(self, analysis_result: Dict[str, Any]):
        """Update available graphs"""
        self.graphs = analysis_result.get('generated_files', {}).get('graphs', {})
        
        self.graph_combo.clear()
        self.graph_combo.addItems(list(self.graphs.keys()))
        
        if self.graphs:
            self.load_graph(list(self.graphs.keys())[0])
    
    def load_graph(self, graph_name: str):
        """Load and display selected graph"""
        if not graph_name or graph_name not in self.graphs:
            return
            
        graph_path = self.graphs[graph_name]
        
        if Path(graph_path).exists():
            pixmap = QPixmap(graph_path)
            if not pixmap.isNull():
                # Scale pixmap to fit in widget while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    self.scroll_area.size() - self.scroll_area.frameSize(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.graph_label.setPixmap(scaled_pixmap)
                self.open_external_btn.setEnabled(True)
            else:
                self.graph_label.setText(f"Could not load graph: {graph_name}")
                self.open_external_btn.setEnabled(False)
        else:
            self.graph_label.setText(f"Graph file not found: {graph_path}")
            self.open_external_btn.setEnabled(False)
    
    def open_external(self):
        """Open current graph in external viewer"""
        current_graph = self.graph_combo.currentText()
        if current_graph and current_graph in self.graphs:
            graph_path = self.graphs[current_graph]
            QDesktopServices.openUrl(QUrl.fromLocalFile(graph_path))

class DocumentationViewWidget(QWidget):
    """Widget for viewing generated documentation"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.docs = {}
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Documentation selection
        controls_layout = QHBoxLayout()
        
        self.doc_combo = QComboBox()
        self.doc_combo.currentTextChanged.connect(self.load_document)
        controls_layout.addWidget(QLabel("Document:"))
        controls_layout.addWidget(self.doc_combo)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(['HTML', 'Markdown'])
        self.format_combo.currentTextChanged.connect(self.load_document)
        controls_layout.addWidget(QLabel("Format:"))
        controls_layout.addWidget(self.format_combo)
        
        controls_layout.addStretch()
        
        self.open_external_btn = QPushButton("Open in Browser")
        self.open_external_btn.clicked.connect(self.open_external)
        self.open_external_btn.setEnabled(False)
        controls_layout.addWidget(self.open_external_btn)
        
        layout.addLayout(controls_layout)
        
        # Document display
        self.doc_view = QWebEngineView()
        layout.addWidget(self.doc_view)
        
        self.setLayout(layout)
    
    def update_documentation(self, analysis_result: Dict[str, Any]):
        """Update available documentation"""
        all_docs = analysis_result.get('generated_files', {}).get('documentation', {})
        
        # Group by document type
        self.docs = {}
        for doc_key, doc_path in all_docs.items():
            if doc_key.endswith('_md') or doc_key.endswith('_html'):
                doc_type = doc_key.rsplit('_', 1)[0]
                format_type = doc_key.rsplit('_', 1)[1]
                
                if doc_type not in self.docs:
                    self.docs[doc_type] = {}
                self.docs[doc_type][format_type] = doc_path
        
        self.doc_combo.clear()
        self.doc_combo.addItems(list(self.docs.keys()))
        
        if self.docs:
            self.load_document()
    
    def load_document(self):
        """Load and display selected document"""
        doc_type = self.doc_combo.currentText()
        format_type = self.format_combo.currentText().lower()
        
        if not doc_type or doc_type not in self.docs:
            return
            
        if format_type not in self.docs[doc_type]:
            # Try the other format
            available_formats = list(self.docs[doc_type].keys())
            if available_formats:
                format_type = available_formats[0]
            else:
                return
        
        doc_path = self.docs[doc_type][format_type]
        
        if Path(doc_path).exists():
            url = QUrl.fromLocalFile(str(Path(doc_path).absolute()))
            self.doc_view.load(url)
            self.open_external_btn.setEnabled(True)
        else:
            self.doc_view.setHtml(f"<h1>Document not found</h1><p>{doc_path}</p>")
            self.open_external_btn.setEnabled(False)
    
    def open_external(self):
        """Open current document in external browser"""
        doc_type = self.doc_combo.currentText()
        format_type = self.format_combo.currentText().lower()
        
        if doc_type and doc_type in self.docs and format_type in self.docs[doc_type]:
            doc_path = self.docs[doc_type][format_type]
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path(doc_path).absolute())))

class ErlVizMainWindow(QMainWindow):
    """Main ErlViz application window"""
    
    def __init__(self):
        super().__init__()
        self.erlviz = None
        self.analysis_worker = None
        self.current_result = None
        
        self.setup_ui()
        self.setup_menu()
        
        # Set window properties
        self.setWindowTitle("ErlViz - Erlang Project Analyzer")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Input section
        input_group = QGroupBox("Project Input")
        input_layout = QVBoxLayout()
        
        # Repository path/URL
        repo_layout = QHBoxLayout()
        repo_layout.addWidget(QLabel("Repository URL or Path:"))
        
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("https://github.com/user/repo or /path/to/local/repo")
        repo_layout.addWidget(self.repo_input)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_repository)
        repo_layout.addWidget(self.browse_btn)
        
        input_layout.addLayout(repo_layout)
        
        # Options
        options_layout = QHBoxLayout()
        
        self.include_submodules_cb = QCheckBox("Include Submodules")
        options_layout.addWidget(self.include_submodules_cb)
        
        self.include_external_deps_cb = QCheckBox("Include External Dependencies")
        self.include_external_deps_cb.setToolTip("Include external library dependencies in analysis (default: project modules only)")
        options_layout.addWidget(self.include_external_deps_cb)
        
        self.use_cache_cb = QCheckBox("Use Cache")
        self.use_cache_cb.setChecked(True)
        options_layout.addWidget(self.use_cache_cb)
        
        self.generate_graphs_cb = QCheckBox("Generate Graphs")
        self.generate_graphs_cb.setChecked(True)
        options_layout.addWidget(self.generate_graphs_cb)
        
        self.generate_docs_cb = QCheckBox("Generate Documentation")
        self.generate_docs_cb.setChecked(True)
        options_layout.addWidget(self.generate_docs_cb)
        
        options_layout.addWidget(QLabel("Output Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(['png', 'svg', 'pdf'])
        options_layout.addWidget(self.format_combo)
        
        options_layout.addWidget(QLabel("Resolution (DPI):"))
        self.dpi_combo = QComboBox()
        self.dpi_combo.addItems(['72', '96', '150', '300', '600', '1200'])
        self.dpi_combo.setCurrentText('300')  # Default to 300 DPI
        options_layout.addWidget(self.dpi_combo)
        
        options_layout.addWidget(QLabel("Exclude Directories:"))
        self.exclude_dirs_input = QLineEdit()
        self.exclude_dirs_input.setPlaceholderText("test tests _build (space-separated)")
        options_layout.addWidget(self.exclude_dirs_input)
        
        options_layout.addStretch()
        
        input_layout.addLayout(options_layout)
        
        # Output directory
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output Directory:"))
        
        self.output_input = QLineEdit()
        self.output_input.setText("./erlviz_output")
        output_layout.addWidget(self.output_input)
        
        self.browse_output_btn = QPushButton("Browse...")
        self.browse_output_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(self.browse_output_btn)
        
        input_layout.addLayout(output_layout)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.analyze_btn = QPushButton("Analyze Project")
        self.analyze_btn.clicked.connect(self.start_analysis)
        button_layout.addWidget(self.analyze_btn)
        
        self.stop_btn = QPushButton("Stop Analysis")
        self.stop_btn.clicked.connect(self.stop_analysis)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        button_layout.addStretch()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        button_layout.addWidget(self.progress_bar)
        
        layout.addLayout(button_layout)
        
        # Progress/status
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        # Results tabs
        self.tabs = QTabWidget()
        
        # Overview tab
        self.overview_widget = ProjectOverviewWidget()
        self.tabs.addTab(self.overview_widget, "Overview")
        
        # Modules tab
        self.modules_widget = ModuleTreeWidget()
        self.tabs.addTab(self.modules_widget, "Modules")
        
        # Graphs tab
        self.graphs_widget = GraphViewWidget()
        self.tabs.addTab(self.graphs_widget, "Graphs")
        
        # Documentation tab
        self.docs_widget = DocumentationViewWidget()
        self.tabs.addTab(self.docs_widget, "Documentation")
        
        layout.addWidget(self.tabs)
        
        central_widget.setLayout(layout)
    
    def setup_menu(self):
        """Setup application menu"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        file_menu.addAction('Open Project...', self.browse_repository)
        file_menu.addSeparator()
        file_menu.addAction('Export Results...', self.export_results)
        file_menu.addSeparator()
        file_menu.addAction('Exit', self.close)
        
        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        tools_menu.addAction('Clear Cache', self.clear_cache)
        tools_menu.addAction('Settings...', self.show_settings)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        help_menu.addAction('About ErlViz', self.show_about)
    
    def browse_repository(self):
        """Browse for repository directory"""
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Select Erlang Project Directory",
            self.repo_input.text() or str(Path.home())
        )
        
        if directory:
            self.repo_input.setText(directory)
    
    def browse_output(self):
        """Browse for output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory", 
            self.output_input.text() or "./erlviz_output"
        )
        
        if directory:
            self.output_input.setText(directory)
    
    def start_analysis(self):
        """Start project analysis"""
        repo_path = self.repo_input.text().strip()
        if not repo_path:
            QMessageBox.warning(self, "Warning", "Please enter a repository URL or path")
            return
        
        output_dir = self.output_input.text().strip()
        if not output_dir:
            output_dir = "./erlviz_output"
        
        # Setup ErlViz
        self.erlviz = ErlViz(output_dir=output_dir)
        
        # Prepare options
        exclude_dirs_text = self.exclude_dirs_input.text().strip()
        exclude_dirs = exclude_dirs_text.split() if exclude_dirs_text else []
        
        options = {
            'include_submodules': self.include_submodules_cb.isChecked(),
            'include_external_deps': self.include_external_deps_cb.isChecked(),
            'use_cache': self.use_cache_cb.isChecked(),
            'generate_graphs': self.generate_graphs_cb.isChecked(),
            'generate_docs': self.generate_docs_cb.isChecked(),
            'output_format': self.format_combo.currentText(),
            'dpi': int(self.dpi_combo.currentText()),
            'exclude_dirs': exclude_dirs
        }
        
        # Start analysis in worker thread
        self.analysis_worker = AnalysisWorker(self.erlviz, repo_path, options)
        self.analysis_worker.progress_updated.connect(self.update_progress)
        self.analysis_worker.analysis_completed.connect(self.analysis_completed)
        self.analysis_worker.analysis_failed.connect(self.analysis_failed)
        
        self.analysis_worker.start()
        
        # Update UI
        self.analyze_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        self.status_text.append(f"Starting analysis of: {repo_path}")
    
    def stop_analysis(self):
        """Stop running analysis"""
        if self.analysis_worker and self.analysis_worker.isRunning():
            self.analysis_worker.terminate()
            self.analysis_worker.wait(3000)  # Wait up to 3 seconds
            
        self.reset_ui_after_analysis()
        self.status_text.append("Analysis stopped by user")
    
    def update_progress(self, message: str):
        """Update progress message"""
        self.status_text.append(message)
        
        # Auto-scroll to bottom
        cursor = self.status_text.textCursor()
        cursor.movePosition(cursor.End)
        self.status_text.setTextCursor(cursor)
    
    def analysis_completed(self, result: Dict[str, Any]):
        """Handle completed analysis"""
        self.current_result = result
        self.reset_ui_after_analysis()
        
        self.status_text.append("Analysis completed successfully!")
        
        # Update result tabs
        self.overview_widget.update_overview(result)
        self.modules_widget.update_modules(result)
        self.graphs_widget.update_graphs(result)
        self.docs_widget.update_documentation(result)
        
        # Show success message
        project_name = result.get('project_name', 'Project')
        stats = result.get('statistics', {})
        total_modules = stats.get('total_modules', 0)
        
        QMessageBox.information(
            self,
            "Analysis Complete",
            f"Successfully analyzed {project_name}\n"
            f"Found {total_modules} modules\n"
            f"Results saved to: {result.get('output_directory', 'Unknown')}"
        )
    
    def analysis_failed(self, error_message: str):
        """Handle failed analysis"""
        self.reset_ui_after_analysis()
        
        self.status_text.append(f"Analysis failed: {error_message}")
        
        QMessageBox.critical(
            self,
            "Analysis Failed",
            f"Analysis failed with error:\n{error_message}"
        )
    
    def reset_ui_after_analysis(self):
        """Reset UI state after analysis completion"""
        self.analyze_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        if self.analysis_worker:
            self.analysis_worker.deleteLater()
            self.analysis_worker = None
    
    def export_results(self):
        """Export analysis results"""
        if not self.current_result:
            QMessageBox.information(self, "No Results", "No analysis results to export")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Analysis Results",
            "erlviz_results.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.current_result, f, indent=2, default=str)
                
                QMessageBox.information(
                    self,
                    "Export Complete",
                    f"Results exported to: {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Failed to export results:\n{e}"
                )
    
    def clear_cache(self):
        """Clear repository cache"""
        reply = QMessageBox.question(
            self,
            "Clear Cache",
            "Are you sure you want to clear the repository cache?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.erlviz:
                self.erlviz.repo_manager.cleanup_cache(0)  # Remove all
            
            QMessageBox.information(self, "Cache Cleared", "Repository cache has been cleared")
    
    def show_settings(self):
        """Show settings dialog"""
        QMessageBox.information(self, "Settings", "Settings dialog not implemented yet")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About ErlViz",
            "ErlViz - Erlang Project Analyzer\n\n"
            "A tool for analyzing Erlang/OTP projects to generate:\n"
            "• Dependency graphs\n"
            "• Communication diagrams\n"
            "• Documentation\n"
            "• NIF analysis\n\n"
            "Built with Python and PySide6"
        )

class ErlVizApplication(QApplication):
    """Main ErlViz application class"""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # Set application properties
        self.setApplicationName("ErlViz")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("ErlViz")
        
        # Setup logging
        self.setup_logging()
        
        # Create main window
        self.main_window = ErlVizMainWindow()
    
    def setup_logging(self):
        """Setup application logging"""
        log_dir = Path.home() / '.erlviz' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / 'erlviz.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def run(self):
        """Run the application"""
        self.main_window.show()
        return self.exec()

def main():
    """Main entry point for ErlViz GUI"""
    app = ErlVizApplication(sys.argv)
    return app.run()

if __name__ == '__main__':
    sys.exit(main())
