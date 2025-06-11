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
                    self.data = json.load(f)
            elif os.path.isdir(self.json_path):
                # directory with multiple JSON files
                self.data = {}
                for root, dirs, files in os.walk(self.json_path):
                    for file in files:
                        if file.endswith('.json'):
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                file_data = json.load(f)
                                # extract repo name from path
                                repo_name = os.path.basename(root)
                                if repo_name not in self.data:
                                    self.data[repo_name] = {}
                                self.data[repo_name].update(file_data)
            else:
                print(f"Invalid path: {self.json_path}")
                return False
                
            return self._process_data()
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def _process_data(self):
        """Process loaded JSON data into DataFrames"""
        commits_data = []
        files_data = []
        
        for repo_name, commits in self.data.items():
            if not isinstance(commits, dict):
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
        
        # ensure date columns are datetime type
        if not self.df_commits.empty and 'date' in self.df_commits.columns:
            self.df_commits['date'] = pd.to_datetime(self.df_commits['date'], errors='coerce')
        if not self.df_files.empty and 'date' in self.df_files.columns:
            self.df_files['date'] = pd.to_datetime(self.df_files['date'], errors='coerce')
        
        return len(commits_data) > 0
    
    def create_app(self):
        """Create and configure Dash application"""
        # initialize app with Bootstrap theme
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
            suppress_callback_exceptions=True
        )
        
        self.app.title = "Codet Dashboard - Git Analysis Visualization"
        
        # create layout
        self.app.layout = self._create_layout()
        
        # register callbacks
        self._register_callbacks()
        
        return self.app
    
    def _create_layout(self):
        """Create the main dashboard layout"""
        if self.df_commits.empty:
            return dbc.Container([
                dbc.Alert("No data available. Please check your JSON file path.", color="warning"),
            ])
        
        # header
        header = dbc.Row([
            dbc.Col([
                html.H1("🔍 Codet Dashboard", className="text-primary mb-0"),
                html.P("Interactive Git Commit Analysis", className="text-muted"),
            ], width=8),
            dbc.Col([
                dbc.Badge(f"Total Commits: {len(self.df_commits)}", color="info", className="me-2"),
                dbc.Badge(f"Total Files: {len(self.df_files)}", color="success"),
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
                return dbc.Alert(f"Error loading content: {str(e)}", color="danger")
        
        # modal callbacks for AI Summary details
        @callback(
            [Output("detail-modal", "is_open"),
             Output("modal-content", "children"),
             Output("modal-title", "children")],
            [Input("json-data-table", "active_cell"),
             Input("close-modal", "n_clicks")],
            [State("detail-modal", "is_open"),
             State("json-data-table", "data")]
        )
        def toggle_modal(active_cell, close_clicks, is_open, table_data):
            ctx = callback_context
            if not ctx.triggered:
                return False, "", "🤖 AI Analysis Details"
            
            trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
            
            if trigger_id == "close-modal":
                return False, "", "🤖 AI Analysis Details"
            
            if trigger_id == "json-data-table" and active_cell:
                if active_cell['column_id'] == 'AI Summary':
                    row_index = active_cell['row']
                    if row_index < len(table_data):
                        row_data = table_data[row_index]
                        commit_hash = row_data.get('Commit Hash', 'Unknown')
                        repo = row_data.get('Repository', 'Unknown')
                        author = row_data.get('Author', 'Unknown')
                        
                        # get full AI summary
                        full_summary = row_data.get('Full AI Summary', row_data.get('AI Summary', ''))
                        
                        if not full_summary or full_summary.strip() == '*No AI analysis available*':
                            full_summary = "🤔 **No detailed AI analysis available for this commit.**\n\nThis could mean:\n- The AI analysis hasn't been run yet\n- The analysis failed during processing\n- No meaningful insights were generated\n\nYou can try running the codet tool with AI analysis enabled to generate insights for this commit."
                        
                        # format the content with markdown-like structure
                        formatted_content = f"""**Commit:** `{commit_hash}`
**Repository:** {repo}
**Author:** {author}

---

### 🤖 AI Analysis

{full_summary}
"""
                        
                        modal_title = f"🤖 AI Analysis - {repo} ({commit_hash})"
                        return True, formatted_content, modal_title
            
            return is_open, "", "🤖 AI Analysis Details"
    
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
            return dbc.Alert("No data matches your filter criteria.", color="info")
        
        # summary statistics
        stats_cards = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(len(commits_df), className="text-primary"),
                        html.P("Total Commits", className="mb-0")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(commits_df['author'].nunique(), className="text-success"),
                        html.P("Unique Authors", className="mb-0")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(commits_df['repo_name'].nunique(), className="text-info"),
                        html.P("Repositories", className="mb-0")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(len(files_df), className="text-warning"),
                        html.P("File Changes", className="mb-0")
                    ])
                ])
            ], width=3)
        ], className="mb-4")
        
        # charts
        charts_row = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Commits by Author"),
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
                    dbc.CardHeader("📁 Commits by Repository"),
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
            return dbc.Alert("No file data matches your filter criteria.", color="info")
        
        # file hotspots analysis
        file_counts = files_df['file_path'].value_counts().head(20)
        dir_counts = files_df['file_dir'].value_counts().head(15)
        ext_counts = files_df['file_ext'].value_counts().head(10)
        
        hotspots_row = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔥 Top Modified Files"),
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
                    dbc.CardHeader("📂 Directory Activity"),
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
                    dbc.CardHeader("📄 File Type Distribution"),
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
            return dbc.Alert("No commit data matches your filter criteria.", color="info")
        
        timeline_chart = dbc.Card([
            dbc.CardHeader("📈 Commit Timeline"),
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
            return dbc.Alert("No commit data matches your filter criteria.", color="info")
        
        # prepare data for table
        table_data = commits_df[['commit_short', 'repo_name', 'author', 'date', 'summary', 'files_count']].copy()
        table_data['date'] = table_data['date'].dt.strftime('%Y-%m-%d %H:%M')
        
        details_table = dbc.Card([
            dbc.CardHeader("📋 Detailed Commit Information"),
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
                    style_cell={'textAlign': 'left', 'padding': '10px'},
                    style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    page_size=15,
                    sort_action="native",
                    filter_action="native"
                )
            ])
        ])
        
        return details_table
    
    def _create_json_browser_tab(self):
        """Create JSON browser tab to view raw data"""
        if not self.data:
            return dbc.Alert("No JSON data available.", color="info")
        
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
                
                # format AI summary with markdown support and better structure
                def format_ai_summary(text, max_length=300):
                    if not text:
                        return '*No AI analysis available*'
                    
                    # clean up the text
                    cleaned_text = text.strip()
                    
                    # if text is too long, truncate smartly
                    if len(cleaned_text) > max_length:
                        # try to cut at sentence end
                        truncated = cleaned_text[:max_length]
                        last_period = truncated.rfind('.')
                        last_newline = truncated.rfind('\n')
                        
                        if last_period > max_length * 0.7:  # if we can cut at a sentence
                            cleaned_text = cleaned_text[:last_period + 1] + '\n\n*[Click to view full analysis]*'
                        elif last_newline > max_length * 0.7:  # if we can cut at a line
                            cleaned_text = cleaned_text[:last_newline] + '\n\n*[Click to view full analysis]*'
                        else:
                            cleaned_text = truncated + '...\n\n*[Click to view full analysis]*'
                    
                    # add some basic markdown formatting if not already present
                    if not any(marker in cleaned_text for marker in ['**', '*', '`', '#']):
                        # auto-format simple text
                        sentences = [s.strip() for s in cleaned_text.split('.') if s.strip()]
                        if len(sentences) > 1:
                            formatted = f"**{sentences[0]}.**\n\n" + '. '.join(sentences[1:])
                            if not formatted.endswith('.'):
                                formatted += '.'
                            cleaned_text = formatted
                    
                    return cleaned_text
                
                # create row index for detail viewing
                row_index = len(table_data)
                
                row_data = {
                    'Repository': repo_name,
                    'Commit Hash': commit_hash[:12] + '...',
                    'Full Hash': commit_hash,  # for tooltip
                    'Author': commit_info.get('commit_author', 'Unknown'),
                    'Email': commit_info.get('commit_email', 'Unknown'),
                    'Date': commit_info.get('commit_date', 'Unknown'),
                    'Summary': truncate_text(commit_info.get('commit_summary', ''), 80),
                    'Message': truncate_text(commit_info.get('commit_message', ''), 150),
                    'Changed Files': format_files_display(files_str, 15),  # show more files, numbered
                    'Files Count': len(changed_files),
                    'URL': commit_info.get('commit_url', ''),
                    'AI Summary': format_ai_summary(commit_info.get('ai_summary', ''), 300),
                    'Full AI Summary': commit_info.get('ai_summary', ''),  # store full summary for modal
                    'Row Index': row_index
                }
                table_data.append(row_data)
        
        # create expandable JSON viewer component
        json_content_section = dbc.Card([
            dbc.CardHeader([
                html.H5("📄 Raw JSON Data Browser", className="mb-0"),
                html.Small(f"Total records: {len(table_data)}", className="text-muted")
            ]),
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
                        dbc.Button(
                            "💾 Export CSV", 
                            id="export-csv-btn",
                            color="primary",
                            size="sm"
                        )
                    ], width=3)
                ], className="mb-3"),
                
                # main data table with horizontal scroll container
                html.Div([
                    dash_table.DataTable(
                    id='json-data-table',
                    data=table_data,
                    columns=[
                        {'name': 'Repository', 'id': 'Repository', 'type': 'text'},
                        {'name': 'Commit', 'id': 'Commit Hash', 'type': 'text'},
                        {'name': 'Author', 'id': 'Author', 'type': 'text'},
                        {'name': 'Email', 'id': 'Email', 'type': 'text'},
                        {'name': 'Date', 'id': 'Date', 'type': 'text'},
                        {'name': 'Summary', 'id': 'Summary', 'type': 'text'},
                        {'name': 'Message', 'id': 'Message', 'type': 'text'},
                        {'name': 'Changed Files', 'id': 'Changed Files', 'type': 'text'},
                        {'name': 'Files #', 'id': 'Files Count', 'type': 'numeric'},
                        {'name': 'MR_LINK', 'id': 'URL', 'type': 'text', 'presentation': 'markdown'},
                        {'name': 'AI Summary', 'id': 'AI Summary', 'type': 'text', 'presentation': 'markdown'}
                    ],
                    # styling
                    style_cell={
                        'textAlign': 'left',
                        'padding': '8px 12px',
                        'fontFamily': 'Arial, sans-serif',
                        'fontSize': '11px',
                        'whiteSpace': 'pre-wrap',
                        'height': 'auto',
                        'minWidth': '80px',
                        'maxWidth': '300px',
                        'overflow': 'auto'
                    },
                    style_header={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center'
                    },
                    style_data={
                        'backgroundColor': 'rgb(248, 249, 250)',
                        'border': '1px solid rgb(220, 220, 220)'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(255, 255, 255)'
                        },
                        {
                            'if': {'column_id': 'URL'},
                            'color': 'blue',
                            'textDecoration': 'underline'
                        },
                        {
                            'if': {'column_id': 'AI Summary'},
                            'backgroundColor': 'rgb(248, 251, 255)',
                            'border': '1px solid rgb(220, 238, 255)',
                            'borderRadius': '4px',
                            'cursor': 'pointer'
                        }
                    ],
                    # functionality
                    page_size=20,
                    sort_action="native",
                    filter_action="native",
                    row_selectable="multi",
                    selected_rows=[],
                    # responsive column widths with emphasis on AI Summary
                    style_cell_conditional=[
                        {'if': {'column_id': 'Repository'}, 'width': '8%', 'minWidth': '80px'},
                        {'if': {'column_id': 'Commit Hash'}, 'width': '6%', 'minWidth': '70px'},
                        {'if': {'column_id': 'Author'}, 'width': '8%', 'minWidth': '80px'},
                        {'if': {'column_id': 'Email'}, 'width': '10%', 'minWidth': '120px'},
                        {'if': {'column_id': 'Date'}, 'width': '8%', 'minWidth': '100px'},
                        {'if': {'column_id': 'Summary'}, 'width': '12%', 'minWidth': '120px'},
                        {'if': {'column_id': 'Message'}, 'width': '15%', 'minWidth': '150px'},
                        {'if': {'column_id': 'Changed Files'}, 'width': '15%', 'minWidth': '200px', 
                         'whiteSpace': 'pre-line', 'fontFamily': 'monospace', 'fontSize': '10px'},
                        {'if': {'column_id': 'Files Count'}, 'width': '3%', 'minWidth': '50px', 'textAlign': 'center'},
                        {'if': {'column_id': 'URL'}, 'width': '5%', 'minWidth': '60px'},
                        {'if': {'column_id': 'AI Summary'}, 'width': '35%', 'minWidth': '450px', 
                         'whiteSpace': 'pre-wrap', 'fontFamily': 'system-ui, -apple-system, sans-serif', 
                         'lineHeight': '1.5', 'fontSize': '12px', 'padding': '12px'}
                    ],
                    # tooltip data for full content
                    tooltip_data=[
                        {
                            'Commit Hash': {'value': row['Full Hash'], 'type': 'text'},
                            'Summary': {'value': row['Summary'], 'type': 'markdown'},
                            'Message': {'value': row['Message'], 'type': 'markdown'},
                            'Changed Files': {'value': row['Changed Files'], 'type': 'markdown'},
                            'AI Summary': {'value': 'Click to view detailed AI analysis in modal', 'type': 'text'}
                        } for row in table_data
                    ],
                    tooltip_duration=None
                )], style={'overflowX': 'auto', 'width': '100%'}),
                
                # summary statistics
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        html.H6("📊 Quick Stats"),
                        html.P([
                            f"Total Commits: {len(table_data)}", html.Br(),
                            f"Repositories: {len(set(row['Repository'] for row in table_data))}", html.Br(),
                            f"Authors: {len(set(row['Author'] for row in table_data))}", html.Br(),
                            f"Total Files Changed: {sum(row['Files Count'] for row in table_data)}"
                        ])
                    ], width=4),
                    dbc.Col([
                        html.H6("💡 Tips"),
                        html.P([
                            "• Click column headers to sort", html.Br(),
                            "• Use the filter boxes under headers", html.Br(),
                            "• Hover over cells to see full content", html.Br(),
                            "• Click on AI Summary for detailed analysis", html.Br(),
                            "• Select rows and export data"
                        ])
                    ], width=8)
                ])
            ])
        ])
        
        # add modal for detailed AI summary view
        modal = dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("🤖 AI Analysis Details", id="modal-title")),
            dbc.ModalBody([
                dcc.Markdown(id="modal-content", style={'lineHeight': '1.6'})
            ], style={'maxHeight': '70vh', 'overflowY': 'auto'}),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
            ),
        ], id="detail-modal", is_open=False, size="xl", scrollable=True)
        
        return html.Div([json_content_section, modal])
    
    def _create_author_chart(self, commits_df):
        """Create commits by author chart"""
        author_counts = commits_df['author'].value_counts().head(10)
        fig = px.bar(
            x=author_counts.values,
            y=author_counts.index,
            orientation='h',
            title="Top 10 Authors by Commit Count",
            labels={'x': 'Number of Commits', 'y': 'Author'}
        )
        fig.update_layout(height=400, showlegend=False)
        return fig
    
    def _create_repo_chart(self, commits_df):
        """Create commits by repository chart"""
        repo_counts = commits_df['repo_name'].value_counts()
        fig = px.pie(
            values=repo_counts.values,
            names=repo_counts.index,
            title="Commits Distribution by Repository"
        )
        fig.update_layout(height=400)
        return fig
    
    def _create_file_hotspots_chart(self, file_counts):
        """Create file hotspots chart"""
        fig = px.bar(
            x=file_counts.values,
            y=[os.path.basename(f) for f in file_counts.index],
            orientation='h',
            title="Most Modified Files",
            labels={'x': 'Number of Changes', 'y': 'File'}
        )
        fig.update_layout(height=500, showlegend=False)
        return fig
    
    def _create_directory_chart(self, dir_counts):
        """Create directory activity chart"""
        fig = px.bar(
            x=dir_counts.values,
            y=dir_counts.index,
            orientation='h',
            title="Most Active Directories",
            labels={'x': 'Number of Changes', 'y': 'Directory'}
        )
        fig.update_layout(height=400, showlegend=False)
        return fig
    
    def _create_extensions_chart(self, ext_counts):
        """Create file extensions chart"""
        fig = px.pie(
            values=ext_counts.values,
            names=[ext if ext else 'No Extension' for ext in ext_counts.index],
            title="File Type Distribution"
        )
        fig.update_layout(height=400)
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
            labels={'commits': 'Number of Commits', 'date': 'Date'}
        )
        fig.update_layout(height=400)
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