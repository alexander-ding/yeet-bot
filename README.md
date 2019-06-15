# YeetBot

This is a Discord Bot that takes one image and overlays all detected faces in that image with a custom mask. Find out more about it on [Bots on Discord](https://bots.ondiscord.xyz/bots/563019457367375882)! 

![image](https://media.giphy.com/media/fs9AJxWGFy56YmcHTp/giphy.gif)

## Commands

All commands start with `!`.

- !help: get help
- !yeet <url>: overlays the current filter onto all faces found in the image. Can also accept an attachment instead.
- !set <url>: sets the current filter. Can also accept an attachment instead.
- !clean: clears the rim of the current filter. *Defunct as of now*
- !default: sets filter to the default filter


## Getting Started: TODOOOOO

1. Make sure you have all the [dependencies](#dependencies) required.
2. Clone this directory from GitHub with ```git clone https://github.com/alexding123/YeetBot.git```
3. `cd YeetBot`
4. `heroku config:pull`. This exports the config correctly into a local `.env`. You will need to have `YEETBOT_TOKEN` set for this. 

Push the code to webend with```heroku container:push worker```.

## Dependencies

- Be sure to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) and login.
- Install `heroku-config` with `heroku config:pull -a yeetbot-cws`.
- Start another virtual environment with `virtualenv env` (install it with `pip install virtualenv`) (make sure it starts with Python3.6)
- Activate said environment (from Windows: `source env/Scripts/activate`)
- Run `pip install -r requirements.txt`
