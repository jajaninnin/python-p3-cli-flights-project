from models.__init__ import CONN, CURSOR
from rich.console import Console
from rich.table import Table

class Flight:
    def __init__(self, name, number, origin, destination, departure_time, arrival_time, id=None):
        self.id = id
        self.name = name
        self.number = number
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not hasattr(self, "_name"):
            if isinstance(new_name, str):
                if 0 < len(new_name) <= 6:
                    self._name = new_name.upper()
                else:
                    raise ValueError("Flight name must be 1-6 char.")
            else:
                raise TypeError("Flight name must be of type str.")
        else:
            raise ValueError("Cannot change the name.")
    
    @property 
    def number(self):
        return self._number

    @number.setter
    def number(self, new_number):
        try: 
            numberAsInt = int(new_number)
            if isinstance(numberAsInt, int):
                if (0 < len(str(numberAsInt)) <= 5):
                    self._number = numberAsInt
                else:
                    raise ValueError("Flight number must be between 1 and 5 digits.")
            else:
                raise TypeError("Flight number must be an int")
        except:
            print("Flight number is not a valid number")
            raise TypeError("Not a valid number")
       
    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, new_origin):
        if isinstance(new_origin, str):
            if 0 < len(new_origin) <= 4:
                self._origin = new_origin.upper()
            else:
                raise ValueError("Flight origin must be 1-4 char.")
        else:
            raise TypeError("Flight origin must be a str")

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, new_destination):
        if isinstance(new_destination, str):
            if 0 < len(new_destination) <= 4:
                self._destination = new_destination.upper()
            else:
                raise ValueError("Flight destination must be 1-4 char.")
        else:
            raise TypeError("Flight destination must be a str")
    
    @property
    def departure_time(self):
        return self._departure_time

    @departure_time.setter
    def departure_time(self, new_departure_time):
        if isinstance(new_departure_time, str):
            if 0 < len(new_departure_time) <= 10:
                self._departure_time = new_departure_time
            else:
                raise ValueError("Departure time must be 1-10 char.")
        else:
            raise TypeError("Flight departure time must be a str")
    
    @property
    def arrival_time(self):
        return self._arrival_time

    @arrival_time.setter
    def arrival_time(self, new_arrival_time):
        if isinstance(new_arrival_time, str):
            if 0 < len(new_arrival_time) <= 10:
                self._arrival_time = new_arrival_time
            else:
                raise ValueError("Arrival time must be 1-10 char.")
        else:
            raise ValueError("Flight arrival time must be a str")

    def bookings(self):
        from models.booking import Booking
        sql = '''
            SELECT * FROM bookings WHERE flight_id = ?
        '''
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        result = []
        for row in rows:
            result.append(Booking.create_instance(row))
        return result
            
    def passengers(self):
        # get all the passengers that are on this flight
        from models.booking import Booking
        from models.passenger import Passenger
        sql = '''
            SELECT * FROM passengers 
            JOIN bookings ON bookings.passenger_id = passengers.id 
            JOIN flights ON flights.id = bookings.flight_id 
            WHERE flights.id = ?
        '''
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        result = []
        for row in rows:
            result.append(Passenger.create_instance(row))
        return result 

    @classmethod
    def create_table(cls):
        # create the table
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS flights(
                id INTEGER PRIMARY KEY,
                name TEXT,
                number INTEGER,
                origin TEXT,
                destination TEXT,
                departure_time TEXT,
                arrival_time TEXT
            );
        """

        CURSOR.execute(create_table_sql)
        CONN.commit()

    @classmethod
    def create_initial_data(cls):
        # put some sample data into the table
        find_all = '''
            SELECT * FROM flights;
        '''
        result = CURSOR.execute(find_all).fetchone()
        if (result == None):
            insert_sql = """
                INSERT INTO flights (name, number, origin, destination, departure_time, arrival_time) VALUES
                    ('FLGHTA', 12345, 'NYC', 'BCN', '12:00pm', '5:20pm'),
                    ('FLGHTB', 67890, 'NYC', 'CDG', '8:00pm', '3:20am'),
                    ('FLGHTC', 11111, 'NYC', 'NAIA', '1:30pm', '1:45pm');
            """
            CURSOR.execute(insert_sql)
            CONN.commit()

    @classmethod
    def drop_table(cls):
        drop_table_sql = """
            DROP TABLE IF EXISTS flights;
        """
        CURSOR.execute(drop_table_sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO flights (name, number, origin, destination, departure_time, arrival_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.number, self.origin, self.destination, self.departure_time, self.arrival_time))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def print_flight_info(cls, flight):
        table = Table(title="Flight Info")
        table.add_column("ID", header_style="bold magenta", style="red")
        table.add_column("Name", header_style="bold magenta")
        table.add_column("Number", header_style="bold magenta")
        table.add_column("Origin", header_style="bold magenta")
        table.add_column("Destination", header_style="bold magenta")
        table.add_column("Departure Time", header_style="bold magenta")
        table.add_column("Arrival Time", header_style="bold magenta")
        table.add_row(
            str(flight.id), 
            flight.name, 
            str(flight.number), 
            flight.origin, 
            flight.destination, 
            flight.departure_time, 
            flight.arrival_time
        )
        console = Console()
        console.print(table)

    @classmethod
    def all_flights(cls):
        sql = '''
            SELECT * FROM flights;
        '''
        flights = CURSOR.execute(sql).fetchall()
        table = Table(title="Flight Info")
        table.add_column("ID", header_style="bold magenta", style="red")
        table.add_column("Name", header_style="bold magenta")
        table.add_column("Number", header_style="bold magenta")
        table.add_column("Origin", header_style="bold magenta")
        table.add_column("Destination", header_style="bold magenta")
        table.add_column("Departure Time", header_style="bold magenta")
        table.add_column("Arrival Time", header_style="bold magenta")
        
        for row in flights:
            flight = cls.create_instance(row)
            table.add_row(
                str(flight.id), 
                flight.name, 
                str(flight.number), 
                flight.origin, 
                flight.destination, 
                flight.departure_time, 
                flight.arrival_time
            )
        console = Console()
        console.print(table)

    @classmethod
    def check_if_flight_exists(cls, flight):
        sql = '''
            SELECT * FROM flights
            WHERE name = ?
            AND number = ?
        '''
        row = CURSOR.execute(sql, (flight.name, flight.number)).fetchone()
        if row:
            print("This flight already exists, try another one")
            return True
        else:
            return False

    @classmethod
    def create(cls, name, number, origin, destination, departure_time, arrival_time):
        try:
            new_flight = cls(name, number, origin, destination, departure_time, arrival_time)
            if cls.check_if_flight_exists(new_flight):
                return None
            else:
                new_flight.save()
                return new_flight
        except:
            print("Flight info invalid, please try again.")

    @classmethod
    def create_instance(cls, flight):
        return cls( 
            id=flight[0], 
            name=flight[1], 
            number=flight[2], 
            origin=flight[3], 
            destination=flight[4], 
            departure_time=flight[5],
            arrival_time=flight[6]
        )

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM flights
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            return cls.create_instance(row)
        else:
            return None
        
    @classmethod
    def delete(cls, id):
        flight_to_delete = cls.find_by_id(id)
        sql = """
            DELETE FROM flights
            WHERE id = ?
        """
        sql_booking = '''
            DELETE FROM bookings
            WHERE flight_id = ?
        '''
        if flight_to_delete:
            CURSOR.execute(sql, (flight_to_delete.id,))
            CONN.commit()
            CURSOR.execute(sql_booking, (flight_to_delete.id,))
            CONN.commit()
            return 'Successfully deleted'
        else:
            return None
        
    def __repr__(self):
        return f"<Flight id={self.id} name={self.name} number={self.number} origin={self.origin} destination={self.destination} departure_time={self.departure_time} arrival_time={self.arrival_time}>"
        
    