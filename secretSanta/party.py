import json
import os
import random
import sys

from secretSanta import SECRETSANTA_INPUT_DIR as inpt_dir


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
    return attendees


class Attendee:
    def __init__(self, name, nickname, email, exclude=[], partner=[]):
        self.name = name
        self.nickname = nickname
        self.email = email
        self.exclude = exclude
        for e in self.exclude:
            if e == self.name:
                print(
                    f"WARNING: did you mean to exclude {self.name} from {self.name}?"
                )
        self.partner = partner
        for p in self.partner:
            if p not in self.exclude:
                self.exclude.append(p)
            if p == self.name:
                print(
                    f"WARNING: did you mean to make {self.name} partner of {self.name}?"
                )


class Party:
    def __init__(self, gdoc="", attendees=[]):
        if not isinstance(attendees, list):
            sys.exit(
                f"ERROR: attendees must be list, received {type(attendees)}"
            )
        if len(attendees) > 0:
            if not isinstance(attendees[0], Attendee):
                sys.exit(
                    f"ERROR: attendees must be list of attendees received list of {type(attendees[0])}"
                )
        self.attendees = attendees
        self.n_guests = len(self.attendees)
        self.attendees_names = [attendee.name for attendee in self.attendees]
        if not isinstance(gdoc, str):
            sys.exit(f"ERROR: gdoc needed, received {gdoc}")
        self.gdoc = gdoc

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
            try:
                # connect
                givers = self.fill_givers()
            except IndexError:
                nFailure += 1

        print(f"Failed {nFailure} times")

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

        subject = "Secret Santa 2024!"
        body = (
            "Hi "
            + attendee.nickname
            + "!"
            + "<br>"
            + "Welcome to the 2024 edition of the Tenney family's Secret Santa!<br><br>"
            + "You have been assigned the following person for Secret Santa : <b>"
            + receiver.name
            + "</b>!<br><br>"
            + "Link to the Google Doc for gifts: %s <br><br>" % self.gdoc
        )
        if len(partner_giver) > 0:
            body += "<br>"
            body += "You might want to know that:<br>"
            for part in partner_giver:
                body += f"<b>{part}</b>'s Secret Santa is <b>{partner_giver[part].name}</b> ({partner_giver[part].email}).<br>"
            body += (
                "We advise you to coordinate to avoid duplicating gifts!<br>"
            )
            body += "<br>"

        body += (
            "We hope this year has been kind to you, and we're happy to report that the Secret Santa Corporation’s latest PR campaign finally quieted the media storm.<br>Meanwhile, the ‘Elvish Enlightenment Enclave’ has become a full-blown movement! The elves organized a ‘March of the Mistletoe’ last winter, demanding shorter working hours and calling for 'Snowcial Justice.'<br>The Secret Santa Corporation, generously provided hot cocoa to all participants. What a heartwarming festive gathering!<br><br>"
            + "Anyway, we're here to spread holiday cheer once again!<br><br>"
            + "If, for any reason, your Secret Santa experience is less than magical, contact our assistant Malik at XXXX@XXXXX<br>"
            + 'Additional instructions: <br>&nbsp;&nbsp;&nbsp;&nbsp;1) If you mail your gift, please indicate the name of the receiver and include some keyword such as "Snowflake". Example: Xander sends a gift to Isaac. Xander addresses it to "Isaac Snowflake Tenney".<br>'
            + "&nbsp;&nbsp;&nbsp;&nbsp;2) Hannah, Josiah, Isaac, and Xander are once again exempt from Secret Santas. Remember to spread some holiday joy to them too!<br><br>"
            + "Let’s make this season more joyful than a sleigh full of chocolate chip cookies!<br><br>"
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

        body += """\
        <br><br><br><br>
        PS: You may consult our refactored code here: https://github.com/malihass/SecretSanta  
        """

        return body, subject, self.attendees[giver_id].email
