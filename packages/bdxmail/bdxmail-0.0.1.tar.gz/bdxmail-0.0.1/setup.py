from setuptools import setup, find_packages
setup(
    name='bdxmail',
    packages=find_packages(),
    include_package_data=True,
    version="0.0.1",
    description='BD EMAIL BOMBER',
    author='AKXVAU',
    author_email='bdXsms69@gmail.com',
    long_description=(open("README.md","r")).read(),
    long_description_content_type="text/markdown",
   install_requires=['lolcat','requests'],
 
    keywords=['hacker', 'spam', 'tool', 'fmail', 'bomber', 'call', 'prank', 'termux', 'hack','fmail bomber','fmail bomber', 'AKXVAU', 'bdxfmail', 'xbomber', 'bdsms.ml', 'python',  'python fmail', 'python bomber', 'python spam','inbox killer', 'inbox', 'killmail', 'bdxmail'],
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
                'bdxmail = bdxmail.bdxmail:menu',
                
            ],
    },
    python_requires='>=3.9'
)
