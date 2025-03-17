# HydrAttack PoC eMailSpoofer Module

**HydrAttack** PoC eMail Spoofer Module is designed to test the security posture of a domain against email spoofing attacks. It performs steps to SPF &amp; DMARC Check (the module verifies whether the target domain has SPF and DMARC records configured), Spoofing Attempt (if the domain lacks proper SPF and DMARC protections, the module spins up a web server and attempts to send spoofed emails from that domain) and Verification (the spoofed email delivery is checked to assess the real-world risk of exploitation).
![](https://github.com/IvanGlinkin/media_support/blob/main/HydrAttack%20PoC%20-%20Email%20Spoofer%20Module%20Logo.png?raw=true)

## ⚠️ Disclaimer

This tool is strictly for educational and security assessment purposes. It should only be used on domains you have explicit permission to test. Misuse of email spoofing can lead to legal consequences.

## ⚡ What is HydrAttack

External Attack Surface Management system ![HydrAttack](https://hydrattack.com/) is an innovative risk management platform, designed to help identify and mitigate web application risks in completely new ways
