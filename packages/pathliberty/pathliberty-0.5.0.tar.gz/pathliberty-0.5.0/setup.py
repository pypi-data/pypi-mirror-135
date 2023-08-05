import re
from setuptools import setup, find_packages

with open('pathliberty/_version.py', encoding='utf-8') as f:
    version = re.search(r'__version__ = \'([^\'"]+)\'', f.read()).group(1)

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pathliberty',
    author = 'Egor Abramov',
    author_email = 'coreegor@gmail.com',
    version=version,
    description="pathlib extensions",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    download_url=f'https://github.com/coreegor/pathliberty/archive/refs/tags/{version}.tar.gz',
    python_requires='>=3.8',
    install_requires=[
        'paramiko==2.9.2',
    ],
    project_urls={
        'Source': 'https://github.com/coreegor/pathliberty',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ]

)
