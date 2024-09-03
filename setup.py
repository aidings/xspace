from setuptools import find_packages, setup

try:
    import subprocess
    result = subprocess.check_output('python -m setuptools_scm', shell=True)
    version = result.decode(encoding='utf-8').strip() 
    version = version.split('+')[0]
    with open('./src/xspace/_version.py', 'w') as f:
        f.write(f"__version__ = '{version}'\n")
except:
    with open('./src/xspace/_version.py', 'r') as f:
        version = f.read().split('=')[-1].strip().strip('\'')

setup(name='xspace',  # 包名
      version=version,  # 版本号
      description='create a empty python package',
      long_description='',
      author='zhifeng.ding',
      author_email='zhifeng.ding@hqu.edu.cn',
      url='https://github.com/aidings/pyproj.git',
      license='',
      install_requires=['setuptools_scm', 'numpy', 'opencv-python', 'pyyaml', 'ipython', 'pillow', 'loguru', 'six', 'imageio>=2.34.0', 'torch', 'torchvision', 'tqdm', 'safetensors'],
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