from setuptools import setup, find_packages

setup(name="vyatkin_chat_client",
      version="0.0.1",
      description="vyatkin_chat_client",
      author="Vyatkin M.",
      author_email="",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
