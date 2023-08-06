![](https://raw.githubusercontent.com/wdbm/upbox/master/media/upbox.png)

Flask text-entry service and database system

# introduction

Upbox is a text-entry web program. Text and an optional comment is entered and then these are saved to a database.

![](https://raw.githubusercontent.com/wdbm/upbox/master/media/screenshot.png)

# setup

```Bash
sudo apt install sqlite
sudo pip install upbox
```

# Flask

```Bash
while true; do
    upbox --home="home.html"
done
```

The service should now be accessible via a link like the following: 10.10.10.95:443/upbox

# Gunicorn

```Bash
sudo gunicorn --workers=1 "upbox.__init__:WSGI(argv=['--home=home.html'])" --bind=0.0.0.0:443 --certfile=/home/user/certificates/fullchain.pem --keyfile=/home/user/certificates/privkey.pem
```

# upbox database structure

There is one table in an upbox database called "data". This table has the following fields:

|**field**|**description**                  |
|---------|---------------------------------|
|comment  |comment for entry                |
|IP       |IP address that created the entry|
|text     |entry text                       |
|timestamp|entry creation timestamp         |
|unique_ID|entry unique identifier          |
