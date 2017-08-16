from setuptools import setup, find_packages

setup(name='module',
      version='0.1',
      description='module',
      url='http://github.com/jamsic/task',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      packages=find_packages(),
      package_data={'module': ['parser/keywords_parser/keywords_provider/data/techs_keywords.csv', 'crawler/data/data.db', 'urlprovider/data/urls.txt']},
      install_requires=[
          'nltk'
      ],
      zip_safe=False)
