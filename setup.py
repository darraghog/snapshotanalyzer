from setuptools import setup

setup(name='Snapshotanalyzer 3000',
    version='0.1',
    author="Darragh OG via ACG",
    author_email='darragh.ogrady@gmail.com',
    description='Snapshotanalyzer 3000 is a tool to manage EBS snapshots of AWS EC2 instances',
    license="GPLv3+",
    packages=['shotty'],
    url='https://github.com/darraghog/snapshotanalyzer',
    install_requires=[
        'click',
        'boto3'
        ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
        '''
)