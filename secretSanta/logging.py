import pickle as pkl
import sys

from secretSanta.party import Party


def read_log(filename):
    party = Party()
    with open(filename, "rb") as handle:
        party = pkl.load(handle)

    party.log(toscreen=True)
