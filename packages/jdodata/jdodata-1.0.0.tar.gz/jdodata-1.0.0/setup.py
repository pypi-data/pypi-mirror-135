import os

from setuptools import setup


def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        else:
            requires.append(pkg)
    return requires


setup(name='jdodata',
      version='1.0.0',
      description="Jianda Open Data",
      long_description="",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "License :: OSI Approved :: Apache Software License",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: SQL",
                   "Topic :: Database"],
      keywords='',
      author='@wukehao',
      author_email='wukehao@jddatatech.com',
      license='MIT',
      packages=['jdodata'],
      include_package_data=True,
      package_data={},
      zip_safe=True,
      install_requires=_process_requirements(),
      entry_points="")
