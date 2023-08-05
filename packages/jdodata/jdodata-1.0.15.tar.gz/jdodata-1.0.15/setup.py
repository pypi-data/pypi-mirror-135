import os
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

    print(requires)
    return requires



def _process_readme():
    with open('README.rst', encoding='utf-8') as fp:
        return fp.read()
    return ''


setup(name='jdodata',
      version='1.0.15',
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
      packages=['jdodata', 'jdodata.utils'],
      include_package_data=True,
      package_data={},
      zip_safe=True,
      setup_requires=['requests'],
      install_requires=_process_requirements(),
      entry_points="")
