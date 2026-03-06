#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Git repository operation wrapper module - Support parallel processing of multiple repositories
"""

import os
from datetime import datetime, timedelta
from typing import List
from git.repo import Repo
from collections import OrderedDict
from tqdm import tqdm

class GitAnalyzer:
    """Git repository operation wrapper class, supports handling multiple repositories simultaneously"""
    
    def __init__(self, repository_paths: List[str]):
        """
        Initialize Git repository wrapper
        
        Args:
            repository_paths: List of Git repository paths, use list even for single repository
        """
        # Ensure input is list type
        if not isinstance(repository_paths, list):
            raise TypeError("repository_paths must be list type, even for single repository")
            
        self.repository_paths = repository_paths
        
        # Initialize logger
        self.logger = self._create_logger()
        self.logger.info(f"Initializing GitWrapper, processing {len(self.repository_paths)} repositories")
        
        # Load all repositories
        self.repo_meta = OrderedDict()  # Dictionary: {path: repository object}
        self._load_repositories()
        
        # self.all_commits stores commit records for all repositories using nested dictionary structure:
        # {
        #   repository_name: {
        #     commit_hash: {
        #       "commit_repo": repository name,
        #       "commit_hash": commit hash,
        #       "commit_summary": commit summary,
        #       "commit_message": full commit message,
        #       "commit_author": author name,
        #       "commit_email": author email,
        #       "commit_date": commit creation datetime,
        #       "commit_committed_time": commit submission datetime,
        #       "commit_files_changed": number of changed files,
        #       "commit_insertions": lines inserted,
        #       "commit_deletions": lines deleted,
        #       "commit_has_deleted_files": whether files were deleted,
        #       "commit_has_new_files": whether new files were added,
        #       "commit_has_renamed_files": whether files were renamed,
        #       "commit_changed_files": list of changed files,
        #       "commit_diff_text": code diff text content
        #     }
        #   }
        # }
        self.all_commits = OrderedDict()
        
    
    def _create_logger(self):
        """Create logger"""
        from .clog import Logger
        return Logger(name="git_wrapper", level="info").logger
    
    def _load_repositories(self):
        """Load all repositories"""
        for repo_path in self.repository_paths:
            repo = Repo(repo_path)
            repo_name = os.path.basename(os.path.abspath(repo_path))
            self.repo_meta[repo_name] = repo
            self.logger.info(f"\tLoaded repository: {repo_name}, path: {repo_path}")

    def generate_commit_url(self, repo_url, commit_id):
        """Generate an HTTPS URL to view specific commit in remote repository"""
        try:
            # Remove 'https://' prefix if exists for standardized parsing
            if repo_url.startswith("https://"):
                repo_path = repo_url.rsplit(".git", 1)[0]
                https_url = f"{repo_path}/-/commit/{commit_id[:7]}"
            else:
                parts = repo_url.split("@")[-1].split(":")  # Get host and path components
                host = parts[0].split("/")[0]  # Extract hostname only, remove port
                repo_path_parts = parts[1].split("/")
                repo_path = "/".join(repo_path_parts[1:]).rsplit(".git", 1)[0]
                https_url = f"https://{host}/{repo_path}/-/commit/{commit_id[:7]}"
            return https_url
        except Exception:
            return ""
    
    def get_all_commits(self, days_back):
        """
        Get commit records within specified time range
        
        Args:
            days_back: How many days back to query commit records
            author_emails: Filter by author emails
            author_names: Filter by author names
            repo_path: Specify repository path, defaults to all repositories
            
        Returns:
            List of commit records
        """
        since_date = datetime.now() - timedelta(days=days_back)
        
        # Iterate through all repositories to collect commit information
        
        for repo_name, repo in tqdm(self.repo_meta.items(), desc="Processing repositories progress"):
            self.all_commits[repo_name] = OrderedDict()
            
            try:
                # Try to get the active branch
                # This handles normal repositories with a current branch
                branch = repo.active_branch
                all_commits = list(repo.iter_commits(branch, since=since_date, no_merges=True))
            except TypeError:
                # Handle detached HEAD state (when not on any branch)
                # This prevents errors when in a detached HEAD state, such as when checking out a specific commit
                branch = repo.head.commit
                all_commits = list(repo.iter_commits(branch, since=since_date, no_merges=True))
            
            for commit in tqdm(all_commits, desc=f"Processing {repo_name} commit records"):
                # Store commit information in variables
                commit_id = commit.hexsha[:7]
                commit_author_name = commit.author.name
                commit_author_email = commit.author.email
                commit_authored_time = commit.authored_datetime
                commit_summary = commit.summary
                commit_files_changed = len(commit.stats.files)
                commit_insertions = commit.stats.total['insertions']
                commit_deletions = commit.stats.total['deletions']
                commit_tree_hexsha = commit.tree.hexsha
                commit_committed_time = datetime.fromtimestamp(commit.committed_date)
                commit_encoding = commit.encoding
                commit_type = commit.type
                commit_message = commit.message
                
                # Check if commit has deleted, new or renamed files
                commit_has_deleted_files = False
                commit_has_new_files = False
                commit_has_renamed_files = False
                commit_changed_files = []
                
                # Get parent commit
                parent_commit = None
                if commit.parents:
                    parent_commit = commit.parents[0]
                    # Iterate through diff items to check file status
                    for diff_item in commit.diff(parent_commit):
                        if diff_item.deleted_file:
                            commit_has_deleted_files = True
                        if diff_item.new_file:
                            commit_has_new_files = True
                        if diff_item.renamed:
                            commit_has_renamed_files = True
                        # Record changed files
                        commit_changed_files.append(diff_item.b_path if diff_item.b_path else diff_item.a_path)
                
                commit_diffs_txt = ""
                parent_commit = commit.parents[0] if commit.parents else None
                if parent_commit:
                    for diff_item in parent_commit.diff(commit, create_patch=True, unified=20, function_context=True):
                        if diff_item.diff:
                            diff_text = diff_item.diff.decode('utf-8', errors='replace')
                            commit_diffs_txt += diff_text
                    



                remote_url = repo.remotes.origin.url if repo.remotes else ""
                commit_url = self.generate_commit_url(remote_url, commit.hexsha)

                self.all_commits[repo_name][str(commit_id)] = {
                    "commit_repo": repo_name,
                    "commit_hash": commit_id,
                    "commit_summary": commit_summary,
                    "commit_message": commit_message.strip(),
                    "commit_author": commit_author_name,
                    "commit_email": commit_author_email,
                    "commit_date": commit_authored_time,
                    "commit_committed_time": commit_committed_time,
                    "commit_files_changed": commit_files_changed,
                    "commit_insertions": commit_insertions,
                    "commit_deletions": commit_deletions,
                    "commit_has_deleted_files": commit_has_deleted_files,
                    "commit_has_new_files": commit_has_new_files,
                    "commit_has_renamed_files": commit_has_renamed_files,
                    "commit_changed_files": commit_changed_files,
                    "commit_diff_text": commit_diffs_txt,
                    "commit_url": commit_url
                }
        return self.all_commits

