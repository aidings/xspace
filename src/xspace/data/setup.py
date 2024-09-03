# -*- coding: utf-8 -*-
# Copyright 2019 Vivo Inc. All Rights Reserved.
# @Time             : 2019/10/20 8:59 AM
# @Author           : ding
# @File             : setup.py
# @description      :
from setuptools import find_packages, setup

try:
    import subprocess
    result = subprocess.check_output('python -m setuptools_scm', shell=True)
    version = result.decode(encoding='utf-8').strip() 
    version = version.split('+')[0]
    with open('./src/{name}/_version.py', 'w') as f:
        f.write(f"__version__ = '{version}'\n")
except:
    with open('./src/{name}/_version.py', 'r') as f:
        version = f.read().split('=')[-1].strip().strip('\'')

setup(name='{name}',        # package name
      version=version,      # version number
      description='',
      long_description='',
      author='zhifeng.ding',
      author_email='zhifeng.ding@hqu.edu.cn',
      url='',
      license='',
      install_requires=[],
      extras_require={},
      dependency_links=[
          "https://pypi.tuna.tsinghua.edu.cn/simple",
          "http://mirrors.aliyun.com/pypi/simple"
      ],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2'
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('src', exclude=["examples", "tests", "project"]),  # must be set when packages is not empty
      package_dir={'': 'src'},  # must be set when packages is not empty
      include_package_data=True,
      scripts= [
          # './script/xxx.py'
      ],
)