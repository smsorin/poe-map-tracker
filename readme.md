# PoE - Map tracker

## Disclaimer

This product isn't affiliated with or endorsed by Grinding Gear Games in any way.

This application is provided as is, with no guarantees of any kind (including but not limited to security, availability or funtionality).

If there's sufficient interest I might try to package this into something nicer, like an `.exe`, but for now you'll have to be somewhat comfortable with the command line.

## Overview

This is an application for tracking map progress in [Path of Exlie](http://pathofexile.com).

The application works by monitoring the clipboard and client log.
It is intened to help you after you're reached maps to identify what mods make the things harder for you (i.e kill your character). Obviously this is useless in HC.

## How to use it

Start the appication on your desktop (same machine you run Path of Exile on). To do this open a command console, go to the directory where you've downloaded the repository and run `python -m webapp`.\
When starting it will dump a few lines with the an ip and port, leave it in the background. Something like:
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.16:5000
```

The 127.0.0.1 is the local address, the other should be your machine's network address.

Open a browser and go to the machine's network address. I prefer using a phone, tablet, laptop so I don't need to Alt-Tab in the game, but having it on the same machine also works. As long as the other device is on the same network (your WiFi for example) it should work. From now on I'll refer to any browser where you've opened the link as the browser.

In game, hit Ctrl+C on a map you consider running. The browser should show you the map with rarity level and mods highlighted.

If the client log is set up correctly you can just jump in the map, and the browser should reflect this by saying `Started...`. Once your back to your hideout it will tell you the total time spent in the map.

If the client log is not set up correctly, you can either fix that, or hit start, Map Done and Died when appropriate. If you don't hit them in the right order the app will try to figure out something reasonable, but don't assume it's very smart.

Hit `Save` or Ctrl+C another map to save the map to the local DB. The local DB of saved runs is used to build your statistics.

After a few map runs you'll start to see a summary under `Your adventure so far...`.
Currently it shows:

* A summary of your map tiers (how many maps of each tier you've ran, how much you died and how fast you are).
* The top 10 deadliest mods, order by how many deaths in total you recorded.
* The top 10 rare deadly mods, ordered by how many deaths/map you recorded. These tend to differ from the ones above since they are the ones that you actively avoid, but got tricked into running once.

## Instalation

### Pre-requisites
You'll need python 3.10+ and pip.
Run 
```
pip install Flask Flask-SocketIO simple-websocket
```
### Download the repository.
Next download the git repository where you've likely found this file.

Save it somewhere easily accessible, you'll need to run a command console to it later.

### Check configuration
The configuraiton file is 'config.py', open it with whatever text editor you want (nothing fancy, notepad is just right).

There are two paths to configure. For both you can open a file explorer go locate them right directory and copy the path.

* POE_CLIENT_LOG - Client.txt - This is a log file from the path of exile client. There are forum posts about it. If this is missing you'll have to click Start, Map Done and Died by yourself.
* MAPS_DB - This is the database with the maps you've run. By default it will be in the local directory, but you can make it point to whatever you want. You might also want to change it betweek leagues. If you have some backup capabilities, this is the file you want backed up.

## Notes and Warnings

This is a app developed in my spare time. Should be functional but it's far from preety.

*This thing is not secure.* It will open a port on your device, than theoretically anybody can connect to. Normally most home networks have a firewall built-in and rely on UpNP to open ports to the outside. This app, by itself won't do UPNP but if you have something strange configure it might be automatically forwarded. It should be OK as long as you're not opening the port to the outside world. Others on the local network can also grieve you (press buttons, delete history, mess up statistics, etc)

*This thing is not secure.* The local database is a very insecure format called pickle. It's read by running potentially insecure code.

*This thing is not secure.* Do not run it on anything that should be secure. 
