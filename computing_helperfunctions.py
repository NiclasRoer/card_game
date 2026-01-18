import os
import sys

def compute_card_value(card_name):
    rank_str, suit = card_name.split(" of ")

    rank_map = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
            "8": 8, "9": 9, "10": 10,
            "Jack": 11, "Queen": 12, "King": 13, "Ace": 14,
            "": 0
    }
    value = rank_map.get(rank_str, None)

    return value, suit

def get_asset_path(relative_path):
    """ Get the absolute path to an asset, works for dev and for PyInstaller bundled exe """
    if hasattr(sys, '_MEIPASS'):
        # Running as a bundled executable
        base_path = sys._MEIPASS
    else:
        # Running in normal Python environment
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def card_name_to_filename(card_name):
    """Convert 'Ace of Spades' -> 'card_spades_A'"""
    rank_map = {
        "2": "02", "3": "03", "4": "04", "5": "05", "6": "06", "7": "07",
        "8": "08", "9": "09", "10": "10",
        "Jack": "J",  # ← map face cards
        "Queen": "Q",
        "King": "K",
        "Ace": "A"
    }
    suit_map = {
        "Hearts": "hearts",
        "Diamonds": "diamonds",
        "Clubs": "clubs",
        "Spades": "spades"
    }
    rank, _, suit = card_name.partition(" of ")
    return f"card_{suit_map[suit]}_{rank_map[rank]}"

def filename_to_card_name(filename):
    """Convert 'card_spades_A' -> 'Ace of Spades'."""
    rank_map_reverse = {
        "02": "2", "03": "3", "04": "4", "05": "5", "06": "6", "07": "7", "08": "8", "09": "9", "10": "10",
        "J": "Jack",
        "Q": "Queen",
        "K": "King",
        "A": "Ace"
    }
    suit_map_reverse = {
        "hearts": "Hearts",
        "diamonds": "Diamonds",
        "clubs": "Clubs",
        "spades": "Spades"
    }

    _, suit, rank = filename.split('_')
    return f"{rank_map_reverse[rank]} of {suit_map_reverse[suit]}"