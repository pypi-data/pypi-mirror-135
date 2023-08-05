from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent


VERSION = '0.1.0'
DESCRIPTION = 'Access SFTP Server'
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="access_sftp_server",
    version=VERSION,
    author="Valentin Baier",
    author_email="valentin_baier@gmx.de",
    license_files=('LICENSE.txt',),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['paramiko', 'openpyxl', 'gspread', 'pandas'],
    keywords=['python', 'sftp', 'server', 'cibc', 'upload_files', 'download_files'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
