# Parcel Selection Logic
import random
import time
from rich import print
from . import format
from . import screen
from . import parcel_delivery


# Define heft_classes from format.py
heft_classes = format.heft_classes


def list_generate(parcels_list, airports_list):
    """
    Takes: 1. parcels list, 2. airports list.
    Combines inputs into a single list as structured dictionaries, and returns it.
    
    { item, co2_item, heft, info, destination_airport, destination_country, latitude, longitude }
    """

    combined_list = []

    for i in range(len(parcels_list)):
        # Attribute a random weight for the item, based on its heft type.
        random_weight = float(f"{random.uniform(heft_classes.get(parcels_list[i][2])[0],heft_classes.get(parcels_list[i][2])[1]):.2f}")

        # Combine into single list
        combined_list.append({"item": parcels_list[i][0],"co2_item": parcels_list[i][1],
        "heft": random_weight,"info": parcels_list[i][3],"destination_airport": airports_list[i][0],
        "destination_country": airports_list[i][1], "latitude": airports_list[i][2],"longitude": airports_list[i][3]})

    return combined_list # Return the combined list


def list_print(game_parcel_list, options_list):
    """
    Print the game_parcel_list to the player,
    so they can choose their parcels.
    """
    
    i = 1 # Start counting from 1, so the menu indexes run from 1-10 (displayed to player).
    
    print(f"[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][PAKETIN VALINTA][/italic #FF7F50]\n")    
    print("[#C39BD3]// Valitse seuraavasta kymmenestä vaihtoehdosta viisi:[/#C39BD3]")
    for item in game_parcel_list:
        item_info = item.get('info')

        j = 106
        while True:
            if j >= len(item_info):
                break
            elif item_info[j] == " ":
                break
            j += 1
        item_info_part_1 = item_info[:j]
        item_info_part_2 = item_info[j+1:]

        if str(i) in options_list:
            print(f"[#C39BD3]•[/#C39BD3] [[yellow]{i}[/yellow]]: [bright_yellow]{item.get('item')}[/bright_yellow]: [bright_blue]{item.get('heft')}kg[/bright_blue]")
            print(f"\t[italic dark_green]{item_info_part_1}[/italic dark_green]")
            if len(item_info_part_2) > 0:
                print(f"\t[italic dark_green]{item_info_part_2}[/italic dark_green]")
        else:
            print(f"[#C39BD3]•[/#C39BD3] [[bright_black]x[/bright_black]]: [strike bright_black]{item.get('item')}: {item.get('heft')}kg[/strike bright_black]")
            print(f"\t[italic strike #014201]{item_info_part_1}[/italic strike #014201]")
            if len(item_info_part_2) > 0:
                print(f"\t[italic strike #014201]{item_info_part_2}[/italic strike #014201]")
        i += 1


#list_print(game_parcel_list)


def list_select(game_parcel_list):
    """
    The player is provided a list of selectable parcels,
    from which they must choose enough before the timer runs out.
    """
    start_time = time.time()
    option = False
    screen.feedback("time",parcel_delivery.how_much_time_is_left(start_time,format.parcel_selection_time_limit))
    options_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    list_print(game_parcel_list, options_list)
    option = input(">> ")
    i = 1
    player_parcel_list = []
    while i <= 5 and parcel_delivery.is_there_time_left(start_time, format.parcel_selection_time_limit):
        if option in options_list:
            player_parcel_list.append(game_parcel_list[int(option) - 1])
            options_list.remove(option)
            i += 1
            screen.feedback("time",parcel_delivery.how_much_time_is_left(start_time, format.parcel_selection_time_limit))
            list_print(game_parcel_list, options_list)
            if i == 6:
                print(f"[bold bright_green]>> Kaikki paketit valittu![/bold bright_green]")
                time.sleep(2)
                break
            option = input(">> ")
        elif option in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            screen.new()
            screen.feedback(option, "Paketti on jo valittu!")
            list_print(game_parcel_list, options_list)
            option = input(">> ")
        else:
            screen.new()
            screen.feedback(option, "error")
            list_print(game_parcel_list, options_list)
            option = input(">> ")
        if i == 6:
            print(f"[bold bright_green]>> Kaikki paketit valittu![/bold bright_green]")
            time.sleep(2)
            break
    return player_parcel_list
