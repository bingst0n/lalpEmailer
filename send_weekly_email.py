"""
Wrapper script that runs draftWeeklyEmail.py, captures its stdout,
and sends the output as an HTML email via Gmail SMTP.
"""

import os
import re
import sys
import subprocess
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ──────────────────────────────────────────────
# EDIT THESE
# ──────────────────────────────────────────────
RECIPIENTS = [
    "adrian_maroto@avenues-ny.org",
    "afsin_hoque@avenues-ny.org",
    "allegra_godfrey@avenues-ny.org",
    "anya_mehra@avenues-ny.org",
    "ava_safir@avenues-ny.org",
    "charles_agabs@avenues-ny.org",
    "David_Fajardor@avenues-ny.org",
    "Elizabeth_TiradoCrespo@avenues-ny.org",
    "Eloise_Faiman@avenues-ny.org",
    "emma_zisu@avenues-ny.org",
    "Gianna_Leydiker@avenues-ny.org",
    "hamin_seo@avenues-ny.org",
    "Ilana_Friedel@avenues-ny.org",
    "ines_stasiulatis@avenues-ny.org",
    "javier_mendez@avenues-ny.org",
    "Jack_Engleman@avenues-ny.org",
    "julie_hage@avenues-ny.org",
    "kenneth_wu@avenues-ny.org",
    "Lada_Roslavker@avenues-ny.org",
    "lyla_vazirani@avenues-ny.org",
    "Marwa_Delaware@avenues-ny.org",
    "maya_ip@avenues-ny.org",
    "milind_arulraj@avenues-ny.org",
    "navya_satpute@avenues-ny.org",
    "river_guest@avenues-ny.org",
    "samuel_collier@avenues-ny.org",
    "semanti_mukherjee@avenues-ny.org",
    "sophia_cote@avenues-ny.org",
    "sourya_gurram@avenues-ny.org",
    "Trish_Gupta@avenues-ny.org",
    "vayav_gidwaney@avenues-ny.org",
    "willow_larson@avenues-ny.org",
    "william_yeh@avenues-ny.org",
    "zarah_jindal@avenues-ny.org",
    "zoe_koivisto@avenues-ny.org",
    "lukas_villegas@avenues-ny.org",
    "Ava_Kulmer@avenues-ny.org",
    "theodore_glazer@avenues-ny.org",
    "salvatore_acquista@avenues-ny.org",
    "kastalia_cheung@avenues-ny.org",
    "India_McLean@avenues-ny.org",
    "labalgeller28@avenues.org",
    "Zaya_Rochester@avenues-ny.org",
    "brady_yang@avenues-ny.org",
    "Mark_Shanker@avenues-ny.org",
    "coco_prince@avenues-ny.org",
    "scarlett_goranson@avenues-ny.org",
    "Amara_DinzeyDAmbrosio@avenues-ny.org",
    "evie_lee@avenues-ny.org",
    "alessandra_garza@avenues-ny.org",
    "annika_bakhshi@avenues-ny.org",
    "abigail_rothman@avenues-ny.org",
    "alexa_feng@avenues-ny.org",
    "jade_saric@avenues-ny.org",
    "naresa_bernier@avenues-ny.org",
    "scarlett_hanin@avenues-ny.org",
    "Lola_Stevens@avenues-ny.org",
    "zoe_wright@avenues-ny.org",
    "emma_allen@avenues-ny.org",
    "olivia_cheung@avenues-ny.org",
    "jomarlyn_laureano@avenues-ny.org",
    "chloe_mcphatter@avenues-ny.org",
    "ryan_kolniak@avenues-ny.org",
    "Yagna_Boinpally@avenues-ny.org",
    "jiliya_pan@avenues-ny.org",
    "Kamsiyochukwu_JoeAni@avenues-ny.org",
    "Scarlett_JamiesonBeath@avenues-ny.org",
    "bonetsofia_kanayet@avenues-ny.org",
    "luca_smith@avenues-ny.org",
    "leah_singh@avenues-ny.org",
    "millan_subramani@avenues-ny.org",
    "Nikita_Gogate@avenues-ny.org",
    "miranda_douvas@avenues-ny.org",
    "lakshmi_patel@avenues-ny.org",
    "gala_schireson@avenues-ny.org",
    "Nicole_Zhang@avenues-ny.org",
    "beyla_szarvas@avenues-ny.org",
    "Jason_Bernstein@avenues-ny.org",
    "oliver_souza@avenues-ny.org",
    "kerala_brown@avenues-ny.org",
    "elle_baylor@avenues-ny.org",
    "rafaela_liebowitz@avenues-ny.org",
    "juan_alcala@avenues-ny.org",
    "harrison_green@avenues-ny.org",
    "sahara_maazel@avenues-ny.org",
    "naveli_rahman@avenues-ny.org",
    "taran_arulraj@avenues-ny.org",
    "anisa_patel@avenues-ny.org",
    "Mila_Simovic@avenues-ny.org",
]

SUBJECT = "LaLP Weekly Update — Awareness Presentations & Read Alouds"

# Dates to skip sending (YYYY, M, D). Add/remove entries to pause/unpause.
SKIP_DATES = [
    date(2026, 3, 18),
    date(2026, 3, 25),
    date(2026, 4, 1),
]

# Date-specific notes to include in emails (YYYY, M, D): note text
DATE_NOTES = {
    date(2026, 4, 7): "Note that some awareness presentations this week are in immersion languages.",
}
# ──────────────────────────────────────────────


def get_email_body() -> str:
    """Run draftWeeklyEmail.py and return its stdout as a string."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "draftWeeklyEmail.py")

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("ERROR: draftWeeklyEmail.py failed", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    return result.stdout


def add_date_note(body: str, today: date) -> str:
    """Add date-specific note before 'Have a great week!' if one exists for today."""
    if today not in DATE_NOTES:
        return body
    
    note = DATE_NOTES[today]
    # Insert the note as a separate paragraph before "Have a great week!"
    if "Have a great week!" in body:
        return body.replace("Have a great week!", f"{note}\n\nHave a great week!")
    else:
        # Fallback: append at the end if the expected text isn't found
        return body + f"\n\n{note}\n"


def build_html(plain_text: str) -> str:
    """Wrap plain text in minimal HTML, preserving line breaks."""
    escaped = (
        plain_text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    html_body = escaped.replace("\n", "<br>\n")
    return f"""\
<html>
<body style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5;">
{html_body}
</body>
</html>"""


def send_email(sender: str, password: str, recipients: list[str], subject: str, html: str):
    """Send an HTML email to each recipient via Gmail SMTP."""
    for recipient in recipients:
        msg = MIMEMultipart("alternative")
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(html, "html"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, recipient, msg.as_string())
            print(f"✓ Email sent to {recipient}")
        except Exception as exc:
            print(f"✗ Failed to send to {recipient}: {exc}", file=sys.stderr)


def main():
    sender = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")

    if not sender or not password:
        print("ERROR: SENDER_EMAIL and EMAIL_PASSWORD environment variables must be set.", file=sys.stderr)
        sys.exit(1)

    if not RECIPIENTS:
        print("ERROR: RECIPIENTS list is empty. Add at least one address.", file=sys.stderr)
        sys.exit(1)

    today = date.today()
    if today in SKIP_DATES:
        print(f"Today ({today}) is in SKIP_DATES. Skipping email.")
        return

    body = get_email_body()
    body = add_date_note(body, today)

    awareness_match = re.search(r"Awareness Presentations \((\d+) available\)", body)
    readaloud_match = re.search(r"Read Alouds \((\d+) available\)", body)
    awareness_count = int(awareness_match.group(1)) if awareness_match else 0
    readaloud_count = int(readaloud_match.group(1)) if readaloud_match else 0

    if awareness_count == 0 and readaloud_count == 0:
        print("No available slots for either Awareness Presentations or Read Alouds. Skipping email.")
        return

    html = build_html(body)
    send_email(sender, password, RECIPIENTS, SUBJECT, html)


if __name__ == "__main__":
    main()
