import setuptools

def get_description():
    with open('README.md', 'r') as file:
        return file.read()

def main():
    setuptools.setup(
        name = 'pacai',
        version = '1.1.0',
        url = 'https://github.com/linqs/pacman',

        keywords = [
            'AI',
            'Artificial Intelligence',
            'Education',
            'Teaching',
        ],

        author = 'linqs',
        author_email = 'linqs.edu@gmail.com',

        description = 'A modified version of the Pacman educational project from the Berkley AI Lab.',
        long_description = get_description(),
        long_description_content_type = 'text/markdown',

        packages = setuptools.find_packages(),

        install_requires = [
            'imageio==2.5.0',
        ],

        python_requires = '>=3.5',

        classifiers = [
            'Intended Audience :: Science/Research',
            'Intended Audience :: Education',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Topic :: Education',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
        ],
    )

if (__name__ == '__main__'):
    main()
