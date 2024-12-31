import os

from prettyPlot.parser import parse_input_file

from secretSanta import SECRETSANTA_INPUT_DIR as inpt_dir
from secretSanta.email_utils import deleteSentEmails, send_email
from secretSanta.party import Attendee, Party, make_attendees

if __name__ == "__main__":
    # ~~~~ Parse input
    inpt = parse_input_file(os.path.join(inpt_dir, "input"), delimiter=" :")
    host_email_address = inpt["hostEmail"]
    host_pwd = inpt["hostPassword"]
    gdoc = inpt["gdoc"]
    dummy_email = "test123@gpail.cop"

    # ~~~~ Init party and matchmaking
    attendees, potential_attendees = make_attendees(file=os.path.join(inpt_dir, "guests.json"))
    party = Party(attendees=attendees, gdoc=gdoc, potential_attendees=potential_attendees)
    party.match()
    # party.log(toscreen=True)
    party.log(toscreen=False)

    # ~~~~ Now Send emails
    for i in range(party.n_guests):
        body, subject, email_address = party.generate_message(i)
        # send_email(email_address, body, subject, host_email_address, host_pwd)

    ## Delete Emails sent so I cannot know who gives what
    # deleteSentEmails(host_email_address, host_pwd)
