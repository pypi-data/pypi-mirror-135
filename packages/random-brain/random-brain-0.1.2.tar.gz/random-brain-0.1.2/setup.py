from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='random-brain',
    version='0.1.2',
    description='Python Random Brain Module',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ethan Nelson',
    author_email='ethanisaacnelson@gmail.com',
    url='https://github.com/einelson/Random-brain',
    packages=['random_brain'],
    install_requires=['numpy', 'keras'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
)

# notes
# https://stackoverflow.com/questions/52700692/a-guide-for-updating-packages-on-pypi
# python setup.py sdist
# python setup.py bdist_wheel
# twine upload dist/*