from setuptools import setup
from setuptools import find_packages

# Get version
with open('VERSION', 'r') as version_file:
    version = version_file.read().strip()
    
# Get requirements
with open('requirements.txt', 'r') as requirements_file:
    requirements = [requirement for requirement in requirements_file.read().split('\n')
                    if len(requirement)]

docs_extras = [
    'Sphinx>=1.0',  # autodoc_member_order = 'bysource', autodoc_default_flags
    'sphinx_rtd_theme',
]

# Get readme contents
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='certbot-dns-safedns',
    version=version,
    description='SafeDNS Authenticator plugin for Certbot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ukfast/certbot-dns-safedns',
    author='UKFast R&D Team',
    author_email='support@ukfast.co.uk',
    license='MIT',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    data_files=[('', ['VERSION', 'requirements.txt', 'setup.py'])],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'docs': docs_extras,
    },
    entry_points={
        "certbot.plugins": [
            "dns_safedns = certbot_dns_safedns.dns_safedns:Authenticator"
        ],
    },
    test_suite='certbot_dns_safedns',
)
