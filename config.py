"""
Configuration manager for StrongHold.
Loads all settings from .env and provides them as a single source of truth
for every sensor and module in the project.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Central configuration class for StrongHold.
    """

    # ============ DATABASE ============
    DB_CONFIG: Dict[str, Any] = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASS', ''),
        'database': os.getenv('DB_NAME', 'stronghold'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'autocommit': True,
        'connect_timeout': 5,
        'charset': 'utf8mb4'
    }

    @classmethod
    def validate(cls) -> None:
        """
        Validate that required configuration values are present.
        Raises ValueError if something critical is missing.
        """
        required = ['DB_HOST', 'DB_USER', 'DB_PASS', 'DB_NAME']
        missing = [r for r in required if not os.getenv(r)]

        if missing:
            raise ValueError(
                f" Missing required configuration in .env file: {', '.join(missing)}\n"
                f"Please create a .env file with these values (see .env.example)."
            )

        print(" Configuration loaded successfully!")
        print(f"   - Database: {cls.DB_CONFIG['host']}:{cls.DB_CONFIG['port']} / {cls.DB_CONFIG['database']}")

    @classmethod
    def get_db_connection_params(cls) -> Dict[str, Any]:
        """
        Returns database connection parameters for PyMySQL.
        """
        return cls.DB_CONFIG.copy()


# ============ QUICK TEST (optional) ============
if __name__ == "__main__":
    try:
        Config.validate()
    except ValueError as e:
        print(e)
