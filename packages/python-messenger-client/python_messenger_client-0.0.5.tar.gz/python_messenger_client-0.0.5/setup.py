from setuptools import setup, find_packages
setup(name="python_messenger_client",
      version="0.0.5",
      description="Messenger Client",
      author="Sergey Kurskiy",
      author_email="kurskiisergey@mail.ru",
      packages=find_packages(),
      install_requires=['PySide2', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      package_data={
            '': ['*.ini', "client\\gui\\ui\\*.ui"],
      },
      )
