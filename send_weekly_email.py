"""
Wrapper script that runs draftWeeklyEmail.py, captures its stdout,
and sends the output as an HTML email via Microsoft 365 SMTP.
"""

import os
import sys
import subprocess
import smtplib
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
]

SUBJECT = "LaLP Weekly Update — Awareness Presentations & Read Alouds"
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


def send_email(sender: str, smtp_user: str, password: str, recipients: list[str], subject: str, html: str):
    """Send an HTML email to each recipient via Microsoft 365 SMTP."""
    for recipient in recipients:
        msg = MIMEMultipart("alternative")
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(html, "html"))

        try:
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login(smtp_user, password)
                server.sendmail(sender, recipient, msg.as_string())
            print(f"✓ Email sent to {recipient}")
        except Exception as exc:
            print(f"✗ Failed to send to {recipient}: {exc}", file=sys.stderr)


def main():
    sender = os.environ.get("SENDER_EMAIL")        # shared mailbox: lalp@avenues-ny.org
    smtp_user = os.environ.get("SMTP_USERNAME")     # your login: harrison_green@avenues-ny.org
    password = os.environ.get("EMAIL_PASSWORD")

    if not sender or not smtp_user or not password:
        print("ERROR: SENDER_EMAIL, SMTP_USERNAME, and EMAIL_PASSWORD environment variables must be set.", file=sys.stderr)
        sys.exit(1)

    if not RECIPIENTS:
        print("ERROR: RECIPIENTS list is empty. Add at least one address.", file=sys.stderr)
        sys.exit(1)

    body = get_email_body()
    html = build_html(body)
    send_email(sender, smtp_user, password, RECIPIENTS, SUBJECT, html)


if __name__ == "__main__":
    main()
