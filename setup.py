from setuptools import setup, find_namespace_packages
setup(
    name='bot_helper',

    packages=find_namespace_packages(),
    install_requires=['markdown'],
    entry_points={'console_scripts': ['bot_helper=project_GO_IT_Python_Core.main:main']}
)