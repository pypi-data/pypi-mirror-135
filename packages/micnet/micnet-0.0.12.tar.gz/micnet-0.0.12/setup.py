import setuptools

# Setting up
setuptools.setup(
        name="micnet", 
        version="0.0.12",
        author="Natalia Favila, David Madrigal-Trejo, Daniel Legorreta",
        author_email="natalia.favila.v@gmail.com",
        description="Toolbox for the visualization and analysis of microbial datasets",
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
	install_requires=['pandas', 
			  'numpy == 1.20.3',
		          'umap-learn == 0.5.1',
                          'typing',
                          'webcolors',
                          'matplotlib-base',
                          'streamlit == 0.88.0',
                          'bokeh == 2.2.2',
	],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
        ],
	include_package_data=True,
	packages=setuptools.find_packages(),
	package_data={'': ['data/*.txt']},
)