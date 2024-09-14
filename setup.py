from setuptools import setup, find_packages

setup(
    name='Stocklib',
    version='1.1.0',
    description='A library to manage stock data and fetch from DB',
    author='David Ogorevc',
    url='https://github.com/DavidTheArduinoFighter/StockMarket',
    packages=find_packages(include=['lib']),
    install_requires=[  # External dependencies
        'mariadb',
        'requests',
    ],
    classifiers=[  # Optional classifiers
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
