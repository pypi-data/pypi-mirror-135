import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name="FeatureCloud",
                 version="0.0.11",
                 author="FeatureCloud",
                 author_email="mohammad.bakhtiari@uni-hamburg.de",
                 description="Secure Federated Learning Platform",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/FeatureCloud/app-template",
                 project_urls={
                     "Bug Tracker": "https://github.com/FeatureCloud/app-template/issues",
                 },
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "Operating System :: OS Independent",
                 ],
                 packages=['FeatureCloud', 'FeatureCloud.apps', 'FeatureCloud.engine', 'FeatureCloud.api',
                           'FeatureCloud.cli',
                           'FeatureCloud.cli.api', 'FeatureCloud.cli.api.backend', 'FeatureCloud.cli.tests'],
                 python_requires=">=3.7",
                 entry_points={'console_scripts': ['FeatureCloud = FeatureCloud.__main__:fc_command',
                                                   'featurecloud = FeatureCloud.__main__:fc_command',
                                                   'fc = FeatureCloud.__main__:fc_command',

                                                   ]
                               },
                 install_requires=['bottle', 'jsonpickle', 'joblib', 'numpy', 'pydot', 'pyyaml', 'flake8~=3.9.2',
                                'pycodestyle~=2.7.0', 'Click~=8.0.1', 'requests', 'urllib3~=1.26.6', 'pandas',
                                   'pyinstaller']

                 )
