import setuptools
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="verify_django_serializer",
    version=os.environ.get("CI_COMMIT_TAG", "1.0-dev"),
    author="Victor Coelho",
    author_email="victorhdcoelho@gmail.com",
    description="Lib to make python packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/victorhdcoelho/verify_django_serializer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=['django', 'django-restframwork'],
    include_package_data=True,
    zip_safe=False
)
