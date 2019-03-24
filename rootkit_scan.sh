wget http://downloads.rootkit.nl/rkhunter-1.2.7.tar.gz
tar xvfz rkhunter-1.2.7.tar.gz
cd rkhunter/
./installer.sh
rm -rf rkhunter-1.2.7
rkhunter --update
rkhunter -c
