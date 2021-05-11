from setuptools import find_packages, setup

setup(name="cryptidsolver",
      version="0.0.1-dev",
      description="Solver for Cryptid boardgame",
      install_requires=[],
      test_requires=["tox", "pytest"],
      packages=find_packages(where=".", exclude="./tests"),
      scripts=[
            "./interactive_solver.py"
      ],
      zip_safe=False)
