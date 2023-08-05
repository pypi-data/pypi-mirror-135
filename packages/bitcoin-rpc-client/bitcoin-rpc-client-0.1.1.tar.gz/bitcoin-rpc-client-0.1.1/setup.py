from pathlib import Path
from setuptools import setup

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

def get_requirements(req_file):
    """
    Extract requirements from provided file.
    """
    req_path = Path(req_file)
    requirements = req_path.read_text().split("\n") if req_path.exists() else []
    return requirements

setup(
    name="bitcoin-rpc-client",
    version="0.1.1",
    keywords="bitcoin btc json-rpc rpc client",
    description="Bitcoin RPC Client",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/c0mm4nd/bitcoin-rpc-client",
    author="CommandM",
    author_email="maoxs2@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["bitcoin_rpc_client"],
    include_package_data=True,
    install_requires=get_requirements("requirements.txt"),
)
