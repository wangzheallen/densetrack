#!/usr/bin/env python

import os
from setuptools.command.build_ext import build_ext
from distutils.core import setup, Extension

USE_SURF = True


class CustomBuildExt(build_ext):
    def build_extensions(self):
        # Avoid a gcc warning: https://stackoverflow.com/a/49041815
        # cc1plus: warning: command line option ‘-Wstrict-prototypes’ is valid
        # for C/ObjC but not for C++
        self.compiler.compiler_so.remove('-Wstrict-prototypes')
        super(CustomBuildExt, self).build_extensions()
    def run(self):
        # import numpy after install_requires
        import numpy
        self.include_dirs.append(numpy.get_include())
        build_ext.run(self)


try:
    include_dirs = [os.path.join(os.environ['CONDA_PREFIX'], 'include')]
    library_dirs = [os.path.join(os.environ['CONDA_PREFIX'], 'lib')]
except KeyError:
    include_dirs = []
    library_dirs = []

extra_compile_args = ['-O3']
macros = [('USE_PYTHON', None)]
libs = ['opencv_videoio', 'opencv_calib3d', 'opencv_features2d',
        'opencv_highgui', 'opencv_imgproc', 'opencv_imgcodecs', 'opencv_core']
if USE_SURF:
    macros.append(('USE_SURF', None))
    libs.append('opencv_xfeatures2d')

densetrack = Extension('densetrack', ['src/DenseTrackStab.cpp'],
                       include_dirs=include_dirs,
                       library_dirs=library_dirs,
                       extra_compile_args=extra_compile_args,
                       libraries=libs, define_macros=macros)

setup(name='densetrack',
      version='1.0',
      cmdclass={'build_ext': CustomBuildExt},
      install_requires=['numpy'],
      ext_modules=[densetrack],
      url='https://github.com/FXPAL/densetrack',
      author='Andreas Girgensohn',
      author_email='andreasg@fxpal.com'
     )
