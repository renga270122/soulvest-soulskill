"""
Database Configuration for SoulSkill Resume Builder
Supports PostgreSQL, MySQL, and MongoDB
"""
import os
from typing import Optional, Dict, List
import json
from datetime import datetime

# Database connection settings
DATABASE_CONFIG = {
    'postgres': {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
        'database': os.getenv('POSTGRES_DB', 'soulskill_db'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', ''),
    },
    'mongodb': {
        'uri': os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'),
        'database': os.getenv('MONGODB_DB', 'soulskill_db'),
    }
}

class DatabaseManager:
    """Abstract database manager supporting multiple backends"""
    
    def __init__(self, db_type: str = 'json'):
        """
        Initialize database manager
        
        Args:
            db_type: 'postgres', 'mongodb', or 'json' (default)
        """
        self.db_type = db_type
        self.connection = None
        
        if db_type == 'postgres':
            self._init_postgres()
        elif db_type == 'mongodb':
            self._init_mongodb()
        else:
            self._init_json()
    
    def _init_postgres(self):
        """Initialize PostgreSQL connection"""
        try:
            import psycopg2
            config = DATABASE_CONFIG['postgres']
            self.connection = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                database=config['database'],
                user=config['user'],
                password=config['password']
            )
            self._create_postgres_tables()
        except ImportError:
            print("⚠️ psycopg2 not installed. Install with: pip install psycopg2-binary")
            self._init_json()  # Fallback to JSON
        except Exception as e:
            print(f"⚠️ PostgreSQL connection failed: {e}. Falling back to JSON storage.")
            self._init_json()
    
    def _init_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            from pymongo import MongoClient
            config = DATABASE_CONFIG['mongodb']
            self.connection = MongoClient(config['uri'])
            self.db = self.connection[config['database']]
            self.resumes = self.db.resumes
            self.users = self.db.users
            self.analytics = self.db.analytics
        except ImportError:
            print("⚠️ pymongo not installed. Install with: pip install pymongo")
            self._init_json()
        except Exception as e:
            print(f"⚠️ MongoDB connection failed: {e}. Falling back to JSON storage.")
            self._init_json()
    
    def _init_json(self):
        """Initialize JSON file storage (default fallback)"""
        self.db_type = 'json'
        self.json_file = 'soulskill_database.json'
        
        # Create file if not exists
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as f:
                json.dump({
                    'resumes': [],
                    'users': [],
                    'analytics': []
                }, f)
    
    def _create_postgres_tables(self):
        """Create PostgreSQL tables if they don't exist"""
        cursor = self.connection.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                subscription_tier VARCHAR(50) DEFAULT 'free'
            )
        """)
        
        # Resumes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                title VARCHAR(255),
                content JSONB NOT NULL,
                template_name VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_public BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Analytics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                event_type VARCHAR(100),
                event_data JSONB,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
        cursor.close()
    
    def save_resume(self, user_email: str, resume_data: Dict) -> str:
        """Save resume to database"""
        resume_data['updated_at'] = datetime.now().isoformat()
        
        if self.db_type == 'postgres':
            return self._save_resume_postgres(user_email, resume_data)
        elif self.db_type == 'mongodb':
            return self._save_resume_mongodb(user_email, resume_data)
        else:
            return self._save_resume_json(user_email, resume_data)
    
    def _save_resume_postgres(self, user_email: str, resume_data: Dict) -> str:
        """Save to PostgreSQL"""
        cursor = self.connection.cursor()
        
        # Get or create user
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]
        else:
            cursor.execute(
                "INSERT INTO users (email, name) VALUES (%s, %s) RETURNING id",
                (user_email, resume_data.get('full_name', ''))
            )
            user_id = cursor.fetchone()[0]
        
        # Save resume
        cursor.execute(
            """INSERT INTO resumes (user_id, title, content, template_name, updated_at)
               VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
               RETURNING id""",
            (user_id, resume_data.get('full_name', 'My Resume'), 
             json.dumps(resume_data), resume_data.get('selected_template', ''))
        )
        resume_id = cursor.fetchone()[0]
        
        self.connection.commit()
        cursor.close()
        return str(resume_id)
    
    def _save_resume_mongodb(self, user_email: str, resume_data: Dict) -> str:
        """Save to MongoDB"""
        resume_data['user_email'] = user_email
        resume_data['created_at'] = datetime.now()
        
        result = self.resumes.insert_one(resume_data)
        return str(result.inserted_id)
    
    def _save_resume_json(self, user_email: str, resume_data: Dict) -> str:
        """Save to JSON file"""
        with open(self.json_file, 'r') as f:
            data = json.load(f)
        
        resume_data['user_email'] = user_email
        resume_data['id'] = len(data['resumes']) + 1
        data['resumes'].append(resume_data)
        
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(resume_data['id'])
    
    def get_user_resumes(self, user_email: str) -> List[Dict]:
        """Get all resumes for a user"""
        if self.db_type == 'postgres':
            return self._get_resumes_postgres(user_email)
        elif self.db_type == 'mongodb':
            return self._get_resumes_mongodb(user_email)
        else:
            return self._get_resumes_json(user_email)
    
    def _get_resumes_postgres(self, user_email: str) -> List[Dict]:
        """Get from PostgreSQL"""
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT r.id, r.content, r.created_at, r.updated_at
               FROM resumes r
               JOIN users u ON r.user_id = u.id
               WHERE u.email = %s
               ORDER BY r.updated_at DESC""",
            (user_email,)
        )
        
        resumes = []
        for row in cursor.fetchall():
            resumes.append({
                'id': row[0],
                'data': row[1],
                'created_at': row[2].isoformat(),
                'updated_at': row[3].isoformat()
            })
        
        cursor.close()
        return resumes
    
    def _get_resumes_mongodb(self, user_email: str) -> List[Dict]:
        """Get from MongoDB"""
        resumes = list(self.resumes.find({'user_email': user_email}))
        for resume in resumes:
            resume['id'] = str(resume['_id'])
            del resume['_id']
        return resumes
    
    def _get_resumes_json(self, user_email: str) -> List[Dict]:
        """Get from JSON file"""
        with open(self.json_file, 'r') as f:
            data = json.load(f)
        
        return [r for r in data['resumes'] if r.get('user_email') == user_email]
    
    def log_analytics(self, event_type: str, event_data: Dict, user_email: Optional[str] = None):
        """Log analytics event"""
        event = {
            'event_type': event_type,
            'event_data': event_data,
            'timestamp': datetime.now().isoformat(),
            'user_email': user_email
        }
        
        if self.db_type == 'mongodb':
            self.analytics.insert_one(event)
        elif self.db_type == 'json':
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            data['analytics'].append(event)
            with open(self.json_file, 'w') as f:
                json.dump(data, f, indent=2)
    
    def close(self):
        """Close database connection"""
        if self.connection and self.db_type == 'postgres':
            self.connection.close()
        elif self.connection and self.db_type == 'mongodb':
            self.connection.close()


# Global database instance
db_manager = None

def get_db_manager() -> DatabaseManager:
    """Get or create database manager singleton"""
    global db_manager
    if db_manager is None:
        db_type = os.getenv('DATABASE_TYPE', 'json')
        db_manager = DatabaseManager(db_type)
    return db_manager
