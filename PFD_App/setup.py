from setuptools import setup, find_packages # type: ignore

def load_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name="Hello_World_App",
    version="0.1.0",
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    install_requires=load_requirements(),
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'mein-app=main:hello',
        ],
    },
)
