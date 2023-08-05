import setuptools

with open("README.md", "r") as file_obj:
    long_description = file_obj.read()

install_requires = [
    "prometheus_client",
    "requests",
    "psutil",
    "pytz",
    "python-dateutil",
    "nubium-schemas>=1.2.0"
]

confluent_requires = [
    "confluent-kafka[avro]==1.6.1"
]

faust_requires = [
    "cython==0.29.17",
    "faust[rocksdb]==1.10.4",
    "idna<3",
    "chardet",
    "python-schema-registry-client<2.0.0",
]

dev_requires = confluent_requires + faust_requires + [
    "pytest",
    "twine",
]

packages = setuptools.find_packages()

setuptools.setup(
    name="nubium-utils",
    version="1.0.1",
    author="Edward Brennan",
    author_email="ebrennan@redhat.com",
    description="Some Kafka utility functions and patterns for the nubium project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.corp.redhat.com/mkt-ops-de/nubium-utils.git",
    packages=packages,
    install_requires=install_requires,
    extras_require={"dev": dev_requires, "confluent": confluent_requires, "faust": faust_requires},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
