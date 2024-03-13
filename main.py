import game.database as database
import game.logic as game


def main():
    err = database.create_database_connection()
    if err:
        print(f"Error occurred while creating new database connection: {err}")
    else:
        print("Database connection established.")
        # start the app
        database.create_database_connection()
        game.intro()
        game.menu()
        game.outro()


if __name__ == "__main__":
    main()

