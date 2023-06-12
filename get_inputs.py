from tzwhere import tzwhere
from geopy import geocoders
import pytz
import datetime as dt



def get_inputs(args):
	if args.city == None:
		LA = 48.0196 
		LO = 66.9237 
		city = 'Astana, KZ'
		print(f'Using default location: {city}, Lat: {LA}, Lon: {LO}')
	else:
		city = args.city
		geolocator = geocoders.Nominatim(user_agent='Sun')  
		location = geolocator.geocode(city)
		if location == None:
			print('Error with city input!, Kindly check.')
			exit()
		LA = location.latitude
		LO = location.longitude
		print(f'Using city input {location}')
		print(f'Lat: {LA}', 'Lon: {LO}')

	tz = tzwhere.tzwhere(forceTZ=True)  #initialize timezone finder 
	timezone = pytz.timezone(tz.tzNameAt(LA, LO, forceTZ=True))

	if args.date_time == None:  #if no time provided, get the current in the timezone of interest
		date_time_local = dt.datetime.now(timezone)    
		print(f'Using default time (current time at location) {date_time_local}')
	else:
		try: 
			date_time = dt.datetime.strptime(args.date_time, '%Y-%m-%d %H:%M:%S')
			date_time_local = timezone.localize(date_time)
			print(f'Using time input {date_time_local}')
		except:
			print('Error with time input, ensure format is %Y-%m-%d %H:%M:%S')
			exit()

	
	print(f'Using timezone {timezone}')

	return date_time_local, LA, LO, city