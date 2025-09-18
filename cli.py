#!/usr/bin/env python3
"""
Command Line Interface for Contact Information Manager
Interactive CLI for EUC interview demonstration.
"""

import sys
from contact_manager import Contact, ContactManager


class ContactCLI:
    """Command line interface for contact management."""
    
    def __init__(self):
        self.manager = ContactManager()
        self.running = True
    
    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("       CONTACT INFORMATION MANAGER")
        print("="*50)
        print("1. View all contacts")
        print("2. Add new contact")
        print("3. Search contacts")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Show statistics")
        print("7. Exit")
        print("-"*50)
    
    def get_user_input(self, prompt: str, required: bool = True) -> str:
        """Get user input with optional validation."""
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value
            print("This field is required. Please enter a value.")
    
    def view_all_contacts(self):
        """Display all contacts in a formatted table."""
        contacts = self.manager.get_all_contacts()
        
        if not contacts:
            print("\nNo contacts found.")
            return
        
        print(f"\n{'='*80}")
        print("ALL CONTACTS")
        print(f"{'='*80}")
        print(f"{'Name':<25} {'Email':<30} {'Company':<15} {'Phone':<10}")
        print(f"{'-'*80}")
        
        for contact in contacts:
            name = f"{contact.first_name} {contact.last_name}"
            print(f"{name:<25} {contact.email:<30} {contact.company:<15} {contact.phone:<10}")
        
        print(f"{'-'*80}")
        print(f"Total: {len(contacts)} contacts")
    
    def add_contact(self):
        """Add a new contact through user input."""
        print(f"\n{'='*40}")
        print("ADD NEW CONTACT")
        print(f"{'='*40}")
        
        try:
            first_name = self.get_user_input("First name: ")
            last_name = self.get_user_input("Last name: ")
            email = self.get_user_input("Email: ")
            phone = self.get_user_input("Phone (optional): ", required=False)
            company = self.get_user_input("Company (optional): ", required=False)
            notes = self.get_user_input("Notes (optional): ", required=False)
            
            contact = Contact(first_name, last_name, email, phone, company, notes)
            
            if self.manager.add_contact(contact):
                print(f"\n✓ Contact '{contact}' added successfully!")
            else:
                print(f"\n✗ Error: A contact with email '{email}' already exists.")
        
        except ValueError as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
    
    def search_contacts(self):
        """Search for contacts by query."""
        print(f"\n{'='*40}")
        print("SEARCH CONTACTS")
        print(f"{'='*40}")
        
        query = self.get_user_input("Enter search term (name, email, or company): ")
        results = self.manager.search_contacts(query)
        
        if not results:
            print(f"\nNo contacts found matching '{query}'.")
            return
        
        print(f"\nFound {len(results)} contact(s) matching '{query}':")
        print(f"{'-'*60}")
        
        for i, contact in enumerate(results, 1):
            print(f"{i}. {contact.first_name} {contact.last_name}")
            print(f"   Email: {contact.email}")
            print(f"   Company: {contact.company or 'N/A'}")
            print(f"   Phone: {contact.phone or 'N/A'}")
            if contact.notes:
                print(f"   Notes: {contact.notes}")
            print()
    
    def update_contact(self):
        """Update an existing contact."""
        print(f"\n{'='*40}")
        print("UPDATE CONTACT")
        print(f"{'='*40}")
        
        email = self.get_user_input("Enter email of contact to update: ")
        contact = self.manager.find_by_email(email)
        
        if not contact:
            print(f"\n✗ No contact found with email '{email}'.")
            return
        
        print(f"\nCurrent information for {contact}:")
        print(f"First name: {contact.first_name}")
        print(f"Last name: {contact.last_name}")
        print(f"Email: {contact.email}")
        print(f"Phone: {contact.phone}")
        print(f"Company: {contact.company}")
        print(f"Notes: {contact.notes}")
        
        print(f"\nEnter new values (press Enter to keep current value):")
        
        updates = {}
        
        # Get updates for each field
        new_first_name = self.get_user_input(f"First name ({contact.first_name}): ", required=False)
        if new_first_name:
            updates['first_name'] = new_first_name
        
        new_last_name = self.get_user_input(f"Last name ({contact.last_name}): ", required=False)
        if new_last_name:
            updates['last_name'] = new_last_name
        
        new_phone = self.get_user_input(f"Phone ({contact.phone}): ", required=False)
        if new_phone is not None:  # Allow empty string to clear phone
            updates['phone'] = new_phone
        
        new_company = self.get_user_input(f"Company ({contact.company}): ", required=False)
        if new_company is not None:  # Allow empty string to clear company
            updates['company'] = new_company
        
        new_notes = self.get_user_input(f"Notes ({contact.notes}): ", required=False)
        if new_notes is not None:  # Allow empty string to clear notes
            updates['notes'] = new_notes
        
        if updates:
            try:
                if self.manager.update_contact(email, **updates):
                    print(f"\n✓ Contact updated successfully!")
                    updated_contact = self.manager.find_by_email(email)
                    print(f"Updated contact: {updated_contact}")
                else:
                    print(f"\n✗ Failed to update contact.")
            except ValueError as e:
                print(f"\n✗ Error: {e}")
        else:
            print(f"\nNo changes made.")
    
    def delete_contact(self):
        """Delete a contact."""
        print(f"\n{'='*40}")
        print("DELETE CONTACT")
        print(f"{'='*40}")
        
        email = self.get_user_input("Enter email of contact to delete: ")
        contact = self.manager.find_by_email(email)
        
        if not contact:
            print(f"\n✗ No contact found with email '{email}'.")
            return
        
        print(f"\nContact to delete: {contact}")
        confirm = self.get_user_input("Are you sure you want to delete this contact? (yes/no): ")
        
        if confirm.lower() in ['yes', 'y']:
            if self.manager.delete_contact(email):
                print(f"\n✓ Contact deleted successfully!")
            else:
                print(f"\n✗ Failed to delete contact.")
        else:
            print(f"\nDeletion cancelled.")
    
    def show_statistics(self):
        """Display contact statistics."""
        stats = self.manager.get_stats()
        
        print(f"\n{'='*40}")
        print("CONTACT STATISTICS")
        print(f"{'='*40}")
        print(f"Total contacts: {stats['total_contacts']}")
        print(f"Unique companies: {stats['unique_companies']}")
        
        if stats['companies']:
            print(f"\nCompanies:")
            for company in stats['companies']:
                # Count contacts for each company
                count = sum(1 for c in self.manager.contacts if c.company == company)
                print(f"  - {company}: {count} contact(s)")
        
        # Additional statistics
        contacts_with_phone = sum(1 for c in self.manager.contacts if c.phone)
        contacts_with_notes = sum(1 for c in self.manager.contacts if c.notes)
        
        print(f"\nAdditional stats:")
        print(f"  Contacts with phone: {contacts_with_phone}")
        print(f"  Contacts with notes: {contacts_with_notes}")
    
    def run(self):
        """Main CLI loop."""
        print("Welcome to Contact Information Manager!")
        print("Sample application for EUC interview demonstration.")
        
        # Add some sample data if no contacts exist
        if not self.manager.contacts:
            print("\nNo contacts found. Adding sample data...")
            sample_contacts = [
                Contact("John", "Doe", "john.doe@techcorp.com", "555-0001", "TechCorp", "Software Engineer"),
                Contact("Jane", "Smith", "jane.smith@datasys.com", "555-0002", "DataSys", "Data Analyst"),
                Contact("Bob", "Johnson", "bob.johnson@techcorp.com", "555-0003", "TechCorp", "Project Manager"),
            ]
            
            for contact in sample_contacts:
                self.manager.add_contact(contact)
            print(f"Added {len(sample_contacts)} sample contacts.")
        
        while self.running:
            try:
                self.display_menu()
                choice = self.get_user_input("Select an option (1-7): ")
                
                if choice == "1":
                    self.view_all_contacts()
                elif choice == "2":
                    self.add_contact()
                elif choice == "3":
                    self.search_contacts()
                elif choice == "4":
                    self.update_contact()
                elif choice == "5":
                    self.delete_contact()
                elif choice == "6":
                    self.show_statistics()
                elif choice == "7":
                    print("\nThank you for using Contact Information Manager!")
                    self.running = False
                else:
                    print("\n✗ Invalid option. Please select 1-7.")
                
                if self.running:
                    input("\nPress Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                self.running = False
            except Exception as e:
                print(f"\n✗ An error occurred: {e}")
                input("Press Enter to continue...")


def main():
    """Entry point for the CLI application."""
    cli = ContactCLI()
    cli.run()


if __name__ == "__main__":
    main()