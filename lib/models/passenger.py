from models.__init__ import CONN, CURSOR
from rich.console import Console
from rich.table import Table

class Passenger:
    all = []

    def __init__(self, first_name, last_name, age, passport, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.passport = passport
        self.id = id
    
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, new_first_name):
        if isinstance(new_first_name, str):
            if 0 < len(new_first_name) <= 10:
                self._first_name = new_first_name.capitalize()
            else:
                return ValueError("Passenger first name must be 1-10 char.")
        else:
            raise TypeError("Passenger first name must be a str")
    
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name):
        if isinstance(new_last_name, str):
            if 0 < len(new_last_name) <= 10:
                self._last_name = new_last_name.capitalize()
            else:
                return ValueError("Passenger last name must be 1-10 char.")
        else:
            raise TypeError("Passenger last name must be a str")
    
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_age):
        try:
            ageasInt = int(new_age)
            if isinstance(ageasInt, int):
                if (0 < ageasInt <= 120):
                    self._age = ageasInt
                else:
                    return ValueError("Age must be between 0 to 120 years old.")
            else:
                raise TypeError("Age must be a int")
        except:
            print("Passenger age is not a valid number")
            return TypeError("Not a valid number")

    @property
    def passport(self):
        return self._passport

    @passport.setter
    def passport(self, new_passport):
        if isinstance(new_passport, str):
            if 4 < len(new_passport) <= 10:
                self._passport = new_passport.upper()
            else:
                raise ValueError("Passenger passport must be 5-10 char.")
        else:
            raise TypeError("Passenger passport must be a str")
    
    def bookings(self):
        from models.booking import Booking
        sql = '''
            SELECT * FROM bookings WHERE passenger_id = ?
        '''
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        result = []
        for row in rows:
            result.append(Booking.create_instance(row))
        return result
            
    def flights(self):   
        # get all the flights that this passenger has
        from models.booking import Booking
        from models.flight import Flight
        sql = '''
            SELECT * FROM flights 
            JOIN bookings ON bookings.flight_id = flights.id 
            JOIN passengers ON passengers.id = bookings.passenger_id 
            WHERE passengers.id = ?
        '''
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        result = []
        for row in rows:
            result.append(Flight.create_instance(row))
        return result

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS passengers (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                age INTEGER,
                passport TEXT
            );
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def create_initial_data(cls):
        find_all = '''
            SELECT * FROM passengers;
        '''
        result = CURSOR.execute(find_all).fetchone()
        if (result == None):
            insert_sql = """
                INSERT INTO passengers (id, first_name, last_name, age, passport) VALUES
                    (1, 'John', 'Smith', 35, 'ABC12345'),
                    (2, 'Jane', 'Doe', 30, 'DEF67890'),
                    (3, 'Peter', 'Python', 40, 'GHI12345'),
                    (4, 'Paula', 'Python', 38, 'GHI67890'),
                    (5, 'Time', 'Traveler', 99, 'JKL00000'),
                    (6, 'David', 'Davidson', 25, 'MNO60890')
                    ;
            """
            CURSOR.execute(insert_sql)
            CONN.commit()
    
    @classmethod
    def drop_table(cls):
        drop_table_sql = """
            DROP TABLE IF EXISTS passengers;
        """
        CURSOR.execute(drop_table_sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO passengers (first_name, last_name, age, passport)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.age, self.passport))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def print_passenger_info(cls, passenger):
        table = Table(title="Passenger Info")
        table.add_column("ID", header_style="bold magenta", style="red")
        table.add_column("First Name", header_style="bold magenta")
        table.add_column("Last Name", header_style="bold magenta")
        table.add_column("Age", header_style="bold magenta")
        table.add_column("Passport Number", header_style="bold magenta")
        table.add_row(
            str(passenger.id), 
            passenger.first_name,
            passenger.last_name,
            str(passenger.age),
            passenger.passport
        )
        console = Console()
        console.print(table)
    
    @classmethod
    def all_passengers(cls):
        sql = '''
            SELECT * FROM passengers;
        '''
        passengers = CURSOR.execute(sql).fetchall()
        table = Table(title="Passenger Info")
        table.add_column("ID", header_style="bold magenta", style="red")
        table.add_column("First Name", header_style="bold magenta")
        table.add_column("Last Name", header_style="bold magenta")
        table.add_column("Age", header_style="bold magenta")
        table.add_column("Passport Number", header_style="bold magenta")
        for row in passengers:
            passenger = cls.create_instance(row)
            table.add_row(
            str(passenger.id), 
            passenger.first_name,
            passenger.last_name,
            str(passenger.age),
            passenger.passport
            )
        console = Console()
        console.print(table)
    
    @classmethod
    def check_if_passport_exists(cls, new_passenger):
        sql = '''
            SELECT * FROM passengers
            WHERE passport = ?
        '''
        row = CURSOR.execute(sql, (new_passenger.passport,)).fetchone()
        if row:
            print("A person with this passport already exists, try another one")
            return True
        else:
            return False

    @classmethod
    def create(cls, first_name, last_name, age, passport):
        try:
            new_passenger = cls(first_name, last_name, age, passport)
            if cls.check_if_passport_exists(new_passenger):
                return None
            else:
                new_passenger.save()
                return new_passenger
        except:
            print("Passenger info invalid, please try again.")

    @classmethod
    def create_instance(cls, passenger):
        return cls( 
            id=passenger[0], 
            first_name=passenger[1], 
            last_name=passenger[2], 
            age=passenger[3], 
            passport=passenger[4], 
        )

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM passengers
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            return cls.create_instance(row)
        else:
            return None
    
    @classmethod
    def delete(cls, id):
        passenger_to_delete = cls.find_by_id(id)
        sql = """
            DELETE FROM passengers
            WHERE id = ?
        """
        sql_booking = '''
            DELETE FROM bookings
            WHERE passenger_id = ?
        '''
        if passenger_to_delete:
            CURSOR.execute(sql, (passenger_to_delete.id,))
            CONN.commit()
            CURSOR.execute(sql_booking, (passenger_to_delete.id,))
            CONN.commit()
            return 'Successfully deleted'
        else:
            return None
        
    def __repr__(self):
        return f"<Passenger id={self.id} first_name={self.first_name} last_name={self.last_name} age={self.age} passport={self.passport}>"