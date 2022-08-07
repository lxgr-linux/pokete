#!/usr/bin/env python3

from setuptools import setup

setup(
    name="pokete",
    version="0.8.2",
    description="A terminal based Pokemon like game",
    author="lxgr-linux",
    author_email="lxgr@protonmail.com",
    license="GPL-3.0",
    packages=["pokete", "pokete.pokete_data", "pokete.pokete_classes", "pokete.playsound", "scrap_engine"],
    entry_points={
        'console_scripts': [
            'pokete = pokete:run_pokete'
        ]
    },
    install_requires=[],
    package_data={"pokete": ["assets/music/*", "playsound/libplaysound.so"]},
    include_package_data=True
)
