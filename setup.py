#!/usr/bin/env python3
"""
Content Nuke - Command-based content automation platform
Transforms development sessions into published multi-platform content
"""

from setuptools import setup, find_packages
import os

# Read VERSION file
with open('VERSION', 'r') as f:
    version = f.read().strip()

# Read README for long description
readme_path = os.path.join('content-nuke-claude', 'README.md')
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = __doc__

setup(
    name='content-nuke',
    version=version,
    description='Command-based content automation platform for Claude Code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jeremy Longshore',
    author_email='jeremylongshore@gmail.com',
    url='https://github.com/jeremylongshore/content-nuke',
    packages=find_packages(),

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],

    keywords='content automation, blog publishing, social media, claude code, slash commands',

    python_requires='>=3.8',

    install_requires=[
        'requests>=2.28.0',
        'python-dotenv>=0.19.0',
    ],

    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'flake8>=5.0.0',
            'mypy>=0.991',
        ],
        'social': [
            'tweepy>=4.14.0',
            'linkedin-api>=2.0.0',
        ],
    },

    entry_points={
        'console_scripts': [
            'content-nuke=scripts.post_x_thread:main',
        ],
    },

    include_package_data=True,
    zip_safe=False,

    project_urls={
        'Bug Reports': 'https://github.com/jeremylongshore/content-nuke/issues',
        'Source': 'https://github.com/jeremylongshore/content-nuke',
        'Documentation': 'https://github.com/jeremylongshore/content-nuke/blob/main/content-nuke-claude/README.md',
    },
)