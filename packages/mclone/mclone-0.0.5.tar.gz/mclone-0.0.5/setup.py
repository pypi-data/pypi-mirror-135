from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()






setup(
    name='mclone',
    packages=find_packages(),
    include_package_data=True,
    version="0.0.5",
    description='Facebook Old Id cloning!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='mao2116',
    author_email='mao2116@yandex.com',
    install_requires=['lolcat','requests',"mechanize"],
    
    
    keywords=["maohacker", "fb hack", " hacking tool", "clone fb", "maotool", "hack", 'fb', "hack", "termux", "mclone", "cloner", "facebook hack", "hackmao2116"],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    
    license='MIT',
    entry_points={
            'console_scripts': [
                'mclone = mclone.main_fuck:mao_main',
            ],
    },
    python_requires='<=2.7.18'
)
