# Pokete
![Example](assets/ss/ss01.png)

[See more example pics](assets/pics.md)
## What is it?
Pokete is a small terminal based game in the style of a very popular and old game by Gamefreak.

## Installation
For Linux just do this:
```shell
# pip install scrap_engine
$ git clone https://github.com/lxgr-linux/pokete.git
$ ./pokete/pokete.py
```

You can also install it from the AUR:
```shell
$ buildaur -S pokete-git
```

For windows first install pynput and then do a Windows equivalent to the above.

## How to play?
Imagine your a Pokete-Trainer and your goal is it to run around in the world and catch/train as many Poketes as possible and to get the best trainer.

First of all you get a starter Pokete (Steini), that you can use to fight battles with other Poketes.
The controls are w a s d to walk around.

When entering the high grass (;), you may be attacked by a wild Pokete. By pressing 1 you can choose between the attacks (as long their AP is over 0) your Pokete got, by pressing the according number, or navigating the "*"-cursor to the attack and pressing enter. The wild Pokete will fight back, you can kill it and gain XP to level up your Pokete or you can catch it to let it fight for you. To catch a Pokete you have to first weaken the enemy and then throw a Poketeball. And with a bit luck you can catch it.
Pressing the "1" key you can take a look at your current deck, see the detailed information of your Pokete and your attacks or rearrange them.
Changes will only be saved by quitting the game using the exit function.

Since your a Pokete-Trainer, you can also fight against other trainers, the one other "a", that's staying in the middle of the landscape will start a fight with you, when you go into his way. You can not escape from such a trainer fight, you either have to win, or lose. Those trainer fights give double the XP.

In case one of your Poketes dies, or is too weak, you can heal it by going into the house, aka, Pokete-Center, talk the the person there and choose the healing option.
There you can also take a look at all your Poketes, and not just the first six. The ones marked with an "o" are the ones in your deck.

By pressing "e" you can get into a menu where player name and later other settings, can be changed.

The red balls all over the map, are Poketeballs, you need to catch Poketes. Stepping on such a ball adds it to your inventory.

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

For additional information you can see [wiki](wiki.md).

## Tips
- In conversations you can very easily skip the text printing by pressing any key
- When you want to see the next text in a conversation, also just press any key
- Don't play on full-screen, the game then starts to be overseeable
- Don't be offended by the other trainers, they may swear at you

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
- [ ] Add Poketedex
- [ ] Effects
- [x] Add color codes for types

## Dependencies
Pokete depends on python3 and the scrap_engine module.
On windows pynput has to be installed too.

## Releases
For release information see [Changelog](Changelog.md).

## Contributing
Feel free to contribute what ever you want to this game.
New Pokete contributions are especially welcome, those are located in /pokete_data/poketes.py

After adding new Poketes and/or Attacks you may want to run
```shell
$ gen-wiki.py
```

to regenerate the wiki and adding them to it.
