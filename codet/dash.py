#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plotly Dash app for codet - Interactive dashboard for Git commit analysis
"""

import os
import json
import argparse
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
from dash import dcc, html, Input, Output, callback, dash_table, State, callback_context
import dash_bootstrap_components as dbc


class CodetDashboard:
    """Dashboard class for codet analysis visualization"""
    
    def __init__(self, json_path=None):
        self.json_path = json_path
        self.data = {}
        self.df_commits = pd.DataFrame()
        self.df_files = pd.DataFrame()
        self.app = None
        
    def load_data(self):
        """Load and parse JSON data from codet analysis"""
        if not self.json_path:
            print("No JSON path provided")
            return False
            
        try:
            # handle different JSON file structures
            if os.path.isfile(self.json_path):
                # single JSON file
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    # extract repo name from file path
                    file_name = os.path.basename(self.json_path)
                    repo_name = os.path.splitext(file_name)[0]  # remove .json extension
                    
                    # extract repo name before first underscore
                    if '_' in repo_name:
                        repo_name = repo_name.split('_')[0]
                    
                    self.data = {repo_name: file_data}
            elif os.path.isdir(self.json_path):
                # directory with multiple JSON files
                self.data = {}
                for root, dirs, files in os.walk(self.json_path):
                    for file in files:
                        if file.endswith('.json'):
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                file_data = json.load(f)
                                # extract repo name from filename before first underscore
                                file_name = os.path.basename(file_path)
                                repo_name = os.path.splitext(file_name)[0]
                                if '_' in repo_name:
                                    repo_name = repo_name.split('_')[0]
                                
                                if repo_name not in self.data:
                                    self.data[repo_name] = {}
                                self.data[repo_name].update(file_data)
            else:
                print(f"Invalid path: {self.json_path}")
                return False
                
            print(f"Data loaded successfully. Structure:")
            for repo_name, data in self.data.items():
                if isinstance(data, dict):
                    print(f"  Repository '{repo_name}': {len(data)} commits")
                    # show first few commit keys for debugging
                    sample_keys = list(data.keys())[:3]
                    print(f"    Sample commit keys: {sample_keys}")
                else:
                    print(f"  Repository '{repo_name}': Invalid data type {type(data)}")
                    
            return self._process_data()
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _process_data(self):
        """Process loaded JSON data into DataFrames"""
        commits_data = []
        files_data = []
        
        print(f"Processing data for {len(self.data)} repositories...")
        for repo_name, commits in self.data.items():
            print(f"Processing repository: {repo_name} with {len(commits) if isinstance(commits, dict) else 0} commits")
            if not isinstance(commits, dict):
                print(f"Skipping {repo_name}: not a dict, type is {type(commits)}")
                continue
                
            for commit_hash, commit_info in commits.items():
                if not isinstance(commit_info, dict):
                    continue
                    
                # process commit data with robust date handling
                commit_date = commit_info.get('commit_date', '')
                if commit_date:
                    try:
                        if isinstance(commit_date, str):
                            # try different date formats
                            for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S.%f']:
                                try:
                                    commit_date = datetime.strptime(commit_date.split('+')[0], fmt)  # handle timezone
                                    break
                                except ValueError:
                                    continue
                            else:
                                # if no format worked, try pandas
                                commit_date = pd.to_datetime(commit_date, errors='coerce')
                                if pd.isna(commit_date):
                                    commit_date = datetime.now()
                        elif not isinstance(commit_date, datetime):
                            commit_date = datetime.now()
                    except:
                        commit_date = datetime.now()
                else:
                    commit_date = datetime.now()
                
                commit_data = {
                    'repo_name': repo_name,
                    'commit_hash': commit_hash,
                    'commit_short': commit_hash[:7] if commit_hash else '',
                    'author': commit_info.get('commit_author', 'Unknown'),
                    'email': commit_info.get('commit_email', 'Unknown'),
                    'date': commit_date,
                    'summary': commit_info.get('commit_summary', ''),
                    'message': commit_info.get('commit_message', ''),
                    'url': commit_info.get('commit_url', ''),
                    'ai_summary': commit_info.get('ai_summary', ''),
                    'files_count': len(commit_info.get('commit_changed_files', []))
                }
                commits_data.append(commit_data)
                
                # process changed files data
                changed_files = commit_info.get('commit_changed_files', [])
                for file_path in changed_files:
                    file_data = {
                        'repo_name': repo_name,
                        'commit_hash': commit_hash,
                        'commit_short': commit_hash[:7] if commit_hash else '',
                        'file_path': file_path,
                        'file_name': os.path.basename(file_path),
                        'file_dir': os.path.dirname(file_path) or 'root',
                        'file_ext': os.path.splitext(file_path)[1] or 'no_ext',
                        'date': commit_date,
                        'author': commit_info.get('commit_author', 'Unknown')
                    }
                    files_data.append(file_data)
        
        self.df_commits = pd.DataFrame(commits_data)
        self.df_files = pd.DataFrame(files_data)
        
        print(f"Created DataFrames:")
        print(f"  Commits: {len(self.df_commits)} records")
        print(f"  Files: {len(self.df_files)} records")
        
        if not self.df_commits.empty:
            print(f"  Unique repositories: {self.df_commits['repo_name'].unique().tolist()}")
            print(f"  Unique authors: {self.df_commits['author'].nunique()}")
        
        # ensure date columns are datetime type
        if not self.df_commits.empty and 'date' in self.df_commits.columns:
            self.df_commits['date'] = pd.to_datetime(self.df_commits['date'], errors='coerce')
        if not self.df_files.empty and 'date' in self.df_files.columns:
            self.df_files['date'] = pd.to_datetime(self.df_files['date'], errors='coerce')
        
        return len(commits_data) > 0
    
    def create_app(self):
        """Create and configure Dash application"""
        # initialize app with custom dashboard theme
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
            suppress_callback_exceptions=True
        )
        
        # color scheme: Black, White, Green
        dashboard_colors = {
            'green': '#76B900',      # Dashboard brand green
            'dark_green': '#5a8c00', # Darker green for hover
            'black': '#000000',      # Pure black
            'dark_gray': '#1a1a1a',  # Dark gray for backgrounds
            'light_gray': '#f8f9fa', # Light gray for alternating rows
            'white': '#ffffff'       # Pure white
        }
        
        self.app.title = "Codet Dashboard - Git Analysis Visualization"
        
        # add global styles for enhanced UX
        self.app.index_string = '''
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>{%title%}</title>
                {%favicon%}
                {%css%}
                <style>
                    /* Global smooth transitions */
                    * {
                        transition: all 0.2s ease-in-out;
                    }
                    
                    /* Enhanced button hover effects */
                    button:hover {
                        transform: translateY(-1px);
                        box-shadow: 0 4px 12px rgba(118, 185, 0, 0.15) !important;
                    }
                    
                    /* Card hover effects */
                    .card:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
                    }
                    
                    /* Smooth badge animations */
                    .badge {
                        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    }
                    
                    /* Input focus effects */
                    .form-control:focus, .form-select:focus {
                        border-color: #76B900 !important;
                        box-shadow: 0 0 0 0.2rem rgba(118, 185, 0, 0.25) !important;
                    }
                    
                    /* Smooth scrollbar */
                    ::-webkit-scrollbar {
                        width: 8px;
                        height: 8px;
                    }
                    ::-webkit-scrollbar-track {
                        background: #f1f1f1;
                        border-radius: 4px;
                    }
                    ::-webkit-scrollbar-thumb {
                        background: #76B900;
                        border-radius: 4px;
                    }
                    ::-webkit-scrollbar-thumb:hover {
                        background: #5a8c00;
                    }
                    
                    /* Loading spinner customization */
                    .spinner-border-sm {
                        color: #76B900 !important;
                    }
                    
                    /* Modal animation enhancement */
                    .modal.fade .modal-dialog {
                        transition: transform 0.3s ease-out;
                    }
                    
                    /* Table enhancement */
                    .dash-table-container {
                        border-radius: 8px;
                        overflow: hidden;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                </style>
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        '''
        
        # create layout
        self.app.layout = self._create_layout()
        
        # register callbacks
        self._register_callbacks()
        
        return self.app
    
    def _create_layout(self):
        """Create the main dashboard layout"""
        if self.df_commits.empty:
            return dbc.Container([
                dbc.Alert("No data available. Please check your JSON file path.", 
                         style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'border': '2px solid #76B900'}),
            ])
        
        # header with dashboard colors
        header = dbc.Row([
            dbc.Col([
                html.H1("🔍 Codet Dashboard", 
                       style={'color': '#000000', 'fontWeight': 'bold'}, 
                       className="mb-0"),
                html.P("Interactive Git Commit Analysis", 
                      style={'color': '#666666'}),
            ], width=8),
            dbc.Col([
                dbc.Badge(f"Total Commits: {len(self.df_commits)}", 
                         style={'backgroundColor': '#76B900', 'color': 'white', 'border': 'none'}, 
                         className="me-2"),
                dbc.Badge(f"Total Files: {len(self.df_files)}", 
                         style={'backgroundColor': '#000000', 'color': 'white', 'border': 'none'}),
            ], width=4, className="text-end align-self-center"),
        ], className="mb-4")
        
        # filters row
        filters_row = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("📅 Date Range", className="fw-bold mb-2"),
                        dcc.DatePickerRange(
                            id='date-range-picker',
                            start_date=self.df_commits['date'].min() if not self.df_commits.empty else None,
                            end_date=self.df_commits['date'].max() if not self.df_commits.empty else None,
                            display_format='YYYY-MM-DD',
                            style={'width': '100%'}
                        )
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("👨‍💻 Authors", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='author-dropdown',
                            options=[{'label': author, 'value': author} 
                                   for author in sorted(self.df_commits['author'].unique())],
                            value=list(self.df_commits['author'].unique()) if not self.df_commits.empty else [],
                            multi=True,
                            placeholder="Select authors..."
                        )
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("📁 Repositories", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='repo-dropdown',
                            options=[{'label': repo, 'value': repo} 
                                   for repo in sorted(self.df_commits['repo_name'].unique())],
                            value=list(self.df_commits['repo_name'].unique()) if not self.df_commits.empty else [],
                            multi=True,
                            placeholder="Select repositories..."
                        )
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("📄 File Types", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='filetype-dropdown',
                            options=[{'label': ext if ext else 'No Extension', 'value': ext} 
                                   for ext in sorted(self.df_files['file_ext'].unique())],
                            value=list(self.df_files['file_ext'].unique()) if not self.df_files.empty else [],
                            multi=True,
                            placeholder="Select file types..."
                        )
                    ])
                ])
            ], width=3)
        ], className="mb-4")
        
        # main content tabs
        tabs = dbc.Tabs([
            dbc.Tab(label="📊 Overview", tab_id="overview"),
            dbc.Tab(label="🔥 Hotspots", tab_id="hotspots"),
            dbc.Tab(label="📈 Timeline", tab_id="timeline"),
            dbc.Tab(label="📋 Details", tab_id="details"),
            dbc.Tab(label="📄 JSON Browser", tab_id="json-browser"),
        ], id="main-tabs", active_tab="overview")
        
        # tab content
        tab_content = html.Div(id="tab-content", className="mt-3")
        
        return dbc.Container([
            header,
            filters_row,
            tabs,
            tab_content
        ], fluid=True)
    
    def _register_callbacks(self):
        """Register all dashboard callbacks"""
        
        @callback(
            Output('tab-content', 'children'),
            [Input('main-tabs', 'active_tab'),
             Input('date-range-picker', 'start_date'),
             Input('date-range-picker', 'end_date'),
             Input('author-dropdown', 'value'),
             Input('repo-dropdown', 'value'),
             Input('filetype-dropdown', 'value')]
        )
        def update_tab_content(active_tab, start_date, end_date, selected_authors, 
                             selected_repos, selected_filetypes):
            try:
                # ensure selected values are not None
                if selected_authors is None:
                    selected_authors = list(self.df_commits['author'].unique()) if not self.df_commits.empty else []
                if selected_repos is None:
                    selected_repos = list(self.df_commits['repo_name'].unique()) if not self.df_commits.empty else []
                if selected_filetypes is None:
                    selected_filetypes = list(self.df_files['file_ext'].unique()) if not self.df_files.empty else []
                
                # filter data based on selections
                filtered_commits = self._filter_data(
                    start_date, end_date, selected_authors, selected_repos
                )
                filtered_files = self._filter_files_data(
                    start_date, end_date, selected_authors, selected_repos, selected_filetypes
                )
                
                if active_tab == "overview":
                    return self._create_overview_tab(filtered_commits, filtered_files)
                elif active_tab == "hotspots":
                    return self._create_hotspots_tab(filtered_files)
                elif active_tab == "timeline":
                    return self._create_timeline_tab(filtered_commits)
                elif active_tab == "details":
                    return self._create_details_tab(filtered_commits)
                elif active_tab == "json-browser":
                    return self._create_json_browser_tab()
                
                return html.Div("Select a tab to view content")
                
            except Exception as e:
                return dbc.Alert(f"Error loading content: {str(e)}", 
                               style={'backgroundColor': '#ffe6e6', 'color': '#000000', 'border': '2px solid #000000'})
        
        # modal callbacks for AI Summary details
        @callback(
            [Output("detail-modal", "is_open"),
             Output("modal-content", "children"),
             Output("modal-title", "children")],
            [Input("json-data-table", "active_cell"),
             Input("close-modal", "n_clicks"),
             Input("close-modal-x", "n_clicks")],
            [State("detail-modal", "is_open"),
             State("json-data-table", "data")]
        )
        def toggle_modal(active_cell, close_clicks, close_x_clicks, is_open, table_data):
            ctx = callback_context
            if not ctx.triggered:
                return False, "", "AI Analysis Details"
            
            trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
            
            if trigger_id in ["close-modal", "close-modal-x"]:
                return False, "", "AI Analysis Details"
            
            if trigger_id == "json-data-table" and active_cell:
                if active_cell['column_id'] == 'ai_summary':
                    row_index = active_cell['row']
                    if row_index < len(table_data):
                        row_data = table_data[row_index]
                        commit_hash = row_data.get('commit_hash', 'Unknown')
                        full_hash = row_data.get('full_hash', commit_hash)
                        repo = row_data.get('repo_name', 'Unknown')
                        author = row_data.get('author', 'Unknown')
                        date = row_data.get('date', 'Unknown')
                        
                        # get full AI summary
                        full_summary = row_data.get('full_ai_summary', '')
                        
                        if not full_summary or not full_summary.strip():
                            full_summary = """### 📝 Analysis Not Available

Unfortunately, no AI analysis is available for this commit. This could be due to:

- **Missing AI Configuration**: The analysis tool may not have been configured with AI capabilities
- **Processing Error**: The AI analysis may have failed during generation
- **Empty Content**: There might not be enough meaningful content to analyze

### 💡 Suggestions

1. **Re-run Analysis**: Try running the codet tool with AI analysis enabled
2. **Check Configuration**: Ensure your AI API tokens and endpoints are properly configured
3. **Manual Review**: You can manually review the commit details below

### 📋 Commit Information

Feel free to examine the commit details in the main table for more context."""
                        
                        # create enhanced content with better formatting
                        formatted_content = f"""## 📊 Commit Overview

| Field | Value |
|-------|-------|
| **Repository** | `{repo}` |
| **Commit Hash** | `{full_hash}` |
| **Author** | {author} |
| **Date** | {date} |

---

## 🤖 AI Analysis Results

{full_summary}

---

## 🔗 Actions

- View this commit in your repository browser
- Compare with related commits
- Review the changed files in detail

*Analysis powered by AI | Generated on {date}*"""
                        
                        modal_title = f"📊 {repo} • {commit_hash}"
                        return True, formatted_content, modal_title
            
            return is_open, "", "AI Analysis Details"
    
    def _filter_data(self, start_date, end_date, selected_authors, selected_repos):
        """Filter commits data based on selections"""
        filtered_df = self.df_commits.copy()
        
        if start_date:
            filtered_df = filtered_df[filtered_df['date'] >= start_date]
        if end_date:
            filtered_df = filtered_df[filtered_df['date'] <= end_date]
        if selected_authors:
            filtered_df = filtered_df[filtered_df['author'].isin(selected_authors)]
        if selected_repos:
            filtered_df = filtered_df[filtered_df['repo_name'].isin(selected_repos)]
            
        return filtered_df
    
    def _filter_files_data(self, start_date, end_date, selected_authors, selected_repos, selected_filetypes):
        """Filter files data based on selections"""
        filtered_df = self.df_files.copy()
        
        if start_date:
            filtered_df = filtered_df[filtered_df['date'] >= start_date]
        if end_date:
            filtered_df = filtered_df[filtered_df['date'] <= end_date]
        if selected_authors:
            filtered_df = filtered_df[filtered_df['author'].isin(selected_authors)]
        if selected_repos:
            filtered_df = filtered_df[filtered_df['repo_name'].isin(selected_repos)]
        if selected_filetypes:
            filtered_df = filtered_df[filtered_df['file_ext'].isin(selected_filetypes)]
            
        return filtered_df
    
    def _create_overview_tab(self, commits_df, files_df):
        """Create overview tab content"""
        if commits_df.empty:
            return dbc.Alert("No data matches your filter criteria.", 
                           style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'border': '2px solid #76B900'})
        
        # summary statistics with dashboard colors
        stats_cards = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(len(commits_df), style={'color': '#76B900', 'fontWeight': 'bold'}),
                        html.P("Total Commits", className="mb-0", style={'color': '#000000'})
                    ])
                ], style={'backgroundColor': '#ffffff', 'border': '2px solid #76B900'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(commits_df['author'].nunique(), style={'color': '#000000', 'fontWeight': 'bold'}),
                        html.P("Unique Authors", className="mb-0", style={'color': '#000000'})
                    ])
                ], style={'backgroundColor': '#f0f8f0', 'border': '2px solid #000000'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(commits_df['repo_name'].nunique(), style={'color': '#76B900', 'fontWeight': 'bold'}),
                        html.P("Repositories", className="mb-0", style={'color': '#000000'})
                    ])
                ], style={'backgroundColor': '#ffffff', 'border': '2px solid #76B900'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(len(files_df), style={'color': '#000000', 'fontWeight': 'bold'}),
                        html.P("File Changes", className="mb-0", style={'color': '#000000'})
                    ])
                ], style={'backgroundColor': '#f0f8f0', 'border': '2px solid #000000'})
            ], width=3)
        ], className="mb-4")
        
        # charts
        charts_row = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Commits by Author", 
                                  style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'fontWeight': 'bold', 'border': 'none', 'borderBottom': '3px solid #76B900'}),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=self._create_author_chart(commits_df),
                            config={'displayModeBar': False}
                        )
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📁 Commits by Repository", 
                                  style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'fontWeight': 'bold', 'border': 'none', 'borderBottom': '3px solid #76B900'}),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=self._create_repo_chart(commits_df),
                            config={'displayModeBar': False}
                        )
                    ])
                ])
            ], width=6)
        ])
        
        return html.Div([stats_cards, charts_row])
    
    def _create_hotspots_tab(self, files_df):
        """Create hotspots analysis tab"""
        if files_df.empty:
            return dbc.Alert("No file data matches your filter criteria.", 
                           style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'border': '2px solid #76B900'})
        
        # file hotspots analysis
        file_counts = files_df['file_path'].value_counts().head(20)
        dir_counts = files_df['file_dir'].value_counts().head(15)
        ext_counts = files_df['file_ext'].value_counts().head(10)
        
        hotspots_row = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔥 Top Modified Files", 
                                  style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'fontWeight': 'bold', 'border': 'none', 'borderBottom': '3px solid #76B900'}),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=self._create_file_hotspots_chart(file_counts),
                            config={'displayModeBar': False}
                        )
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📂 Directory Activity", 
                                  style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'fontWeight': 'bold', 'border': 'none', 'borderBottom': '3px solid #76B900'}),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=self._create_directory_chart(dir_counts),
                            config={'displayModeBar': False}
                        )
                    ])
                ])
            ], width=6)
        ], className="mb-4")
        
        extensions_row = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📄 File Type Distribution", 
                                  style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'fontWeight': 'bold', 'border': 'none', 'borderBottom': '3px solid #76B900'}),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=self._create_extensions_chart(ext_counts),
                            config={'displayModeBar': False}
                        )
                    ])
                ])
            ], width=12)
        ])
        
        return html.Div([hotspots_row, extensions_row])
    
    def _create_timeline_tab(self, commits_df):
        """Create timeline analysis tab"""
        if commits_df.empty:
            return dbc.Alert("No commit data matches your filter criteria.", 
                           style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'border': '2px solid #76B900'})
        
        timeline_chart = dbc.Card([
            dbc.CardHeader("📈 Commit Timeline", 
                          style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'fontWeight': 'bold', 'border': 'none', 'borderBottom': '3px solid #76B900'}),
            dbc.CardBody([
                dcc.Graph(
                    figure=self._create_timeline_chart(commits_df),
                    config={'displayModeBar': True}
                )
            ])
        ])
        
        return timeline_chart
    
    def _create_details_tab(self, commits_df):
        """Create detailed commits table tab"""
        if commits_df.empty:
            return dbc.Alert("No commit data matches your filter criteria.", 
                           style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'border': '2px solid #76B900'})
        
        # prepare data for table
        table_data = commits_df[['commit_short', 'repo_name', 'author', 'date', 'summary', 'files_count']].copy()
        table_data['date'] = table_data['date'].dt.strftime('%Y-%m-%d %H:%M')
        
        details_table = dbc.Card([
            dbc.CardHeader("📋 Detailed Commit Information", 
                          style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'fontWeight': 'bold', 'border': 'none', 'borderBottom': '3px solid #76B900'}),
            dbc.CardBody([
                dash_table.DataTable(
                    data=table_data.to_dict('records'),
                    columns=[
                        {'name': 'Commit', 'id': 'commit_short'},
                        {'name': 'Repository', 'id': 'repo_name'},
                        {'name': 'Author', 'id': 'author'},
                        {'name': 'Date', 'id': 'date'},
                        {'name': 'Summary', 'id': 'summary'},
                        {'name': 'Files', 'id': 'files_count', 'type': 'numeric'},
                    ],
                    style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'system-ui, -apple-system, sans-serif', 'fontSize': '12px'},
                    style_header={'backgroundColor': '#000000', 'color': '#ffffff', 'fontWeight': 'bold', 'border': '1px solid #76B900'},
                    style_data={'backgroundColor': '#ffffff', 'color': '#000000', 'border': '1px solid #cccccc'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f8f9fa'
                        }
                    ],
                    page_size=12,
                    sort_action="native",
                    filter_action="native"
                )
            ])
        ])
        
        return details_table
    
    def _create_json_browser_tab(self):
        """Create JSON browser tab to view raw data"""
        if not self.data:
            return dbc.Alert("No JSON data available.", 
                           style={'backgroundColor': '#f0f8f0', 'color': '#000000', 'border': '2px solid #76B900'})
        
        # flatten JSON data for table display
        table_data = []
        for repo_name, commits in self.data.items():
            if not isinstance(commits, dict):
                continue
                
            for commit_hash, commit_info in commits.items():
                if not isinstance(commit_info, dict):
                    continue
                
                # format changed files as numbered list
                changed_files = commit_info.get('commit_changed_files', [])
                if changed_files:
                    files_str = '\n'.join([f"{i+1}. {file}" for i, file in enumerate(changed_files)])
                else:
                    files_str = 'No files'
                
                # truncate long text fields for better display
                def truncate_text(text, max_length=100):
                    if not text:
                        return ''
                    return text[:max_length] + '...' if len(text) > max_length else text
                
                # special handling for files display - no truncation for files
                def format_files_display(files_str, max_files=10):
                    if not files_str or files_str == 'No files':
                        return files_str
                    lines = files_str.split('\n')
                    if len(lines) > max_files:
                        visible_lines = lines[:max_files]
                        remaining = len(lines) - max_files
                        return '\n'.join(visible_lines) + f'\n... and {remaining} more files'
                    return files_str
                
                # format AI summary for better UX - show call-to-action instead of content
                def format_ai_summary(text, max_display_length=600):
                    if not text or not text.strip():
                        return '📝 **No Analysis**\n\n*Click to generate AI insights*'
                    
                    # Always show call-to-action for better UX
                    return '🤖 **View Details**\n\n*Click to view AI analysis*'
                
                # create row index for detail viewing
                row_index = len(table_data)
                
                # create MR link if URL exists
                commit_url = commit_info.get('commit_url', '')
                mr_link = '[📋 MR](' + commit_url + ')' if commit_url else '🚫 N/A'
                
                row_data = {
                    'repo_name': repo_name,
                    'commit_hash': commit_hash[:12] + '...',
                    'full_hash': commit_hash,  # for tooltip
                    'author': commit_info.get('commit_author', 'Unknown'),
                    'email': commit_info.get('commit_email', 'Unknown'),
                    'date': commit_info.get('commit_date', 'Unknown'),
                    'summary': truncate_text(commit_info.get('commit_summary', ''), 80),
                    'message': truncate_text(commit_info.get('commit_message', ''), 150),
                    'changed_files': format_files_display(files_str, 15),  # show more files, numbered
                    'files_count': len(changed_files),
                    'mr_link': mr_link,
                    'ai_summary': format_ai_summary(commit_info.get('ai_summary', ''), 600),
                    'full_ai_summary': commit_info.get('ai_summary', ''),  # store full summary for modal
                    'row_index': row_index
                }
                table_data.append(row_data)
        
        # create expandable JSON viewer component with dashboard colors
        json_content_section = dbc.Card([
            dbc.CardHeader([
                html.H5("📄 Raw JSON Data Browser", 
                       className="mb-0",
                       style={'color': '#000000', 'fontWeight': 'bold'}),
                html.Small(f"Total records: {len(table_data)}", 
                          style={'color': '#666666'})
            ], style={'backgroundColor': '#f0f8f0', 'border': 'none', 'borderBottom': '3px solid #76B900'}),
            dbc.CardBody([
                # search and filter controls
                dbc.Row([
                    dbc.Col([
                        dbc.InputGroup([
                            dbc.InputGroupText("🔍"),
                            dbc.Input(
                                id="json-search-input",
                                placeholder="Search in table data...",
                                type="text"
                            )
                        ])
                    ], width=6),
                    dbc.Col([
                        dbc.Select(
                            id="json-repo-filter",
                            options=[{"label": "All Repositories", "value": "all"}] + 
                                   [{"label": repo, "value": repo} for repo in sorted(self.data.keys())],
                            value="all"
                        )
                    ], width=3),
                    dbc.Col([
                        dbc.Button([
                            html.I(className="fas fa-download", style={'marginRight': '8px'}),
                            "Export CSV"
                        ], 
                                  id="export-csv-btn",
                                  size="sm",
                                  style={
                                      'backgroundColor': '#76B900', 
                                      'borderColor': '#76B900', 
                                      'color': 'white',
                                      'fontWeight': '500',
                                      'padding': '8px 16px',
                                      'borderRadius': '6px',
                                      'transition': 'all 0.2s ease-in-out',
                                      'boxShadow': '0 2px 4px rgba(118, 185, 0, 0.2)'
                                  })
                    ], width=3)
                ], className="mb-3"),
                
                # main data table with horizontal scroll container
                html.Div([
                    dash_table.DataTable(
                    id='json-data-table',
                    data=table_data,
                    columns=[
                        {'name': 'Repository', 'id': 'repo_name', 'type': 'text'},
                        {'name': 'Commit', 'id': 'commit_hash', 'type': 'text'},
                        {'name': 'Author', 'id': 'author', 'type': 'text'},
                        {'name': 'Email', 'id': 'email', 'type': 'text'},
                        {'name': 'Date', 'id': 'date', 'type': 'text'},
                        {'name': 'Summary', 'id': 'summary', 'type': 'text'},
                        {'name': 'Message', 'id': 'message', 'type': 'text'},
                        {'name': 'Changed Files', 'id': 'changed_files', 'type': 'text'},
                        {'name': 'Files #', 'id': 'files_count', 'type': 'numeric'},
                        {'name': 'MR', 'id': 'mr_link', 'type': 'text', 'presentation': 'markdown'},
                        {'name': 'AI Summary', 'id': 'ai_summary', 'type': 'text', 'presentation': 'markdown'}
                    ],
                    # styling with unified font size
                    style_cell={
                        'textAlign': 'left',
                        'padding': '8px 12px',
                        'fontFamily': 'system-ui, -apple-system, sans-serif',
                        'fontSize': '12px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'minWidth': '80px',
                        'maxWidth': '300px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis'
                    },
                    style_header={
                        'backgroundColor': '#000000',  # dashboard black
                        'color': '#ffffff',            # White text
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                        'border': '1px solid #76B900'  # Green borders
                    },
                    style_data={
                        'backgroundColor': '#ffffff',   # White background
                        'color': '#000000',            # Black text
                        'border': '1px solid #cccccc'  # Light gray borders
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f8f9fa'  # Light gray for alternating rows
                        },
                        {
                            'if': {'column_id': 'mr_link'},
                            'color': '#76B900',           # dashboard green for links
                            'textDecoration': 'underline',
                            'fontWeight': 'bold',
                            'transition': 'all 0.2s ease-in-out'
                        },
                        {
                            'if': {'column_id': 'ai_summary'},
                            'backgroundColor': 'linear-gradient(135deg, #f0f8f0 0%, #e8f5e8 100%)',
                            'border': '2px solid #76B900',
                            'borderRadius': '8px',
                            'cursor': 'pointer',
                            'textAlign': 'center',
                            'fontWeight': '600',
                            'padding': '16px 12px',
                            'boxShadow': '0 2px 4px rgba(118, 185, 0, 0.1)',
                            'transition': 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                            'position': 'relative',
                            'overflow': 'hidden'
                        }
                    ],
                    # functionality
                    page_size=10,
                    sort_action="native",
                    filter_action="native",
                    row_selectable="multi",
                    selected_rows=[],
                    css=[
                        {
                            'selector': '.dash-table-container .dash-cell div.dash-cell-value',
                            'rule': 'display: inline; white-space: inherit; overflow: inherit;'
                        },
                        {
                            'selector': '.dash-table-container .dash-cell[data-dash-column="ai_summary"]',
                            'rule': '''
                                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                                position: relative !important;
                            '''
                        },
                        {
                            'selector': '.dash-table-container .dash-cell[data-dash-column="ai_summary"]:hover',
                            'rule': '''
                                transform: translateY(-2px) !important;
                                box-shadow: 0 8px 25px rgba(118, 185, 0, 0.25) !important;
                                border-color: #5a8c00 !important;
                                background: linear-gradient(135deg, #e8f5e8 0%, #d4f0d4 100%) !important;
                            '''
                        },
                        {
                            'selector': '.dash-table-container .dash-cell[data-dash-column="ai_summary"]:active',
                            'rule': '''
                                transform: translateY(0px) !important;
                                box-shadow: 0 2px 8px rgba(118, 185, 0, 0.2) !important;
                            '''
                        },
                        {
                            'selector': '.dash-table-container .dash-cell[data-dash-column="mr_link"]:hover',
                            'rule': '''
                                color: #5a8c00 !important;
                                transform: scale(1.05) !important;
                                transition: all 0.2s ease-in-out !important;
                            '''
                        },
                        {
                            'selector': '.dash-table-container .dash-cell:hover',
                            'rule': '''
                                background-color: rgba(118, 185, 0, 0.05) !important;
                                transition: background-color 0.2s ease-in-out !important;
                            '''
                        },
                        {
                            'selector': '.dash-table-container thead th',
                            'rule': '''
                                position: sticky !important;
                                top: 0 !important;
                                z-index: 10 !important;
                                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
                            '''
                        }
                    ],
                    # responsive column widths with emphasis on AI Summary
                    style_cell_conditional=[
                        {'if': {'column_id': 'repo_name'}, 'width': '8%', 'minWidth': '80px'},
                        {'if': {'column_id': 'commit_hash'}, 'width': '6%', 'minWidth': '70px'},
                        {'if': {'column_id': 'author'}, 'width': '8%', 'minWidth': '80px'},
                        {'if': {'column_id': 'email'}, 'width': '10%', 'minWidth': '120px'},
                        {'if': {'column_id': 'date'}, 'width': '8%', 'minWidth': '100px'},
                        {'if': {'column_id': 'summary'}, 'width': '12%', 'minWidth': '120px'},
                        {'if': {'column_id': 'message'}, 'width': '15%', 'minWidth': '150px'},
                        {'if': {'column_id': 'changed_files'}, 'width': '15%', 'minWidth': '200px', 
                         'whiteSpace': 'pre-line', 'fontFamily': 'system-ui, -apple-system, sans-serif', 'fontSize': '12px'},
                        {'if': {'column_id': 'files_count'}, 'width': '3%', 'minWidth': '50px', 'textAlign': 'center'},
                        {'if': {'column_id': 'mr_link'}, 'width': '5%', 'minWidth': '60px', 'textAlign': 'center'},
                        {'if': {'column_id': 'ai_summary'}, 'width': '37%', 'minWidth': '450px', 'maxWidth': '500px',
                         'whiteSpace': 'pre-wrap', 'fontFamily': 'system-ui, -apple-system, sans-serif', 
                         'lineHeight': '1.5', 'fontSize': '12px', 'padding': '12px',
                         'overflow': 'auto', 'maxHeight': '200px', 'wordWrap': 'break-word'}
                    ],
                    # tooltip data for enhanced user experience
                    tooltip_data=[
                        {
                            'commit_hash': {'value': f"Full Hash: {row['full_hash']}", 'type': 'text'},
                            'summary': {'value': f"Full Summary: {row['summary']}", 'type': 'text'},
                            'message': {'value': f"Complete Message: {row['message']}", 'type': 'text'},
                            'changed_files': {'value': f"All Changed Files:\n{row['changed_files']}", 'type': 'text'},
                            'mr_link': {'value': '🔗 Click to open commit in repository', 'type': 'text'},
                            'ai_summary': {'value': '🤖 Click for comprehensive AI analysis with detailed insights', 'type': 'text'}
                        } for row in table_data
                    ],
                    tooltip_duration=None
                )], style={'overflowX': 'auto', 'width': '100%'}),
                
                # summary statistics
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        html.H6("📊 Quick Stats", style={'color': '#000000', 'fontWeight': 'bold'}),
                        html.P([
                            f"Total Commits: {len(table_data)}", html.Br(),
                            f"Repositories: {len(set(row['repo_name'] for row in table_data))}", html.Br(),
                            f"Authors: {len(set(row['author'] for row in table_data))}", html.Br(),
                            f"Total Files Changed: {sum(row['files_count'] for row in table_data)}"
                        ], style={'color': '#000000'})
                    ], width=4),
                    dbc.Col([
                        html.H6("💡 User Guide", style={'color': '#000000', 'fontWeight': 'bold'}),
                        html.P([
                            "• **Sort & Filter**: Click column headers to sort, use filter boxes below", html.Br(),
                            "• **Interactive Cells**: Hover over any cell for enhanced visual feedback", html.Br(),
                            "• **AI Analysis**: Click the green 'View Details' button for full AI insights", html.Br(),
                            "• **Quick Links**: Click MR links to open commit pages directly", html.Br(),
                            "• **Export Data**: Use the download button to export filtered results", html.Br(),
                            "• **Multi-Select**: Select multiple rows for batch operations"
                        ], style={'color': '#000000', 'fontSize': '13px', 'lineHeight': '1.6'})
                    ], width=8)
                ])
            ])
        ])
        
        # add modal for detailed AI summary view with enhanced UX
        modal = dbc.Modal([
            dbc.ModalHeader([
                html.Div([
                    html.I(className="fas fa-robot", style={'color': '#76B900', 'marginRight': '12px', 'fontSize': '24px'}),
                    dbc.ModalTitle("AI Analysis Details", 
                                  id="modal-title",
                                  style={'color': '#000000', 'fontWeight': '600', 'fontSize': '20px', 'margin': '0'})
                ], style={'display': 'flex', 'alignItems': 'center'}),
                html.Button(
                    "×",
                    id="close-modal-x",
                    n_clicks=0,
                    style={
                        'background': 'none',
                        'border': 'none',
                        'fontSize': '24px',
                        'color': '#666',
                        'cursor': 'pointer',
                        'padding': '0',
                        'marginLeft': 'auto'
                    }
                )
            ], style={
                'backgroundColor': 'linear-gradient(135deg, #f0f8f0 0%, #e8f5e8 100%)',
                'borderBottom': '3px solid #76B900',
                'borderRadius': '8px 8px 0 0',
                'padding': '20px 24px',
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center'
            }),
            dbc.ModalBody([
                html.Div(id="modal-loading", children=[
                    dbc.Spinner(
                        html.Div(id="loading-output"),
                        size="sm",
                        color="success",
                        type="border",
                        fullscreen=False,
                    )
                ], style={'display': 'none', 'textAlign': 'center', 'padding': '20px'}),
                dcc.Markdown(
                    id="modal-content", 
                    style={
                        'lineHeight': '1.7', 
                        'color': '#000000',
                        'fontSize': '14px',
                        'fontFamily': 'system-ui, -apple-system, sans-serif'
                    }
                )
            ], style={
                'maxHeight': '70vh', 
                'overflowY': 'auto', 
                'backgroundColor': '#ffffff',
                'padding': '24px',
                'borderRadius': '0 0 8px 8px'
            }),
            dbc.ModalFooter([
                html.Div([
                    dbc.Button([
                        html.I(className="fas fa-copy", style={'marginRight': '8px'}),
                        "Copy Content"
                    ], 
                              id="copy-content-btn", 
                              size="sm",
                              outline=True,
                              color="secondary",
                              style={'marginRight': '12px'}),
                    dbc.Button([
                        html.I(className="fas fa-times", style={'marginRight': '8px'}),
                        "Close"
                    ], 
                              id="close-modal", 
                              n_clicks=0,
                              style={
                                  'backgroundColor': '#76B900', 
                                  'borderColor': '#76B900', 
                                  'color': 'white',
                                  'fontWeight': '500',
                                  'padding': '8px 20px',
                                  'borderRadius': '6px',
                                  'transition': 'all 0.2s ease-in-out'
                              })
                ])
            ], style={
                'backgroundColor': '#f8f9fa', 
                'borderTop': '1px solid #e9ecef',
                'borderRadius': '0 0 8px 8px',
                'padding': '16px 24px',
                'display': 'flex',
                'justifyContent': 'flex-end'
            }),
        ], id="detail-modal", is_open=False, size="xl", scrollable=True, 
           style={'borderRadius': '8px', 'overflow': 'hidden'})
        
        return html.Div([json_content_section, modal])
    
    def _create_author_chart(self, commits_df):
        """Create commits by author chart with dashboard colors"""
        author_counts = commits_df['author'].value_counts().head(10)
        fig = px.bar(
            x=author_counts.values,
            y=author_counts.index,
            orientation='h',
            title="Top 10 Authors by Commit Count",
            labels={'x': 'Number of Commits', 'y': 'Author'},
            color_discrete_sequence=['#76B900']  # dashboard green
        )
        fig.update_layout(
            height=400, 
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),
            title=dict(font=dict(color='#000000', size=16))
        )
        fig.update_xaxes(gridcolor='#cccccc', zerolinecolor='#cccccc')
        fig.update_yaxes(gridcolor='#cccccc', zerolinecolor='#cccccc')
        return fig
    
    def _create_repo_chart(self, commits_df):
        """Create commits by repository chart with dashboard colors"""
        repo_counts = commits_df['repo_name'].value_counts()
        # Create green gradient for pie chart
        green_shades = ['#76B900', '#5a8c00', '#4a7a00', '#3a6800', '#2a5600']
        fig = px.pie(
            values=repo_counts.values,
            names=repo_counts.index,
            title="Commits Distribution by Repository",
            color_discrete_sequence=green_shades
        )
        fig.update_layout(
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),
            title=dict(font=dict(color='#000000', size=16))
        )
        fig.update_traces(textfont_color='white', textfont_size=12)
        return fig
    
    def _create_file_hotspots_chart(self, file_counts):
        """Create file hotspots chart with dashboard colors"""
        fig = px.bar(
            x=file_counts.values,
            y=[os.path.basename(f) for f in file_counts.index],
            orientation='h',
            title="Most Modified Files",
            labels={'x': 'Number of Changes', 'y': 'File'},
            color_discrete_sequence=['#76B900']  # dashboard green
        )
        fig.update_layout(
            height=500, 
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),
            title=dict(font=dict(color='#000000', size=16))
        )
        fig.update_xaxes(gridcolor='#cccccc', zerolinecolor='#cccccc')
        fig.update_yaxes(gridcolor='#cccccc', zerolinecolor='#cccccc')
        return fig
    
    def _create_directory_chart(self, dir_counts):
        """Create directory activity chart with dashboard colors"""
        fig = px.bar(
            x=dir_counts.values,
            y=dir_counts.index,
            orientation='h',
            title="Most Active Directories",
            labels={'x': 'Number of Changes', 'y': 'Directory'},
            color_discrete_sequence=['#5a8c00']  # Darker dashboard green
        )
        fig.update_layout(
            height=400, 
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),
            title=dict(font=dict(color='#000000', size=16))
        )
        fig.update_xaxes(gridcolor='#cccccc', zerolinecolor='#cccccc')
        fig.update_yaxes(gridcolor='#cccccc', zerolinecolor='#cccccc')
        return fig
    
    def _create_extensions_chart(self, ext_counts):
        """Create file extensions chart with dashboard colors"""
        # Create black to green gradient for file types
        black_green_shades = ['#000000', '#1a1a1a', '#333333', '#4a7a00', '#5a8c00', '#76B900']
        fig = px.pie(
            values=ext_counts.values,
            names=[ext if ext else 'No Extension' for ext in ext_counts.index],
            title="File Type Distribution",
            color_discrete_sequence=black_green_shades
        )
        fig.update_layout(
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),
            title=dict(font=dict(color='#000000', size=16))
        )
        fig.update_traces(textfont_color='white', textfont_size=12)
        return fig
    
    def _create_timeline_chart(self, commits_df):
        """Create commit timeline chart"""
        if commits_df.empty:
            # return empty chart if no data
            fig = px.line(title="Daily Commit Activity - No Data Available")
            fig.update_layout(height=400)
            return fig
        
        # ensure date column is datetime
        commits_df_copy = commits_df.copy()
        if not pd.api.types.is_datetime64_any_dtype(commits_df_copy['date']):
            # convert to datetime if not already
            commits_df_copy['date'] = pd.to_datetime(commits_df_copy['date'], errors='coerce')
        
        # remove any invalid dates
        commits_df_copy = commits_df_copy.dropna(subset=['date'])
        
        if commits_df_copy.empty:
            # return empty chart if no valid dates
            fig = px.line(title="Daily Commit Activity - No Valid Dates")
            fig.update_layout(height=400)
            return fig
        
        # group by date for daily commit counts
        daily_commits = commits_df_copy.groupby(commits_df_copy['date'].dt.date).size().reset_index()
        daily_commits.columns = ['date', 'commits']
        
        fig = px.line(
            daily_commits,
            x='date',
            y='commits',
            title="Daily Commit Activity",
            labels={'commits': 'Number of Commits', 'date': 'Date'},
            color_discrete_sequence=['#76B900']  # dashboard green
        )
        fig.update_layout(
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),
            title=dict(font=dict(color='#000000', size=16))
        )
        fig.update_xaxes(gridcolor='#cccccc', zerolinecolor='#cccccc')
        fig.update_yaxes(gridcolor='#cccccc', zerolinecolor='#cccccc')
        fig.update_traces(line=dict(color='#76B900', width=3))
        return fig


def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Codet Dashboard - Interactive visualization for Git commit analysis"
    )
    
    parser.add_argument(
        "-p", "--path",
        type=str,
        required=True,
        help="Path to JSON file or directory containing codet analysis results"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address to run the dashboard (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8050,
        help="Port to run the dashboard (default: 8050)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode"
    )
    
    return parser


def main():
    """Main entry point for the dashboard"""
    parser = create_parser()
    args = parser.parse_args()
    
    # check if path exists
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        return 1
    
    # create dashboard instance
    dashboard = CodetDashboard(args.path)
    
    # load data
    print("Loading data...")
    if not dashboard.load_data():
        print("Failed to load data. Please check your JSON file format.")
        return 1
    
    print(f"Successfully loaded {len(dashboard.df_commits)} commits and {len(dashboard.df_files)} file changes")
    
    # create and run app
    print("Creating dashboard...")
    app = dashboard.create_app()
    
    print(f"Starting dashboard at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    
    return 0


if __name__ == "__main__":
    exit(main())