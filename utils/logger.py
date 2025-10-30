#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module logger - Logging cho các tools

Mục đích: Ghi lại các thao tác và lỗi để debug
Lý do: Dễ theo dõi và khắc phục sự cố
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


# Global logger instance
_logger: Optional[logging.Logger] = None


def setup_logger(name: str = 'myPythonTool', 
                 log_dir: str = 'logs',
                 log_to_file: bool = True,
                 log_to_console: bool = True,
                 level: int = logging.INFO) -> logging.Logger:
    """
    Thiết lập logger cho tool
    
    Args:
        name: Tên logger
        log_dir: Thư mục chứa log files
        log_to_file: Có ghi log ra file không
        log_to_console: Có hiển thị log trên console không
        level: Mức độ logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logging.Logger: Logger instance
    
    Giải thích:
    - Tạo logger với config linh hoạt
    - Hỗ trợ ghi cả file và console
    - Tự động tạo thư mục logs nếu chưa có
    - Format log message rõ ràng, dễ đọc
    """
    global _logger
    
    # Nếu logger đã tồn tại, trả về luôn
    if _logger is not None:
        return _logger
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Xóa handlers cũ nếu có
    logger.handlers.clear()
    
    # Format log message
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        # Tạo thư mục logs
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        # Tên file log với timestamp
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f'{name}_{timestamp}.log')
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    _logger = logger
    return logger


def get_logger() -> logging.Logger:
    """
    Lấy logger instance hiện tại
    
    Returns:
        logging.Logger: Logger instance
    
    Giải thích:
    - Nếu logger chưa được setup, tự động setup với config mặc định
    - Đảm bảo luôn có logger để sử dụng
    """
    global _logger
    
    if _logger is None:
        _logger = setup_logger()
    
    return _logger


def log_info(message: str) -> None:
    """
    Ghi log thông tin
    
    Args:
        message: Thông báo cần log
    
    Mục đích: Wrapper ngắn gọn cho logger.info()
    """
    logger = get_logger()
    logger.info(message)


def log_error(message: str, exc_info: bool = False) -> None:
    """
    Ghi log lỗi
    
    Args:
        message: Thông báo lỗi
        exc_info: Có ghi exception traceback không
    
    Mục đích: Wrapper ngắn gọn cho logger.error()
    """
    logger = get_logger()
    logger.error(message, exc_info=exc_info)


def log_warning(message: str) -> None:
    """
    Ghi log cảnh báo
    
    Args:
        message: Thông báo cảnh báo
    
    Mục đích: Wrapper ngắn gọn cho logger.warning()
    """
    logger = get_logger()
    logger.warning(message)


def log_debug(message: str) -> None:
    """
    Ghi log debug
    
    Args:
        message: Thông báo debug
    
    Mục đích: Wrapper ngắn gọn cho logger.debug()
    """
    logger = get_logger()
    logger.debug(message)


def log_success(message: str) -> None:
    """
    Ghi log thành công
    
    Args:
        message: Thông báo thành công
    
    Giải thích:
    - Custom log level cho thông báo thành công
    - Dùng INFO level nhưng có prefix đặc biệt
    """
    logger = get_logger()
    logger.info(f"✅ {message}")


def log_operation(operation: str, details: str = '') -> None:
    """
    Ghi log thao tác
    
    Args:
        operation: Tên thao tác
        details: Chi tiết thao tác
    
    Mục đích: Theo dõi các thao tác người dùng thực hiện
    """
    logger = get_logger()
    if details:
        logger.info(f"🔧 {operation} - {details}")
    else:
        logger.info(f"🔧 {operation}")

