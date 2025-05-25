from datetime import datetime, timedelta
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import uuid
import json
from enum import Enum

class ItemStatus(Enum):
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"
    LOST = "lost"

class UserRole(Enum):
    STUDENT = "student"
    FACULTY = "faculty"
    LIBRARIAN = "librarian"
    ADMIN = "admin"

class LibraryException(Exception):
    """Base exception class for library-related errors"""
    pass

class ItemNotAvailableException(LibraryException):
    """Raised when attempting to check out an unavailable item"""
    pass

class UserNotFoundException(LibraryException):
    """Raised when a user is not found in the system"""
    pass

class Logger:
    """Handles logging of library operations"""
    
    def __init__(self, log_file: str = "library_log.txt"):
        self.log_file = log_file
    
    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)

class Person:
    """Base class for all persons in the library system"""
    
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone
        self.id = str(uuid.uuid4())
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

class LibraryUser(Person):
    """Represents a library user with borrowing privileges"""
    
    def __init__(self, name: str, email: str, phone: str, role: UserRole):
        super().__init__(name, email, phone)
        self.role = role
        self.borrowed_items: List[str] = []  # List of item IDs
        self.reserved_items: List[str] = []  # List of item IDs
        self.fines: float = 0.0
    
    def to_dict(self) -> dict:
        user_dict = super().to_dict()
        user_dict.update({
            "role": self.role.value,
            "borrowed_items": self.borrowed_items,
            "reserved_items": self.reserved_items,
            "fines": self.fines
        })
        return user_dict

class LibraryItem(ABC):
    """Abstract base class for all library items"""
    
    def __init__(self, title: str, location: str, cost: float):
        self.id = str(uuid.uuid4())
        self.title = title
        self.location = location
        self.cost = cost
        self.status = ItemStatus.AVAILABLE
        self.checked_out_to: Optional[str] = None
        self.due_date: Optional[datetime] = None
        self.reserved_by: List[str] = []
    
    @abstractmethod
    def get_checkout_duration(self) -> timedelta:
        pass
    
    @abstractmethod
    def get_daily_fine(self) -> float:
        pass
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "cost": self.cost,
            "status": self.status.value,
            "checked_out_to": self.checked_out_to,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "reserved_by": self.reserved_by,
            "type": self.__class__.__name__
        }

class Book(LibraryItem):
    """Represents a physical book in the library"""
    
    def __init__(self, title: str, author: str, isbn: str, location: str, cost: float,
                 publisher: str, publication_year: int, edition: str):
        super().__init__(title, location, cost)
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.publication_year = publication_year
        self.edition = edition
    
    def get_checkout_duration(self) -> timedelta:
        return timedelta(days=21)  # 3 weeks for books
    
    def get_daily_fine(self) -> float:
        return 0.50  # $0.50 per day
    
    def to_dict(self) -> dict:
        book_dict = super().to_dict()
        book_dict.update({
            "author": self.author,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "publication_year": self.publication_year,
            "edition": self.edition
        })
        return book_dict

class DVD(LibraryItem):
    """Represents a DVD in the library"""
    
    def __init__(self, title: str, director: str, location: str, cost: float,
                 runtime: int, release_year: int):
        super().__init__(title, location, cost)
        self.director = director
        self.runtime = runtime
        self.release_year = release_year
    
    def get_checkout_duration(self) -> timedelta:
        return timedelta(days=7)  # 1 week for DVDs
    
    def get_daily_fine(self) -> float:
        return 1.00  # $1.00 per day
    
    def to_dict(self) -> dict:
        dvd_dict = super().to_dict()
        dvd_dict.update({
            "director": self.director,
            "runtime": self.runtime,
            "release_year": self.release_year
        })
        return dvd_dict

class Magazine(LibraryItem):
    """Represents a magazine in the library"""
    
    def __init__(self, title: str, publisher: str, location: str, cost: float,
                 issue_number: str, publication_date: datetime):
        super().__init__(title, location, cost)
        self.publisher = publisher
        self.issue_number = issue_number
        self.publication_date = publication_date
    
    def get_checkout_duration(self) -> timedelta:
        return timedelta(days=14)  # 2 weeks for magazines
    
    def get_daily_fine(self) -> float:
        return 0.25  # $0.25 per day
    
    def to_dict(self) -> dict:
        magazine_dict = super().to_dict()
        magazine_dict.update({
            "publisher": self.publisher,
            "issue_number": self.issue_number,
            "publication_date": self.publication_date.isoformat()
        })
        return magazine_dict

class LibraryDatabase:
    """Handles data persistence for the library system"""
    
    def __init__(self, filename: str = "library_data.json"):
        self.filename = filename
        self.users: Dict[str, LibraryUser] = {}
        self.items: Dict[str, LibraryItem] = {}
        self.load_data()
    
    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                
                # Load users
                for user_data in data.get('users', []):
                    user = LibraryUser(
                        name=user_data['name'],
                        email=user_data['email'],
                        phone=user_data['phone'],
                        role=UserRole(user_data['role'])
                    )
                    user.id = user_data['id']
                    user.borrowed_items = user_data['borrowed_items']
                    user.reserved_items = user_data['reserved_items']
                    user.fines = user_data['fines']
                    self.users[user.id] = user
                
                # Load items
                for item_data in data.get('items', []):
                    item: LibraryItem
                    if item_data['type'] == 'Book':
                        item = Book(
                            title=item_data['title'],
                            author=item_data['author'],
                            isbn=item_data['isbn'],
                            location=item_data['location'],
                            cost=item_data['cost'],
                            publisher=item_data['publisher'],
                            publication_year=item_data['publication_year'],
                            edition=item_data['edition']
                        )
                    elif item_data['type'] == 'DVD':
                        item = DVD(
                            title=item_data['title'],
                            director=item_data['director'],
                            location=item_data['location'],
                            cost=item_data['cost'],
                            runtime=item_data['runtime'],
                            release_year=item_data['release_year']
                        )
                    elif item_data['type'] == 'Magazine':
                        item = Magazine(
                            title=item_data['title'],
                            publisher=item_data['publisher'],
                            location=item_data['location'],
                            cost=item_data['cost'],
                            issue_number=item_data['issue_number'],
                            publication_date=datetime.fromisoformat(item_data['publication_date'])
                        )
                    
                    item.id = item_data['id']
                    item.status = ItemStatus(item_data['status'])
                    item.checked_out_to = item_data['checked_out_to']
                    item.due_date = datetime.fromisoformat(item_data['due_date']) if item_data['due_date'] else None
                    item.reserved_by = item_data['reserved_by']
                    self.items[item.id] = item
                    
        except FileNotFoundError:
            # Initialize with empty data if file doesn't exist
            self.save_data()
    
    def save_data(self):
        data = {
            'users': [user.to_dict() for user in self.users.values()],
            'items': [item.to_dict() for item in self.items.values()]
        }
        
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

class LibrarySystem:
    """Main class that handles library operations"""
    
    def __init__(self):
        self.database = LibraryDatabase()
        self.logger = Logger()
    
    def add_user(self, name: str, email: str, phone: str, role: UserRole) -> LibraryUser:
        user = LibraryUser(name, email, phone, role)
        self.database.users[user.id] = user
        self.database.save_data()
        self.logger.log(f"New user created: {user.name} ({user.id})")
        return user
    
    def add_item(self, item: LibraryItem):
        self.database.items[item.id] = item
        self.database.save_data()
        self.logger.log(f"New item added: {item.title} ({item.id})")
    
    def check_out_item(self, user_id: str, item_id: str):
        user = self.database.users.get(user_id)
        item = self.database.items.get(item_id)
        
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        
        if not item:
            raise LibraryException(f"Item {item_id} not found")
        
        if item.status != ItemStatus.AVAILABLE:
            raise ItemNotAvailableException(f"Item {item.title} is not available")
        
        item.status = ItemStatus.CHECKED_OUT
        item.checked_out_to = user.id
        item.due_date = datetime.now() + item.get_checkout_duration()
        user.borrowed_items.append(item.id)
        
        self.database.save_data()
        self.logger.log(f"Item {item.title} checked out to {user.name}")
    
    def return_item(self, item_id: str):
        item = self.database.items.get(item_id)
        
        if not item:
            raise LibraryException(f"Item {item_id} not found")
        
        if item.status != ItemStatus.CHECKED_OUT:
            raise LibraryException(f"Item {item.title} is not checked out")
        
        user = self.database.users.get(item.checked_out_to)
        if user:
            user.borrowed_items.remove(item.id)
            
            # Calculate late fees
            if item.due_date and datetime.now() > item.due_date:
                days_late = (datetime.now() - item.due_date).days
                fine = days_late * item.get_daily_fine()
                user.fines += fine
                self.logger.log(f"Late fee of ${fine:.2f} added to {user.name}'s account")
        
        item.status = ItemStatus.AVAILABLE
        item.checked_out_to = None
        item.due_date = None
        
        # Handle reservations
        if item.reserved_by:
            next_user_id = item.reserved_by.pop(0)
            item.status = ItemStatus.RESERVED
            self.logger.log(f"Item {item.title} is now reserved for user {next_user_id}")
        
        self.database.save_data()
        self.logger.log(f"Item {item.title} returned")
    
    def reserve_item(self, user_id: str, item_id: str):
        user = self.database.users.get(user_id)
        item = self.database.items.get(item_id)
        
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        
        if not item:
            raise LibraryException(f"Item {item_id} not found")
        
        if user_id in item.reserved_by:
            raise LibraryException(f"User has already reserved this item")
        
        item.reserved_by.append(user_id)
        user.reserved_items.append(item_id)
        
        self.database.save_data()
        self.logger.log(f"Item {item.title} reserved by {user.name}")
    
    def pay_fines(self, user_id: str, amount: float):
        user = self.database.users.get(user_id)
        
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        
        if amount > user.fines:
            raise LibraryException("Payment amount exceeds outstanding fines")
        
        user.fines -= amount
        self.database.save_data()
        self.logger.log(f"Payment of ${amount:.2f} received from {user.name}")
    
    def get_user_items(self, user_id: str) -> Dict[str, List[LibraryItem]]:
        user = self.database.users.get(user_id)
        
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        
        return {
            "borrowed": [self.database.items[item_id] for item_id in user.borrowed_items],
            "reserved": [self.database.items[item_id] for item_id in user.reserved_items]
        }
