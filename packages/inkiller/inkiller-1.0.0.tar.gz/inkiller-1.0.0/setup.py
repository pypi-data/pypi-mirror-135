from setuptools import setup, find_packages
#MAO2116
setup(
    name='inkiller',
    packages=find_packages(),
    include_package_data=True,
    version="1.0.0",
    description='BD SMS BOMBER',
    author='AKXVAU',
    author_email='ak27h.vai@gmail.com',
    long_description=(open("README.md","r")).read(),
    long_description_content_type="text/markdown",
   install_requires=['lolcat','requests'],
 
    keywords=['hacker', 'spam', 'tool', 'sms', 'bomber', 'call', 'prank', 'termux', 'hack','sms bomber','sms bomber', 'AKXVAU', 'inkiller', 'inkill'],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    
    license='MIT',
    entry_points={
            'console_scripts': [
                'inkiller = inkiller.inkiller:menu',
                
            ],
    },
    python_requires='>=3.9'
)
