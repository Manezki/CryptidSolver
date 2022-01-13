from setuptools import find_packages, setup

setup(
    name="cryptidsolver",
    version="0.1.0",
    description="Solver for Cryptid boardgame",
    python_required=">=3.6",
    install_requires=[],
    packages=find_packages(where=".", exclude="./tests"),
    scripts=["./interactive_solver.py"],
    zip_safe=False,
)
