import io
import os
PATH = os.path.abspath (os.path.dirname (__file__))

from setuptools import setup


with io.open (os.path.join (PATH, 'README.md'), encoding = 'utf-8') as f:
  long_description = f.read()

setup (
        name = 'optunapi',
        version = '0.1.4',
        author  = 'Matteo Barbetti',
        author_email = 'matteo.barbetti@fi.infn.it',
        description  = 'API to distribute hyperparameters optimization through HTTP requests',
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/mbarbetti/optunapi',
        license = 'MIT',
        python_requires  = '>=3.6',
        install_requires = [
                             'optuna',
                             'fastapi',
                             'requests',
                             'uvicorn[standard]',
                           ],
        classifiers = [
                        'Development Status :: 3 - Alpha',
                        'Intended Audience :: Science/Research',
                        'Intended Audience :: Developers',
                        'License :: OSI Approved :: MIT License',
                        'Programming Language :: Python :: 3',
                        'Programming Language :: Python :: 3.6',
                        'Programming Language :: Python :: 3.7',
                        'Programming Language :: Python :: 3.8',
                        'Programming Language :: Python :: 3.9',
                        'Programming Language :: Python :: 3 :: Only',
                        'Topic :: Scientific/Engineering',
                        'Topic :: Scientific/Engineering :: Mathematics',
                        'Topic :: Scientific/Engineering :: Artificial Intelligence',
                        'Topic :: Internet',
                        'Topic :: Internet :: WWW/HTTP',
                        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                      ],
  )
  