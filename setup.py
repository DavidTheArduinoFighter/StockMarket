from setuptools import setup, find_packages

setup(
    name='StockLib',
    version='1.1.0',
    description='A library to manage stock data and fetch from DB',
    author='David Ogorevc',
    url='https://github.com/DavidTheArduinoFighter/StockMarket',
    packages=find_packages(include=['lib', 'docker', 'docker.python']),
    include_package_data=True,
    install_requires=[
        'mariadb',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
