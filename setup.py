from setuptools import setup, find_packages
from pkg_resources import parse_requirements

with open('requirements.txt', encoding='utf-8') as f:
    install_requires = [str(requirement) for requirement in parse_requirements(f)]

setup(
    name='semantic-human-matting',
    version='1.0.0',
    author='Chen et al.',
    description='Robust Human Matting via Semantic Guidance, ACCV 2022',
    license='MIT license',
    url='https://github.com/wangziyao318/SemanticGuidedHumanMatting',
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(),
    install_requires = install_requires
)
