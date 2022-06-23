[![Wiki](https://github.com/lxgr-linux/pokete/actions/workflows/main.yml/badge.svg)](https://github.com/lxgr-linux/pokete/actions/workflows/main.yml)
[![Code-Validation](https://github.com/lxgr-linux/pokete/actions/workflows/main_validate.yml/badge.svg)](https://github.com/lxgr-linux/pokete/actions/workflows/main_validate.yml)
[![GitHub-Pages Build](https://github.com/lxgr-linux/pokete/actions/workflows/documentation.yml/badge.svg)](https://github.com/lxgr-linux/pokete/actions/workflows/documentation.yml)
<br>
![Python Version](https://img.shields.io/github/pipenv/locked/python-version/lxgr-linux/pokete)
![License](https://img.shields.io/github/license/lxgr-linux/pokete)
![AUR version](https://img.shields.io/aur/version/pokete-git)
<br>
![Total Lines of Code](https://img.shields.io/tokei/lines/github/lxgr-linux/pokete)
![Open Issues](https://img.shields.io/github/issues/lxgr-linux/pokete)
![Open pull requests](https://img.shields.io/github/issues-pr/lxgr-linux/pokete)
![commit activity](https://img.shields.io/github/commit-activity/m/lxgr-linux/pokete)
![commits since last release](https://img.shields.io/github/commits-since/lxgr-linux/pokete/latest/master?include_prereleases)
![GitHub contributors](https://img.shields.io/github/contributors/lxgr-linux/pokete)

# Pokete -- Grey Edition

![Example](assets/ss/ss01.png)

[See more example pics](assets/pics.md)
## What is it?
Pokete is a small terminal based game in the style of a very popular and old game by Gamefreak.

## Installation
For Linux just do this:
```shell
# pip install scrap_engine playsound pygobject
$ git clone https://github.com/lxgr-linux/pokete.git
$ ./pokete/pokete.py
```

You can also install it from the AUR:
```shell
$ buildaur -S pokete-git
```

Or you can just run the AppImage from the release page.

NOTE: In that case you first have to create the `~/.cache/pokete/` folder.

For Windows and OSX:

```shell
git clone https://github.com/lxgr-linux/pokete.git
pip install scrap_engine pynput playsound pygobject
```
To run just execute `pokete.py`.

## Usage
The game can be run normaly by not supplying any options.
For non gameplay related usage see `--help`.
Try it out [online](https://replit.com/@lxgr-linux/pokete).

## How to play?
Imagine you're a Pokete-Trainer and you run around in the world to catch/train as many Poketes as possible with the ultimate goal of becoming the best trainer.

First of all you get a starter Pokete (Steini), that you can use to fight battles with other Poketes.
The controls are w a s d to walk around.

When entering the high grass (;), you may be attacked by a wild Pokete. By pressing 1 you can choose between the attacks (as long their AP is over 0) your Pokete has, and by pressing the according number, or navigating with the "\*"-cursor to the attack and pressing enter. The wild Pokete will fight back but you can kill it and gain XP to level up your Pokete. If you would like to catch the wild Pokete, you must first weaken it and then throw a Poketeball. With a bit of luck, you can catch it and have it fight for you.

Pressing the "1" key you can take a look at your current deck, see the detailed information of your Pokete and your attacks or rearrange them.
Changes will only be saved by quitting the game using the exit function.

Since you're a Pokete-Trainer, you can also fight against other trainers (the  other "a" in the middle of the landscape). He will start a fight with you when you get close enough to him. You can not escape from such a trainer fight, you either have to win, or lose. These trainer fights give double the XP.

When one of your Poketes die, or is too weak, you can heal it by going into the house (Pokete-Center), talk the the person there and choose the healing option.
Here you can also take a look at all of your Poketes, and not just the six in your team. The ones marked with an "o" are the ones in your deck.

By pressing "e" you can get into a menu where player name, and later other settings, can be changed.

The red balls all over the map are Poketeballs. You'll need these to catch Poketes. Stepping on such a ball will add it to your inventory.

See [How to play](HowToPlay.md).

## Game depth
Not only are there Poketes that are stronger than others, but also Poketes with different types, which are effective against some types and ineffective against others.

Type|Effective against|Ineffective against
---|---|---
Normal||
Stone|Flying, Fire|Plant
Plant|Stone, Ground, Water|Fire, Ice
Water|Stone, Flying, Fire|Plant, Ice
Fire|Flying, Plant, Undead, Ice|Stone, Water
Ground|Normal|Flying
Electro|Stone, Flying|Ground
Flying|Plant|Stone
Undead|Normal, Ground, Plant, Water|Fire
Ice|Water, Plant|Fire

For additional information you can see [wiki](wiki.md) or
[the multi-page wiki](https://lxgr-linux.github.io/pokete/wiki-multi).

## Mods
Mods can be written to extend Pokete. To load a mod, the mod has to be placed in `mods` and mods have to be enabled in the menu.
For an example mod see [example.py](mods/example.py).

## Tips
- In conversations you can very easily skip the text printing by pressing any key
- When you want to see the next text in a conversation: press any key
- Don't play on full-screen; the game will not run properly
- Don't be offended by the other trainers; they may swear at you

## TODO
- [x] Add a wizard to set name and choose starter Pokete at the start
- [ ] Add More maps
- [x] Add types for attacks and Poketes
- [x] Add evolving
- [ ] Add more than one Pokete for trainers
- [x] Coloured Poketes
- [x] A store to buy Poketeballs
- [x] Add potions
- [x] Add Intro
- [x] Add trading
- [x] Add Poketedex
- [x] Effects
- [x] Add colour codes for types

## Dependencies
Pokete depends on python3 and the scrap_engine module.
On windows pynput has to be installed too.

## Documentation
- [Documentation for pokete_classes](https://lxgr-linux.github.io/pokete/doc/pokete_classes/index.html)
- [Documentation for pokete_data](https://lxgr-linux.github.io/pokete/doc/pokete_data/index.html)
- [Documentation for the gen-wiki file](https://lxgr-linux.github.io/pokete/doc/gen_wiki.html "gen_wiki.py")
- [Documentation for the prepare_pages file](https://lxgr-linux.github.io/pokete/doc/prepare_pages.html "prepare_pages.py")
- [Documentation for the pokete_general_use_fns](https://lxgr-linux.github.io/pokete/doc/pokete_general_use_fns.html "pokete_general_use_fns.py")
- [Documentation for the main file "pokete.py"](https://lxgr-linux.github.io/pokete/doc/pokete.html "pokete.py")

## Releases
For release information see [Changelog](Changelog.md).

## Contributing
Feel free to contribute what ever you want to this game.
New Pokete contributions are especially welcome, those are located in /pokete_data/poketes.py

To see how to add more poketes/types/attacks to the game, see [the DevGuide](DevGuide.md)

After adding new Poketes and/or Attacks you may want to run
```shell
$ ./gen_wiki.py
```

to regenerate the wiki and adding them to it.

## Credits
Music:
- Eric Skiff - Resistor Anthems - Available at [http://EricSkiff.com/music](http://EricSkiff.com/music)
- Marllon Silva (xDeviruchi) - 8-bit-fantasy-adventure-music-pack - Available at [itch.io](https://xdeviruchi.itch.io/8-bit-fantasy-adventure-music-pack)
- SketchyLogic - Map - Available at [opengameart.org](https://opengameart.org/content/nes-shooter-music-5-tracks-3-jingles)

## Trouble shooting
If you're experiencing problems on Japanese systems take a look at [this](https://gist.github.com/z80oolong/c7523367b798bdda094f859342f4c8be).
