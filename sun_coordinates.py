import pytz
import datetime as dt
import numpy as np
from numpy import sin,cos,arctan,arccos


def sun_coordinates(date_time_local, LA, LO):
	
	date_time_utc = date_time_local.astimezone(pytz.utc) 
	t_input = date_time_utc.replace(tzinfo=None) 
	
	PI = np.pi
	rEO = 149600000 
	rE = (6378 + 6357)/2 
	phiE = 23.4*PI/180 
	tday = 86164.0905 
	tyear = 366.25*tday 
	t0 = dt.datetime(2020, 3, 20, 12, 0, 0) 
	tdiff = t_input - t0 
	t = tdiff.total_seconds() 

	TLL = PI/180*LO + 2*PI/tday*t + PI 
	PLL = PI/2 - 2*PI/360*LA 
	TEO = 2*PI/tyear*t 
	
	Perp = rEO*(sin(phiE)*sin(TEO)*cos(PLL) - cos(phiE)*sin(TEO)*sin(TLL)*sin(PLL) - cos(TEO)*cos(TLL)*sin(PLL)) - rE    
	North = rEO*(sin(phiE)*sin(TEO)*sin(PLL) + cos(phiE)*sin(TEO)*sin(TLL)*cos(PLL) + cos(TEO)*cos(TLL)*cos(PLL))
	East = rEO*(cos(TEO)*sin(TLL) - cos(phiE)*sin(TEO)*cos(TLL))

	
	Theta_raw = arctan(North/East)   
	Theta_deg = Theta_raw*180/PI
	
	if North > 0 and East > 0:
		Theta_from_North = 90 - Theta_deg
	
	if North > 0 and East < 0:
		Theta_deg = Theta_deg + 180
		Theta_from_North = 450 - Theta_deg
	
	if North < 0 and East < 0:
		Theta_deg = Theta_deg + 180
		Theta_from_North = 450 - Theta_deg

	if North < 0 and East > 0:
		Theta_deg = Theta_deg + 360
		Theta_from_North = 450 - Theta_deg

	Theta = Theta_deg*PI/180
	Theta_from_North = int(Theta_from_North)

	Phi = arccos(Perp/np.sqrt(Perp*Perp + North*North + East*East))  
	Phi_from_Horizon = int(90 - Phi*360/(2*PI))

	return Theta, Phi, Theta_from_North, Phi_from_Horizon
