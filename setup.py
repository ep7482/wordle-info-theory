import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='wordle_clone', 
                packages=['wordle_clone'], 
                install_requires=install_requires)