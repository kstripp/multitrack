#add_library( sgp4sdp4 sgp4sdp4.c)
#add_library( sgp_in sgp_in.c)
#add_library( sgp_math sgp_math.c)
#add_library( sgp_obs sgp_obs.c)
#add_library( sgp_time sgp_time.c)
#add_library( solar solar.c)

#set( LIBS ${LIBS}
#	sgp4sdp4
#	sgp_in
#	sgp_math
#	sgp_obs
#	sgp_time
#	solar
#	)

set (multitrack_SRCS ${multitrack_SRCS}
	sgp4sdp4.c
	sgp_in.c
	sgp_math.c
	sgp_obs.c
	sgp_time.c
	solar.c
	)
