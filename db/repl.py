from table import Table
from row import Row

table = Table("database.db")


def execute_insert(command):

    parts = command.split()

    id = int(parts[1])
    username = parts[2]

    row = Row(id, username)

    table.insert(row)

    print("Executed.")


def execute_select():

    cursor = table.start()

    while not cursor.end_of_table:

        id, username = cursor.value()

        print(id, username)

        cursor.advance()


def main():

    while True:

        command = input("db > ").strip()

        if command == ".exit":
            table.pager.close()
            print("Database closed.")
            break

        if command.startswith("insert"):
            execute_insert(command)

        elif command == "select":
            execute_select()

        elif command == ".pages":
            print(f"Number of pages: {table.num_pages}")


        else:
            print("Unknown command")


if __name__ == "__main__":
    main()