from setuptools import setup, find_packages

setup(
    name="credforge",
    version="0.1.0",
    description="A collection of tools for credential processing and analysis",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        # List your project's runtime dependencies here
    ],
    entry_points={
        'console_scripts': [
            'split-credentials=split_credentials:main',
            'combine-list-passwords=combine_list_passwords:main',
            'password-analyzer=password_analyzer:main',
            'process-ntds=process_ntds:main',
            'remove-duplicates=remove_duplicates:main',
            'responder2hashcat=responder2hashcat:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
