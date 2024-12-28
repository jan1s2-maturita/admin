import os
DEBUG = True
# INSECURE KEY - only for testing
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY", "private.pem")
PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY", "public.pem")

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

