#####################################################################
# Setup
#####################################################################
cmake_minimum_required (VERSION 2.6)
project ( multitrack )

# Project Version
set (multitrack_VERSION_MAJOR 0)
set (multitrack_VERSION_MINOR 0)

# Configuration file
configure_file(
	"${PROJECT_SOURCE_DIR}/config.h.in"
    "${PROJECT_BINARY_DIR}/config.h"
	)


#####################################################################
# Compiler flags
#####################################################################
add_definitions ( -Wall )


#####################################################################
# Include Path
#####################################################################
include_directories ( "${PROJECT_BINARY_DIR}" )
include_directories ( "${PROJECT_BINARY_DIR}/src" )
include_directories ( "${PROJECT_SOURCE_DIR}/src" )

#####################################################################
# SGP4 SDP4 Library
#####################################################################
include_directories ( "${PROJECT_BINARY_DIR}/sgp4sdp4" )
include_directories ( "${PROJECT_SOURCE_DIR}/sgp4sdp4" )
add_subdirectory ( sgp4sdp4 )
set ( LIBS ${LIBS} sgp4sdp4 )

#####################################################################
# Math Library
#####################################################################
find_library( M_LIB m )
set ( LIBS ${LIBS} ${M_LIB} )

#####################################################################
# Sources
#####################################################################
set (SRCS ${SRCS}
	src/main.c
	)

set (HDRS ${HDRS}
	sgp4sdp4/sgp4sdp4.h
	)

#####################################################################
# Compile and Link
#####################################################################
add_executable ( multitrack ${SRCS} )
target_link_libraries ( multitrack ${LIBS} )