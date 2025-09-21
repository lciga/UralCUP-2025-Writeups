#!/bin/sh

# Apache2 setup
# sed -i -e 's/MaxKeepAliveRequests 100/MaxKeepAliveRequests 10000/g' /etc/apache2/apache2.conf
# sed -i -e 's/KeepAliveTimeout 5/KeepAliveTimeout 30/g' /etc/apache2/apache2.conf

# IPtables setup
iptables -A INPUT -p tcp --dport 80 -m state --state NEW -m recent --set --name web
iptables -A INPUT -p tcp --dport 80 -m state --state NEW -m recent --name web --update --seconds 30 --hitcount 2 -j DROP
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Run nginx
nginx -g "daemon off;"