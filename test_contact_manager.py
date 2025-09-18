#!/usr/bin/env python3
"""
Tests for Contact Information Manager
Demonstrates testing practices for EUC interview.
"""

import unittest
import tempfile
import os
import json
from contact_manager import Contact, ContactManager


class TestContact(unittest.TestCase):
    """Test cases for Contact class."""
    
    def test_valid_contact_creation(self):
        """Test creating a valid contact."""
        contact = Contact("John", "Doe", "john.doe@email.com", "555-0001", "TechCorp")
        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Doe")
        self.assertEqual(contact.email, "john.doe@email.com")
        self.assertEqual(contact.phone, "555-0001")
        self.assertEqual(contact.company, "TechCorp")
    
    def test_email_normalization(self):
        """Test that email is normalized to lowercase."""
        contact = Contact("John", "Doe", "JOHN.DOE@EMAIL.COM")
        self.assertEqual(contact.email, "john.doe@email.com")
    
    def test_invalid_name_validation(self):
        """Test name validation with invalid inputs."""
        with self.assertRaises(ValueError):
            Contact("", "Doe", "john@email.com")  # Empty first name
        
        with self.assertRaises(ValueError):
            Contact("John", "", "john@email.com")  # Empty last name
        
        with self.assertRaises(ValueError):
            Contact("John123", "Doe", "john@email.com")  # Invalid characters in name
    
    def test_invalid_email_validation(self):
        """Test email validation with invalid inputs."""
        with self.assertRaises(ValueError):
            Contact("John", "Doe", "")  # Empty email
        
        with self.assertRaises(ValueError):
            Contact("John", "Doe", "invalid-email")  # Invalid email format
        
        with self.assertRaises(ValueError):
            Contact("John", "Doe", "john@")  # Incomplete email
    
    def test_contact_update(self):
        """Test updating contact information."""
        contact = Contact("John", "Doe", "john@email.com")
        contact.update(company="NewCorp", phone="555-9999")
        self.assertEqual(contact.company, "NewCorp")
        self.assertEqual(contact.phone, "555-9999")
    
    def test_contact_serialization(self):
        """Test converting contact to/from dictionary."""
        original = Contact("John", "Doe", "john@email.com", "555-0001", "TechCorp", "Test notes")
        data = original.to_dict()
        recreated = Contact.from_dict(data)
        
        self.assertEqual(original.first_name, recreated.first_name)
        self.assertEqual(original.last_name, recreated.last_name)
        self.assertEqual(original.email, recreated.email)
        self.assertEqual(original.phone, recreated.phone)
        self.assertEqual(original.company, recreated.company)
        self.assertEqual(original.notes, recreated.notes)


class TestContactManager(unittest.TestCase):
    """Test cases for ContactManager class."""
    
    def setUp(self):
        """Set up test environment with temporary file."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.manager = ContactManager(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary file after test."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_contact(self):
        """Test adding a new contact."""
        contact = Contact("John", "Doe", "john@email.com")
        result = self.manager.add_contact(contact)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.contacts), 1)
    
    def test_duplicate_email_prevention(self):
        """Test that duplicate emails are prevented."""
        contact1 = Contact("John", "Doe", "john@email.com")
        contact2 = Contact("Jane", "Smith", "john@email.com")  # Same email
        
        self.assertTrue(self.manager.add_contact(contact1))
        self.assertFalse(self.manager.add_contact(contact2))  # Should fail
        self.assertEqual(len(self.manager.contacts), 1)
    
    def test_find_by_email(self):
        """Test finding contact by email."""
        contact = Contact("John", "Doe", "john@email.com")
        self.manager.add_contact(contact)
        
        found = self.manager.find_by_email("john@email.com")
        self.assertIsNotNone(found)
        self.assertEqual(found.first_name, "John")
        
        not_found = self.manager.find_by_email("nonexistent@email.com")
        self.assertIsNone(not_found)
    
    def test_search_contacts(self):
        """Test searching contacts by various criteria."""
        contacts = [
            Contact("John", "Doe", "john@techcorp.com", company="TechCorp"),
            Contact("Jane", "Smith", "jane@datacorp.com", company="DataCorp"),
            Contact("Bob", "Johnson", "bob@techcorp.com", company="TechCorp"),
        ]
        
        for contact in contacts:
            self.manager.add_contact(contact)
        
        # Search by first name (John appears in both "John" and "Johnson")
        results = self.manager.search_contacts("John")
        self.assertEqual(len(results), 2)  # John Doe and Bob Johnson
        
        # Search for exact first name
        results = self.manager.search_contacts("Jane")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].first_name, "Jane")
        
        # Search by company
        results = self.manager.search_contacts("TechCorp")
        self.assertEqual(len(results), 2)
        
        # Search by email domain
        results = self.manager.search_contacts("techcorp.com")
        self.assertEqual(len(results), 2)
    
    def test_update_contact(self):
        """Test updating existing contact."""
        contact = Contact("John", "Doe", "john@email.com")
        self.manager.add_contact(contact)
        
        result = self.manager.update_contact("john@email.com", company="NewCorp")
        self.assertTrue(result)
        
        updated = self.manager.find_by_email("john@email.com")
        self.assertEqual(updated.company, "NewCorp")
    
    def test_delete_contact(self):
        """Test deleting contact."""
        contact = Contact("John", "Doe", "john@email.com")
        self.manager.add_contact(contact)
        self.assertEqual(len(self.manager.contacts), 1)
        
        result = self.manager.delete_contact("john@email.com")
        self.assertTrue(result)
        self.assertEqual(len(self.manager.contacts), 0)
        
        # Try to delete non-existent contact
        result = self.manager.delete_contact("nonexistent@email.com")
        self.assertFalse(result)
    
    def test_persistence(self):
        """Test saving and loading contacts from file."""
        contact = Contact("John", "Doe", "john@email.com", "555-0001", "TechCorp")
        self.manager.add_contact(contact)
        
        # Create new manager instance with same file
        new_manager = ContactManager(self.temp_file.name)
        self.assertEqual(len(new_manager.contacts), 1)
        
        loaded_contact = new_manager.find_by_email("john@email.com")
        self.assertIsNotNone(loaded_contact)
        self.assertEqual(loaded_contact.first_name, "John")
        self.assertEqual(loaded_contact.company, "TechCorp")
    
    def test_get_stats(self):
        """Test getting statistics about contacts."""
        contacts = [
            Contact("John", "Doe", "john@email.com", company="TechCorp"),
            Contact("Jane", "Smith", "jane@email.com", company="DataCorp"),
            Contact("Bob", "Johnson", "bob@email.com", company="TechCorp"),
            Contact("Alice", "Brown", "alice@email.com", company=""),  # No company
        ]
        
        for contact in contacts:
            self.manager.add_contact(contact)
        
        stats = self.manager.get_stats()
        self.assertEqual(stats['total_contacts'], 4)
        self.assertEqual(stats['unique_companies'], 2)  # TechCorp and DataCorp
        self.assertIn("TechCorp", stats['companies'])
        self.assertIn("DataCorp", stats['companies'])


def run_tests():
    """Run all tests and display results."""
    print("=== Running Contact Manager Tests ===\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestContact))
    suite.addTests(loader.loadTestsFromTestCase(TestContactManager))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n=== Test Summary ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall result: {'PASS' if success else 'FAIL'}")
    return success


if __name__ == "__main__":
    run_tests()