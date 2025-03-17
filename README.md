# HydrAttack PoC eMailSpoofer Module

**HydrAttack** PoC eMail Spoofer Module is designed to test the security posture of a domain against email spoofing attacks. It performs steps to SPF &amp; DMARC Check (the module verifies whether the target domain has SPF and DMARC records configured), Spoofing Attempt (if the domain lacks proper SPF and DMARC protections, the module spins up a web server and attempts to send spoofed emails from that domain) and Verification (the spoofed email delivery is checked to assess the real-world risk of exploitation).
![](https://github.com/IvanGlinkin/media_support/blob/main/HydrAttack%20PoC%20-%20Email%20Spoofer%20Module%20Logo.png?raw=true)

---

### ⚠️ Legal Disclaimer

This software and associated materials are intended solely for proof-of-concept (PoC) and security research purposes. Unauthorized use of this code for real-world phishing attacks, fraudulent activities, or any malicious intent is strictly prohibited.

---

### <a href="https://hydrattack.com/" target=_blank><img src="https://github.com/IvanGlinkin/media_support/blob/main/znak.png?raw=true" width="25"><a>  What is HydrAttack 
External Attack Surface Management system ![HydrAttack](https://hydrattack.com/) is an innovative risk management platform, designed to help identify and mitigate web application risks in completely new ways

<a href="https://twitter.com/EASM_HydrAttack" target=_blank><img src="https://cdn-icons-png.flaticon.com/128/5969/5969020.png" width="50"><a>
<a href="https://t.me/EASM_HydrAttack" target=_blank><img src="https://cdn-icons-png.flaticon.com/128/2111/2111646.png" width="45"><a>
<a href="https://www.linkedin.com/company/HydrAttack" target=_blank><img src="https://cdn-icons-png.flaticon.com/128/174/174857.png" width="45"><a>

---

### HowTo

#### Detailed instruction
  
1. Install Docker (if you have already had it, just skip this step)
   * for Ubuntu: official page: https://docs.docker.com/engine/install/ubuntu/
   * for Windows: https://docs.docker.com/desktop/setup/install/windows-install/
   * for MacOS: https://docs.docker.com/desktop/setup/install/mac-install/

2. Download the repository to your PC
   * Using Git: `git clone https://github.com/IvanGlinkin/HydrAttack-PoC-eMail-Spoofer-Module.git`
   * Download ZIP: https://github.com/IvanGlinkin/HydrAttack-PoC-eMail-Spoofer-Module/archive/refs/heads/main.zip
   
3. Go to the folder
   * U/Linux: `cd HydrAttack-PoC-eMail-Spoofer-Module`
   * Windows: `dir HydrAttack-PoC-eMail-Spoofer-Module`
  
4. Create an image (DO NOT FORGET ABOUT THE DOT (.) )
   
   `docker build -t docker-hydrattack-poc-email-spoofer .`

5. Launch the container
   
   `docker run -it --rm -e DOMAIN=abracadabra.ahha -e SENDTO=your@email.com docker-hydrattack-poc-email-spoofer`
   
   * DOMAIN - testing domain name, e.g. *abracadabra.ahha*
   * SENDTO - email address, where to send a report, e.g. *your@email.com*




     
#### Short instruction
  
```
cd ~/Documents
git clone https://github.com/IvanGlinkin/HydrAttack-PoC-eMail-Spoofer-Module.git
cd HydrAttack-PoC-eMail-Spoofer-Module
docker build -t docker-hydrattack-poc-email-spoffer .
docker run -it --rm -e DOMAIN=abracadabra.ahha -e SENDTO=your@email.com docker-hydrattack-poc-email-spoffer
```

---

### The risk of SPF/DKIM/DMARC absent
Each piece of code particularly and each application in general should be written in secure way to avoid any errors which could lead to a particular breach or exposure. The email mechanisms are not an exclusion and also should be protected properly. In this knowledge base article let’s consider main email authentication mechanisms helping us to not be phished and deceived.

**Sender Policy Framework*** also known as **SPF** helps verify that an email sent from a domain is coming from an authorized mail server. So, the domain owner publishes an SPF record in DNS (Domain Name System), specifying which mail servers are allowed to send emails on behalf of the domain. When an email is received, the recipient’s mail server checks the SPF record of the sending domain. If the email comes from an authorized mail server, it passes SPF; otherwise, it fails SPF and may be marked as spam or rejected.

#### DNS record example:
```
•	Type: 	TXT
•	Name: 	@
•	Data: 	v=spf1 ip4:192.168.1.1 include:_spf.yourmailserver.com -all
•	TTL: 	1 hour
```

This means that only 192.168.1.1 and yourmailserver’s mail servers are authorized to send emails for the domain

**DomainKeys Identified Mail** also known as **DKIM** is an email authentication method that allows the recipient to verify that an email was actually sent by the claimed sender and was not modified in transit. It does this by adding a digital signature to the email.
The domain owner generates a key pair, where the public key is published in the domain’s DNS as a TXT record, and the private key is stored securely on the sending mail server.


#### DKIM record example:
```
•	Type: 	TXT
•	Name: 	dkim._domainkey
•	Data: 	v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQE... (public key)
•	TTL: 	1 hour
```
When an email is sent, the mail server uses the private key to create a DKIM signature, which is added as a special DKIM-Signature header in the email. The receiving mail server retrieves the public key from the sender’s DNS which uses to verify the DKIM signature. If the signature matches, the email passes DKIM authentication.

**Domain-based Message Authentication, Reporting, and Conformance** also known as **DMARC* builds on SPF and DKIM to provide stricter email authentication and reporting. It allows domain owners to specify how failed SPF/DKIM emails should be handled by recipients.
DMARC record is also published in DNS and If an email fails SPF or DKIM, the recipient’s mail server follows the DMARC policy:
```
•	p=none:	        Take no action, just monitor
•	p=quarantine:	Mark as spam
•	p=reject: 	Block the email entirely
```


#### DMARC record example:
```
•	Type: 	TXT
•	Name: 	_dmark
•	Data: 	v=DMARC1; p=reject; rua=mailto:reports@yourdomain.com; ruf=mailto:forensics@yourdomain.com; adkim=s; aspf=s
•	TTL: 	1 hour
```
This means all failed emails are blocked (p=reject), reports about the attack are sending to reporting addresses (rua/ruf), and enabling strict mode, ensuring DKIM signatures must match exactly (adkim=s)


### A Complete Security Setup:
1.	SPF ensures the email comes from an authorized mail server.
2.	DKIM ensures the email hasn’t been tampered with.
3.	DMARC enforces policies based on SPF/DKIM results and provides reports.
