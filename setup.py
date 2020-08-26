import io
import os

import setuptools


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(base_dir, 'README.md')
    with io.open(file, encoding='utf-8') as f:
        return f.read()


def get_requirements():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(base_dir, 'requirements.txt')
    with io.open(file, encoding='utf-8') as f:
        content = f.read()
        li_req = content.split('\n')
        return [e.strip() for e in li_req if len(e)]


setuptools.setup(
    name='augbuilder',
    version='0.0.2',
    author='7bits',
    author_email='aloha@7bits.it',
    description='A No-code solution to create the images transformation pipeline.',  # noqa: E501
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    project_urls={
        'source': 'https://gitlab.7bits.it/internship-2020/ml-framework/augmentation-pipeline-builder',  # noqa: E501
        'demo site': 'https://augbuilder.herokuapp.com/',
    },
    packages=setuptools.find_packages(),
    install_requires=get_requirements(),
    include_package_data=True,
    data_files=[
        ('config', ['augbuilder/augmentation.json']),
        ('requirements', ['requirements.txt']),
    ],
    zip_safe=False,
    entry_points={'console_scripts': ['augbuilder = augbuilder.main:run']},
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
