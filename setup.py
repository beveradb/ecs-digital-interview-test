from setuptools import setup

setup(
    name='run_migrations',
    version='0.2',
    py_modules=['run_migrations'],
    install_requires=[
        'Click',
        'click_log',
        'mysql-connector-python',
        'MySQL-python;python_version<"3"'
    ],
    entry_points='''
        [console_scripts]
        run_migrations=run_migrations:cli
    ''',
)
