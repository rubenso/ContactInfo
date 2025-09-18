# ContactInfo

A sample contact information management application for EUC (End User Computing) interview demonstration.

## Overview

This application demonstrates fundamental programming concepts and best practices through a simple contact management system. It showcases:

- Object-oriented programming principles
- Data validation and error handling
- File I/O and data persistence
- Command-line interface design
- Unit testing practices
- Code documentation and organization

## Features

### Core Functionality
- **Add Contacts**: Create new contacts with validation
- **View Contacts**: Display all contacts in a formatted list
- **Search Contacts**: Find contacts by name, email, or company
- **Update Contacts**: Modify existing contact information
- **Delete Contacts**: Remove contacts from the system
- **Statistics**: View summary information about your contacts

### Data Management
- **Data Validation**: Email format validation, name validation
- **Duplicate Prevention**: Prevents duplicate contacts by email
- **Data Persistence**: Automatically saves data to JSON file
- **Error Handling**: Graceful handling of invalid inputs and edge cases

### User Interface
- **Command Line Interface**: Interactive menu-driven CLI
- **Batch Operations**: Programmatic API for bulk operations
- **Sample Data**: Automatically creates sample contacts for demonstration

## Files Description

### `contact_manager.py`
The core module containing the main business logic:
- `Contact` class: Represents individual contact with validation
- `ContactManager` class: Handles CRUD operations and data persistence

### `cli.py`
Interactive command-line interface for user interaction:
- Menu-driven interface
- Input validation and user-friendly prompts
- Formatted output displays

### `test_contact_manager.py`
Comprehensive test suite demonstrating testing best practices:
- Unit tests for Contact class
- Integration tests for ContactManager
- Test data isolation using temporary files
- Edge case testing

## Usage

### Running the Application

1. **Interactive CLI Mode**:
   ```bash
   python cli.py
   ```
   
2. **Programmatic Usage**:
   ```bash
   python contact_manager.py
   ```

3. **Running Tests**:
   ```bash
   python test_contact_manager.py
   ```

### Example Usage

```python
from contact_manager import Contact, ContactManager

# Create a contact manager
manager = ContactManager()

# Add a new contact
contact = Contact("John", "Doe", "john.doe@email.com", "555-0001", "TechCorp")
manager.add_contact(contact)

# Search for contacts
results = manager.search_contacts("TechCorp")

# Update a contact
manager.update_contact("john.doe@email.com", phone="555-9999")

# Get statistics
stats = manager.get_stats()
print(f"Total contacts: {stats['total_contacts']}")
```

## Technical Implementation

### Data Model
```
Contact:
  - first_name (required, validated)
  - last_name (required, validated)
  - email (required, unique, validated)
  - phone (optional)
  - company (optional)
  - notes (optional)
  - created_at (auto-generated)
  - updated_at (auto-updated)
```

### Validation Rules
- **Names**: Non-empty, letters/spaces/hyphens/apostrophes only
- **Email**: Valid email format, automatically normalized to lowercase
- **Uniqueness**: Email addresses must be unique across all contacts

### Data Persistence
- Data is stored in JSON format (`contacts.json`)
- Automatic loading on startup
- Automatic saving after modifications
- Graceful handling of missing or corrupted data files

## Code Quality Features

### Error Handling
- Input validation with meaningful error messages
- Graceful degradation for missing files
- Exception handling throughout the application

### Testing
- Comprehensive unit test coverage
- Test data isolation using temporary files
- Both positive and negative test cases
- Integration testing of complete workflows

### Documentation
- Detailed docstrings for all classes and methods
- Type hints for improved code clarity
- Inline comments for complex logic
- Comprehensive README with examples

## Design Patterns Used

1. **Single Responsibility Principle**: Each class has a clear, focused purpose
2. **Data Validation**: Input validation at the model level
3. **Separation of Concerns**: Business logic separated from UI logic
4. **Factory Pattern**: `from_dict()` class method for object creation
5. **Error Handling**: Consistent exception handling patterns

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## Sample Data

The application includes sample contacts that are automatically created on first run:

1. **John Doe** - Software Engineer at TechCorp
2. **Jane Smith** - Data Analyst at DataSys  
3. **Bob Johnson** - Project Manager at TechCorp
4. **Alice Brown** - Designer at StartupXYZ

This sample data allows immediate exploration of all features without manual data entry.

## Interview Demonstration Points

This application demonstrates:

1. **Programming Fundamentals**: Classes, methods, data structures
2. **Best Practices**: Validation, error handling, documentation
3. **Testing**: Unit tests with good coverage
4. **User Experience**: Intuitive CLI with clear feedback
5. **Data Management**: Persistence, CRUD operations, search
6. **Code Organization**: Modular design with clear separation of concerns

Perfect for showcasing technical skills in an EUC interview context!