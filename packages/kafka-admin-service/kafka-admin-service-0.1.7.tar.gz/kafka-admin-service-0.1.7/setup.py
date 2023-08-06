# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, 'requirements.txt'), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="kafka-admin-service",
    version="0.1.7",
    description="Kafka admin service class, provides basic management functions such as USER creation, USER deletion, USER listing all and USER password changing, TOPIC creation, TOPIC deletion, TOPIC listing all, and ACL creation, ACL deletion and ACL listing all.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    license_files=("LICENSE",),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=["kafka admin service", "kafka admin client"],
    py_modules=["kafka_admin_service"],
    install_requires=requires,
    packages=find_packages("."),
    zip_safe=False,
    include_package_data=True,
)