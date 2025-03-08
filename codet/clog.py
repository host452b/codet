#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Logging system module
Provides colored log output functionality
"""

import os
import sys
import logging
import colorlog
from typing import Optional


class Logger:
    """Logger class that provides colored log output"""
    
    # Log level mapping
    LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    # Color mapping
    COLORS = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    
    def __init__(self, name: str = 'codet', level: str = 'info', 
                 log_file: Optional[str] = None):
        """
        Initialize logger
        
        Args:
            name (str): Logger name
            level (str): Log level, options: debug, info, warning, error, critical
            log_file (str, optional): Log file path, if provided will also output to file
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.LEVELS.get(level.lower(), logging.INFO))
        self.logger.handlers = []  # Clear existing handlers
        
        # Create console handler and set colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors=self.COLORS
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Create file handler if log file path is provided
        if log_file:
            os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Output debug level log"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Output info level log"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Output warning level log"""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False, stack_info: bool = False):
        """
        Output error level log
        
        Args:
            message (str): Error message
            exc_info (bool): Whether to include exception info, defaults to False
            stack_info (bool): Whether to include stack info, defaults to False
        """
        import traceback
        stack_trace = "\n" + traceback.format_stack()[:-1]
        self.logger.error(f"{message}{stack_trace if stack_info else ''}", exc_info=exc_info)
    
    def critical(self, message: str):
        """Output critical error level log"""
        self.logger.critical(message)


# Create default logger instance
default_logger = Logger()

# Export convenience functions
debug = default_logger.debug
info = default_logger.info
warning = default_logger.warning
error = default_logger.error
critical = default_logger.critical

