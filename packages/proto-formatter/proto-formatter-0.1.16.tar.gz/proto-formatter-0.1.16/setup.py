import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

install_requires = [
    'attrdict>=2.0.1',
]

dev_requires = [
    'build==0.5.1',
    'twine>=3.4.2,<4',
    'pip-tools>=5,<6',
    'pytest>=6.2.4,<6.3',
    'attrdict>=2.0.1',
]

setuptools.setup(
    name="proto-formatter",
    version="0.1.16",
    author="YiXiaoCuoHuaiFenZi",
    author_email="249664317@qq.com",
    description="Protocol Buffers file formatter.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YiXiaoCuoHuaiFenZi/proto-formatter",
    project_urls={
        "Bug Tracker": "https://github.com/YiXiaoCuoHuaiFenZi/proto-formatter/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=install_requires,
    setup_requires=[],
    tests_require=[],
    extras_require={
        "dev": dev_requires
    },
    entry_points={
        'console_scripts': ['proto_formatter=proto_formatter.main:main'],
    },
)
