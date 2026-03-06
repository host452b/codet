#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Command line interface module
"""

import sys
import os
import argparse
import codet
from codet.codet import CodeTrailExecutor

class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter
):
    pass


HELLO_CODET = r"""
===========================================================================
---------------------------------codet-------------------------------------
 ██████╗ ██████╗ ██████╗ ███████╗    ████████╗██████╗  █████╗ ██╗██╗     
██╔════╝██╔═══██╗██╔══██╗██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗██║██║     
██║     ██║   ██║██║  ██║█████╗         ██║   ██████╔╝███████║██║██║     
██║     ██║   ██║██║  ██║██╔══╝         ██║   ██╔══██╗██╔══██║██║██║     
╚██████╗╚██████╔╝██████╔╝███████╗       ██║   ██║  ██║██║  ██║██║███████╗
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
 --------------------------------codet-------------------------------------
===========================================================================
"""


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def main():
    """CLI main entry function"""
    print(HELLO_CODET)
    
    parser = argparse.ArgumentParser(
        description=(
            f"codet is a CLI tool for analyzing git commit history."
            f"\n1. quickly understand commit records, analyze code changes, and identify commit hotspots."
            f"\n2. filter commits based on time range, "
            f"search for specific keywords in commit diffs, "
            f"or filter by author email."
            f"\n3. as an optional feature, codet integrates AI through API tokens to provide deeper analysis.\n\n"
        ),
        epilog=(
            "Additional:\n"
            f"\tFor more details, visit https://github.com/host452b/codet"
        ),
        formatter_class=CustomFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {codet.__version__}"
    )
    #########################################################
    ### BASIC OPTIONS
    #########################################################
    parser.add_argument(
        "-d",
        "--days",
        type=int,
        default=30,
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Look back for git commits in the past N days (default: 30 days)"
    )
    parser.add_argument(
        "-e",
        "--email",
        type=str,
        action="append",
        default=[],
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Filter commits by git commit author email, can be used multiple times (e.g., -e user1@example.com -e user2@example.com)"
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        action="append",
        default=[],
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Filter commits by git commit author name, can be used multiple times (e.g., -u 'John Doe' -u 'Jane Smith')"
    )
    parser.add_argument(
        "-k",
        "--keyword",
        type=str,
        action="append",
        default=[],
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Search for keywords in commit diffs, can be used multiple times (e.g., -k keyword1 -k keyword2)"
    )
    parser.add_argument(
        "-c",
        "--commit",
        type=str,
        action="append",
        default=[],
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Filter by specific commit hash (string, can use multiple -c)"
    )
    parser.add_argument(
        "-g",
        "--debug",
        action="store_true",
        default=False,
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Enable debug mode (default: False)"
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        default=True,
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Recursively search for git projects in subdirectories (default: True)"
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=os.getcwd(),
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Specify the path to analyze (default: current directory)"
    )
    parser.add_argument(
        "-s",
        "--hotspot",
        action="store_true",
        default=True,
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Count changes in files and directories within search scope to identify active areas (default: False)"
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["union", "intersection"],
        default="union",
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Search mode: union (match any condition) or intersection (match all conditions) (default: union)"
    )
    #########################################################
    # AI PART OPTIONS
    # supports any OpenAI-compatible API gateway:
    #   - OpenAI, Azure OpenAI, Ollama, vLLM,
    #     LiteLLM, or any OpenAI-compatible gateway.
    # just pass the endpoint via -oe and model via -mo.
    #########################################################
    parser.add_argument(
        "-mo",
        "--model",
        type=str,
        default=None,
        help=(
            f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} "
            "Model name as required by your API provider "
            "(e.g., gpt-4.1, openai/openai/gpt-5-nano, llama3)"
        ),
    )
    parser.add_argument(
        "-to",
        "--api-token",
        type=str,
        default=None,
        help=(
            f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} "
            "Bearer token for the AI endpoint. "
            "If env var AI_API_TOKEN is set, it will override this value. "
            "If not provided, AI analysis is skipped."
        ),
    )
    parser.add_argument(
        "-oe",
        "--openai-endpoint",
        type=str,
        default=None,
        help=(
            f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} "
            "Base URL of any OpenAI-compatible API "
            "(e.g., https://api.openai.com/v1, "
            "http://localhost:11434/v1)"
        ),
    )
    # add custom prompt argument
    parser.add_argument(
        "-cp",
        "--custom-prompt",
        type=str,
        default=None,
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Specify a custom prompt message for the user (default: empty)"
    )
    parser.add_argument(
        "-f",
        "--input-file",
        type=argparse.FileType("r"),
        default=None,
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} Input file to read and AI analyze with prompt (default: None)"
    )
    parser.add_argument(
        "-oj",
        "--output-cook-json",
        action="store_true",
        default=False,
        help=f"{Colors.GREEN}{Colors.BOLD}[Optional]{Colors.END} generate dir repo_name_cook for cook.json file (default: None)"
    )
    # check environment variable and override argument default if present
    api_token_env = os.getenv("AI_API_TOKEN")
    if api_token_env is not None:
        parser.set_defaults(api_token=api_token_env)

    #########################################################
    ### print help if no arguments are provided
    #########################################################
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args()
    
    executor = CodeTrailExecutor(args)
    executor.initialize_repo()
    executor.raw()
    executor.cook()
    executor.hotspot()
    executor.generate_report()
    executor.generate_cook_json()


if __name__ == "__main__":
    main()
