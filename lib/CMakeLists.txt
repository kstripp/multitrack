include_directories ( ${LIBS}/sgp4sdp4 )
add_subdirectory ( sgp4sdp4 )
set ( LIBS ${LIBS} sgp4sdp4 )
