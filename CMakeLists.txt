#####################################################################
# Setup
#####################################################################
cmake_minimum_required( VERSION 2.6 )
project( multitrack )
set (multitrack_VERSION_MAJOR 0)
set (multitrack_VERSION_MINOR 0)
set ( CMAKE_BUILD_TYPE Release )

list (APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

configure_file(
	"${PROJECT_SOURCE_DIR}/config.h.in"
    "${PROJECT_BINARY_DIR}/config.h"
	)


#####################################################################
# Compiler flags
#####################################################################
add_definitions ( -Wall -march=native )

#include_directories ( ${CMAKE_SOURCE_DIR}/lib )
#add_subdirectory ( lib )
#set( LIBS ${LIBS} lib )

include_directories ( ${PROJECT_SOURCE_DIR}/sgp4sdp4 )
include_directories ( ${PROJECT_BINARY_DIR}/sgp4sdp4 )
#add_subdirectory ( sgp4sdp4 )
#set( LIBS ${LIBS} sgp4sdp4 )

include_directories ( ${CMAKE_SOURCE_DIR}/src )
#add_subdirectory ( src )
#set (multitrack_SRCS ${multitrack_SRCS} src )


#####################################################################
# Header files
#####################################################################
set (multitrack_HDRS ${multitrack_HDRS}
	sgp4sdp4/sgp4sdp4.h
	)

#####################################################################
# Source files
#####################################################################
set (multitrack_SRCS ${multitrack_SRCS}
	src/main.c
	sgp4sdp4/sgp4sdp4.c
	sgp4sdp4/sgp_in.c
	sgp4sdp4/sgp_math.c
	sgp4sdp4/sgp_obs.c
	sgp4sdp4/sgp_time.c
	sgp4sdp4/solar.c
	)

#####################################################################
# Compile and Link
#####################################################################
add_executable ( multitrack ${multitrack_SRCS} )
#target_link_libraries ( multitrack ${LIBS} ) 
#set_target_properties ( multitrack PROPERTIES LINKER_LANGUAGE C )
