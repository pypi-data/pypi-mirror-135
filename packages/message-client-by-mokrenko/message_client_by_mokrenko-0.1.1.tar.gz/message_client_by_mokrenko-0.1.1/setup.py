from setuptools import setup, find_packages

setup(name="message_client_by_mokrenko",
      version="0.1.1",
      description="Message Client Package",
      author="Vladimir Mokrenko",
      author_email="v.v.mokrenko@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
