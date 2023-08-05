from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Gdrive auth and list drive package'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="airflow_cust_base", 
        version=VERSION,
        author="Simona",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=['oauth2client'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'gdrive'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
