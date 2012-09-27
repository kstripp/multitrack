/***************************************************************************
 * This file is part of Multitrack.                                        *
 *                                                                         *
 * Copyright (C) 2012 K. Scott Tripp                                       *
 *                                                                         *
 * AUTHORS:	K. Scott Tripp, <kscott.tripp@gmail.com>                       *
 * 			Neoklis Kyriazis, 5B4AZ                                        *
 *                                                                         *
 * Multitrack is free software: you can redistribute it and/or modify      *
 * it under the terms of the GNU General Public License as published by    *
 * the Free Software Foundation, either version 3 of the License, or       *
 * (at your option) any later version.                                     *
 *                                                                         *
 * Multitrack is distributed in the hope that it will be useful,           *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of          *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           *
 * GNU General Public License for more details.                            *
 *                                                                         *
 * You should have received a copy of the GNU General Public License       *
 * along with Multitrack.  If not, see <http://www.gnu.org/licenses/>.     *
 ***************************************************************************/

#include <getopt.h>
#include "sgp4sdp4.h"

/* Main program */
int main( int argc, char **argv )
{	
	FILE * outFile = stdout; //Default output to terminal
	int c = 0;
	int unix_aos = 0; 
	int unix_los = 0;
	int t_index = 0;
	int header_flag = 1;
	static int verbose_flag;
	
	/* Default TLE source file */
	//TODO: remove dependency on having a single TLE in the file
	//TODO: make the file an option
	char tle_file[255] = "./rax.txt";

/********************************************************************
 * Command line arguments                                           *
 * -a, --aos-time,	UNIX time of AOS                                *
 * -l, --los-time,	UNIX time of LOS                                *
 * -s, --sat-id, 	NORAD Sat ID                                    *
 * -o, --outfile, 	output file name                                *
 * -t, --tle-file, 	TLE file name  	                                *
 * -n, --no-header,	Do not print header								*
 ********************************************************************/

	while(1)
	{
		static struct option long_options[] =
		{
			/* Flag options */
			{"verbose",		no_argument,	&verbose_flag, 1},
			{"brief",		no_argument,	&verbose_flag, 0},
			{"no-header",	no_argument,	0, 'n'},
			/* Non-flag options */
			{"aos-time",	required_argument,	0, 'a'},
			{"los-time",	required_argument,	0, 'l'},
//			{"sat-id",		required_argument,	0, 's'},
			{"outfile",		no_argument,	0, 'o'},
			{"tle-file",	no_argument,	0, 't'},
			{0,0,0,0}
		};

		int opt_index = 0;		//should this really be inside the loop?

		c = getopt_long(argc, argv, "na:l:s:o:t:", long_options, &opt_index);

		/* Detect end of options */
		if( c== -1)
			break;

		switch (c)
		{
			case 0:
				if (long_options[opt_index].flag != 0)
					break;
				printf("option %s", long_options[opt_index].name);
				if(optarg)
					printf(" with arg %s", optarg);
				printf("\n");
				break;
			
			case 'n':
				header_flag = 0;
				break;

			case 'a':
				unix_aos = atoi(optarg);
				break;

			case 'l':
				unix_los = atoi(optarg);
				break;

			case 'o':
				outFile = fopen(optarg, "w");
				break;
			
			case 't':
				sprintf(tle_file, "%s", optarg);
				break;

			case '?':
				/* supposedly an error message has been printed */
				break;

			default:
				abort ();
		}
	}

	/* Observer's geodetic co-ordinates.      */
	/* Lat North, Lon East in rads, Alt in km */
	//TODO: read in qth file for this info
	geodetic_t obs_geodetic = {0.7368, -1.4615, 0.251, 0.0};

	/* Two-line Orbital Elements for the satellite */
	tle_t tle ;

	/* Zero vector for initializations */
	vector_t zero_vector = {0,0,0,0};

	/* Satellite position and velocity vectors */
	vector_t vel = zero_vector;
	vector_t pos = zero_vector;
	/* Satellite Az, El, Range, Range rate */
	vector_t obs_set;

	/* Solar ECI position vector  */
	vector_t solar_vector = zero_vector;
	/* Solar observed azi and ele vector  */
	vector_t solar_set;

	/* Calendar date and time (UTC) */
	struct tm utc;

	/* Satellite's predicted geodetic position */
	geodetic_t sat_geodetic;

	double
		tsince,            /* Time since epoch (in minutes) */
		jul_epoch,         /* Julian date of epoch          */
		jul_utc,           /* Julian UTC date               */
		eclipse_depth = 0, /* Depth of satellite eclipse    */
		/* Satellite's observed position, range, range rate */
		sat_azi, sat_ele, sat_range, sat_range_rate,
		/* Satellites geodetic position and velocity */
		sat_lat, sat_lon, sat_alt, sat_vel,
		/* Solar azimuth and elevation */
		sun_azi, sun_ele;

	/* Used for storing function return codes */
	int flg;

	char
		ephem[5],       /* Ephemeris in use string  */
		sat_status[12]; /* Satellite eclipse status */


	/* Input one (first!) TLE set from file */
	flg = Input_Tle_Set(tle_file, &tle);

	//printf("%s\n", tle_file);

	/* Abort if file open fails */
	if( flg == -1 )
	{
		printf(" TLE file open failed - Exiting!\n");
		exit(-1);
	}

	/* Print satellite name and TLE read status */
	if(verbose_flag)
	{
		printf(" %s: ", tle.sat_name);
	}
	
	if( flg == -2 )
	{
		printf("TLE set bad - Exiting!\n");
		exit(-2);
	}
	else if(verbose_flag)
	{
		printf("TLE set good - Happy Tracking!\n");
	}

	/* Printout of tle set data for tests if needed */
	/*  printf("\n %s %s %i  %i  %i\n"
		" %14f %10f %8f %8f\n"
		" %8f %8f %9f %8f %8f %12f\n",
		tle.sat_name, tle.idesg, tle.catnr, tle.elset, tle.revnum,
		tle.epoch, tle.xndt2o, tle.xndd6o, tle.bstar,
		tle.xincl, tle.xnodeo, tle.eo, tle.omegao, tle.xmo, tle.xno);
	 */

	/** !Clear all flags! **/
	/* Before calling a different ephemeris  */
	/* or changing the TLE set, flow control */
	/* flags must be cleared in main().      */
	ClearFlag(ALL_FLAGS);

	/** Select ephemeris type **/
	/* Will set or clear the DEEP_SPACE_EPHEM_FLAG       */
	/* depending on the TLE parameters of the satellite. */
	/* It will also pre-process tle members for the      */
	/* ephemeris functions SGP4 or SDP4 so this function */
	/* must be called each time a new tle set is used    */
	select_ephemeris(&tle);
	
	/* Check for input AOS and LOS */
	if (unix_aos != 0)
	{
		t_index = unix_aos;
	}
	
	/* Print file header */
	if (header_flag)
	{
		fprintf(outFile, "Timestamp azimuth elevation range rate\n");
	}

	do  /* Loop */
	{
		/* Get UTC calendar and convert to Julian */
		
		if(unix_aos == 0)
		{
			UTC_Calendar_Now(&utc);
			
			/* Get UNIX time to display */
			t_index = time(0);
		}
		else
		{
			UTC_Calendar(&utc, t_index);
		}
		
		jul_utc = Julian_Date(&utc);

		/* Convert satellite's epoch time to Julian  */
		/* and calculate time since epoch in minutes */
		jul_epoch = Julian_Date_of_Epoch(tle.epoch);
		tsince = (jul_utc - jul_epoch) * xmnpda;

		/* Copy the ephemeris type in use to ephem string */
		if( isFlagSet(DEEP_SPACE_EPHEM_FLAG) )
			strcpy(ephem,"SDP4");
		else
			strcpy(ephem,"SGP4");

		/* Call NORAD routines according to deep-space flag */
		if( isFlagSet(DEEP_SPACE_EPHEM_FLAG) )
			SDP4(tsince, &tle, &pos, &vel);
		else
			SGP4(tsince, &tle, &pos, &vel);

		/* Scale position and velocity vectors to km and km/sec */
		Convert_Sat_State( &pos, &vel );

		/* Calculate velocity of satellite */
		Magnitude( &vel );
		sat_vel = vel.w;

		/** All angles in rads. Distance in km. Velocity in km/s **/
		/* Calculate satellite Azi, Ele, Range and Range-rate */
		Calculate_Obs(jul_utc, &pos, &vel, &obs_geodetic, &obs_set);

		/* Calculate satellite Lat North, Lon East and Alt. */
		Calculate_LatLonAlt(jul_utc, &pos, &sat_geodetic);

		/* Calculate solar position and satellite eclipse depth */
		/* Also set or clear the satellite eclipsed flag accordingly */
		Calculate_Solar_Position(jul_utc, &solar_vector);
		Calculate_Obs(jul_utc,&solar_vector,&zero_vector,&obs_geodetic,&solar_set);

		if( Sat_Eclipsed(&pos, &solar_vector, &eclipse_depth) )
			SetFlag( SAT_ECLIPSED_FLAG );
		else
			ClearFlag( SAT_ECLIPSED_FLAG );

		/* Copy a satellite eclipse status string in sat_status */
		if( isFlagSet( SAT_ECLIPSED_FLAG ) )
			strcpy( sat_status, "Eclipsed" );
		else
			strcpy( sat_status, "In Sunlight" );

		/* Convert and print satellite and solar data */
		sat_azi = Degrees(obs_set.x);
		sat_ele = Degrees(obs_set.y);
		sat_range = obs_set.z;
		sat_range_rate = obs_set.w;
		sat_lat = Degrees(sat_geodetic.lat);
		sat_lon = Degrees(sat_geodetic.lon);
		sat_alt = sat_geodetic.alt;

		sun_azi = Degrees(solar_set.x);
		sun_ele = Degrees(solar_set.y);

		/*
		printf("\n Date: %02d/%02d/%04d UTC: %02d:%02d:%02d  Ephemeris: %s"
				"\n Azi=%6.1f Ele=%6.1f Range=%8.1f Range Rate=%6.2f"
				"\n Lat=%6.1f Lon=%6.1f  Alt=%8.1f  Vel=%8.3f"
				"\n Stellite Status: %s - Depth: %2.3f"
				"\n Sun Azi=%6.1f Sun Ele=%6.1f\n",
				utc.tm_mday, utc.tm_mon, utc.tm_year,
				utc.tm_hour, utc.tm_min, utc.tm_sec, ephem,
				sat_azi, sat_ele, sat_range, sat_range_rate,
				sat_lat, sat_lon, sat_alt, sat_vel,
				sat_status, eclipse_depth,
				sun_azi, sun_ele);
*/
//		sleep(1);

		fprintf(outFile, "%i %f %f %f\n", 
				t_index, sat_azi, sat_ele, sat_range_rate);
		

		/* Increment the time between AOS and LOS. */
		t_index++;

	}  /* End of do */
	while ( t_index < unix_los );
	fclose(outFile);
	
	return(0);
} /* End of main() */

/*------------------------------------------------------------------*/

