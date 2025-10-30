#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup.py - Cài đặt myPythonTool như một command line tool toàn cục

Mục đích: 
    - Cho phép cài đặt myPythonTool như một package Python
    - Tạo command "myptool" có thể chạy từ bất kỳ đâu

Cách cài đặt:
    pip install -e .        # Cài đặt ở chế độ development (editable)
    
    Hoặc:
    pip install .           # Cài đặt bình thường

Cách sử dụng sau khi cài:
    myptool                 # Chạy từ bất kỳ đâu
"""

from setuptools import setup, find_packages
import os

# Đọc file README
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

# Đọc file requirements
requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
requirements = []
if os.path.exists(requirements_path):
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

# Cấu hình package
setup(
    # Thông tin cơ bản
    name="myPythonTool",
    version="1.0.0",
    description="Bộ công cụ Python đa năng cho các tác vụ hàng ngày",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Tác giả
    author="Your Name",
    author_email="your.email@example.com",
    
    # URL dự án
    url="https://github.com/yourusername/myPythonTool",
    
    # Tìm tất cả packages
    packages=find_packages(),
    
    # Include các file không phải .py
    include_package_data=True,
    package_data={
        '': ['*.json', '*.md', '*.txt'],
    },
    
    # Dependencies
    install_requires=requirements,
    
    # Yêu cầu Python version
    python_requires='>=3.7',
    
    # Entry points - Tạo command line tool
    # Khi cài đặt, sẽ tạo command "myptool" trỏ đến hàm main() trong menu/__init__.py
    entry_points={
        'console_scripts': [
            'myptool=menu:main',
        ],
    },
    
    # Phân loại
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    
    # Keywords
    keywords='utilities tools file-management automation',
)

