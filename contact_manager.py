#!/usr/bin/env python3
"""
Contact Information Manager
A simple application to demonstrate contact management functionality for EUC interview.

Features:
- Add new contacts
- View all contacts
- Search contacts by name or email
- Update contact information
- Delete contacts
- Data validation
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Optional


class Contact:
    """Represents a contact with basic information."""
    
    def __init__(self, first_name: str, last_name: str, email: str, 
                 phone: str = "", company: str = "", notes: str = ""):
        self.first_name = self._validate_name(first_name)
        self.last_name = self._validate_name(last_name)
        self.email = self._validate_email(email)
        self.phone = phone
        self.company = company
        self.notes = notes
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
    
    def _validate_name(self, name: str) -> str:
        """Validate that name is not empty and contains only valid characters."""
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        # Allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", name.strip()):
            raise ValueError("Name contains invalid characters")
        return name.strip()
    
    def _validate_email(self, email: str) -> str:
        """Validate email format."""
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")
        
        # Basic email validation pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email.strip()):
            raise ValueError("Invalid email format")
        return email.strip().lower()
    
    def update(self, **kwargs):
        """Update contact information."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key in ['first_name', 'last_name']:
                    setattr(self, key, self._validate_name(value))
                elif key == 'email':
                    setattr(self, key, self._validate_email(value))
                else:
                    setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert contact to dictionary for serialization."""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        """Create contact from dictionary."""
        contact = cls(
            data['first_name'],
            data['last_name'],
            data['email'],
            data.get('phone', ''),
            data.get('company', ''),
            data.get('notes', '')
        )
        contact.created_at = data.get('created_at', contact.created_at)
        contact.updated_at = data.get('updated_at', contact.updated_at)
        return contact
    
    def __str__(self) -> str:
        """String representation of contact."""
        return f"{self.first_name} {self.last_name} <{self.email}>"


class ContactManager:
    """Manages a collection of contacts with CRUD operations."""
    
    def __init__(self, data_file: str = "contacts.json"):
        self.data_file = data_file
        self.contacts: List[Contact] = []
        self.load_contacts()
    
    def add_contact(self, contact: Contact) -> bool:
        """Add a new contact. Returns False if email already exists."""
        if self.find_by_email(contact.email):
            return False
        self.contacts.append(contact)
        self.save_contacts()
        return True
    
    def find_by_email(self, email: str) -> Optional[Contact]:
        """Find contact by email address."""
        email = email.lower().strip()
        for contact in self.contacts:
            if contact.email == email:
                return contact
        return None
    
    def search_contacts(self, query: str) -> List[Contact]:
        """Search contacts by name or email."""
        query = query.lower().strip()
        results = []
        for contact in self.contacts:
            if (query in contact.first_name.lower() or 
                query in contact.last_name.lower() or 
                query in contact.email.lower() or
                query in contact.company.lower()):
                results.append(contact)
        return results
    
    def update_contact(self, email: str, **kwargs) -> bool:
        """Update contact by email. Returns True if successful."""
        contact = self.find_by_email(email)
        if contact:
            contact.update(**kwargs)
            self.save_contacts()
            return True
        return False
    
    def delete_contact(self, email: str) -> bool:
        """Delete contact by email. Returns True if successful."""
        contact = self.find_by_email(email)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            return True
        return False
    
    def get_all_contacts(self) -> List[Contact]:
        """Get all contacts sorted by last name, then first name."""
        return sorted(self.contacts, key=lambda c: (c.last_name, c.first_name))
    
    def save_contacts(self):
        """Save contacts to JSON file."""
        try:
            data = [contact.to_dict() for contact in self.contacts]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving contacts: {e}")
    
    def load_contacts(self):
        """Load contacts from JSON file."""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.contacts = [Contact.from_dict(item) for item in data]
        except FileNotFoundError:
            # File doesn't exist yet, start with empty list
            self.contacts = []
        except Exception as e:
            print(f"Error loading contacts: {e}")
            self.contacts = []
    
    def get_stats(self) -> Dict:
        """Get statistics about contacts."""
        total = len(self.contacts)
        companies = set(c.company for c in self.contacts if c.company)
        return {
            'total_contacts': total,
            'unique_companies': len(companies),
            'companies': sorted(list(companies))
        }


def main():
    """Main function to demonstrate the contact manager."""
    manager = ContactManager()
    
    print("=== Contact Information Manager ===")
    print("Sample application for EUC interview demonstration\n")
    
    # Add some sample contacts if none exist
    if not manager.contacts:
        print("Adding sample contacts...")
        sample_contacts = [
            Contact("John", "Doe", "john.doe@email.com", "555-0001", "TechCorp", "Software Engineer"),
            Contact("Jane", "Smith", "jane.smith@email.com", "555-0002", "DataSys", "Data Analyst"),
            Contact("Bob", "Johnson", "bob.johnson@email.com", "555-0003", "TechCorp", "Project Manager"),
            Contact("Alice", "Brown", "alice.brown@email.com", "555-0004", "StartupXYZ", "Designer"),
        ]
        
        for contact in sample_contacts:
            manager.add_contact(contact)
        print(f"Added {len(sample_contacts)} sample contacts.\n")
    
    # Display all contacts
    print("All Contacts:")
    print("-" * 50)
    for contact in manager.get_all_contacts():
        print(f"{contact} | {contact.company} | {contact.phone}")
    
    # Show statistics
    stats = manager.get_stats()
    print(f"\nStatistics:")
    print(f"Total contacts: {stats['total_contacts']}")
    print(f"Unique companies: {stats['unique_companies']}")
    if stats['companies']:
        print(f"Companies: {', '.join(stats['companies'])}")
    
    # Demonstrate search functionality
    print(f"\nSearch demonstration:")
    search_results = manager.search_contacts("Tech")
    print(f"Search for 'Tech': {len(search_results)} results")
    for contact in search_results:
        print(f"  - {contact}")
    
    print(f"\nContact manager demonstration complete!")


if __name__ == "__main__":
    main()