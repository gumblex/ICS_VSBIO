from distutils.command.build import build
from setuptools.command.install import install
from distutils.core import setup, Extension
import distutils 
import platform

version = '0.0.4.2'

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

class CustomBuild(build):
	def run(self):
		self.run_command('build_ext')
		build.run(self)


class CustomInstall(install):
	def run(self):
		self.run_command('build_ext')
		self.do_egg_install()


if platform.system() == 'Windows':
	define_macros = [('_WIN32', None), ('VSBIODLL_EXPORTS', None)]
elif platform.system() == 'Linux': 
	define_macros = [('LINUXSO', None)]
define_macros += [('PYD', None)]

if which('swig') or which('swig.exe') :
	sources=['ICS_VSBIO/StandardLibrary/src/OFile.cpp',
		'ICS_VSBIO/VSBIO/src/VSBIO.cpp',
		'ICS_VSBIO/VSBIO/src/MessageTimeDecoderVSB.cpp',
		'ICS_VSBIO/VSBIODLL.cpp',
		'ICS_VSBIO/VSBIOInterface.i',
		'ICS_VSBIO/VSBIOFlags.i']	
else:
	sources=['ICS_VSBIO/StandardLibrary/src/OFile.cpp',
		'ICS_VSBIO/VSBIO/src/VSBIO.cpp',
		'ICS_VSBIO/VSBIO/src/MessageTimeDecoderVSB.cpp',
		'ICS_VSBIO/VSBIODLL.cpp',
		'ICS_VSBIO/VSBIOInterface_wrap.cpp',
		'ICS_VSBIO/VSBIOFlags_wrap.cpp']	
module1 = Extension('_VSBIOInterface',
				sources=sources,
				swig_opts=['-c++', '-py3'],
				include_dirs=['ICS_VSBIO/VSBIO/include', 'ICS_VSBIO/StandardLibrary/include', 'ICS_VSBIO/Hardware/include', 'ICS_VSBIO/Core/include'],
				define_macros= define_macros)

module2 = Extension('_VSBIOFlags',
				sources=['ICS_VSBIO/VSBIOFlags.i'],
				swig_opts=['-c++', '-py3'],
				include_dirs=['ICS_VSBIO/VSBIO/include', 'ICS_VSBIO/StandardLibrary/include', 'ICS_VSBIO/Hardware/include', 'ICS_VSBIO/Core/include'],
				define_macros= define_macros)

setup(  name            = 'ICS_VSBIO',
		version         = version,
		author          = 'Zaid Nackasha',
		author_email    = 'znackasha@intrepidcs.com',
		description     = 'Python package to help users read and write Intrepid\'s vsb files',
		url             = 'https://github.com/intrepidcs/ICS_VSBIO',
		download_url 	= 'https://github.com/intrepidcs/ICS_VSBIO/archive/' + version + '.tar.gz',
		platforms       = ['x86_64'],
		packages        = ['ICS_VSBIO'],
		package_dir     = {'ICS_VSBIO': 'ICS_VSBIO'},
		cmdclass		= {'build': CustomBuild, 'install': CustomInstall},		
		ext_modules     = [module1, module2],
		py_modules		= ['module1', 'module2'] )
