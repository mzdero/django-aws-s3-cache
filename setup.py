from setuptools import setup, find_packages

setup(
    name='django-aws-s3-cache',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'boto3==1.21.*',
        'Django==4.1.*',
    ],
    author='Max Zdero',
    author_email='max.zdero@gmail.com',
    description='A Django cache backend using AWS S3',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mzdero/django-aws-s3-cache',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Framework :: Django',
    ],
)
