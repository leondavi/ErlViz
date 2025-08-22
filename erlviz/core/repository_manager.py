"""
ErlViz Repository Manager
Handles cloning and managing Git repositories for analysis
"""

import git
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
import requests
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class RepositoryManager:
    """Manages Git repository operations for ErlViz"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / '.erlviz' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def get_repository(self, repo_url: str, use_cache: bool = True) -> Optional[str]:
        """
        Get a repository, either from cache or by cloning
        Returns the local path to the repository
        """
        try:
            repo_name = self._extract_repo_name(repo_url)
            local_path = self.cache_dir / repo_name
            
            if use_cache and local_path.exists():
                logger.info(f"Using cached repository: {local_path}")
                # Try to update if it's a git repository
                try:
                    repo = git.Repo(local_path)
                    repo.remotes.origin.pull()
                    logger.info("Repository updated from remote")
                except Exception as e:
                    logger.warning(f"Could not update repository: {e}")
                return str(local_path)
            
            # Clone repository
            logger.info(f"Cloning repository: {repo_url}")
            repo = git.Repo.clone_from(repo_url, local_path)
            logger.info(f"Repository cloned to: {local_path}")
            
            # Handle submodules
            if self._has_submodules(local_path):
                self._handle_submodules(repo, local_path)
            
            return str(local_path)
            
        except Exception as e:
            logger.error(f"Error getting repository {repo_url}: {e}")
            return None
    
    def _extract_repo_name(self, repo_url: str) -> str:
        """Extract repository name from URL"""
        parsed = urlparse(repo_url)
        path = parsed.path.strip('/')
        
        if path.endswith('.git'):
            path = path[:-4]
            
        # Handle GitHub URLs
        if 'github.com' in parsed.netloc:
            parts = path.split('/')
            if len(parts) >= 2:
                return f"{parts[0]}_{parts[1]}"
        
        # Fallback to last path component
        return path.split('/')[-1] or 'repository'
    
    def _has_submodules(self, repo_path: Path) -> bool:
        """Check if repository has submodules"""
        gitmodules_path = repo_path / '.gitmodules'
        return gitmodules_path.exists()
    
    def _handle_submodules(self, repo: git.Repo, repo_path: Path, include_private: bool = False) -> None:
        """Handle git submodules"""
        try:
            logger.info("Initializing submodules")
            
            # Read .gitmodules to check submodule accessibility
            gitmodules_path = repo_path / '.gitmodules'
            accessible_submodules = []
            
            if gitmodules_path.exists():
                with open(gitmodules_path, 'r') as f:
                    content = f.read()
                    
                # Extract submodule URLs
                import re
                url_pattern = r'url\s*=\s*(.+)'
                urls = re.findall(url_pattern, content)
                
                for url in urls:
                    url = url.strip()
                    if self._is_submodule_accessible(url, include_private):
                        accessible_submodules.append(url)
                    else:
                        logger.warning(f"Skipping inaccessible submodule: {url}")
            
            # Initialize and update accessible submodules
            if accessible_submodules:
                repo.git.submodule('init')
                repo.git.submodule('update')
                logger.info(f"Updated {len(accessible_submodules)} submodules")
            else:
                logger.info("No accessible submodules found")
                
        except Exception as e:
            logger.warning(f"Error handling submodules: {e}")
    
    def _is_submodule_accessible(self, submodule_url: str, include_private: bool) -> bool:
        """Check if a submodule is publicly accessible"""
        try:
            # Skip private repositories unless explicitly included
            if not include_private and any(host in submodule_url for host in ['private', 'internal']):
                return False
            
            # For HTTP/HTTPS URLs, try a HEAD request
            if submodule_url.startswith(('http://', 'https://')):
                # Convert to GitHub API URL if it's a GitHub repo
                if 'github.com' in submodule_url:
                    api_url = self._github_url_to_api(submodule_url)
                    if api_url:
                        response = requests.head(api_url, timeout=10)
                        return response.status_code == 200
                
                # Try direct access
                response = requests.head(submodule_url, timeout=10)
                return response.status_code == 200
            
            # For SSH URLs, assume accessible if include_private is True
            if submodule_url.startswith('git@'):
                return include_private
            
            return True
            
        except Exception:
            return False
    
    def _github_url_to_api(self, github_url: str) -> Optional[str]:
        """Convert GitHub URL to API URL"""
        try:
            parsed = urlparse(github_url)
            if 'github.com' not in parsed.netloc:
                return None
                
            path = parsed.path.strip('/')
            if path.endswith('.git'):
                path = path[:-4]
                
            parts = path.split('/')
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
                return f"https://api.github.com/repos/{owner}/{repo}"
                
        except Exception:
            pass
        
        return None
    
    def analyze_repository_structure(self, repo_path: str) -> Dict[str, Any]:
        """Analyze repository structure and metadata"""
        repo_path = Path(repo_path)
        
        structure = {
            'path': str(repo_path),
            'name': repo_path.name,
            'is_erlang_project': False,
            'build_system': None,
            'source_directories': [],
            'test_directories': [],
            'documentation': {},
            'submodules': []
        }
        
        # Check if it's an Erlang project
        erlang_indicators = [
            'rebar.config',
            'rebar3.config', 
            'Makefile',
            'erlang.mk',
            'src/**/*.erl',
            'apps/**/src/**/*.erl'
        ]
        
        for indicator in erlang_indicators:
            if list(repo_path.glob(indicator)):
                structure['is_erlang_project'] = True
                break
        
        # Determine build system
        if (repo_path / 'rebar.config').exists() or (repo_path / 'rebar3.config').exists():
            structure['build_system'] = 'rebar3'
        elif (repo_path / 'Makefile').exists():
            if (repo_path / 'erlang.mk').exists():
                structure['build_system'] = 'erlang.mk'
            else:
                structure['build_system'] = 'make'
        
        # Find source directories
        src_patterns = ['src', 'src_erl', 'apps/*/src', 'lib/*/src']
        for pattern in src_patterns:
            src_dirs = list(repo_path.glob(pattern))
            structure['source_directories'].extend([str(d) for d in src_dirs if d.is_dir()])
        
        # Find test directories
        test_patterns = ['test', 'tests', 'apps/*/test', 'lib/*/test']
        for pattern in test_patterns:
            test_dirs = list(repo_path.glob(pattern))
            structure['test_directories'].extend([str(d) for d in test_dirs if d.is_dir()])
        
        # Find documentation
        doc_files = {
            'readme': self._find_readme(repo_path),
            'changelog': self._find_file(repo_path, ['CHANGELOG', 'CHANGES', 'HISTORY']),
            'license': self._find_file(repo_path, ['LICENSE', 'LICENCE', 'COPYING']),
            'contributing': self._find_file(repo_path, ['CONTRIBUTING', 'CONTRIBUTE']),
            'doc_dir': str(repo_path / 'doc') if (repo_path / 'doc').exists() else None
        }
        structure['documentation'] = {k: v for k, v in doc_files.items() if v}
        
        # Find submodules
        if (repo_path / '.gitmodules').exists():
            structure['submodules'] = self._parse_gitmodules(repo_path / '.gitmodules')
        
        return structure
    
    def _find_readme(self, repo_path: Path) -> Optional[str]:
        """Find README file"""
        readme_patterns = ['README*', 'readme*', 'Readme*']
        for pattern in readme_patterns:
            readme_files = list(repo_path.glob(pattern))
            if readme_files:
                return str(readme_files[0])
        return None
    
    def _find_file(self, repo_path: Path, names: list) -> Optional[str]:
        """Find file by multiple possible names"""
        for name in names:
            for ext in ['', '.md', '.txt', '.rst']:
                file_path = repo_path / f"{name}{ext}"
                if file_path.exists():
                    return str(file_path)
        return None
    
    def _parse_gitmodules(self, gitmodules_path: Path) -> list:
        """Parse .gitmodules file"""
        submodules = []
        
        try:
            with open(gitmodules_path, 'r') as f:
                content = f.read()
            
            import re
            
            # Parse submodule sections
            sections = re.split(r'\[submodule\s+"([^"]+)"\]', content)[1:]
            
            for i in range(0, len(sections), 2):
                if i + 1 < len(sections):
                    name = sections[i]
                    config = sections[i + 1]
                    
                    # Extract path and url
                    path_match = re.search(r'path\s*=\s*(.+)', config)
                    url_match = re.search(r'url\s*=\s*(.+)', config)
                    
                    if path_match and url_match:
                        submodules.append({
                            'name': name.strip(),
                            'path': path_match.group(1).strip(),
                            'url': url_match.group(1).strip()
                        })
                        
        except Exception as e:
            logger.error(f"Error parsing .gitmodules: {e}")
        
        return submodules
    
    def cleanup_cache(self, max_age_days: int = 30) -> None:
        """Clean up old cached repositories"""
        import time
        
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60
        
        for repo_dir in self.cache_dir.iterdir():
            if repo_dir.is_dir():
                repo_age = current_time - repo_dir.stat().st_mtime
                if repo_age > max_age_seconds:
                    logger.info(f"Cleaning up old repository: {repo_dir}")
                    shutil.rmtree(repo_dir)
    
    def get_repository_info(self, repo_path: str) -> Dict[str, Any]:
        """Get detailed information about a repository"""
        repo_path = Path(repo_path)
        
        info = {
            'path': str(repo_path),
            'exists': repo_path.exists(),
            'is_git_repo': False,
            'remote_url': None,
            'branch': None,
            'commit_hash': None,
            'commit_message': None,
            'is_dirty': False
        }
        
        if not repo_path.exists():
            return info
        
        try:
            repo = git.Repo(repo_path)
            info['is_git_repo'] = True
            info['is_dirty'] = repo.is_dirty()
            
            # Get remote URL
            if repo.remotes:
                info['remote_url'] = list(repo.remotes.origin.urls)[0]
            
            # Get current branch
            if not repo.head.is_detached:
                info['branch'] = repo.active_branch.name
            
            # Get latest commit
            latest_commit = repo.head.commit
            info['commit_hash'] = latest_commit.hexsha[:8]
            info['commit_message'] = latest_commit.message.strip()
            
        except Exception as e:
            logger.warning(f"Error getting repository info: {e}")
        
        return info
