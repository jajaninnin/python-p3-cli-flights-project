from models.__init__ import CONN, CURSOR
from models.flight import Flight
from models.passenger import Passenger
from rich.console import Console
from rich.table import Table

class Booking:
    all = []

    def __init__(self, passenger_id, flight_id, seat, id=None):
        self.passenger_id = passenger_id
        self.flight_id = flight_id
        self.seat = seat
        self.id = id
        Booking.add_new_booking(self)

    @classmethod
    def add_new_booking(cls, new_booking):
        cls.all.append(new_booking)
    
    # @property
    # def passenger_id(self):
    #     return self._passenger_id

    # @passenger_id.setter
    # def passenger(self, new_passenger_id):
    #     if isinstance(new_passenger_id, Passenger.id):
    #         self._passenger_id = new_passenger_id
    #     else: 
    #         raise TypeError("Must be of type Passenger.")

    # @property
    # def flight_id(self):
    #     return self._flight 

    # @flight_id.setter
    # def flight_id(self, new_flight_id):
    #     if isinstance(new_flight_id, Flight.id):
    #         self._flight_id = new_flight_id
    #     else:
    #         raise TypeError("Must be of type Flight")
    
    @property
    def seat(self):
        return self._seat

    @seat.setter
    def seat(self, new_seat):
        if isinstance(new_seat, str):
            if 0 < len(new_seat) <= 3:
                self._seat = new_seat.upper()
            else:
                raise ValueError("Seat must be 1-3 char.")
        else:
            raise TypeError("Seat must be a str")
   
    @classmethod
    def check_if_seat_is_booked(cls, new_seat, flight_id):
        sql = '''
            SELECT seat FROM bookings 
            WHERE seat = ?
            AND flight_id = ?
        '''
        seat_already_booked = CURSOR.execute(sql, (new_seat, flight_id)).fetchone()
        if (seat_already_booked):
            print("Seat is already booked, try another one")
            return True
        else:
            return False
    
    @classmethod
    def check_if_already_on_flight(cls, passenger_id, flight_id):
        sql = '''
            SELECT * FROM bookings 
            WHERE passenger_id = ?
            AND flight_id = ?
        '''
        passenger_already_on_flight = CURSOR.execute(sql, (passenger_id, flight_id)).fetchone()
        if (passenger_already_on_flight):
            print("Passenger is already booked on this flight, try another one")
            return True
        else:
            return False

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS bookings(
                id INTEGER PRIMARY KEY,
                passenger_id INTEGER,
                flight_id INTEGER,
                seat TEXT,
                FOREIGN KEY (passenger_id) REFERENCES passengers(id),
                FOREIGN KEY (flight_id) REFERENCES flights(id)
            );
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        drop_table_sql = """
            DROP TABLE IF EXISTS bookings;
        """
        CURSOR.execute(drop_table_sql)
        CONN.commit()

    @classmethod
    def create_initial_data(cls):
        find_all = '''
            SELECT * FROM bookings;
        '''
        result = CURSOR.execute(find_all).fetchone()
        if (result == None):
            insert_sql = """
                INSERT INTO bookings (id, passenger_id, flight_id, seat) VALUES
                    (1, 1, 1, '1A'),
                    (2, 2, 1, '2A'),
                    (3, 3, 1, '3A'),
                    (4, 4, 2, '12B'),
                    (5, 5, 2, '15C'),
                    (6, 6, 3, '1A')
                    ;
            """
            CURSOR.execute(insert_sql)
            CONN.commit()
        
    def save(self):
        sql = """
            INSERT INTO bookings (passenger_id, flight_id, seat)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.passenger_id, self.flight_id, self.seat))
        CONN.commit()
        self.id = CURSOR.lastrowid
    
    @classmethod
    def print_booking_info(cls, booking):
        table = Table(title="Booking Info")
        table.add_column("ID", header_style="bold magenta", style="red")
        table.add_column("Passenger ID", header_style="bold magenta")
        table.add_column("Flight ID", header_style="bold magenta")
        table.add_column("Seat", header_style="bold magenta")
        table.add_row(
            str(booking.id), 
            str(booking.passenger_id),
            str(booking.flight_id),
            booking.seat
        )
        console = Console()
        console.print(table)

    @classmethod
    def all_bookings(cls):
        sql = '''
            SELECT * FROM bookings;
        '''
        bookings = CURSOR.execute(sql).fetchall()
        table = Table(title="Booking Info")
        table.add_column("ID", header_style="bold magenta", style='red')
        table.add_column("Passenger ID", header_style="bold magenta")
        table.add_column("Flight ID", header_style="bold magenta")
        table.add_column("Seat", header_style="bold magenta")
        for row in bookings:
            booking = cls.create_instance(row)
            table.add_row(
            str(booking.id), 
            str(booking.passenger_id),
            str(booking.flight_id),
            booking.seat
            )
        console = Console()
        console.print(table)
    
    @classmethod
    def create(cls, passenger_id, flight_id, seat):
        is_seat_booked = cls.check_if_seat_is_booked(seat, flight_id)
        is_on_flight = cls.check_if_already_on_flight(passenger_id, flight_id)
        passenger_does_not_exist = Passenger.find_by_id(passenger_id) == None
        flight_does_not_exist = Flight.find_by_id(flight_id) == None
        if is_seat_booked or is_on_flight:
            return None
        elif passenger_does_not_exist:
            print("Passenger id does not exist. Try another one.")
            return None
        elif flight_does_not_exist:
            print("Flight id does not exist. Try another one.")
            return None
        else:
            new_booking = cls(passenger_id, flight_id, seat)
            new_booking.save()
            return new_booking

    @classmethod
    def create_instance(cls, booking):
        return cls( 
            id=booking[0], 
            passenger_id=booking[1], 
            flight_id=booking[2],
            seat=booking[3]
        )
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM bookings
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            return cls.create_instance(row)
        else:
            return None
        
    @classmethod
    def delete(cls, id):
        booking_to_delete = cls.find_by_id(id)
        sql = """
            DELETE FROM bookings
            WHERE id = ?
        """
        if booking_to_delete:
            CURSOR.execute(sql, (booking_to_delete.id,))
            CONN.commit()
            return 'Successfully deleted'
        else:
            return None

    def __repr__(self):
        return f"<Order passenger={self.passenger.first_name}, {self.passenger.l}  flight={self.flight.name}>"