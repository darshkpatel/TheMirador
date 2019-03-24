wget http://downloads.rootkit.nl/rkhunter-1.2.7.tar.gz
tar xvfz rkhunter-1.2.7.tar.gz
cd rkhunter/
./installer.sh
rm -rf rkhunter-1.2.7
rkhunter --update
rkhunter -c
echo 'run crontab -e and append the following lines'
echo '0 3 * * * /usr/sbin/chkrootkit 2>&1 | mail -s "chkrootkit output of the server" you@yourdomain.tld)'
