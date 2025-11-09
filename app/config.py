from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict, ValidationError
import sys


class Settings(BaseSettings):
    database_user: str = Field(..., description="Database username")
    database_password: str = Field(..., description="Database password")
    database_host: str = Field(..., description="Database host")
    database_port: int = Field(..., description="Database port")
    database_name: str = Field(..., description="Database name")
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def database_url(self) -> str:
        """Generate database URL from individual components"""
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"


def load_settings() -> Settings:
    """Load settings with proper error handling"""
    try:
        return Settings()
    except ValidationError as e:
        missing_fields = []
        for error in e.errors():
            if error['type'] == 'missing':
                field_name = error['loc'][0]
                env_var_name = field_name.upper()
                missing_fields.append(env_var_name)
        
        error_message = f"""
╔════════════════════════════════════════════════════════════════════╗
║                   CONFIGURATION ERROR                              ║
╚════════════════════════════════════════════════════════════════════╝

Missing required environment variables in .env file:
{chr(10).join(f'  ❌ {field}' for field in missing_fields)}

Please create a .env file in the project root with the following variables:

DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_database

Example .env file:
──────────────────────────────────────────────────────────────────
DATABASE_USER=iot_user
DATABASE_PASSWORD=*****
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=iot_sensors
──────────────────────────────────────────────────────────────────
"""
        print(error_message, file=sys.stderr)
        sys.exit(1)


settings = load_settings()