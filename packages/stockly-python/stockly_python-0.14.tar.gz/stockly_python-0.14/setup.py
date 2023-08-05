from distutils.core import setup

setup(
    name='stockly_python',  # How you named your package folder (MyLib)
    packages=['stockly_python'],  # Chose the same as "name"
    version='0.14',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='testing',  # Give a short description about your library
    author='dev@stockly.us',  # Type in your name
    author_email='dev@stockly.us',  # Type in your E-Mail
    url='https://github.com/user/reponame',  # Provide either the link to your github or to your website
    download_url='https://gitlab.com/vzinjuvadia/stockly-python/-/archive/1.0.3/stockly-python-1.0.3.tar.gz',
    keywords=['BOT', 'STOCKLY', 'PYTHON'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'PyJWT',
        'websocket-client',
        'pymitter',
        'requests',
        'certifi'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    package_data={'stockly_python': ['config/*', ]}
)
