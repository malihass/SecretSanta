import json
import os
import random
import sys

from secretSanta import SECRETSANTA_INPUT_DIR as inpt_dir
from secretSanta import logger


def make_attendees(file=os.path.join(inpt_dir, "guests.json")):
    attendees = []
    with open(file) as f:
        data = json.load(f)
    for name in data["event_attendees"]:
        attendees.append(
            Attendee(
                name=name,
                nickname=data["attendees_db"][name]["nickname"],
                email=data["attendees_db"][name]["email"],
                exclude=data["attendees_db"][name]["exclude"],
                partner=data["attendees_db"][name]["partner"],
            )
        )
    potential_attendees = data["potential_attendees"]
    return attendees, potential_attendees


class Attendee:
    def __init__(self, name, nickname, email, exclude=[], partner=[]):
        self.name = name
        self.nickname = nickname
        self.email = email
        self.exclude = exclude
        for e in self.exclude:
            if e == self.name:
                logger.warning(
                    f"Did you mean to exclude {self.name} from {self.name}?"
                )
        self.partner = partner
        for p in self.partner:
            if p not in self.exclude:
                self.exclude.append(p)
            if p == self.name:
                logger.warning(
                    f"Did you mean to make {self.name} partner of {self.name}?"
                )


class Party:
    def __init__(self, gdoc="", attendees=[], potential_attendees=[]):
        if not isinstance(attendees, list):
            raise TypeError(
                f"attendees must be list, received {type(attendees)}"
            )
        if len(attendees) > 0:
            if not isinstance(attendees[0], Attendee):
                raise TypeError(
                    f"attendees must be list of attendees received list of {type(attendees[0])}"
                )
        self.potential_attendees = potential_attendees
        self.attendees = attendees
        self.check_excludes_partners()
        self.n_guests = len(self.attendees)
        self.attendees_names = [attendee.name for attendee in self.attendees]
        if not isinstance(gdoc, str):
            raise ValueError(f"gdoc needed, received {gdoc}")
        self.gdoc = gdoc

    def check_excludes_partners(self):
        found_error = False
        for attendee in self.attendees:
            for excluded in attendee.exclude:
                if excluded not in self.potential_attendees:
                    logger.error(
                        f"For {attendee.name}, {excluded} might be a typo"
                    )
                    found_error = True
        if found_error:
            raise ValueError("Typos in guest input file")

    def fill_givers(self):
        receivers = list(range(self.n_guests))
        givers = []
        for i in range(self.n_guests):
            # Make a list of potential givers that could give to person i
            potential_givers = receivers.copy()

            # Remove the receiver
            potential_givers.pop(potential_givers.index(i))

            # Did I give to you before ? If yes, remove me from givers list
            receiver_name = self.attendees_names[i]
            for igiver, giver in enumerate(self.attendees):
                if receiver_name in giver.exclude:
                    potential_givers.pop(potential_givers.index(igiver))

            # Remove people who already gave
            for igiver in givers:
                if igiver in potential_givers:
                    potential_givers.pop(potential_givers.index(igiver))

            # Choose any of the potential givers
            giverID = random.choice(potential_givers)
            givers.append(giverID)

        return givers

    def match(self):
        # ~~~~ List of previous pairs
        previousGiver = [attendee.name for attendee in self.attendees]
        previousReceiver = [attendee.exclude for attendee in self.attendees]

        # ~~~~ Figure out who gives to who
        # Try until it works
        givers = None
        nFailure = 0
        while givers is None:
            if nFailure >= 1e6:
                raise RuntimeError(
                    "Failed too many times, you may need to relax the exclude list"
                )
            try:
                # connect
                givers = self.fill_givers()
            except IndexError:
                nFailure += 1

        logger.info(f"Failed {nFailure} times")
        self.givers = givers

        self.giver_receiver_pairs = {}
        self.receiver_giver_pairs = {}
        for i in range(self.n_guests):
            self.giver_receiver_pairs[self.givers[i]] = i
            self.receiver_giver_pairs[i] = self.givers[i]

    def log(self, toscreen=False):
        # ~~~~ LOG
        for i in range(self.n_guests):
            string = (
                self.attendees[self.givers[i]].name
                + " gives to "
                + self.attendees[i].name
            )
            string += " / "
            if len(self.attendees[self.givers[i]].exclude) == 0:
                string += " nobody "
            else:
                for ientry in range(
                    len(self.attendees[self.givers[i]].exclude)
                ):
                    string += self.attendees[self.givers[i]].exclude[ientry]
                    if (
                        not ientry
                        == len(self.attendees[self.givers[i]].exclude) - 1
                    ):
                        string += " and "
            string += " before "

            if toscreen:
                print(string)
            else:
                import pickle as pkl

                with open("log.pkl", "wb") as handle:
                    pkl.dump(self, handle, protocol=pkl.HIGHEST_PROTOCOL)

    def get_id_by_name(self, name):
        return self.attendees_names.index(name)

    def get_name_by_id(self, attendee_id):
        return self.attendees_names[attendee_id]

    def get_partner_giver(self, giver_id):
        p_giver = {}
        for p in self.attendees[giver_id].partner:
            try:
                p_id = self.get_id_by_name(p)
                p_giver[p] = self.attendees[self.receiver_giver_pairs[p_id]]
            except ValueError:
                pass
        return p_giver

    def generate_message(self, giver_id):
        attendee = self.attendees[giver_id]
        receiver = self.attendees[self.giver_receiver_pairs[giver_id]]
        partner_giver = self.get_partner_giver(giver_id)

        subject = "Secret Santa 2025!"
        body = (
            "Hi "
            + attendee.nickname
            + "!"
            + "<br>"
            + "Welcome to the 2025 edition of the extended Tenney family's Secret Santa!<br><br>"
            + "You have been assigned the following person for Secret Santa : <b>"
            + receiver.name
            + "</b>!<br><br>"
            + "Link to the Google Doc for gifts: %s <br><br>" % self.gdoc
        )

        if len(partner_giver) > 0:
            body += "You might want to know that:<br>"
            for part in partner_giver:
                body += f"<b>{part}</b>'s Secret Santa is <b>{partner_giver[part].name}</b> ({partner_giver[part].email}).<br>"
        body += "We advise you to coordinate to avoid duplicating gifts!<br>"
        body += "<br>"
        body += (
            "We are aware that many of you are concerned about the North Pole Shutdown. The Secret Santa Corporation had to stop paying agents at the Department of Reindeers. But don’t you worry, they will still help make this Christmas season magical: prestige and visibility are great forms of salary after all!<br><br>"
            + "Anyway, we're here to spread holiday cheer once again!<br><br>"
            + "If, for any reason, your Secret Santa experience is less than magical, contact our assistant Malik at XXXX@XXXX.XXX<br>"
            + 'Additional instructions: <br>&nbsp;&nbsp;&nbsp;&nbsp;1) If you mail your gift, please indicate the name of the receiver and include some keyword such as "Snowflake". Example: Xander sends a gift to Isaac. Xander addresses it to "Isaac Snowflake Tenney".<br>'
            + "&nbsp;&nbsp;&nbsp;&nbsp;2) Hannah, Josiah, Isaac, Xander and Bennett are exempt from Secret Santas. Remember to spread some holiday joy to them too!<br><br>"
            + "Let’s make this season more joyful than a cozy fireplace and bottomless mugs of hot cocoa!<br><br>"
            + "<b>Merry Christmas! <3 Joyeux Noel! <3 Bark Bark! <3<b><br><br>"
        )

        body += """\
        <html>
          <head></head>
          <body>
            <p align="center"><b><font style="color: red;">The Secret </font><font style="color: green;">Santa Corporation</b></p>
          </body>
        </html>
        """

        return body, subject, self.attendees[giver_id].email
