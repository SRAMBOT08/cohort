#!/usr/bin/env python3
"""
Test script for Gamification API endpoints
Tests all gamification endpoints locally before deployment
"""

import requests
import json
from typing import Dict, Optional

BASE_URL = "http://127.0.0.1:8000"
TOKEN = None

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_section(title: str):
    """Print a section header"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(message: str):
    """Print a success message"""
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message: str):
    """Print an error message"""
    print(f"{RED}✗ {message}{RESET}")

def print_info(message: str):
    """Print an info message"""
    print(f"{YELLOW}ℹ {message}{RESET}")

def get_auth_token(email: str, password: str) -> Optional[str]:
    """Authenticate and get JWT token"""
    print_section("AUTHENTICATION")
    url = f"{BASE_URL}/api/auth/token/"
    data = {
        "username": email,  # The API expects 'username' field but accepts email
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            token = response.json().get('access')
            print_success(f"Successfully authenticated as {email}")
            return token
        else:
            print_error(f"Authentication failed: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Authentication error: {str(e)}")
        return None

def test_endpoint(method: str, endpoint: str, data: Optional[Dict] = None, 
                 expected_status: int = 200, description: str = ""):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    
    if TOKEN:
        headers['Authorization'] = f'Bearer {TOKEN}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method == 'PATCH':
            response = requests.patch(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            print_error(f"Unsupported method: {method}")
            return False
        
        status_ok = response.status_code == expected_status
        
        if status_ok:
            print_success(f"{method} {endpoint}")
            if description:
                print(f"   {description}")
            print(f"   Status: {response.status_code}")
            
            # Try to print response data
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"   Response: List with {len(data)} items")
                    if len(data) > 0:
                        print(f"   First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'N/A'}")
                elif isinstance(data, dict):
                    print(f"   Response keys: {list(data.keys())}")
                else:
                    print(f"   Response: {str(data)[:100]}")
            except:
                print(f"   Response: {response.text[:100]}")
        else:
            print_error(f"{method} {endpoint}")
            print(f"   Expected: {expected_status}, Got: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
        
        return status_ok
    
    except Exception as e:
        print_error(f"{method} {endpoint}")
        print(f"   Error: {str(e)}")
        return False

def test_gamification_endpoints():
    """Test all gamification endpoints"""
    
    results = {
        'passed': 0,
        'failed': 0
    }
    
    # Test ViewSet endpoints
    print_section("TESTING VIEWSET ENDPOINTS")
    
    endpoints = [
        ('GET', '/api/gamification/seasons/', 'List all seasons'),
        ('GET', '/api/gamification/seasons/current/', 'Get current active season'),
        ('GET', '/api/gamification/episodes/', 'List all episodes'),
        ('GET', '/api/gamification/episode-progress/', 'List episode progress'),
        ('GET', '/api/gamification/season-scores/', 'List season scores'),
        ('GET', '/api/gamification/legacy-scores/', 'List legacy scores'),
        ('GET', '/api/gamification/vault-wallets/', 'List vault wallets'),
        ('GET', '/api/gamification/scd-streaks/', 'List SCD streaks'),
        ('GET', '/api/gamification/leaderboard/', 'Get leaderboard'),
        ('GET', '/api/gamification/titles/', 'List all titles'),
        ('GET', '/api/gamification/user-titles/', 'List user titles'),
        ('GET', '/api/gamification/dashboard/', 'Get user dashboard'),
        ('GET', '/api/gamification/progress-notifications/', 'List progress notifications'),
    ]
    
    for method, endpoint, description in endpoints:
        if test_endpoint(method, endpoint, description=description):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Test with specific IDs if data exists
    print_section("TESTING DETAIL ENDPOINTS")
    
    # Try to get a season ID
    try:
        response = requests.get(f"{BASE_URL}/api/gamification/seasons/", 
                              headers={'Authorization': f'Bearer {TOKEN}'})
        if response.status_code == 200:
            seasons = response.json()
            if isinstance(seasons, list) and len(seasons) > 0:
                season_id = seasons[0]['id']
                if test_endpoint('GET', f'/api/gamification/seasons/{season_id}/', 
                               description=f'Get season {season_id} details'):
                    results['passed'] += 1
                else:
                    results['failed'] += 1
            else:
                print_info("No seasons found to test detail endpoint")
    except Exception as e:
        print_error(f"Error testing season detail: {str(e)}")
    
    # Try to get an episode ID
    try:
        response = requests.get(f"{BASE_URL}/api/gamification/episodes/", 
                              headers={'Authorization': f'Bearer {TOKEN}'})
        if response.status_code == 200:
            episodes = response.json()
            if isinstance(episodes, list) and len(episodes) > 0:
                episode_id = episodes[0]['id']
                if test_endpoint('GET', f'/api/gamification/episodes/{episode_id}/', 
                               description=f'Get episode {episode_id} details'):
                    results['passed'] += 1
                else:
                    results['failed'] += 1
            else:
                print_info("No episodes found to test detail endpoint")
    except Exception as e:
        print_error(f"Error testing episode detail: {str(e)}")
    
    return results

def test_mentor_endpoints():
    """Test mentor-specific endpoints"""
    print_section("TESTING MENTOR ENDPOINTS")
    
    results = {
        'passed': 0,
        'failed': 0
    }
    
    # Note: These require mentor role
    mentor_endpoints = [
        ('POST', '/api/gamification/mentor/approve-task/', 'Approve student task'),
        ('GET', '/api/gamification/mentor/student-progress/1/', 'Get student progress'),
        ('POST', '/api/gamification/mentor/finalize-season/1/', 'Finalize student season'),
    ]
    
    print_info("Note: Mentor endpoints require mentor role authentication")
    for method, endpoint, description in mentor_endpoints:
        # Expected to fail or require specific data for student role
        test_endpoint(method, endpoint, description=description, expected_status=200)
    
    return results

def test_floorwing_endpoints():
    """Test floor wing endpoints"""
    print_section("TESTING FLOOR WING ENDPOINTS")
    
    results = {
        'passed': 0,
        'failed': 0
    }
    
    # Note: These require floor wing role
    floorwing_endpoints = [
        ('GET', '/api/gamification/floorwing/seasons/', 'Manage seasons'),
        ('GET', '/api/gamification/floorwing/seasons/1/', 'Manage season detail'),
        ('GET', '/api/gamification/floorwing/seasons/1/episodes/', 'Manage episodes'),
        ('GET', '/api/gamification/floorwing/episodes/1/', 'Manage episode detail'),
    ]
    
    print_info("Note: Floor wing endpoints require floor wing role authentication")
    for method, endpoint, description in floorwing_endpoints:
        test_endpoint(method, endpoint, description=description, expected_status=200)
    
    return results

def main():
    """Main test runner"""
    global TOKEN
    
    print(f"\n{YELLOW}╔═══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{YELLOW}║     GAMIFICATION API ENDPOINTS TEST SUITE                 ║{RESET}")
    print(f"{YELLOW}╚═══════════════════════════════════════════════════════════╝{RESET}")
    
    # Authenticate
    email = input("\nEnter email (default: student@cohortsummit.com): ").strip() or "student@cohortsummit.com"
    password = input("Enter password (default: password): ").strip() or "password"
    
    TOKEN = get_auth_token(email, password)
    
    if not TOKEN:
        print_error("Failed to authenticate. Exiting.")
        return
    
    # Run tests
    total_results = {'passed': 0, 'failed': 0}
    
    # Test main gamification endpoints
    results = test_gamification_endpoints()
    total_results['passed'] += results['passed']
    total_results['failed'] += results['failed']
    
    # Ask if user wants to test role-specific endpoints
    print_section("ROLE-SPECIFIC ENDPOINTS")
    test_mentor = input("\nTest mentor endpoints? (y/n, default: n): ").strip().lower() == 'y'
    if test_mentor:
        mentor_results = test_mentor_endpoints()
        # Note: Not adding to total as they may fail with student role
    
    test_fw = input("Test floor wing endpoints? (y/n, default: n): ").strip().lower() == 'y'
    if test_fw:
        fw_results = test_floorwing_endpoints()
        # Note: Not adding to total as they may fail with student role
    
    # Print summary
    print_section("TEST SUMMARY")
    print(f"\n{GREEN}Passed: {total_results['passed']}{RESET}")
    print(f"{RED}Failed: {total_results['failed']}{RESET}")
    print(f"Total: {total_results['passed'] + total_results['failed']}")
    
    if total_results['failed'] == 0:
        print(f"\n{GREEN}✓ All gamification endpoints are working correctly!{RESET}")
    else:
        print(f"\n{RED}✗ Some endpoints failed. Please review the errors above.{RESET}")

if __name__ == "__main__":
    main()
