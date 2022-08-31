import os
import platform
import sys
import sysconfig
from glob import glob

try:
    from ConfigParser import ConfigParser  # Python 2
except ImportError:
    from configparser import ConfigParser

from setuptools import setup, Extension, find_packages


def RemovePrefixes(optlist, bad_prefixes):
    for bad_prefix in bad_prefixes:
        for i, flag in enumerate(optlist):
            if flag.startswith(bad_prefix):
                optlist.pop(i)
                break
    return optlist


def ReadConfig(section, value, default):
    try:
        config = ConfigParser()
        config.read('setup.cfg')
        return config.get(section, value)
    except:  # pylint: disable=bare-except
        return default


lib_dirs = ReadConfig('build_ext',
                      'library_dirs',
                      sysconfig.get_config_var('LIBDIR')).split(':')
extra_compile_args = ReadConfig('cc_options', 'extra_compile_args', '').split()
extra_link_args = ReadConfig('cc_options', 'extra_link_args', '').split()

static_libs = []
deps = ['libgflags.a', 'libglog.a']
for dep in deps:
    for lib_dir in lib_dirs:
        path = os.path.join(lib_dir, dep)
        if os.path.isfile(path):
            static_libs.append(path)
print(static_libs, deps)
assert len(static_libs) == len(deps), (static_libs, deps, lib_dirs)

cvars = sysconfig.get_config_vars()
cvars['OPT'] = str.join(' ', RemovePrefixes(
    cvars.get('OPT').split(),
    ['-g', '-O', '-Wstrict-prototypes']))

ext_modules = []

if sys.platform == "darwin":
    extra_compile_args.insert(0, '-stdlib=libc++')

if sys.platform in ('darwin', 'linux2', 'linux'):
    extra_compile_args = [
                             '-std=c++0x',
                             '-g0',
                             '-O3',
                             '-Wno-deprecated-register'] + extra_compile_args
    extra_link_args = static_libs + extra_link_args
    if ('CPython' == platform.python_implementation()) and \
            ((sys.version_info[0] == 2 and sys.version_info > (2, 7, 0)) or
             (sys.version_info[0] == 3 and sys.version_info >= (3, 5, 0))):
        ext_modules.append(Extension(
            'tracepointdebug.cdbg_native',
            sources=glob('tracepointdebug/external/googleclouddebugger/*.cc'),
            extra_compile_args=extra_compile_args, extra_link_args=extra_link_args))

install_requires = ['six >= 1.11',
                    'websocket-client >= 0.56.0',
                    'pystache >= 0.6.0'
                    ]

if sys.version_info[0] == 2:
    install_requires.append('antlr4-python2-runtime==4.9.2')
    install_requires.append('futures') # futures lib has became the standard lib after python3. İnstall only for python2.
elif sys.version_info[0] == 3:
    install_requires.append('antlr4-python3-runtime==4.9.2')

setup(
    name='sidekick-agent-python',
    version='0.0.7',
    packages=find_packages(exclude=('tests', 'tests.*',)),
    include_package_data=True,
    author='Thundra',
    author_email='python@thundra.io',
    url='https://runsidekick.com',
    description='Sidekick Python Debugger',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    zip_safe=False,
    setup_requires=['wheel'],
    install_requires=install_requires,
    ext_modules=ext_modules
)
