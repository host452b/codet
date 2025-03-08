import os
import sys
import datetime 
from typing import List, Dict, Any, Optional
from codet.git_compoent import GitAnalyzer
from collections import OrderedDict

class CodeTrailExecutor:
    """Code trail executor for analyzing Git commit history"""
    
    def __init__(self, args):
        """
        Initialize executor
        
        Args:
            args: Command line arguments object
        """
        self.args = args
        self.git_analyzer = None
        # Process all repositories together instead of one by one
        self.raw_commits = OrderedDict()
        self.cooked_commits = OrderedDict()
        self.keyword_results = []
        self.hotspot_data = {}
        self.logger = None
        
        # Set log level
        log_level = "debug" if args.debug else "info"
        self.setup_logger(log_level)
        
    def setup_logger(self, level):
        """Setup logger"""
        from codet.clog import Logger
        self.logger = Logger(name="codet", level=level)
        self.logger.info("Initializing CodeTrail executor")
        
    def initialize_repo(self):
        """Initialize Git repository, supports recursive mode"""
        
        self.logger.info(f"Analyzing path: {self.args.path}")
        # Collect all directory paths
        dir_path_list = []
        
        if self.args.recursive:
            # Recursive mode: scan all subdirectories for Git repos
            self.logger.info("Recursive mode enabled, scanning all subdirectories")
            
            # Use os.walk to recursively scan directories
            for root, dirs, _ in os.walk(self.args.path):
                # Only add directories containing .git
                if '.git' in os.listdir(root):
                    dir_path_list.append(root)
        else:
            # Non-recursive mode: only analyze specified directory
            if not os.path.exists(os.path.join(self.args.path, ".git")):
                self.logger.error(f"Current path {self.args.path} is not a valid Git repository. Please check path. Use -r flag to enable recursive mode to analyze parent directories")
            
            # Try to load specified directory as Git repo
            dir_path_list = [self.args.path]
            
        return self._try_add_repo(dir_path_list)
    
    def _try_add_repo(self, dir_path_list):
        """Try to add directories as Git repositories to repo list"""
        success = False
        valid_git_repos = []
        
        # First check which directories are valid Git repos
        for dir_path in dir_path_list:
            if os.path.exists(os.path.join(dir_path, ".git")):
                valid_git_repos.append(dir_path)
                self.logger.info(f"\tFound Git repo at {dir_path}")
        
        # Return false if no valid Git repos found
        if not valid_git_repos:
            self.logger.warning("No valid Git repositories found")
            return False
            
        # Pass all valid Git repo paths to GitAnalyzer
        try:
            self.git_analyzer = GitAnalyzer(valid_git_repos)
            self.logger.info(f"\tSuccessfully loaded {len(valid_git_repos)} Git repositories")
            success = True
        except Exception as e:
            self.logger.error(f"Unknown error initializing GitAnalyzer: {str(e)}")
                
        return success

    def raw(self):
        """Collect raw commit data from all repositories"""
        self.logger.info("Starting to collect raw commit data")
        
        # Calculate date range
        from_date = (datetime.datetime.now() - datetime.timedelta(days=self.args.days)).strftime('%Y-%m-%d')
        self.logger.info(f"Collecting commits since {from_date}")
        self.raw_commits = self.git_analyzer.get_all_commits(days_back=self.args.days)

    def cook(self):
        """Filter and process raw commit data based on parameters"""
        self.logger.info("Starting to process commit data")

        # Check if there is raw data
        if len(self.raw_commits) == 0:
            self.logger.warning("No matching commits found")
            return

        # Check conditions (union mode vs intersection mode)
        # Default is union mode (match any condition)
        # Search mode explanation:
        # 1. Union Mode: Include commit if it matches ANY filter condition (email, username or keyword)
        #    Example: If email A and keyword B specified, include commits with email A OR containing keyword B
        # 2. Intersection Mode: Include commit only if it matches ALL specified filter conditions
        #    Example: If email A and keyword B specified, include commits only with email A AND containing keyword B
        self.logger.info("Union mode: match any condition")
        self.logger.info("Intersection mode: must match all conditions")

        union_mode = self.args.mode == "union"  # Check mode based on args.mode
        if union_mode:
            self.logger.info("[Search Mode] Using Union Mode - Match any condition")
            self.logger.info("  Union mode: commit included if it matches any email, username or keyword condition")
            self.logger.info(f"  - Email conditions: {', '.join(self.args.email) if self.args.email else 'none'}")
            self.logger.info(f"  - User conditions: {', '.join(self.args.user) if self.args.user else 'none'}")
            self.logger.info(f"  - Keyword conditions: {', '.join(self.args.keyword) if self.args.keyword else 'none'}")
        else:
            self.logger.info("[Search Mode] Using Intersection Mode - Must match all conditions")
            self.logger.info("  Intersection mode: commit included only if it matches all specified conditions")
            self.logger.info(f"  - Email conditions: {', '.join(self.args.email) if self.args.email else 'none'} (must match if specified)")
            self.logger.info(f"  - User conditions: {', '.join(self.args.user) if self.args.user else 'none'} (must match if specified)")
            self.logger.info(f"  - Keyword conditions: {', '.join(self.args.keyword) if self.args.keyword else 'none'} (must match if specified)")

        # Iterate through commits in all repos
        for repo_name, commits in self.raw_commits.items():
            self.cooked_commits[repo_name] = {}
            
            # Iterate through all commits in this repo
            for commit_hash, commit_data in commits.items():
                # Include all commits if no filters specified
                if (not self.args.email or len(self.args.email) == 0) and \
                   (not self.args.user or len(self.args.user) == 0) and \
                   (not self.args.keyword or len(self.args.keyword) == 0):
                    self.cooked_commits[repo_name][commit_hash] = commit_data
                    continue

                # Union mode: match any condition
                if union_mode:
                    should_include = False
                    
                    # Filter by author email (match any email)
                    if self.args.email and len(self.args.email) > 0:
                        if commit_data["commit_email"] in self.args.email:
                            should_include = True
                        
                    # Filter by author name (match any name)
                    if not should_include and self.args.user and len(self.args.user) > 0:
                        if commit_data["commit_author"] in self.args.user:
                            should_include = True
                        
                    # Filter by keywords (match any keyword)
                    if not should_include and self.args.keyword and len(self.args.keyword) > 0:
                        # Check commit message and diff text for keywords
                        commit_text = commit_data.get("commit_message", "") + commit_data.get("commit_diff_text", "")
                        for keyword in self.args.keyword:
                            if keyword.lower() in commit_text.lower():
                                should_include = True
                                break
                    
                    # Add to processed data if matches any condition
                    if should_include:
                        self.cooked_commits[repo_name][commit_hash] = commit_data
                
                # Intersection mode: must match all specified conditions
                else:
                    should_include = True
                    
                    # Check if filters are specified
                    has_email_filter = self.args.email and len(self.args.email) > 0
                    has_user_filter = self.args.user and len(self.args.user) > 0
                    has_keyword_filter = self.args.keyword and len(self.args.keyword) > 0
                    
                    # Filter by author email (must match all emails)
                    if has_email_filter:
                        for email in self.args.email:
                            if email not in commit_data["commit_email"]:
                                should_include = False
                                break
                        
                    # Filter by author name (must match all names)
                    if has_user_filter and should_include:
                        for user in self.args.user:
                            if user not in commit_data["commit_author"]:
                                should_include = False
                                break
                        
                    # Filter by keywords (must match all keywords)
                    if has_keyword_filter and should_include:
                        commit_text = commit_data.get("commit_message", "") + commit_data.get("commit_diff_text", "")
                        commit_text_lower = commit_text.lower()
                        for keyword in self.args.keyword:
                            if keyword.lower() not in commit_text_lower:
                                should_include = False
                                break
                    
                    # Add to processed data if matches all conditions
                    if should_include:
                        self.cooked_commits[repo_name][commit_hash] = commit_data
                
        # Count total matching commits
        total_commits = sum(len(commits) for commits in self.cooked_commits.values())
        self.logger.info(f"Processing complete, found {total_commits} matching commits")
        
        # Print commit details in table format
        from prettytable import PrettyTable
        table = PrettyTable()
        table.field_names = ["#", "Repository", "Commit ID", "Commit Summary", "Email", "URL", "Date"]
        table.align["#"] = "r"  # Right align
        table.align["Repository"] = "l"  # Left align
        table.align["Commit ID"] = "l"
        table.align["Commit Summary"] = "l"
        table.align["Email"] = "l" 
        table.align["URL"] = "l"
        table.align["Date"] = "r"  # Right align
        
        row_num = 1
        for repo_name, commits in self.cooked_commits.items():
            for commit_hash, commit_data in commits.items():
                table.add_row([
                    row_num,
                    repo_name,
                    commit_hash[:7],
                    commit_data['commit_summary'],
                    commit_data['commit_email'],
                    commit_data['commit_url'],
                    commit_data['commit_date']
                ])
                row_num += 1
        
        self.logger.info("\n" + str(table))

    def hotspot(self):
        """
        Analyze code hotspots by tracking file and directory change frequency
        Show directory, file and function changes in tree structure, reusing GitPython logic
        """
        if not self.args.hotspot:
            self.logger.info("Hotspot analysis disabled. Use -s or --hotspot flag to enable.")
            return
        
        self.logger.info("Starting code hotspot analysis... \n")
        
        # Initialize statistics data structures
        hotspots = {}  # Store directory and file change counts
        file_repos = {}  # Store repository names for files
        
        # Iterate through commits to count file changes
        for repo_name, commits in self.cooked_commits.items():
            for commit_hash, commit_data in commits.items():
                # Get list of changed files
                changed_files = commit_data.get("commit_changed_files", [])
                
                # Update hotspot statistics
                for file_path in changed_files:
                    if file_path not in hotspots:
                        hotspots[file_path] = 1
                        file_repos[file_path] = repo_name
                    else:
                        hotspots[file_path] += 1
        
        self.logger.info("Code hotspot analysis results:")
        
        # Sort files by change count
        sorted_files = sorted(
            hotspots.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Calculate total changes across all files
        total_changes = sum(count for _, count in hotspots.items())
        self.logger.info(f"Code hotspot analysis complete, detected {total_changes} total file changes")
        
        # Get color function based on change count tiers
        def get_color_by_count(count, max_count):
            if count >= max_count * 5/6:  # Highest tier
                return "\033[35m"  # Purple
            elif count >= max_count * 4/6:  # Second tier
                return "\033[31m"  # Dark red
            elif count >= max_count * 3/6:  # Third tier
                return "\033[91m"  # Red
            elif count >= max_count * 2/6:  # Fourth tier
                return "\033[33m"  # Orange
            elif count >= max_count * 1/6:  # Fifth tier
                return "\033[93m"  # Yellow
            else:
                return None  # No color, skip printing
        
        # Get maximum change count
        max_changes = 0
        if hotspots:
            max_changes = max(hotspots.values())
        
        # Group files by directory, keep only top 5 tiers
        dir_files = {}
        for file_path, count in sorted_files:
            # Check if in top 5 tiers
            color = get_color_by_count(count, max_changes)
            if color:  # Only process files in top 5 tiers
                # Get first level directory name
                dir_name = 'root'
                if '/' in file_path:
                    dir_name = file_path.split('/')[0]
                
                # Get repository name
                repo_name = file_repos.get(file_path, "unknown")
                dir_key = f"{repo_name}/{dir_name}"
                
                if dir_key not in dir_files:
                    dir_files[dir_key] = []
                dir_files[dir_key].append((file_path, count))

        # Create table using PrettyTable
        from prettytable import PrettyTable
        table = PrettyTable()
        table.field_names = ["Directory", "File", "Changes"]
        table.align["Directory"] = "l"  # Left align
        table.align["File"] = "l"  # Left align
        table.align["Changes"] = "r"  # Right align
        
        # Get max width for each column
        max_dir_width = max(len(dir_key) for dir_key in dir_files.keys())
        max_file_width = max(len(file_path) for files in dir_files.values() for file_path, _ in files)
        max_count_width = 10
        
        # Add data to table by directory
        sorted_dir_names = sorted(dir_files.keys())
        prev_dir = None
        for dir_key in sorted_dir_names:
            # Add separator row if directory changes
            if prev_dir is not None:
                table.add_row(["-" * max_dir_width, "-" * max_file_width, "-" * max_count_width])
            prev_dir = dir_key
            
            files = dir_files[dir_key]
            # Add first file (with directory name)
            first_file = files[0]
            color = get_color_by_count(first_file[1], max_changes)
            if color:
                end_color = "\033[0m"
                table.add_row([
                    f"{color}{dir_key}{end_color}",
                    f"{color}{first_file[0]}{end_color}",
                    f"{color}{first_file[1]}{end_color}"
                ])
            
            # Add remaining files (empty directory column)
            for file_path, count in files[1:]:
                color = get_color_by_count(count, max_changes)
                if color:
                    end_color = "\033[0m"
                    table.add_row([
                        "",
                        f"{color}{file_path}{end_color}",
                        f"{color}{count}{end_color}"
                    ])
        
        # Print table
        self.logger.info("\n" + str(table))
        self.logger.info("\nHotspot analysis complete")

    def generate_report(self):
        """
        Generate a comprehensive git patch/diff report file based on analyzed commits
        
        This method creates a text file containing aggregated git patches from analyzed commits,
        including contextual information and the actual diff content.
        """
        import os
        from datetime import datetime
        
        if not hasattr(self, 'cooked_commits') or not self.cooked_commits:
            self.logger.warning("No processed commits available for report generation")
            return
            
        self.logger.info("Generating git patch/diff report file...")
        
        # Generate timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(os.getcwd(), f"git_patch_report_{timestamp}.diff")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"# Git Patch/Diff Report\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Process each repository
            for repo_name, commits in self.cooked_commits.items():
                if not commits:
                    continue
                    
                f.write(f"===============================================================================\n")
                f.write(f"Repository: {repo_name}\n")
                f.write(f"===============================================================================\n\n")
                
                # Process each commit
                for commit_hash, commit_data in commits.items():
                    # Write commit metadata
                    f.write(f"-------------------------------------------------------------------------------\n")
                    f.write(f"Commit: {commit_hash}\n")
                    f.write(f"Author: {commit_data.get('commit_author', 'Unknown')} <{commit_data.get('commit_email', 'Unknown')}>\n")
                    f.write(f"Date: {commit_data.get('commit_date', 'Unknown')}\n\n")
                    
                    # Write commit message
                    f.write(f"Commit Message:\n")
                    f.write(f"{commit_data.get('commit_message', 'No message')}\n\n")
                    
                    # Write analysis prompt
                    pre_prompt = """
As an expert in the current {0} project, you need analyze the Git commit message and diff info related to '{1}' feature. Answer these questions:
1. What are the main changes in this commit for {0}.
2. What problems might these changes solve for {0}.
3. Extract key info from the commit message and explain how it describes the code submission for {0}.
4. Analyze the relationship between the submitted code and its description. Point out which code implements the goals in the commit message for {0}.
5. Evaluate the impact of this commit on the project. Which files or functionalities are affected for {0}. 
6. Explain the context and significance of this commit. Does it address issues or implement new features for {0}.
7. If there are changes involving "tests/trt-test-defs/", please briefly mention the impact of these changes for {0}.
8. Don't explaining abbreviations.

the output should not include the above rules and requirements; it should be naturally integrated.
""".format(repo_name, self.args.keyword if hasattr(self, 'args') and hasattr(self.args, 'keyword') else "")
                    
                    f.write("Analysis Context:\n")
                    f.write(pre_prompt)
                    f.write("\n\n")
                    
                    # Write changed files list
                    if 'commit_changed_files' in commit_data and commit_data['commit_changed_files']:
                        f.write("Changed Files:\n")
                        for file_path in commit_data['commit_changed_files']:
                            f.write(f"  - {file_path}\n")
                        f.write("\n")
                    
                    # Write the actual git diff/patch content
                    if 'commit_diff_text' in commit_data and commit_data['commit_diff_text']:
                        f.write("Git Patch/Diff:\n")
                        f.write(commit_data['commit_diff_text'])
                        f.write("\n\n")
                    else:
                        f.write("No diff information available for this commit\n\n")
                    
                    # Write commit URL if available
                    if 'commit_url' in commit_data and commit_data['commit_url']:
                        f.write(f"Commit URL: {commit_data['commit_url']}\n\n")
            
        self.logger.info(f"Git patch/diff report generated: {output_file} - can be opened directly in Cursor for code change analysis or integrated with various LLM Agent tools")
