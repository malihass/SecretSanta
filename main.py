import sys

sys.path.append("utils")
from prettyPlot.parser import parse_input_file
from email_utils import send_email, deleteSentEmails
from party import Attendee, Party

if __name__ == "__main__":
    # ~~~~ Parse input
    inpt = myparser.parse_input_file()
    hostEmail = inpt["hostEmail"]
    hostPassword = inpt["hostPassword"]
    gdoc = inpt["gdoc"]
    dummy_email = "test123@gpail.cop"

    # ~~~~ List of attendees
    attendees = []

    gary_tenney = Attendee(
        name="Gary Tenney",
        email=dummy_email,
        exclude=["Jason Tenney", "Wendy Tenney", "Aaron Tenney", "Beth Bergeron"],
        partner=["Esther Tenney"],
    )
    esther_tenney = Attendee(
        name="Esther Tenney",
        email=dummy_email,
        exclude=["Amy Tenney", "Kristin Tenney", "Wendy Tenney", "Malik Hassanaly", "Jason Tenney"],
        partner=["Gary Tenney"],
    )
    wendy_tenney = Attendee(
        name="Wendy Tenney",
        email=dummy_email,
        exclude=["Gary Tenney", "Amy Tenney", "Kristin Tenney", "Malik Hassanaly"],
        partner=["Aaron Tenney", "Isaac Tenney", "Hannah Tenney", "Josiah Tenney"],
    )
    aaron_tenney = Attendee(
        name="Aaron Tenney",
        email=dummy_email,
        exclude=["Beth Bergeron", "Malik Hassanaly", "Esther Tenney"],
        partner=["Wendy Tenney", "Isaac Tenney", "Hannah Tenney", "Josiah Tenney"],
    )
    hannah_tenney = Attendee(
        name="Hannah Tenney",
        email=dummy_email,
        exclude=[],
        partner=["Wendy Tenney", "Isaac Tenney", "Aaron Tenney", "Josiah Tenney"],
    )
    josiah_tenney = Attendee(
        name="Josiah Tenney",
        email=dummy_email,
        exclude=[],
        partner=["Wendy Tenney", "Isaac Tenney", "Hannah Tenney", "Aaron Tenney"],
    )
    isaac_tenney = Attendee(
        name="Isaac Tenney",
        email=dummy_email,
        exclude=[],
        partner=["Wendy Tenney", "Aaron Tenney", "Hannah Tenney", "Josiah Tenney"],
    )
    amy_tenney = Attendee(
        name="Amy Tenney",
        email=dummy_email,
        exclude=["Jason Tenney", "Gary Tenney", "Kristin Tenney", "Malik Hassanaly", "Aaron Tenney"],
        partner=["Aaron Abma"],
    )
    beth_bergeron = Attendee(
        name="Beth Bergeron",
        email=dummy_email,
        exclude=["Malik Hassanaly", "Esther Tenney", "Jason Tenney", "Amy Tenney", "Wendy Tenney"],
        partner=["Kolin Bergeron", "Xander Bergeron"],
    )
    jason_tenney = Attendee(
        name="Jason Tenney",
        email=dummy_email,
        exclude=["Wendy Tenney", "Beth Bergeron", "Amy Tenney", "Kristin Tenney"],
        partner=[],
    )
    kristin_tenney = Attendee(
        name="Kristin Tenney",
        email=dummy_email,
        exclude=["Aaron Tenney", "Wendy Tenney", "Amy Tenney", "Gary Tenney", "Esther Tenney"],
        partner=["Malik Hassanaly"],
    )
    malik_hassanaly = Attendee(
        name="Malik Hassanaly",
        email=dummy_email,
        exclude=["Aaron Tenney", "Gary Tenney", "Beth Bergeron", "Amy Tenney"],
        partner=["Kristin Tenney"],
    )
    kolin_bergeron = Attendee(
        name="Kolin Bergeron",
        email=dummy_email,
        exclude=[],
        partner=["Beth Bergeron", "Xander Bergeron"],
    )
    xander_bergeron = Attendee(
        name="Xander Bergeron",
        email=dummy_email,
        exclude=[],
        partner=["Beth Bergeron", "Kolin Bergeron"],
    )
    aaron_abma = Attendee(
        name="Aaron Abma",
        email=dummy_email,
        exclude=[],
        partner=["Amy Tenney"]
    )

    # Name of guest /  email adress / person guest gave to the past years
    attendees = [
        gary_tenney,
        esther_tenney,
        wendy_tenney,
        aaron_tenney,
        amy_tenney,
        beth_bergeron,
        jason_tenney,
        kristin_tenney,
        malik_hassanaly,
    ]
    party = Party(attendees=attendees, gdoc=gdoc)
    party.match()
    party.log(toscreen=True)

    # ~~~~ Now Send emails
    for i in range(party.n_guests):
        body, subject, email_address = party.generate_message(i)
        # send_email(email_address, body, subject, host_email_address, host_pwd)

    # # Delete Emails sent so I cannot know who gives what
    # deleteSentEmails()
