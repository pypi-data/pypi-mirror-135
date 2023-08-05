from setuptools import setup

setup(name='pydta',
      version='0.0.2',
      description='A Python package for drug-target affinity prediction using biomolecular language processing',
      url='https://github.com/boun-tabi/pydta',
      author='Riza Ozcelik',
      author_email='riza.ozcelik@boun.edu.tr',
      license='MIT',
      install_requires=[
            'scikit_learn==0.24.2',
            'tensorflow==2.3.0',
            'torch==1.8.1',
            'tokenizers==0.10.3',
            'transformers==4.10.0',
            'gensim==3.8.3',
            'biopython==1.78',
            'xgboost==1.4.0'
      ],
      include_package_data=True,
      zip_safe=False)