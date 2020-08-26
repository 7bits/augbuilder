import os
import subprocess


def run():
    package_path = os.path.dirname(__file__)
    path = os.path.join(package_path, 'aug_run.py')
    res = subprocess.run(
        ['streamlit', 'run', path],
    )
    res.check_returncode()
