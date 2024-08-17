from api.main import main
from database.utils import check_migrations


if __name__ == "__main__":
    check_migrations()
    main()
