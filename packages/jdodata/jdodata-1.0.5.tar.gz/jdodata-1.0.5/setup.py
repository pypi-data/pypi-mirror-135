import os
import requests
from setuptools import setup


def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(
                return_code)
        else:
            requires.append(pkg)
    return requires

def _md_to_rst(fp):
    """
    将markdown格式转换为rst格式
    @param from_file: {str} markdown文件的路径
    @param to_file: {str} rst文件的路径
    """
    response = requests.post(
        url='http://c.docverter.com/convert',
        data={'to': 'rst', 'from': 'markdown'},
        files={'input_files[]': fp}
    )

    if response.ok:
        return response.content.decode('utf-8')
    return ''


def _process_readme():
    content = ""
    with open('README.md') as fp:
        content = _md_to_rst(fp)
    return content


setup(name='jdodata',
      version='1.0.5',
      description="Jianda Open Data",
      long_description=_process_readme(),
      classifiers=["Development Status :: 5 - Production/Stable",
                   "License :: OSI Approved :: Apache Software License",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3.9",
                   "Programming Language :: Python :: 3.10",
                   "Topic :: Office/Business :: Financial"
                   ],
      keywords='简答数据,jianda,jianda data,open data',
      author='@wukehao',
      author_email='wukehao@jddatatech.com',
      license='MIT',
      packages=['jdodata'],
      include_package_data=True,
      package_data={},
      zip_safe=True,
      install_requires=_process_requirements(),
      entry_points="")
