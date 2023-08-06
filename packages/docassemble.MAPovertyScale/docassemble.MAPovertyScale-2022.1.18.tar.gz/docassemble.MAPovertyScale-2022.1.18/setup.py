import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.MAPovertyScale',
      version='2022.01.18',
      description=('Contains most recent poverty scale in poverty.yml'),
      long_description='Contains most recent poverty scale in poverty.yml\r\n\r\nWhen you include this in your package, you will have 4 variables\r\navailable in the main Docassemble namespace:\r\n\r\n* poverty_level_update (year of update as a string)\r\n* poverty_base (base amount of poverty scale)\r\n* poverty_increment (amount for each additional household member)\r\n*  poverty_multiplier # threshold multiplier for Massachusetts Courts, 1.25\r\n\r\nTo use: \r\n\r\n```\r\n---\r\ninclude:\r\n  - docassemble.MAPovertyScale:poverty.yml\r\n---\r\nreconsider: True\r\ncode: |\r\n  additional_income_allowed = household_size * poverty_increment\r\n  household_income_limit = (poverty_base + additional_income_allowed) * poverty_multiplier\r\n\r\n  household_income_qualifies = int((household_income_limit)/12) >=  int(household_monthly_income)\r\n```',
      long_description_content_type='text/markdown',
      author='System Administrator',
      author_email='qsteenhuis@suffolk.edu',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=[],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/MAPovertyScale/', package='docassemble.MAPovertyScale'),
     )

