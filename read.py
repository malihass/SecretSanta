import pickle as pkl
import sys

sys.path.append("utils")
from party import Party

party = Party()

with open("log.pkl", "rb") as handle:
    party = pkl.load(handle)

party.log(toscreen=True)
