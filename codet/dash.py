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
from dash import dcc, html, Input, Output, callback, dash_table
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
                    
                # process commit data
                commit_date = commit_info.get('commit_date', '')
                if commit_date:
                    try:
                        if isinstance(commit_date, str):
                            # try different date formats
                            for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                                try:
                                    commit_date = datetime.strptime(commit_date, fmt)
                                    break
                                except ValueError:
                                    continue
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
                            start_date=self.df_commits['date'].min(),
                            end_date=self.df_commits['date'].max(),
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
                            value=list(self.df_commits['author'].unique()),
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
                            value=list(self.df_commits['repo_name'].unique()),
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
                            value=list(self.df_files['file_ext'].unique()),
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
            
            return html.Div("Select a tab to view content")
    
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
        # group by date for daily commit counts
        daily_commits = commits_df.groupby(commits_df['date'].dt.date).size().reset_index()
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