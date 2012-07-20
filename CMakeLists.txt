#####################################################################
# Setup
#####################################################################
cmake_minimum_required (VERSION 2.6)
project ( satpredict )

# Project Version
set (satpredict_VERSION_MAJOR 0)
set (satpredict_VERSION_MINOR 0)

# Configuration file
configure_file(
	"${PROJECT_SOURCE_DIR}/config.h.in"
    "${PROJECT_BINARY_DIR}/config.h"
	)

list (APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

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
# Scripts
#####################################################################
set (SCRIPTS ${SCRIPTS}
	src/multitrack.py
	src/tleupdate
	)

#####################################################################
# Scripts
#####################################################################
set (CONFIG ${CONFIG}
	src/multitrack.conf
	)

#####################################################################
# Compile and Link
#####################################################################
add_executable ( satpredict ${SRCS} )
target_link_libraries ( satpredict ${LIBS} )

#####################################################################
# Install
#####################################################################
install ( TARGETS satpredict DESTINATION bin )
install ( PROGRAMS ${SCRIPTS} DESTINATION bin )
install ( FILES ${CONFIG} DESTINATION etc/multitrack )

# Create uninstall target
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake
    IMMEDIATE @ONLY)

add_custom_target(uninstall
    COMMAND ${CMAKE_COMMAND} -P
    ${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake)
