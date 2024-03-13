import time
import threading
from rich import print # Rich printing (colours, bolding, etc.)
from . import format # Game constants
from . import screen # Screen clearing etc.
from . import parcel_selection # Selection logic
from . import parcel_delivery # Delivery logic
from . import parcel_results # End screen logic
from . import database


# Gameplay loop
def game_loop(player_list):
    random_parcels = database.fetch_10_random_parcels_from_db()
    random_airports = database.fetch_10_random_airports_from_db()
    game_parcel_list = parcel_selection.list_generate(random_parcels, random_airports) # Generate parcel options for current game.

    # 1: Player chooses their 5 parcels.
    for player in player_list:
        screen.new()
        print(f"""[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][PAKETIN VALINTA][/italic #FF7F50]
[#6A5ACD]•[/#6A5ACD] Pelaajan [bold blue]{player["name"]}[/bold blue] vuoro valita pakettinsa! 
[#6A5ACD]•[/#6A5ACD] Sinulla on {format.parcel_selection_time_limit} sekuntia aikaa valita vapaasti viisi (5) pakettia tulevasta listasta.
  Jos aikasi loppuu kesken, [bold red]häviät![/bold red]

[yellow]*[/yellow] Paina [green]ENTER[/green] aloittaaksesi vuorosi [yellow]*[/yellow]
""")
        input()
        screen.new()

        player["parcels_picked"] = parcel_selection.list_select(game_parcel_list)

        if len(player["parcels_picked"]) != 5:
            screen.new()
            player["gameover"] = True
            print("\n\t   [red]Voi ei![/red]")
            print("[red]\tAikasi loppui![/red]\n")
            print("Paina [green]ENTER[/green] siirtyäksesi eteenpäin.")
            input()

    # 2: Players deliver their parcels.
    for player in player_list:
        if player["gameover"] != True:
            screen.new()
            format.parcel_delivery_time_limit = format.actual_parcel_delivery_time_limit
            print(f"""[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][PAKETIN KULJETUS][/italic #FF7F50]
[#6A5ACD]•[/#6A5ACD] Pelaajan [bold blue]{player["name"]}[/bold blue] vuoro kuljettaa pakettinsa! 
[#6A5ACD]•[/#6A5ACD] Sinulla on {format.parcel_delivery_time_limit} sekuntia aikaa kuljettaa kaikki pakettisi.
  Jos aikasi loppuu kesken, [bold red]häviät![/bold red]

[yellow]*[/yellow] Paina [green]ENTER[/green] aloittaaksesi vuorosi [yellow]*[/yellow]
""")
            input()
            player_co2, player_co2_add = 0, 0
            # Start timer
            start_time = time.time()
            while len(player["parcels_picked"]) != len(player["parcels_delivered"]) and parcel_delivery.is_there_time_left(start_time,format.parcel_delivery_time_limit):
                screen.new()
                # Player chooses parcel to deliver
                time_left = parcel_delivery.how_much_time_is_left(start_time, format.parcel_delivery_time_limit)
                screen.feedback("time", time_left)
                if parcel_delivery.is_there_time_left(start_time, format.parcel_delivery_time_limit):
                    parcel_selected = parcel_delivery.select_delivery(player)
                    player["parcels_delivered"].append(player["parcels_picked"][parcel_selected])

                # Player chooses delivery method
                screen.new()
                time_left = parcel_delivery.how_much_time_is_left(start_time, format.parcel_delivery_time_limit)
                screen.feedback("time", time_left)
                if parcel_delivery.is_there_time_left(start_time, format.parcel_delivery_time_limit):
                    player_co2_add, time_lost = parcel_delivery.select_delivery_method(parcel_selected, player,start_time)
                    format.parcel_delivery_time_limit -= time_lost

                player["location"] = [player["parcels_picked"][parcel_selected].get("latitude"), player["parcels_picked"][parcel_selected].get("longitude")]

                # Tally co2 emissions
                player_co2 = player["co2"]
                player["co2"] = player_co2 + player_co2_add

            if not parcel_delivery.is_there_time_left(start_time, format.parcel_delivery_time_limit):
                screen.new()
                player["gameover"] = True
                print("\n\t   [red]Voi ei![/red]")
                print("[red]\tAikasi loppui![/red]\n")
                print("Paina [green]ENTER[/green] siirtyäksesi eteenpäin.")
                input()

            if player["co2"] != 0:
                score = int(((1/player["co2"]) * 1000000) * 1000)
            else:
                score = 0

            if not player["gameover"]:
                player["score"] = score


    # 3: Players are shown the scoreboard
    database.insert_new_player_scores_in_to_db(player_list)
    screen.new()
    parcel_results.show_end_screen(player_list)

# Startup sequence
def intro():
    screen.clear()
    print(f"[yellow]Haluatko katsoa intron ([/yellow][bright_green]K[/bright_green][yellow]/[/yellow][bright_red]E[/bright_red][yellow])?[/yellow] [blink italic red](Saattaa sisältää välkkyviä valoja)[/blink italic red]")
    user_input = input(">> ")
    while user_input.lower() not in ["k","e"]:
        screen.clear()
        print(f"[ Virheellinen syöte: [red]\"{user_input}\"[/red] ! ]")
        print(f"[yellow]Haluatko katsoa intron ([/yellow][bright_green]K[/bright_green][yellow]/[/yellow][bright_red]E[/bright_red][yellow])?[/yellow] [blink italic red](Saattaa sisältää välkkyviä valoja)[/blink italic red]")
        user_input = input(">> ")

    if user_input == "k":

        intro_line1 = "                                                                                                                                                                   __  _                                                                                                                                  "
        intro_line2 = "                                                                                                                                                                   \ `/ |                                                                                                                                 "
        intro_line3 = "                                                                                                                                                                    \__`!                                                                                                                                 "
        intro_line4 = "██████╗  █████╗ ██╗  ██╗███████╗████████╗████████╗██╗██████╗ ██╗██╗      ██████╗ ████████╗████████╗██╗                                                              / ,' `-.__________________                                                                                                            "
        intro_line5 = "██╔══██╗██╔══██╗██║ ██╔╝██╔════╝╚══██╔══╝╚══██╔══╝██║██╔══██╗██║██║     ██╔═══██╗╚══██╔══╝╚══██╔══╝██║_____________________________________________________________'-'\_____                LI`-.                                                                                                         "
        intro_line6 = "██████╔╝███████║█████╔╝ █████╗     ██║      ██║   ██║██████╔╝██║██║     ██║   ██║   ██║      ██║   ██║                                                                <____()-=O=O=O=O=O=[]====--)                                                                                                        "
        intro_line7 = "██╔═══╝ ██╔══██║██╔═██╗ ██╔══╝     ██║      ██║   ██║██╔═══╝ ██║██║     ██║   ██║   ██║      ██║   ██║__________________________________________________________________`.___ ,-----,_______...-'                                                                                                         "
        intro_line8 = "██║     ██║  ██║██║  ██╗███████╗   ██║      ██║   ██║██║     ██║███████╗╚██████╔╝   ██║      ██║   ██║                                                                       /    .'                                                                                                                      "
        intro_line9 = "╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝ ╚═════╝    ╚═╝      ╚═╝   ╚═╝                                                                      /   .'                                                                                                                        "
        intro_line10 ="                                                                                                                                                                           /  .'                                                                                                                          "
        intro_line11 ="                                                                                                                                                                           `-'                                                                                                                            "
        list_of_intro_lines = [intro_line1, intro_line2, intro_line3, intro_line4, intro_line5, intro_line6, intro_line7,
                               intro_line8, intro_line9, intro_line10, intro_line11]

        i = 0
        for frame in range(len(intro_line6)-102):
            screen.clear()
            for row in list_of_intro_lines:
                print(f"[#fffefe]{row[-103-i:-1-i]}[/#fffefe]")
            time.sleep(0.05)
            i += 1
        time.sleep(1)

        start_colors = ["#fffefe","#fffefe","#fffefe","#fffefe","#fffefe","#fffefe","#fffefe","#fffefe","#fffefe","#fffefe","#fffefe","#fffefe","#fffefe","#fffefe","#fffefe"]
        end_colors = ["#ff355e","#fd5b78","#ff6037","#ff9966","#ff9933","#ffcc33","#ffff66","#ccff00","#66ff66","#aaf0d1","#50bfe6","#ff6eff","#ee34d2","#ff00cc","#ff00cc"]
        for frame in range(len(range(15))):
            screen.clear()
            for row in list_of_intro_lines:
                print(f"[{start_colors[0]}]{row[0:8]}[/{start_colors[0]}][{start_colors[1]}]{row[8:16]}[/{start_colors[1]}][{start_colors[2]}]{row[16:24]}[/{start_colors[2]}][{start_colors[3]}]{row[24:32]}[/{start_colors[3]}][{start_colors[4]}]{row[32:41]}[/{start_colors[4]}][{start_colors[5]}]{row[41:50]}[/{start_colors[5]}][{start_colors[6]}]{row[50:53]}[/{start_colors[6]}][{start_colors[7]}]{row[53:61]}[/{start_colors[7]}][{start_colors[8]}]{row[61:64]}[/{start_colors[8]}][{start_colors[9]}]{row[64:72]}[/{start_colors[9]}][{start_colors[10]}]{row[72:81]}[/{start_colors[10]}][{start_colors[11]}]{row[81:90]}[/{start_colors[11]}][{start_colors[12]}]{row[90:99]}[/{start_colors[12]}][{start_colors[13]}]{row[99:102]}[/{start_colors[13]}]")
            start_colors[frame] = end_colors[frame]
            time.sleep(0.4)

        time.sleep(3)


# Exit sequence
def outro():
    fading_color_list1 = ["#ababab", "#929493", "#7e807f", "#6d6e6d", "#575757", "#3f403f", "#2b2b2b", "#1b1c1c"]
    fading_color_list2 = ["#3CB371", "#31945d", "#257347", "#1f613c", "#194f30", "#113822", "#0a2114", "#07170e"]
    for i in range(len(fading_color_list1)):
        screen.clear()
        print(f"""[{fading_color_list1[i]}]Kiitos kun pelasit![{fading_color_list1[i]}][{fading_color_list2[i]}]
     _   _  _   _  _                     _  _         _ 
    | \ | |(_) (_)| |                   (_)(_)       | |
    |  \| |  __ _ | | __ ___  _ __ ___   _  _  _ __  | |
    | . ` | / _` || |/ // _ \| '_ ` _ \ | || || '_ \ | |
    | |\  || (_| ||   <|  __/| | | | | || || || | | ||_|
    |_| \_| \__,_||_|\_|\___||_| |_| |_||_||_||_| |_|(_)
    [/{fading_color_list2[i]}]""")
        if i == 0:
            time.sleep(1.5)
        else:
            time.sleep(0.4)

    screen.clear() # Return user to clean terminal


# Start menu
def menu():
    screen.new()
    option = False

    while option != "4":
        print(f"""[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][ALKUVALIKKO][/italic #FF7F50]
[#6A5ACD]•[/#6A5ACD] [bold blue]1:[/bold blue] Ohje
[#6A5ACD]•[/#6A5ACD] [bold blue]2:[/bold blue] Uusi peli
[#6A5ACD]•[/#6A5ACD] [bold blue]3:[/bold blue] Pistetaulukko
[#6A5ACD]•[/#6A5ACD] [bold blue]4:[/bold blue] EXIT
""")
        option = input(">> ")
        if option == "1":
            menu_help()
            screen.new()
        elif option == "2":
            menu_newgame()
            screen.new()
        elif option == "3":
            menu_hiscore()
            screen.new()
        else: # If the user input other than predefined, throw error in feedback box.
            screen.feedback(option, "error")


# Begin a new game
def menu_newgame():
    screen.new()
    option = False
    player_list = list()
    
    while option != "4":
        if player_list != []:
            print(f"""[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][ALKUVALIKKO / UUSI PELI][/italic #FF7F50]
[#6A5ACD]•[/#6A5ACD] [bold blue]1:[/bold blue] Lisää uusi pelaaja
[#6A5ACD]•[/#6A5ACD] [bold blue]2:[/bold blue] Aloita peli
[#6A5ACD]•[/#6A5ACD] [bold blue]3:[/bold blue] Poista pelaaja
[#6A5ACD]•[/#6A5ACD] [bold blue]4:[/bold blue] Palaa alkuvalikkoon

[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][PELAAJAT][/italic #FF7F50]""")
            for player in player_list:
                print(f"[#6A5ACD]•[/#6A5ACD] [bold blue]{player['name']}[/bold blue]")
        if player_list == []:
            print(f"""[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][ALKUVALIKKO / UUSI PELI][/italic #FF7F50]
[#6A5ACD]•[/#6A5ACD] [bold blue]1:[/bold blue] Lisää uusi pelaaja
[#6A5ACD]•[/#6A5ACD] [bold blue]2:[/bold blue] Aloita peli
[#6A5ACD]•[/#6A5ACD] [bold blue]4:[/bold blue] Palaa alkuvalikkoon

[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][PELAAJAT][/italic #FF7F50]""")
        
        option = input("\n>> ")
        if option == "1": # Add player
            player_name = input(">> Syötä pelaajan nimi (max. 13 merkkiä): ")
            player_in_list = False
            
            for player in player_list:
                if player.get("name") == player_name:
                    player_in_list = True
            
            if player_in_list:
                screen.new()
                screen.feedback(player_name, "Nimimerkki on jo käytössä!")
            elif len(player_name) > 13:
                screen.new()
                screen.feedback(player_name, "Nimimerkki on liian pitkä!")
            else:
                player_new = format.player_structure(player_name) # Use player dict() structure from format.py
                player_list.append(player_new) # Add new player to next game participants
                screen.new()
                screen.feedback(player_name, "Pelaaja lisätty!")

        elif option == "2": # Start game
            if player_list == []:
                screen.new()
                screen.feedback("Not enought players","Et voi aloittaa peliä lisäämättä vähintään yhtä pelaajaa!")
            else:
                screen.new()
                game_loop(player_list)
                break # Return to main menu
        
        elif option == "3": # Remove player
            if player_list == []:
                screen.new()
                screen.feedback(option, "error")
            else: 
                player_remove = input(">> Poista pelaaja: ")
                for player in player_list:
                    if player.get("name") == player_remove: # If player present
                        player_list.remove(player)
                        screen.new()
                        screen.feedback(player_remove, "Pelaaja poistettu!")
                    else:
                        screen.feedback(player_remove, "error")
        elif option == "4":
            screen.new()
        else: # If the user input other than predefined, throw error in feedback box.
            screen.new()
            screen.feedback(option, "error")
    
    player_list = list() # Reset player_list if the user leaves newgame menu.


# Display help
def menu_help():
    screen.new()
    option = False
    while option == False:
        print(f"""[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][ALKUVALIKKO / OHJE][/italic #FF7F50]
[#6A5ACD]•[/#6A5ACD] Pelin tavoitteena on toimittaa kaikki pelivuoron alussa
  valitut paketit niiden kohteeseen, ennen määräajan loppumista.
[#6A5ACD]•[/#6A5ACD] Peliä voi pelata kerrallaan yksi tai useampi henkilö.
[#6A5ACD]•[/#6A5ACD] Suoritus pisteytetään pelaajan hiilidioksidipäästöjen mukaan.
  Päästöjen suuruuteen vaikuttaa: [yellow]tavaranimikkeen tyyppi[/yellow], [yellow]kuljettu matka[/yellow] ja [yellow]kuljetusmuoto[/yellow].

[yellow]*[/yellow] Paina [green]ENTER[/green] palataksesi alkuvalikkoon [yellow]*[/yellow]
""")
        option = input()


# Display hiscores
def menu_hiscore():
    screen.new()

    players_with_highest_scores = database.fetch_player_highscores_from_db(10)
    #players_with_highest_scores = [(1,"Kek",4000),(1,"Bob",12000),(2,"Bill",5400),(3,"Steve",30),(3,"ABC",1),(4,"ACDC",4430),(5,"Riikinkukkoko",460),(6,"Vaahtokarkki",60),(6,"Kaakao",10000),(6,"Teemu",9001)]

    if len(players_with_highest_scores) != 0:
        i = 1
        player_colors = ["bold #FFD700", "bold #C0C0C0", "bold #CD7F32", "#9c9c9c", "#9c9c9c", "#9c9c9c", "#9c9c9c",
                         "#9c9c9c", "#9c9c9c", "#9c9c9c"]
        print(f"[italic #FF7F50]Sija. \t Nimi. \t\t Pistemäärä. \t Pelinnumero.[/italic #FF7F50]")
        for player in players_with_highest_scores:
            if len(player[1]) > 5:
                print(
                    f"[{player_colors[i - 1]}]{i} \t {player[1]} \t {player[2]} \t\t {player[0]}[/{player_colors[i - 1]}]")
            else:
                print(
                    f"[{player_colors[i - 1]}]{i} \t {player[1]} \t\t {player[2]} \t\t {player[0]}[/{player_colors[i - 1]}]")
            i += 1
    else:
        print("\n[red]Pistetaulukko on tyhjä![/red]")
        print("\n[yellow]Olisiko aika täydentää sitä?[/yellow] [green];)[/green]")

    print("\n[yellow]*[/yellow] Paina [green]ENTER[/green] palataksesi alkuvalikkoon [yellow]*[/yellow]")
    input()
