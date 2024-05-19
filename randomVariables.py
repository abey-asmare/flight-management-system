import random
import pytz
from datetime import datetime, timedelta
import flet as ft

# Set a timezone for the departure time
timezone = pytz.timezone('Africa/Addis_Ababa')


class Randomly:
    _last_departure_time = None
    _all_id_generated = []
    _alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # List of reasons for flight cancellations
    _cancellation_reasons = [
        "Weather Conditions",
        "Mechanical Issues",
        "Air Traffic Control Issues",
        "Security Concerns",
        "Operational Issues",
        "Airport Closure",
        "Travel Restrictions",
        "Natural Disasters",
        "Fuel Shortages",
        "Pilot or Crew Availability",
        "Personal Mistake",
        "Other",
    ]
    # List of international airplane types
    _airplanes = {
        'international':
            [
                'Boeing 787 Dreamliner',
                'Boeing 767',
                'Airbus A330',
                'Boeing 747',
                'Boeing 777'
            ],

        # List of local airplane types
        'local':
            [
                'Cessna 208 Caravan',
                'Britten-Norman BN-2 Islander',
                'CASA C-212 Aviocar',
                'Beechcraft 1900',
                'd.Havilland Canada DHC-6 Twin O'
            ]
    }
    # Dictionary of Ethiopian airport codes
    _airport_codes = {
        'local':
            [
                {'ADD': 'Addis Ababa, Ethiopia'},
                {'GDQ': 'Gondar, Ethiopia'},
                {'AMH': 'Arba Minch, Ethiopia'},
                {'BJR': 'Bahir Dar, Ethiopia'},
                {'DIR': 'Dire Dawa, Ethiopia'},
                {'LLI': 'Lalibela, Ethiopia'},
                {'MQX': 'Makale, Ethiopia'},
                {'JIM': 'Jimma, Ethiopia'},
                {'JIJ': 'Jijiga, Ethiopia'},
                {'AXU': 'Axum, Ethiopia'}
            ],

        # Dictionary of international airport codes
        'international':
            [
                {'LAX': 'Los Angeles, USA'},
                {'JFK': 'New York, USA'},
                {'HND': 'Tokyo, Japan'},
                {'CDG': 'Paris, France'},
                {'DXB': 'Dubai, UAE'},
                {'SIN': 'Singapore'},
                {'AMS': 'Amsterdam, Netherlands'},
                {'FRA': 'Frankfurt, Germany'},
                {'ICN': 'Incheon, South Korea'},
                {'SFO': 'San Francisco, USA'}
            ]
    }

    def _generate_id(self):
        rand_a = random.choices(self._alphabets, k=2)
        rand_num = rand_a[0] + rand_a[1] + str(random.randint(1000, 9999))

        if rand_num in self._all_id_generated:
            return self._generate_id()
        self._all_id_generated.append(rand_num)
        return str(rand_num)

    def _flight_type(self):
        return random.choice(["local", "international"])

    def _generate_destination(self):
        destination: dict = random.choice(self._airport_codes[self.flight_type])
        if destination is self._airport_codes['local'][0]:
            return self._generate_destination()
        return list(destination.keys())[0] #dict

    @classmethod
    def get_destination(cls, airport_code:str):
        for type_, value in cls._airport_codes.items():
            for airport_dict in value:
                for a_code, country in airport_dict.items():
                    if a_code == airport_code:
                        return a_code
        return {'404': 'Not Found'}

    @classmethod
    def get_cancellation_reasons(cls):
        return cls._cancellation_reasons

    def _generate_airpane_type(self):
        return random.choice(self._airplanes[self.flight_type])

    def _generate_departure_time(self):
        if not self._last_departure_time:
            Randomly._last_departure_time = datetime.now().replace(minute=0, second=0, microsecond=0)
        else:
            Randomly._last_departure_time += timedelta(seconds=10)

        return self._last_departure_time


    def __init__(self, **kwargs):
        self._flight_id = self._generate_id()
        self._departure_time = kwargs.get('departure_time') if kwargs.get('departure_time') is not None else  self._generate_departure_time()
        self._flight_type = kwargs.get('flight_type') if kwargs.get('flight_type') is not None else  self._flight_type()
        self._origin = kwargs.get('origin') if kwargs.get('origin') is not None else list(self._airport_codes['local'][0].keys())[0]
        self._airplane_type = kwargs.get('airplane_type') if kwargs.get('airplane_type') is not None else self._generate_airpane_type()
        self._destination = kwargs.get('destination') if kwargs.get('destination') is not None else self._generate_destination()

    @classmethod
    def get_air_planes(cls, option=True):
        all_planes = cls._airplanes['international'] + cls._airplanes['local']
        if option:
            return [ft.dropdown.Option(plane) for plane in all_planes]

        return all_planes

    @classmethod
    def get_airport_codes(cls, option=True, is_local=False):
        airport_list = []
        if is_local:
            airports = cls._airport_codes['local']
        else:
            airports = cls._airport_codes['local'] + cls._airport_codes['international']
        for airport in airports:
            for code, name in airport.items():
                # Extract the airport code and name
                airport_list.append(f"{code}, {name}")
        if option:
            return [ft.dropdown.Option(airport) for airport in airport_list]
        return airport_list

    # todo: have a getter and setter for each members
    @property
    def flight_type(self):
        return self._flight_type
    @flight_type.setter
    def flight_type(self, value):
        self._flight_type = value

    @property
    def destination(self):
        return self._destination
    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def airplane_type(self):
        return self._airplane_type
    @airplane_type.setter
    def airplane_type(self, value):
        self._airplane_type = value

    @property
    def departure_time(self):
        return self._departure_time
    @departure_time.setter
    def departure_time(self, value):
        self._departure_time = value

    @property
    def flight_id(self):
        return self._flight_id
    @flight_id.setter
    def flight_id(self, value):
        self._flight_id = self._flight_id

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value


