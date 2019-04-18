# YeetBot

This is a Discord Bot [(OAuth)](https://discordapp.com/api/oauth2/authorize?client_id=563019457367375882&permissions=34816&redirect_uri=https%3A%2F%2Fwww.github.com%2Falexding123&scope=bot) that takes one image and overlays all detected faces in that image with a custom mask. Just go click on the `OAuth` link for invitation!

![image](https://media.giphy.com/media/fs9AJxWGFy56YmcHTp/giphy.gif)

## Commands

All commands start with `!`.
* !help: get help
* !yeet <url>: overlays the current filter onto all faces found in the image. Can also accept an attachment instead.
* !set <url>: sets the current filter. Can also accept an attachment instead.
* !clean: clears the rim of the current filter. *Defunct as of now*
* !default: sets filter to the default filter






## Getting Started: TODOOOOO

1. Make sure you have all the [dependencies](#dependencies) required.
2. Clone this directory from GitHub with ```git clone https://github.com/alexding123/YeetBot.git```
3. `cd YeetBot`
4. `heroku config:pull`. This exports the config correctly into a local `.env`. You will need to have `YEETBOT_TOKEN`, `GITHUB_USERNAME`, and `GITHUB_PASSWORD` set for this. 

Push the code to webend with```heroku container:push worker```.

## Dependencies

TODO
