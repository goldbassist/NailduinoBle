sudo apt-get update;sudo apt-get upgrade -y

sudo apt-get install libdbus-1-dev libglib2.0-dev libdbus-glib-1-dev -y
sudo apt-get install libusb-dev libudev-dev libreadline-dev libical-dev -y

mkdir -p work/bluepy
cd work/bluepy
wget https://www.kernel.org/pub/linux/bluetooth/bluez-5.4.tar.xz
xz -d bluez-5.4.tar.xz
tar xvf bluez-5.4.tar
cd bluez-5.4
./configure --disable-systemd
make

sudo make install

cd ../../../

echo "run"
echo " $ sudo hcitool lescan"
echo " $ sudo hciconfig hci0 up"
echo " $ python rasplayBle.py"
