import os
DEBUG = True
# INSECURE KEY - only for testing
PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH", "public.pem")

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

