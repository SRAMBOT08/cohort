#!/bin/bash
# =============================================================================
# Supabase Migration Script
# =============================================================================
# This script helps you migrate your Django application to Supabase PostgreSQL
# 
# Usage:
#   ./migrate_to_supabase.sh [option]
#
# Options:
#   test      - Test Supabase connection
#   backup    - Backup current database (if using PostgreSQL)
#   migrate   - Run Django migrations on Supabase
#   full      - Full migration (backup + migrate + verify)
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_error ".env file not found!"
        print_info "Create .env file from .env.example"
        print_info "cp .env.example .env"
        exit 1
    fi
}

# Check if DATABASE_URL is set
check_database_url() {
    if grep -q "^DATABASE_URL=postgresql://" .env; then
        print_success "DATABASE_URL configured"
    else
        print_error "DATABASE_URL not configured in .env"
        print_info "Add your Supabase connection string to .env:"
        print_info "DATABASE_URL=postgresql://postgres.[ref]:[pass]@aws-0-[region].pooler.supabase.com:6543/postgres"
        exit 1
    fi
}

# Test Supabase connection
test_connection() {
    print_header "Testing Supabase Connection"
    
    if [ -f test_supabase_connection.py ]; then
        python3 test_supabase_connection.py
    else
        print_warning "test_supabase_connection.py not found, using Django check"
        python3 manage.py check --database default
    fi
}

# Backup current database
backup_database() {
    print_header "Backing Up Current Database"
    
    # Check if we have a local database to backup
    if [ -f db.sqlite3 ]; then
        print_info "Backing up SQLite database..."
        timestamp=$(date +%Y%m%d_%H%M%S)
        cp db.sqlite3 "db.sqlite3.backup_${timestamp}"
        print_success "SQLite backed up to db.sqlite3.backup_${timestamp}"
        
        # Export data to JSON
        print_info "Exporting data to JSON..."
        python3 manage.py dumpdata \
            --natural-foreign \
            --natural-primary \
            --exclude contenttypes \
            --exclude auth.permission \
            --indent 2 \
            > "backup_data_${timestamp}.json"
        print_success "Data exported to backup_data_${timestamp}.json"
    else
        print_warning "No local SQLite database found"
    fi
}

# Run migrations on Supabase
run_migrations() {
    print_header "Running Migrations on Supabase"
    
    print_info "Checking for pending migrations..."
    python3 manage.py showmigrations
    
    print_info "Running migrations..."
    python3 manage.py migrate --noinput
    
    print_success "Migrations completed!"
}

# Create superuser
create_superuser() {
    print_header "Create Superuser"
    
    print_info "Creating superuser for admin access..."
    print_warning "You'll be prompted for username, email, and password"
    
    python3 manage.py createsuperuser
}

# Collect static files
collect_static() {
    print_header "Collecting Static Files"
    
    print_info "Collecting static files..."
    python3 manage.py collectstatic --noinput
    
    print_success "Static files collected!"
}

# Verify migration
verify_migration() {
    print_header "Verifying Migration"
    
    print_info "Checking database connection..."
    python3 manage.py check --database default
    
    print_info "Listing tables..."
    python3 manage.py dbshell << EOF
\dt
\q
EOF
    
    print_success "Verification complete!"
}

# Load backup data
load_backup_data() {
    print_header "Loading Backup Data"
    
    # Find latest backup file
    latest_backup=$(ls -t backup_data_*.json 2>/dev/null | head -1)
    
    if [ -n "$latest_backup" ]; then
        print_info "Found backup: $latest_backup"
        read -p "Load this backup into Supabase? (y/N): " confirm
        
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            python3 manage.py loaddata "$latest_backup"
            print_success "Data loaded successfully!"
        else
            print_warning "Backup loading skipped"
        fi
    else
        print_warning "No backup files found"
    fi
}

# Full migration process
full_migration() {
    print_header "Full Migration to Supabase"
    
    # Step 1: Check environment
    check_env_file
    check_database_url
    
    # Step 2: Test connection
    test_connection
    
    # Step 3: Backup current data
    read -p "Backup current database? (Y/n): " backup_confirm
    if [ "$backup_confirm" != "n" ] && [ "$backup_confirm" != "N" ]; then
        backup_database
    fi
    
    # Step 4: Run migrations
    print_info "Ready to migrate to Supabase..."
    read -p "Continue with migration? (Y/n): " migrate_confirm
    if [ "$migrate_confirm" != "n" ] && [ "$migrate_confirm" != "N" ]; then
        run_migrations
    else
        print_warning "Migration cancelled"
        exit 0
    fi
    
    # Step 5: Load backup data (optional)
    load_backup_data
    
    # Step 6: Create superuser
    read -p "Create superuser? (Y/n): " superuser_confirm
    if [ "$superuser_confirm" != "n" ] && [ "$superuser_confirm" != "N" ]; then
        create_superuser
    fi
    
    # Step 7: Collect static files
    read -p "Collect static files? (Y/n): " static_confirm
    if [ "$static_confirm" != "n" ] && [ "$static_confirm" != "N" ]; then
        collect_static
    fi
    
    # Step 8: Verify
    verify_migration
    
    print_header "Migration Complete!"
    print_success "Your application is now using Supabase PostgreSQL"
    print_info "Next steps:"
    print_info "  1. Test your application locally: python3 manage.py runserver"
    print_info "  2. Deploy to your hosting platform"
    print_info "  3. Update your frontend VITE_API_BASE_URL"
}

# Main script
main() {
    cd "$(dirname "$0")"  # Change to backend directory
    
    case "${1:-}" in
        test)
            check_env_file
            check_database_url
            test_connection
            ;;
        backup)
            check_env_file
            backup_database
            ;;
        migrate)
            check_env_file
            check_database_url
            run_migrations
            ;;
        full)
            full_migration
            ;;
        *)
            print_header "Supabase Migration Script"
            echo "Usage: $0 [option]"
            echo ""
            echo "Options:"
            echo "  test      - Test Supabase connection"
            echo "  backup    - Backup current database"
            echo "  migrate   - Run Django migrations on Supabase"
            echo "  full      - Full migration (recommended)"
            echo ""
            echo "Examples:"
            echo "  $0 test              # Test connection"
            echo "  $0 full              # Full migration with prompts"
            exit 1
            ;;
    esac
}

main "$@"
