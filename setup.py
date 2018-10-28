#!/usr/bin/env python

from setuptools.command.build_ext import build_ext
from distutils.core import setup, Extension

USE_SURF = True


# Avoid a gcc warning below: https://stackoverflow.com/a/49041815
# cc1plus: warning: command line option ‘-Wstrict-prototypes’ is valid
# for C/ObjC but not for C++
class BuildExt(build_ext):
    def build_extensions(self):
        self.compiler.compiler_so.remove('-Wstrict-prototypes')
        super(BuildExt, self).build_extensions()


extra_compile_args = ['-O3']
macros = [('USE_PYTHON', None)]
libs = ['opencv_videoio', 'opencv_calib3d', 'opencv_features2d',
        'opencv_highgui', 'opencv_imgproc', 'opencv_imgcodecs', 'opencv_core']
#        'avformat', 'avdevice', 'avutil', 'avcodec', 'swscale']
if USE_SURF:
    macros.append(('USE_SURF', None))
    libs.append('opencv_xfeatures2d')

densetrack = Extension('densetrack', ['src/DenseTrackStab.cpp'],
                       extra_compile_args=extra_compile_args,
                       libraries=libs, define_macros=macros)

setup(name='densetrack',
      version='1.0',
      cmdclass={'build_ext': BuildExt},
      ext_modules=[densetrack],
      url='https://github.com/FXPAL/densetrack',
      author='Andreas Girgensohn',
      author_email='andreasg@fxpal.com'
     )
