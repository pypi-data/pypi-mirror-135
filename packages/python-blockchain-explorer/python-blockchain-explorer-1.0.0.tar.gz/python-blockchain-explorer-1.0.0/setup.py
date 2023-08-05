from setuptools import setup

setup(
    name="python-blockchain-explorer",
    version="1.0.0",
    description="A minimal, yet complete, python API for etherscan.io. arbiscan.io ...",
    url="https://github.com/orthogonalglobal/python-blockchain-explorer",
    author="Dion and Robert",
    license="MIT",
    packages=[
        "explorer",
        "explorer.configs",
        "explorer.enums",
        "explorer.modules",
        "explorer.utils",
    ],
    install_requires=["requests"],
    include_package_data=True,
    zip_safe=False,
)
