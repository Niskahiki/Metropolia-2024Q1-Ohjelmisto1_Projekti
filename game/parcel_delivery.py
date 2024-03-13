# Parcel Delivery Logic
from geopy import distance
from . import format
from . import screen
from rich import print
import time


# Select which parcel to deliver
def select_delivery(player_data):
    """
    Takes the players data as input and lets them choose a parcel to deliver.
    Returns the index of the parcel in the list: 'parcels_picked' in player data.
    """

    # creates a list of valid inputs to be used later to check if the players input is valid
    list_of_valid_inputs = []
    for parcel in player_data.get("parcels_picked"):
        if parcel not in player_data.get("parcels_delivered"):
            list_of_valid_inputs.append(str(player_data.get("parcels_picked").index(parcel)+1))

    # asks the player to give an input and doesn't let the player proceed until a valid input is given
    while True:
        print(f"[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][PAKETIN KULJETUS][/italic #FF7F50]\n")
        print(f"[#C39BD3]// Valitse paketti, jonka haluat kuljettaa:[/#C39BD3]")

        # prints parcel options to the player
        for parcel in player_data.get("parcels_picked"):
            parcel_number = f"[yellow]{player_data.get('parcels_picked').index(parcel)+1}[/yellow]"
            if parcel in player_data.get("parcels_delivered"):
                parcel_number = "[bright_black]X[/bright_black]"

            distance_from_player = distance.distance(player_data.get("location"), (parcel.get("latitude"), parcel.get("longitude")))
            dot_and_number = f"[#C39BD3]•[/#C39BD3] [{parcel_number}]:"
            tuote = f"Tuote: [bright_yellow]{parcel.get('item')}[/bright_yellow],"
            paino = f"Paino: [bright_blue]{parcel.get('heft')} kg[/bright_blue],"
            kohde = f"Kohde: [bright_green]{parcel.get('destination_airport')}[/bright_green],"
            etaisuus = f"Etäisyys: [bright_red]{float(str(distance_from_player)[:-3]):.2f} km[/bright_red]"

            longest_name_length = 0
            for parcel1 in player_data["parcels_picked"]:
                if len(parcel1["item"]) > longest_name_length:
                    longest_name_length = len(parcel1["item"])

            longest_destination_name_length = 0
            for parcel1 in player_data["parcels_picked"]:
                if len(parcel1["destination_airport"]) > longest_destination_name_length:
                    longest_destination_name_length = len(parcel1["destination_airport"])

            if parcel not in player_data.get("parcels_delivered"):
                print(f"{dot_and_number} {tuote:<{longest_name_length+39}} {paino:<42} {kohde:<{longest_destination_name_length+37}} {etaisuus}")
            else:
                print(f"• [strike bright_black][{parcel_number}]: Tuote: { parcel.get('item') + ',' :<{longest_name_length + 1}} Paino: { str(parcel.get('heft')) + ' kg,' :<8} Kohde: { parcel.get('destination_airport') }")

        option = input(">> ")

        if option in list_of_valid_inputs:
            #screen.feedback(option, "Paketti valittu")
            break
        elif option in ["1","2","3","4","5"]:
            screen.feedback(option, "Paketti on jo toimitettu!")
        else:
            screen.feedback(option, "error")

    return int(option)-1 # Returns the parcel ( dict() ) index for which parcel the player wishes to deliver.


# Select form of delivery transport.
def select_delivery_method(chosen_location, player_data, start_time):
    """
    Takes the chosen travel location and the data of the acting player,
    lets the player choose an airplane and returns the number corresponding to the chosen airplane.
    The numbers that correspond to the airplanes are:
    1. "Rahtikone"
    2. "Matkustajakone"
    3. "Yksityiskone"
    """
    
    #calculates the distance from players current location to the chosen destination
    distance_from_player = distance.distance(player_data.get("location"), ((player_data.get("parcels_picked")[int(chosen_location)].get("latitude")), (player_data.get("parcels_picked")[int(chosen_location)].get("longitude"))))

    #calculates the default flight time that is used to calculate the flight times of different airplane options
    default_flight_time = float(str(distance_from_player)[:-3]) / format.transport_speed1 # flight time in hours, 800km/h used as a default speed of a commercial airplane
    
    screen.feedback("time",how_much_time_is_left(start_time,format.parcel_delivery_time_limit))

    #asks the player to choose an airplane and doesn't let them proceed until a valid input is given
    while True:
        print(f"[#6A5ACD]//[/#6A5ACD] [italic #FF7F50][PAKETIN KULJETUS / TOIMITUSTAPA][/italic #FF7F50]")
        if player_data["location"] == [60.3172, 24.963301]:
            print(f"[#6A5ACD]•[/#6A5ACD]Sijaintisi: [#76D7C4]Helsinki-Vantaan lentoasema[/#76D7C4]")
        else:
            for parcel in player_data["parcels_picked"]:
                if parcel["latitude"] == player_data["location"][0] and parcel["longitude"] == player_data["location"][1]:
                    location = parcel["destination_airport"]
            print(f"[#6A5ACD]•[/#6A5ACD]Sijaintisi: [#76D7C4]{location}[/#76D7C4]")
        print(f"[#6A5ACD]•[/#6A5ACD]Kohteena:   [#76D7C4]{player_data.get('parcels_picked')[int(chosen_location)].get('destination_airport')}[/#76D7C4], etäisyys: [bright_red]{float(str(distance_from_player)[:-3]):.0f} km[/bright_red]\n")
        print(f"[#C39BD3]Valitse toimitustapa![/#C39BD3]")
        print(f"[#C39BD3]•[/#C39BD3] [[yellow]1[/yellow]]: [bright_yellow]Rahtikone:[/bright_yellow]      Lentoaika: [bright_blue]{default_flight_time * format.transport_speed3:.1f}[/bright_blue] tuntia [bright_red](-{default_flight_time * format.transport_speed3:.1f} sekunttia peliaikaa)[/bright_red]")
        print(f"[#C39BD3]•[/#C39BD3] [[yellow]2[/yellow]]: [bright_yellow]Matkustajakone:[/bright_yellow] Lentoaika: [bright_blue]{default_flight_time:.1f}[/bright_blue] tuntia [bright_red](-{default_flight_time:.1f} sekunttia peliaikaa)[/bright_red]")
        print(f"[#C39BD3]•[/#C39BD3] [[yellow]3[/yellow]]: [bright_yellow]Yksityiskone:[/bright_yellow]   Lentoaika: [bright_blue]{default_flight_time * format.transport_speed2:.1f}[/bright_blue] tuntia [bright_red](-{default_flight_time * format.transport_speed2:.1f} sekunttia peliaikaa)[/bright_red]")
        option = input(">> ")

        if option in ["1","2","3"]:
            #print(f"Valitsit lentokoneen {option}")
            break
        else:
            screen.feedback(option, "error")

    # CO2 emissions based on distance & delivery method.
    match option:
        case "1":
            CO2_multiplier = format.transport1_co2
            time_lost = default_flight_time * format.transport_speed3
        case "2":
            CO2_multiplier = format.transport2_co2
            time_lost = default_flight_time
        case "3":
            CO2_multiplier = format.transport3_co2
            time_lost = default_flight_time * format.transport_speed2

    total_weight = 0
    for parcel in player_data["parcels_picked"]:
        if parcel not in player_data["parcels_delivered"]:
            total_weight += parcel["heft"]
            total_weight += player_data["parcels_picked"][chosen_location]["heft"]

    delivery_CO2 = float(str(distance_from_player)[:-3]) * 0.36 * total_weight * CO2_multiplier
    parcel_CO2 = player_data["parcels_picked"][chosen_location].get("co2_item")
    CO2_full = delivery_CO2 + parcel_CO2

    return CO2_full, time_lost


def is_there_time_left(start_time, time_limit):
    if time.time() - start_time > time_limit:
        return False
    return True


def how_much_time_is_left(start_time, time_limit):
    #Returns the remaining time represented as a boxes -> string
    number_of_boxes = int(20 * (time_limit - (time.time() - start_time)) / time_limit) * "█"
    time_left = float(f"{time_limit - (time.time() - start_time):.2f}")
    if int(len(number_of_boxes*2)) > 25:
        return f"[#40ff19]{number_of_boxes}[/#40ff19] [bold blue]{time_left}s[/bold blue] [#40ff19]{number_of_boxes}[/#40ff19]"
    elif len(number_of_boxes*2) > 10:
        return f"[#ffec17]{number_of_boxes}[/#ffec17] [bold blue]{time_left}s[/bold blue] [#ffec17]{number_of_boxes}[/#ffec17]"
    else:
        return f"[#ff1717]{number_of_boxes}[/#ff1717] [blink2 bold red]{time_left}s[/blink2 bold red] [#ff1717]{number_of_boxes}[/#ff1717]"
