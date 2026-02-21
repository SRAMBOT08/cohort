# Backend Utility Scripts Archive

This folder contains utility scripts used during development and deployment setup. These scripts are not required for normal application operation but may be useful for:

- Setting up test data
- Managing users and roles
- Data migration and import
- Password resets
- Verification and debugging

## Script Categories

### User Management
- `create_*.py` - Scripts for creating test users and data
- `add_*.py` - Scripts for adding students, profiles, etc.
- `make_*.py` - Scripts for creating admins and mentors
- `reset_*.py` - Password reset utilities

### Data Import/Export
- `import_*.py` - Data import utilities from Excel/CSV
- `export_*.py` - Data export utilities
- `preview_*.py` - Preview data before import

### Setup & Configuration  
- `setup_*.py` - Initial setup scripts for mentors, floor wings, etc.
- `call_*.py` - Helper scripts that call other setup scripts

### Verification & Testing
- `check_*.py` - Verification scripts for data integrity
- `verify_*.py` - Login and configuration verification
- `validate_*.py` - Environment and config validation

### Student/Mentor Management
- `assign_*.py` - Student-mentor assignment utilities
- `sync_*.py` - Data synchronization scripts
- `update_*.py` - Update utilities

### Miscellaneous
- `list_*.py` - List users and data
- `inspect_*.py` - Data inspection utilities
- `clear_*.py` - Data clearing utilities
- `push_*.py` - Deployment push utilities

## Usage

These scripts are typically run directly with Python:
```bash
python3 script_name.py
```

**Note:** Most scripts require the Django environment to be properly configured with database access.
