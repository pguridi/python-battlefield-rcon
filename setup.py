from setuptools import find_packages, setup


with open("README.md") as f:
    readme = f.read()

setup_requirements = []
test_requirements = []

install_requires = [
]

setup(
    name="battlefield_rcon",
    version="0.1.1",
    description="Simple Python client library for Battlefield 3/4 RCON remote management protocol.",
    long_description=readme,
    author="Pedro Guridi",
    author_email="pedro.guridi@gmail.com",
    install_requires=install_requires,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/pguridi/python-battlefield-rcon/",
    setup_requires=setup_requirements,
    entry_points={},
    include_package_data=False,
    packages=find_packages(exclude=["tests"]),
)
