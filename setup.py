from setuptools import find_packages, setup

with open('./src/xspace/_version.py', 'r') as f:
    version = f.read().split('=')[-1].strip().strip('\'')


setup(name='xspace',  # 包名
      version=version,  # 版本号
      description='xspace is a tool for data processing and visualization',
      long_description='',
      author='zhifeng.ding',
      author_email='zhifeng.ding@hqu.edu.cn',
      url='https://github.com/aidings/pyproj.git',
      license='',
      install_requires=['numpy', 'opencv-python', 'pyyaml', 
                        'ipython', 'pillow', 'loguru', 'six', 'imageio>=2.34.0', 
                        'torch', 'torchvision', 'tqdm', 'safetensors', 'openpyxl'],
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
      packages=find_packages('src', exclude=["examples", "tests", "project"]),  # 必填
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      scripts= [
          './scripts/xproj'
      ],
)