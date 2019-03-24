# TheMirador

TheMirador is an watchtower for linux systems, it monitors user configured system file integrity and access, sudo command access, ssh logins, iptables changes, it emails the admin on any of this events using postfix and also logs the incidents and will also dump system memory contents to a file for forensics. We also run a rootkit scan on installation and email the results to the admin. We also made a systemd service for the same.


### Key Features:

* File Integrity Monitoring
* File Access Monitoring
* IPTABLES rule monitoring 
* sudo access monitoring 
* systemd service 
* Email alerts to speicified admin 
* Dump system memory to file on incident
* Logs for analysis


# For Future Releases:
* Sign Emails 
* Stop notifications temporarily by replying to email
* Set Alert Levels for folders
* Set Alert Levels for memory
* rootkit detection on install
