import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pdp-kafka-reader",
    version="0.0.5",
    author="Filip Beć",
    author_email="filip.bec@porsche.digital",
    description="PDP Kafka package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    scripts=[
        "bin/kafka-reader",
        "bin/export-avro-jar",
    ],
    python_requires=">=3.6",
    package_data={
        "pdp_kafka_reader": ["jars/*"],
    },
    zip_safe=False,
    install_requires=[
        "fastavro==1.4.7",
        "pandas==1.1.5",
        "numpy==1.19.5",
        "pyarrow==3.0.0",
        "importlib_resources",
    ],
)
