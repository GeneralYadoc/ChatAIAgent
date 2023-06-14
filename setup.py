from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="chatai-agent",
    version="1.1.1",
    license="MIT",
    description="Send messages to ChatGPT and get answers conveniently.",
    author="General Yadoc",
    author_email="133023047+GeneralYadoc@users.noreply.github.com",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',       
        'License :: OSI Approved :: MIT License',
    ],
    url="https://github.com/GeneralYadoc/ChatAIAgent",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"]
)
