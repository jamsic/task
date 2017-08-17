from setuptools import setup, find_packages

setup(name='module',
      version='0.1',
      description='module',
      url='http://github.com/jamsic/task',
      author='jamsic',
      author_email='jamsic@yandex.ru',
      packages=find_packages(),
      package_data={'module': ['parser/keywords_parser/keywords_provider/data/techs_keywords.csv', 'crawler/data/data.db', 'urlprovider/data/urls.txt']},
      install_requires=[
          'nltk', 'requests', 'numpy', 'bs4'
      ],
      zip_safe=False)
