# DedeDropPi
Mini webapp to take water drop photo
listen on port 8080
index.html file in root redirectory allow us to redirect the user-agent to the cgi page

to start the server
```
python3 -m server
```

## Other configs
### to use 80 port instead 8080 without staring the python as root
```
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to 8080
sudo iptables-save
```
