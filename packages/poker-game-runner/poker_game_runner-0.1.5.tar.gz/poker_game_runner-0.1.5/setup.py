from setuptools import setup

setup(
    name='poker_game_runner',
    version='0.1.5',    
    description='open_spiel poker tournament runner',
    url='https://github.com/bovle/poker_game_runner.git',
    author='Frederik Børsting',
    author_email='frederik@live.dk',
    license='mit',
    packages=['poker_game_runner', 'poker_game_runner/bots'],
    install_requires=[ 'open-spiel>=1.0.2', 'numpy>=1.19.0'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
    ],
)