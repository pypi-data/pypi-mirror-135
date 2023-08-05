from setuptools import setup, find_packages

VERSION = '0.85'
DESCRIPTION = 'Python library for client who want to connect with takeme-service'

# Setting up
setup(
    name="takeme-client-python",
    version=VERSION,
    author="Restravity (Ciputra Dhimas)",
    author_email="<ciputra.developer@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['certifi', 'charset-normalizer', 'idna', 'pycryptodome', 'requestor',
                      'requests', 'unicode', 'urllib3'],
    keywords=['takeme', 'takeme client', 'python', 'takeme-client-python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)