sudo netctl start lxcbridge
sudo sysctl -q net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o enp3s0f2 -j MASQUERADE
