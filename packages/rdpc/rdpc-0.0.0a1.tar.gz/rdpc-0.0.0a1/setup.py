import setuptools

setuptools.setup(
    name="rdpc",
    version="0.0.0-alpha1",
    description="Data Producer and consumer Library for Kafka.",
    packages=setuptools.find_packages("src"),
    package_dir={'' : 'src'},
    author="Yulong",
    author_email="yulong.wang@rakuten.com",
    licenses="",
    install_requires=['']
)