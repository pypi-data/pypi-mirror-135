import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kaskada_grpc",
    version="0.0.6",
    author="Kaskada",
    author_email="support@kaskada.com",
    description="Kaskada's gRPC client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://kaskada.com",
    project_urls={
        "Documentation": "https://docs.kaskada.com/",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Jupyter",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
    ],
    package_dir={"": "src"},
    packages=["kaskada.api.v1alpha", "kaskada.errdetails.v1alpha", "validate"],
    python_requires=">=3.6",
    install_requires=[
        'grpcio~=1.34.0',
        'grpcio-tools',
        'googleapis-common-protos',
        'protobuf',
    ],
)
