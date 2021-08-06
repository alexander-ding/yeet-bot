# YeetBot

This is a Discord Bot that overlays all detected faces in images with a customizable sticker. Find out more about it on [Bots on Discord](https://bots.ondiscord.xyz/bots/563019457367375882) and [Discord Bot List](https://discordbots.org/bot/563019457367375882).  

![image](https://media.giphy.com/media/fs9AJxWGFy56YmcHTp/giphy.gif)

## Commands

All commands start with `!`.

- `!help`: get help
- `!yeet <url>`: overlays the current sticker onto all faces found in the image. Can also accept an attachment instead
- `!set <url>`: sets the current sticker. Can also accept an attachment instead
- `!clean`: removes the background of the current sticker
- `!default`: reverts to default sticker
- `!scale`: sets width/height scaling to apply to the sticker
- `!shift`: sets displacement to apply to the sticker


## Getting Started

1. Make sure you have all the [dependencies](#dependencies) required.
2. Clone the repository and `cd` into the root directory of the repository.
3. `heroku config:pull`. This exports the config correctly into a local `.env`. You will need to have `YEETBOT_TOKEN` set for this. 
4. `pip install -r requirements.txt` and get started!

Push the code to webend with```heroku container:push worker```.

## Dependencies

- Be sure to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) and login.
- Install `heroku-config` with `heroku config:pull -a yeetbot-cws`.
