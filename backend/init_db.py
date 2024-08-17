from dotenv import load_dotenv
from database.utils import create_tables, database_url

load_dotenv()


DATABASE_URI = database_url()


def main():
    create_tables(database_uri=DATABASE_URI, echo=True)


if __name__ == "__main__":
    main()
