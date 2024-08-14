import os
from database.utils import create_tables
from dotenv import load_dotenv

load_dotenv()




DATABASE_URI = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def main():
    create_tables(database_uri=DATABASE_URI, echo=True)


if __name__ == "__main__":
    main()
