import sys

sys.path.append("utils")

from email_utils import deleteSentEmails, send_email
from party import Attendee, Party, make_attendees
from prettyPlot.parser import parse_input_file


if __name__ == "__main__":
    # ~~~~ Parse input
    inpt = parse_input_file()
    hostEmail = inpt["hostEmail"]
    hostPassword = inpt["hostPassword"]
    gdoc = inpt["gdoc"]
    dummy_email = "test123@gpail.cop"

    # ~~~~ Init party and matchmaking
    attendees = make_attendees()
    party = Party(attendees=attendees, gdoc=gdoc)
    party.match()
    party.log(toscreen=True)

    # ~~~~ Now Send emails
    for i in range(party.n_guests):
        body, subject, email_address = party.generate_message(i)
        # send_email(email_address, body, subject, host_email_address, host_pwd)

    # # Delete Emails sent so I cannot know who gives what
    # deleteSentEmails()
