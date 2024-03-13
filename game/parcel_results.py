# Parcel End Screen Logic
from . import screen
import time
from rich.console import Console
from rich.table import Table
from rich import print
from . import parcel_delivery


def show_end_screen(player_list: list[dict]) -> None:
    """
    Print end screen to player with scores

    :param player_list: List of player dictionaries
    :type player_list: list[dict]
    :returns: None
    """

    screen.clear()

    player_list = sorted(player_list, key=lambda x: x['score'], reverse=True)  # Sort list by score (first largest etc.)

    # Design score table UI
    console = Console()
    score_table = Table(show_header=True, header_style="bold blue")
    score_table.add_column("Nro.", style="yellow")
    score_table.add_column("Nimi", style="yellow")
    score_table.add_column("Pisteet", style='yellow')
    score_table.add_column("CO2", style="yellow")

    # Add player score rows and print them
    for i in range(0, len(player_list)):
        # Time.sleep() and screen.clear() are used for small "loading animation"
        time.sleep(0.1)
        screen.clear()

        if player_list[i]['score'] == 0:
            player_list[i]['score'] = 'Game Over'

        score_table.add_row(
            str(i + 1) + ".",
            player_list[i]['name'],
            str(player_list[i]['score']),
            str(int(player_list[i]['co2'])) + " g"
        )

        # Print the created rows
        console.print(score_table)

    print("Paina [green]ENTER[/green] siirtyäksesi eteenpäin.")
    input()

    # Call main menu function here

