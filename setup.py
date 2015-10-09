from setuptools import setup

setup(
    name="sd-ironmq",
    version="0.1.2",
    description="Server Density plugin to monitor IronMQs",
    long_description=open('README.rst').read() + '\n\n',
    author="Murat Knecht",
    author_email="muratk@engagespark.com",
    url="https://github.com/engagespark/sd-ironmq",
    license="MIT",
    py_modules=["IronMQ"],
    install_requires=open("requirements.txt").read().split(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
    ],
)
