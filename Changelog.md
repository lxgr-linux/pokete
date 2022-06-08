# Changelog

## [0.7.2] - 2022-06-08

Crucial bugfix related to natures and pokete dex.

## [0.7.1] - 2022-06-08

Just some small bugfixes.

## [0.7.0] - 2022-06-06

### Under the hood
- Massive code reorganisation
- Added `PeriodicEventManager`, introducing a centralized approach to handling periodically occurring events
- Enabled pipenv support

### Game design and behaviour
- After all Poketes are dead, players are now transported back to the last visited Pokete center
- Multiple Poketes in a fight are now automatically possible
- NPCs are way smarter now and support multi-answer chats
- Added achievements visible via a submenu
- Added commandline options
- Several new Poketes have been added:
	+ [Voglus](wiki.md#voglus)
	+ [Ratatat](wiki.md#ratatat)
	+ [Crabbat](wiki.md#crabbat)
	+ [Rustacean](wiki.md#rustacean)
	+ [Saugh](wiki.md#saugh)
	+ [Corcos day](wiki.md#corcos-day)
	+ [Corcos night](wiki.md#corcos-night)
	+ [Raupathor day](wiki.md#raupathor-day)
	+ [Raupathor night](wiki.md#raupathor-night)
	+ [Mothor](wiki.md#mothor)
- Also the maps "Agrawos" and "Sunny Beach" have been added
- Weather influencing effectivities has been added
- Added notifications
- Ingame time was added:
	+ Day and Night active Poketes
	+ A clock
	+ Time stops after a certain period of idling
- Treats and the Pokete-Care where added to make leveling easier
- The game is now available as an AppImage
- The newly added natures now influence a Poketes stats on an individual basis

[This](https://lxgr-linux.github.io/posts/pokete_1/) article summarises the changes further.

Again very special thanks to @MaFeLP for supporting me!

## [0.6.0] - 2021-11-09

What changed until this release?
- Added [Diamondos](wiki.md#diamondos), [Dia stab](wiki.md#dia-stab), [Dazzle](wiki.md#dazzle), [Dia spikes](wiki.md#dia-spikes)
- Added [Megapois](wiki.md#megapois), [Poison thorn](wiki.md#poison-thorn)
- Added [Dicko](wiki.md#dicko), [Lil nut](wiki.md#lil-nut)
- Added [Mowcow](wiki.md#mowcow), [Supercow power](wiki.md#supercow-power)
- Added [Wheeto](wiki.md#wheeto), [Special smell](wiki.md#special-smell)
- Added Flowy Town, Mowcow Meadow, The Fields of Agrawos
- Reformated files
- Added Github pages, special thanks to MaFeLP
- Added validation action
- Made the savefile json
- Added subtypes to better organise generic attacks
- Added Devguide
- Added modloader
- Added .editorconfig
- Added Pipfile and Pipfile.lock
- Overhauled Roadmap
- Added multipage wiki
- Completely rewrote gen_wiki.py
- Reformated, moved, outsourced, chnages a lot of code
Again special thanks to MaFeLP


## [0.5.1] - 2021-09-19

Some minor changes due to API changes in scrap_engine v1.0.0.
scrap_engine v1.0.0 is now required.


## [0.5.0] - 2021-09-10

What changed until this release?
- Improve Help
- Added CODENAME: Grey Edition
- Now unvisited maps names are not displayed in Roadmap anymore
- Added question when exiting
- Added startuptime to savefile
- Added Route 7
- Added coloured Minimap
- Added [Spikes](wiki.md#spikes), [Bubble gun](wiki.md#bubble-gun), [Flame throw](wiki.md#flame-throw), [Toe breaker](wiki.md#toe-breaker), [Wind blow](wiki.md#wind-blow), [Storm gust](wiki.md#storm-gust), [Rock smash](wiki.md#rock-smash)
- Added [Dicki](wiki.md#dicki), [Dick energy](wiki.md#dick-energy), [Ground hit](wiki.md#ground-hit), [Hiding](wiki.md#hiding)
- Added [Schmetterling](wiki.md#Schmetterling), [Schmetter](wiki.md#schmetter)
- Added abbility to learn a new attack very fifth level
- Added second type
- Added savable attacks
- Added [Poison](wiki.md#types) Type
- Added Learn Discs that can be used to teach new attack to Poketes
- Added abilities
- Added flying
- scrap_engine v0.3.3 is now needed


## [0.4.1] - 2021-08-08

What changed until this release?
- Added [EffectFreezing](wiki.md#freezing)
- Added ice Poketes ([Cubl](wiki.md#cubl), [Spikl](wiki.md#spikl)) and attacks ([freeze](wiki.md#freeze), [Snow storm](wiki.md#snow-storm), [Sword of ice](wiki.md#sword-of-ice))
- Added some more new Poketes ([Confuso](wiki.md#confuso), [Poisopla](wiki.md#poisopla)) and attacks ([Confusion](wiki.md#confusion), [Posion spores](wiki.md#poison-spores), [Root slap](wiki.md#root-slap))
- Added shiny Poketes
- Outsourced all map information to maps.py
- Added version checking to warn about data loss when downgrading
- Sorted the Poketes and attacks in the wiki by types
- Fixed the effectivity of [EffectBurning](wiki.md#burning)
- Fixed logic bug in most effects, so that some types are not affected by some effects
- Added Pokete dex for the user to keep track of all Pokete 'races' they have ever caught regardless of wether or not the Poketes are in the deck or not
- Cleaned up save file to be more readable for humans
- Changed development flow


## [0.4.0] - 2021-08-01

What changed until this release?
- Added confirmation for running away
- Made playmap_1 way easier
- Changed attack list to start with 1 and not 0
- Renamed attacs to attacks
- Added several new attacks
- Added several new moves (downgrade...)
- Added Rock-ville
- Added new mechanic that moves movemap to ensure all text fits on movemap
- Fixed bug with exclamations out of movemap
- Added support for more than one move per attack
- Increased attack AP to avoid running back to the Pokete-center as often
- Changed roadmap mechanism
- Added effects
- Added coloured output for OutP (scrap_engine >= v0.3.1 is now needed)
- Fixed bug with saving in shops
- Fixed bug with moves when confused
- Outsourced general-use functions
- Made some functions a class
- Made some other quality of life changes


## [0.3.8] - 2021-07-07

What changed until this release?
- Added coloured type tags and attack labels
- Added ice type
- Added about
- Added a now Pokete
- Made some minor fixes and changes


## [0.3.7] - 2021-06-30

What changed until this release?
- Added trading with other players in the same network
- Simplified some code


## [0.3.6] - 2021-06-28

What changed until this release?
- scrap_engine 0.3.0 in now needed
- Added initiative attribute for Poketes to determine which Pokete attacks first
- Several minor fixed and additions

## [0.3.5] - 2021-06-25

What changed until this release?
- Compatibility with scrap_engine 0.2.0
- Added validation for pokete_data
- Added Intro

## [0.3.4] - 2021-06-21

What changed until this release?
- Added Changelog.md
- Added Route 6, bigmountain see and bigmountain cave
- Improved wiki.md
- Added Wolfiro
- Added saving Poketeballs
- Added some new attacks
- Fixed some bugs

## [0.3.3] - 2021-06-15

What changed until this release?
- Trainers are now more likely to use effective attacks
- Added autosave
- Added a proper settings system
- Added undead type
- Added some new Poketes and attacks
- Added HowToPlay.md
- Added trainer saving
- Added Route 5
- Added confirmation texts when doing sensible stuff
- Moved some stuff around
- Fixed some bugs

## [0.3.2] - 2021-06-08

What changed until this release?
- Added route 3
- Added route 4
- Added Deepest forest
- minor fixes
- Added pics
- Fixed some values
- Fixed some bugs with trainers

## [0.3.1] - 2021-06-04

What changed until this release?
- Added Abandoned village
- Added clampi
- Added more NPCs
- Added .desktop (MaFeLP) and logo
- Made additions to the item system

## [0.3.0] - 2021-05-30

This is the first real release of Pokete, because at this point most of the key game mechanics are implemented and most stuff that's still missing is just game content.
