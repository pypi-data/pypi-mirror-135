import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="badurls",
    version="0.7",
    author="Anish M",
    author_email="aneesh25861@gmail.com",
    description="Simple URL obfuscation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    keywords = ['social engineering','cybersecurity','student project'],
    url="https://github.com/Anish-M-code/URL-obfuscator",
    packages=["badurls"],
    classifiers=[
        'Topic :: Security',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Development Status :: 5 - Production/Stable',      
        'Intended Audience :: Developers',  
        'Operating System :: OS Independent',    
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   
        'Programming Language :: Python :: 3',      
        'Intended Audience :: Developers',
        'Intended Audience :: Education',

    ],
    entry_points={"console_scripts": ["badurls = badurls:main",],},
)
