# Backend Test Archive

This folder contains standalone test scripts used during development. These are integration and API tests that verify various endpoints and functionality.

## Test Categories

### API Endpoint Tests
- `test_*_endpoints.py` - Tests for specific feature endpoints (CLT, CFC, SCD, IIPC, etc.)
- `test_api_*.py` - General API testing scripts

### Authentication & Authorization
- `test_login_*.py` - Login functionality tests  
- `test_credentials.py` - Credential verification
- `test_cors.py` - CORS configuration tests

### Integration Tests
- `test_integration.py` - Basic integration tests
- `test_full_integration.py` - Comprehensive integration tests
- `test_complete_review_flow.py` - End-to-end review workflow tests

### Feature-Specific Tests
- `test_hackathon_api.py` - Hackathon registration tests
- `test_leetcode.py` - LeetCode integration tests
- `test_notification_flow.py` - Notification system tests
- `test_announcement_notifications.py` - Announcement notifications

### Performance & Scaling
- `test_scaling_changes.py` - Performance and scaling tests
- `test_full_leaderboard.py` - Leaderboard performance

### Admin & Management
- `test_admin_endpoints.py` - Admin API tests
- `test_mentor_api.py` - Mentor functionality tests
- `test_floorwing_endpoints.py` - Floor wing tests
- `test_student_*.py` - Student-related tests

### Misc Tests
- `test_file_upload.py` - File upload functionality
- `test_review_status.py` - Review status tracking
- `test_config.py` - Configuration tests
- `test_read.py` - Read operation tests

## Note

These are standalone test scripts. For the main comprehensive E2E test suite, see the `/tests` directory in the project root.

## Usage

Run individual tests with:
```bash
python3 test_name.py
```

Make sure your Django environment is properly configured before running tests.
