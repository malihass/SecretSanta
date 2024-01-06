import os
import pickle as pkl

from secretSanta import SECRETSANTA_INPUT_DIR as inpt_dir
from secretSanta.logging import read_log
from secretSanta.party import Party, make_attendees


def basic_party():
    attendees = make_attendees(os.path.join(inpt_dir, "guests.json"))
    party = Party(attendees=attendees, gdoc="dumGDOC")
    return party


def test_party():
    party = basic_party()
    party.match()
    party.log(toscreen=True)


def test_msg():
    party = basic_party()
    party.match()
    body, subject, email_address = party.generate_message(0)
    print(body)


def test_log():
    party = basic_party()
    party.match()
    party.log(toscreen=True)
    party.log(toscreen=False)

    print("")

    party2 = basic_party()
    with open("log.pkl", "rb") as handle:
        party2 = pkl.load(handle)
    party2.log(toscreen=True)
