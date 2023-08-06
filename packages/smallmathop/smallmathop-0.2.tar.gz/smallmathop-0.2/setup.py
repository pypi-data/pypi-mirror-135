from setuptools import setup, find_packages



setup(
    name='smallmathop',
    version='0.2',
    description='Math Operations Tool',
    long_description='Some basic math operations',
    long_description_content_type='text/markdown',
    author='Satya',
    author_email='supersuper1075@gmail.com',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    # Find all packages (__init__.py)
     package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",

   

    # dependency_links=[]
)