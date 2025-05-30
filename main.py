import mysql.connector
import os

connection = mysql.connector.connect(
    host = "HOST NAME HERE",
    user = "USER NAME HERE",
    password = "PASSWORD HERE",
    database = "DATABASE NAME HERE",
    auth_plugin='mysql_native_password'
)

cursor = connection.cursor()

tableName = "competitors"
fields = ["Competitor", "Number_of_games_played", "Number_of_wins", "Win_loss_ratio", "Last_played_commander"]

global session

print("""
             __    __     ______   ______        __    __     ______     __   __     ______     ______     ______     ______       
            /\\ "-./  \\   /\\__  _\\ /\\  ___\\      /\\ "-./  \\   /\\  __ \\   /\\ "-.\\ \\   /\\  __ \\   /\\  ___\\   /\\  ___\\   /\\  == \\      
            \\ \\ \\-./\\ \\ \\/_\\/\\ \\/ \\ \\ \\__  \\    \\ \\ \\-./\\ \\  \\ \\  __ \\  \\ \\ \\-.  \\  \\ \\  __ \\  \\ \\ \\__ \\  \\ \\  __\\   \\ \\  __<      
             \\ \\_\\ \\ \\_\\    \\ \\_\\  \\ \\_____\\     \\ \\_\\ \\ \\_\\  \\ \\_\\ \\_\\  \\ \\_\\\\"\\_\\  \\ \\_\\ \\_\\  \\ \\_____\\  \\ \\_____\\  \\ \\_\\ \\_\\    
              \\/_/  \\/_/     \\/_/   \\/_____/      \\/_/  \\/_/   \\/_/\\/__/  \\/_/ \\/_/   \\/_/\\/__/  \\/_____/   \\/_____/   \\/_/ /_/    
        """)
print("\n")

def register_player():
    print("\nEnter data for the following fields:")
    noGamesPlayed = 0
    noGamesWon = 0
    nameCheck = True
    values = []
    for field in fields:
        if field == "Number_of_games_played":
            value = input(f"{field}: ").strip()
            noGamesPlayed = int(value)
        elif field == "Number_of_wins":
            value = input(f"{field}: ").strip()
            noGamesWon = int(value)
        elif field == "Win_loss_ratio":
            if noGamesPlayed != noGamesWon:
                ratio = noGamesWon / (noGamesPlayed - noGamesWon)
                value = round(ratio, 2)
            else:
                value = 1
        elif field == "Last_played_commander":
            value = input(f"{field}: ").strip()
        else:
            value = input(f"{field}: ").strip()
            nameCheck = True
            cursor.execute(f"SELECT 1 FROM competitors WHERE Competitor = %s", (value,))
            if cursor.fetchone():
                print("Player already registered. Try updating their data.\n")
                nameCheck = False
                break
        values.append(value)

    placeholder = ', '.join(['%s'] * len(fields))
    fieldNames = ', '.join(fields)
    query = f"INSERT INTO {tableName} ({fieldNames}) VALUES ({placeholder})"

    try:
        if nameCheck:
            cursor.execute(query, values)
            connection.commit()
            print("\n")
            print(f"Data successfully inserted for new player.\n")
    except mysql.connector.Error as error:
        print(f"An error occurred: {error}\n")
        connection.rollback()


def update_player():
    player = input("Whose data do you want to update: ").strip().title()
    cursor.execute("SELECT * FROM competitors WHERE Competitor = %s", (player,))
    row = cursor.fetchone()
    values = []
    if row:
        print("\nEnter data for the following fields:")
        noGamesPlayed = 0
        noGamesWon = 0
        value = 0
        commander = 0
        ratio = 0
        newFields = ["Number_of_games_played", "Number_of_wins", "Win_loss_ratio", "Last_played_commander"]
        for field in newFields:
            if field == "Number_of_games_played":
                value = input(f"{field}: ").strip()
                noGamesPlayed = int(value)
            elif field == "Number_of_wins":
                value = input(f"{field}: ").strip()
                noGamesWon = int(value)
            elif field == "Last_played_commander":
                value = input(f"{field}: ").strip()
                values.append(value)
            else:
                if noGamesPlayed != noGamesWon:
                    ratio = noGamesWon / (noGamesPlayed - noGamesWon)
                    value = round(ratio, 2)
                    ratio = float(value)
                else:
                    value = 1
                    ratio = float(value)
            values.append(value)

        parameters = (noGamesPlayed, noGamesWon, ratio, value, player)
        query = f"UPDATE competitors SET Number_of_games_played	= %s, Number_of_wins = %s, Win_loss_ratio = %s, Last_played_commander = %s WHERE Competitor = %s"
        try:
            cursor.execute(query, parameters)
            connection.commit()
            print(f"Data successfully inserted for player {player}.\n")
        except mysql.connector.Error as error:
            print(f"An error occurred: {error}\n")
            connection.rollback()
    else:
        print("Player does not exist. Try registering them.\n")

def delete_player():
    player = input("Whose data do you want to delete: ").strip().title()
    cursor.execute("SELECT * FROM competitors WHERE Competitor = %s", (player,))
    row = cursor.fetchone()
    check = input("Are you sure you would like to delete these records? y/n\n")
    if row:
        while True:
            if check == "y":
                playerCheck = input(f"Type {player} to confirm\n")
                if playerCheck == player:
                    cursor.execute(f"DELETE FROM {tableName} WHERE Competitor = %s", (player,))
                    connection.commit()
                    print("Record successfully deleted\n")
                    break
                else:
                    confirm = input("Names don't match. Try again? y/n\n")
                    if confirm == "y":
                        continue
                    elif confirm == "n":
                        break
                    else:
                        print("Invalid input")
            elif check == "n":
                break
            else:
                print("Invalid input")
    else:
        print("Player does not exist.\n")

def view_all_records():
    try:
        print("\n")
        cursor.execute(f"SELECT * FROM {tableName}")
        rows = cursor.fetchall()
        print(f"{'Name':<20} {'Played':<7} {'Wins':<5} {'Win-Loss Ratio':<17} {'Last used commander'}")
        print("-" * 72)
        for row in rows:
            print(f"{row[0]:<20} {row[1]:<7} {row[2]:<5} {row[3]:<17} {row[4]}")
        print("\n")
    except mysql.connector.Error as error:
        print(f"An error occurred: {error}\n")
        connection.rollback()

def single_player():
    try:
        print("\n")
        player = input("Whose data do you want to view?\n")
        cursor.execute(f"SELECT * FROM {tableName} WHERE Competitor = '{player}'")
        rows = cursor.fetchall()
        print("\n")
        print(f"{'Name':<20} {'Played':<7} {'Wins':<5} {'Win-Loss Ratio':<17} {'Last used commander'}")
        print("-" * 72)
        for row in rows:
            print(f"{row[0]:<20} {row[1]:<7} {row[2]:<5} {row[3]:<17} {row[4]}")
        print("\n")
    except mysql.connector.Error as error:
        print(f"An error occurred: {error}\n")
        connection.rollback()


def quit():
    print("Bye!")
    return False

actionsList = {
    'r': register_player,
    'u': update_player,
    'd': delete_player,
    's': single_player,
    'v': view_all_records,
    'q': quit
}

def main():
    session = True
    while session:
        choice = input("""What would you like to do?
    
    - Register new player (r)
    - Update an existing player's data (u)
    - Delete a player's record (d)
    - View a single player's record (s)
    - View all records (v)
    - Exit (q)?\n""")
        if choice in actionsList:
            result = actionsList[choice]()
            if result is False:
                session = False
        else:
            print("Invalid input, please try again.\n")
            pass

if __name__ == "__main__":
    main()

