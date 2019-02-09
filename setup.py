from setuptools import setup

setup(
    name='run_migrations',
    version='0.1',
    py_modules=['run_migrations'],
    install_requires=[
        'Click',
        'click_log',
        'mysql-connector-python',
        'MySQL-python'
    ],
    entry_points='''
        [console_scripts]
        run_migrations=run_migrations:cli
    ''',
)
