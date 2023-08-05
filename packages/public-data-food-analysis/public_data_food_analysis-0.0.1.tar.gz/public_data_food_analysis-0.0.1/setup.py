from distutils.core import setup
setup(
  name = 'public_data_food_analysis',         # How you named your package folder (MyLib)
  packages = ['public_data_food_analysis'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='	apache-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This project analyzes food data from a few input sources.',   # Give a short description about your library
  author = 'Qiwen Zhang',                   # Type in your name
  author_email = 'owenzhang1999@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/QiwenZz/public_data_food_analysis',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/QiwenZz/public_data_food_analysis/archive/refs/tags/0.0.1.tar.gz',    # I explain this later on
  keywords = ['circadian ryhthm', 'food loggings'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
    'pandas',
    'numpy',
    'scipy',
    'seaborn',
    'matplotlib',
    'datetime',
    'nltk',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)