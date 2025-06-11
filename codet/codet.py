import os
import sys
import datetime 
import re
import json
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
        # get max width for directory column
        # check if dir_files is empty
        if not dir_files:
            self.logger.info("No matching files found in hotspot analysis")
            return
            
        # get max width for directory column
        max_dir_width = 0
        for dir_key in dir_files.keys():
            if len(dir_key) > max_dir_width:
                max_dir_width = len(dir_key)
                
        # get max width for file path column 
        max_file_width = 0
        for files in dir_files.values():
            for file_path, _ in files:
                if len(file_path) > max_file_width:
                    max_file_width = len(file_path)
                    
        # fixed width for changes count column
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

    def ai_analysis(self, text_input):
        from openai import AzureOpenAI
        api_token = self.args.api_token
        endpoint = self.args.openai_endpoint
        llm_model = self.args.model
        custom_prompt = self.args.custom_prompt
        input_file = self.args.input_file

        if custom_prompt:
            print(f"===> CUSTOM PROMPT MESSAGE IS:\n\t: {custom_prompt}")
            text_input += custom_prompt

        if input_file:
            print(f"===> READING INPUT FILE:\n\t{input_file.name}")
            try:
                file_content = input_file.read()
                text_input += "Please analyze the additional file attachments together with the provided materials. \n"
                text_input += "File attachments as follows: \n"
                text_input += file_content
                text_input += "\n"
            except Exception as e:
                self.logger.error(f"Failed to read input file: {str(e)}")
                return

        if not (api_token and endpoint and llm_model):
            self.logger.warning(">>-------> No API token or endpoint or model provided, skipping AI analysis <-------<< ")
            return
        
        client = AzureOpenAI(
            api_version="2024-02-15-preview",
            azure_endpoint=endpoint,
            api_key=api_token,
        )
        
        chat_completion = client.chat.completions.create(
            model=llm_model,
            messages=[
                {
                    "role": "user",
                    "content": text_input,
                }
            ],
            temperature=0.5,  # higher temperature means more creative
            top_p=0.7,        # higher top_p means more creative
            max_tokens=1024 * 4,  # max tokens to generate
            stream=True,
        )

        full_reply = ""
        for chunk in chat_completion:
            if chunk.choices and chunk.choices[0].delta.content:
                full_reply += chunk.choices[0].delta.content
        print("=========================================== ")
        print(full_reply)
        return full_reply


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
            # write report header: general info for the whole report
            f.write("# Git Patch/Diff Report\n")
            f.write("# Generated: {0}\n\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            # iterate over each repository and its commits
            for repo_name, commits in self.cooked_commits.items():
                if not commits:
                    continue

                # section header for each repository
                f.write("===============================================================================\n")
                f.write("Repository: {0}\n".format(repo_name))
                f.write("===============================================================================\n\n")

                ai_input_text = ""
                # process each commit in the current repository
                for commit_hash, commit_data in commits.items():
                    # section for each commit's raw data
                    f.write("-------------------------------------------------------------------------------\n")
                    f.write("Commit: {0}\n".format(commit_hash))
                    f.write("Author: {0} <{1}>\n".format(
                        commit_data.get('commit_author', 'Unknown'),
                        commit_data.get('commit_email', 'Unknown')
                    ))
                    f.write("Date: {0}\n\n".format(commit_data.get('commit_date', 'Unknown')))
                    
                    # write commit message section
                    f.write("Commit Message:\n")
                    f.write("{0}\n\n".format(commit_data.get('commit_message', 'No message')))
                    
                    # write analysis context prompt for AI (for transparency)
                    # this is the prompt that will be used for AI analysis
                    pre_prompt = (
                        "\n"
                        "As an expert in the current {0} project, you need analyze the Git commit message and diff info related to '{1}' feature. Answer these questions:\n"
                        "1. What are the main changes in this commit for {0}.\n"
                        "2. What problems might these changes solve for {0}.\n"
                        "3. Extract key info from the commit message and explain how it describes the code submission for {0}.\n"
                        "4. Analyze the relationship between the submitted code and its description. Point out which code implements the goals in the commit message for {0}.\n"
                        "5. Evaluate the impact of this commit on the project. Which files or functionalities are affected for {0}.\n"
                        "6. Explain the context and significance of this commit. Does it address issues or implement new features for {0}.\n"
                        "7. If there are changes involving \"tests/trt-test-defs/\", please briefly mention the impact of these changes for {0}.\n"
                        "8. Don't explaining abbreviations.\n"
                        "\n"
                        "the output should not include the above rules and requirements; it should be naturally integrated.\n"
                    ).format(
                        repo_name,
                        self.args.keyword if hasattr(self, 'args') and hasattr(self.args, 'keyword') else ""
                    )
                    
                    # clearly mark the start of the analysis context for this commit
                    f.write("# --------- Analysis Context (for AI) ---------\n")
                    f.write(pre_prompt)
                    f.write("\n\n")
                    
                    # write changed files section if available
                    if 'commit_changed_files' in commit_data and commit_data['commit_changed_files']:
                        f.write("# --------- Changed Files ---------\n")
                        for file_path in commit_data['commit_changed_files']:
                            f.write("  - {0}\n".format(file_path))
                        f.write("\n")
                    
                    # write git diff/patch section if available
                    if 'commit_diff_text' in commit_data and commit_data['commit_diff_text']:
                        f.write("# --------- Git Patch/Diff ---------\n")
                        f.write(commit_data['commit_diff_text'])
                        f.write("\n\n")
                    else:
                        f.write("# --------- No diff information available for this commit ---------\n\n")
                    
                    # write commit URL if available
                    if 'commit_url' in commit_data and commit_data['commit_url']:
                        f.write("# --------- Commit URL ---------\n")
                        f.write("{0}\n\n".format(commit_data['commit_url']))

                    # accumulate text for AI analysis (for this repository)
                    ai_input_text += (
                        "Repository: {0}\n"
                        "Commit: {1}\n"
                        "Author: {2} <{3}>\n"
                        "Date: {4}\n"
                        "Commit Message:\n{5}\n"
                        "{6}\n"
                    ).format(
                        repo_name,
                        commit_hash,
                        commit_data.get('commit_author', 'Unknown'),
                        commit_data.get('commit_email', 'Unknown'),
                        commit_data.get('commit_date', 'Unknown'),
                        commit_data.get('commit_message', 'No message'),
                        pre_prompt
                    )
                    if 'commit_changed_files' in commit_data and commit_data['commit_changed_files']:
                        ai_input_text += "Changed Files:\n"
                        for file_path in commit_data['commit_changed_files']:
                            ai_input_text += "  - {0}\n".format(file_path)
                    if 'commit_diff_text' in commit_data and commit_data['commit_diff_text']:
                        ai_input_text += "Git Patch/Diff:\n"
                        ai_input_text += commit_data['commit_diff_text'] + "\n"
                    if 'commit_url' in commit_data and commit_data['commit_url']:
                        ai_input_text += "Commit URL: {0}\n".format(commit_data['commit_url'])
                    ai_input_text += "\n"

                    # call ai_analysis for this repository if there is any input
                    ai_output = None
                    if ai_input_text.strip():
                        try:
                            ai_output = self.ai_analysis(ai_input_text)
                        except Exception as e:
                            self.logger.warning("AI analysis failed for repository {0}: {1}".format(repo_name, e))
                            ai_output = None

                    # write AI analysis output section, clearly separated from raw data
                    if ai_output:
                        f.write("===============================================================================\n")
                        f.write("# ===================== AI Analysis Output (LLM Generated) =====================\n")
                        f.write(ai_output)
                        f.write("\n")
            
        self.logger.info(f"Git patch/diff report generated: {output_file}")
        self.logger.info(f"\033[1;33m\033[1mFile path: {os.path.abspath(output_file)}\033[0m")
        self.logger.info(f"This report can be opened directly in Cursor for code change analysis or integrated with various LLM Agent tools")

    def generate_cook_json(self):
        """Generates a JSON report for each repository with detailed commit info and AI-extracted keywords."""
        if not self.args.output_cook_json: 
            self.logger.info("JSON report generation skipped. Use -oj or --output-cook-json flag to enable.")
            return

        if not hasattr(self, 'cooked_commits') or not self.cooked_commits:
            self.logger.warning("No processed commits available for JSON report generation.")
            return

        self.logger.info("Generating JSON reports for cooked commits...")

        for repo_name, commits in self.cooked_commits.items():
            if not commits:
                continue

            self.logger.info(f"Processing repository: {repo_name}")
            all_commits_data = OrderedDict()

            for commit_hash, commit_data in commits.items():
                ai_text = (
                    f"{commit_data.get('commit_summary', '')}\n"
                    f"{commit_data.get('commit_message', '')}\n"
                    f"{commit_data.get('commit_diff_text', '')}"
                )
    
                if ai_text.strip():
                    try:
                        ai_output = self.ai_analysis(ai_text)
                    except Exception as e:
                        self.logger.warning("AI analysis failed in func generate_cook_json for repository {0}: {1}".format(repo_name, e))
                        ai_output = None

                # convert datetime to string if present
                commit_date = commit_data.get("commit_date")
                print(f"commit_date: {commit_date}, {type(commit_date)}")
                if commit_date and hasattr(commit_date, 'isoformat'):
                    commit_date = commit_date.isoformat()

                final_commit_data = {
                    "commit_email": commit_data.get("commit_email"),
                    "commit_author": commit_data.get("commit_author"),
                    "commit_summary": commit_data.get("commit_summary"),
                    "commit_message": commit_data.get("commit_message") or commit_data.get("commit_diff_text"),
                    "commit_date": commit_date,
                    "commit_url": commit_data.get("commit_url"),
                    "commit_changed_files": commit_data.get("commit_changed_files"),
                    "ai_summary": ai_output
                }
    
                all_commits_data[commit_hash] = final_commit_data

                # use current date if no commit date available
                date_str = commit_data.get("commit_date")
                if date_str and hasattr(date_str, 'strftime'):
                    date_str = date_str.strftime("%Y%m%d")
                elif not date_str:
                    date_str = datetime.now().strftime("%Y%m%d")
                    
                # create output directory if not exists
                output_dir = f"cook_{repo_name}_json"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    
                output_filename = os.path.join(output_dir, f"{repo_name}_{date_str}_{commit_hash}_cook.json")
                
                self.logger.info(f"Saving JSON report to '{output_filename}'")
                with open(output_filename, 'w', encoding='utf-8') as f:
                    json.dump(all_commits_data, f, indent=4)
        
        self.logger.info("JSON report generation complete.")
