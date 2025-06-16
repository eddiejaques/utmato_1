from typing import Dict, List, Set, Tuple, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection, cursor
import os

# Load environment variables from .env file
load_dotenv()

class DatabaseConfig(BaseModel):
    """Database configuration model"""
    host: str = Field(..., description="Database host")
    port: str = Field(default="5432", description="Database port")
    name: str = Field(..., description="Database name")
    user: str = Field(..., description="Database user")
    password: str = Field(..., description="Database password")

class TableSchema(BaseModel):
    """Table schema model"""
    name: str
    columns: List[str]

class SchemaValidationResult(BaseModel):
    """Schema validation result model"""
    exists: bool
    missing_columns: Set[str]
    extra_columns: Set[str]

def get_db_config() -> DatabaseConfig:
    """Get database configuration from environment variables"""
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and ensure all required variables are set.")
        exit(1)
    
    return DatabaseConfig(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        name=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def get_required_tables() -> Dict[str, List[str]]:
    """Get required tables and their columns based on schema.sql"""
    return {
        'organizations': [
            'id', 'name', 'domain', 'subscription_id', 'subscription_status',
            'created_at', 'updated_at'
        ],
        'users': [
            'id', 'clerk_user_id', 'organization_id', 'email', 'role',
            'created_at', 'updated_at'
        ],
        'campaigns': [
            'id', 'organization_id', 'created_by_user_id', 'name', 'objective',
            'audience_details', 'created_at', 'updated_at'
        ],
        'links': [
            'id', 'campaign_id', 'created_by_user_id', 'destination_url',
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
            'full_url', 'created_at', 'updated_at'
        ],
        'invitations': [
            'id', 'organization_id', 'email', 'token', 'status',
            'expires_at', 'created_at'
        ]
    }

def check_table_structure(
    cur: cursor, 
    table_name: str, 
    expected_columns: List[str]
) -> SchemaValidationResult:
    """Check if a table has the expected structure"""
    # Check if table exists
    cur.execute("""
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
        )
    """, (table_name,))
    exists = cur.fetchone()[0]

    if not exists:
        return SchemaValidationResult(
            exists=False,
            missing_columns=set(expected_columns),
            extra_columns=set()
        )

    # Get actual columns
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = %s
    """, (table_name,))
    actual_columns = {row[0] for row in cur.fetchall()}
    
    return SchemaValidationResult(
        exists=True,
        missing_columns=set(expected_columns) - actual_columns,
        extra_columns=actual_columns - set(expected_columns)
    )

def validate_schema(conn: connection) -> bool:
    """Validate the database schema against requirements"""
    cur = conn.cursor()
    required_tables = get_required_tables()
    all_valid = True
    
    for table_name, expected_columns in required_tables.items():
        result = check_table_structure(cur, table_name, expected_columns)
        
        if result.exists:
            print(f"\n✅ Table '{table_name}' exists")
            
            if result.missing_columns:
                print(f"❌ Missing columns in '{table_name}': {', '.join(result.missing_columns)}")
                all_valid = False
                
            if result.extra_columns:
                print(f"ℹ️  Extra columns in '{table_name}' (not in schema): {', '.join(result.extra_columns)}")
        else:
            print(f"\n❌ Table '{table_name}' does not exist")
            all_valid = False
    
    return all_valid

def check_pgcrypto_extension(cur: cursor) -> bool:
    """Check if pgcrypto extension is enabled"""
    cur.execute("""
        SELECT EXISTS (
            SELECT 1 FROM pg_extension WHERE extname = 'pgcrypto'
        )
    """)
    return cur.fetchone()[0]

def check_rls_enabled(cur: cursor, table_names: List[str]) -> Dict[str, bool]:
    """Check if RLS is enabled for each table"""
    rls_status = {}
    cur.execute("""
        SELECT relname, relrowsecurity
        FROM pg_class
        WHERE relname = ANY(%s)
          AND relkind = 'r'
    """, (table_names,))
    for relname, relrowsecurity in cur.fetchall():
        rls_status[relname] = relrowsecurity
    # Mark missing tables as False
    for t in table_names:
        if t not in rls_status:
            rls_status[t] = False
    return rls_status

def main() -> None:
    """Main function to check database schema"""
    try:
        # Get database configuration
        config = get_db_config()
        print(f"Connecting to database {config.name} at {config.host}...")
        
        # Connect to database
        conn = psycopg2.connect(
            host=config.host,
            port=config.port,
            database=config.name,
            user=config.user,
            password=config.password
        )
        
        # Validate schema
        is_valid = validate_schema(conn)
        
        # Check pgcrypto extension
        cur = conn.cursor()
        has_pgcrypto = check_pgcrypto_extension(cur)
        if has_pgcrypto:
            print("\n✅ 'pgcrypto' extension is enabled.")
        else:
            print("\n❌ 'pgcrypto' extension is NOT enabled!")
            is_valid = False

        # Check RLS enabled for all required tables
        required_tables = list(get_required_tables().keys())
        rls_status = check_rls_enabled(cur, required_tables)
        for table, enabled in rls_status.items():
            if enabled:
                print(f"✅ RLS enabled for table '{table}'")
            else:
                print(f"❌ RLS NOT enabled for table '{table}'!")
                is_valid = False

        if is_valid:
            print("\n✅ All tables, columns, extension, and RLS match the required schema!")
        else:
            print("\n❌ Schema verification failed. Please check the issues above.")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main() 