set (multitrack_SRCS ${multitrack_SRCS} main.c )

include_directories ( ${CMAKE_SOURCE_DIR}/sgp4sdp4 )
link_directories(${CMAKE_SOURCE_DIR}/sgp4sdp4)

include_directories ( ${CMAKE_SOURCE_DIR}/src )
link_directories(${CMAKE_SOURCE_DIR}/src)

#link_directories(${CMAKE_SOURCE_DIR}/lib)

set (multitrack_HDRS ${multitrack_HDRS}
	${CMAKE_SOURCE_DIR}/sgp4sdp4/sgp4sdp4.h
	)

#####################################################################
# Compile and Link
#####################################################################
add_executable ( multitrack ${multitrack_SRCS} )
target_link_libraries ( multitrack ${LIBS} ) 
set_target_properties ( multitrack PROPERTIES LINKER_LANGUAGE C )
