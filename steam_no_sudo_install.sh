LOCAL_APP_DIR='~/Apps'

touch $LOCAL_APP_DIR/
touch $LOCAL_APP_DIR/Steam
touch ~/.profile

cd /tmp
wget https://repo.steampowered.com/steam/archive/stable/steam_latest.deb
dpkg -x steam_latest.deb ~/Apps/Steam

echo "export PATH=\$PATH:/home/super/Apps/steam" >> ~/.profile
