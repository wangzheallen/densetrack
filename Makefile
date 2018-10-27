# set the binaries that have to be built
TARGETS := DenseTrackStab Video

# set the build configuration set 
BUILD := release
#BUILD := debug

# set bin and build dirs
BUILDDIR := .build_$(BUILD)
BINDIR := $(BUILD)

# use SURF
USE_SURF = true

# libraries 
LDLIBS = $(addprefix -l, $(LIBS) $(LIBS_$(notdir $*)))
LIBS := \
	opencv_core opencv_highgui opencv_videoio opencv_imgproc opencv_calib3d opencv_features2d \
	avformat avdevice avutil avcodec swscale
ifdef USE_SURF
LIBS += opencv_xfeatures2d
endif

# set some flags and compiler/linker specific commands
CXXFLAGS = -pipe -D __STDC_CONSTANT_MACROS -D STD=std -Wall $(CXXFLAGS_$(BUILD)) -I. -I/opt/include
ifdef USE_SURF
CXXFLAGS += -DUSE_SURF
endif

CXXFLAGS_debug := -ggdb
CXXFLAGS_release := -O3 -DNDEBUG -ggdb
LDFLAGS = -L/opt/lib -pipe -Wall $(LDFLAGS_$(BUILD))
LDFLAGS_debug := -ggdb
LDFLAGS_release := -O3 -ggdb

include make/generic.mk
