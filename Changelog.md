0.6.1
------
Test release

0.6.0
------
released: 2021-11-09

What changed until this release?
- Added [Diamondos](./wiki#diamondos), [Dia stab](./wiki#dia-stab), [Dazzle](./wiki#dazzle), [Dia spikes](./wiki#dia-spikes)
- Added [Megapois](./wiki#megapois), [Poison thorn](./wiki#poison-thorn)
- Added [Dicko](./wiki#dicko), [Lil nut](./wiki#lil-nut)
- Added [Mowcow](./wiki#mowcow), [Supercow power](./wiki#supercow-power)
- Added [Wheeto](./wiki#wheeto), [Special smell](./wiki#special-smell)
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


0.5.1
------
released: 2021-09-19

Some minor changes due to API changes in scrap_engine v1.0.0.
scrap_engine v1.0.0 is now required.


0.5.0
------
released: 2021-09-10

What changed until this release?
- Improve Help
- Added CODENAME: Grey Edition
- Now unvisited maps names are not displayed in Roadmap anymore
- Added question when exiting
- Added startuptime to savefile
- Added Route 7
- Added coloured Minimap
- Added [Spikes](./wiki#spikes), [Bubble gun](./wiki#bubble-gun), [Flame throw](./wiki#flame-throw), [Toe breaker](./wiki#toe-breaker), [Wind blow](./wiki#wind-blow), [Storm gust](./wiki#storm-gust), [Rock smash](./wiki#rock-smash)
- Added [Dicki](./wiki#dicki), [Dick energy](./wiki#dick-energy), [Ground hit](./wiki#ground-hit), [Hiding](./wiki#hiding)
- Added [Schmetterling](./wiki#Schmetterling), [Schmetter](./wiki#schmetter)
- Added abbility to learn a new attack very fifth level
- Added second type
- Added savable attacks
- Added [Poison](./wiki#types) Type
- Added Learn Discs that can be used to teach new attack to Poketes
- Added abilities
- Added flying
- scrap_engine v0.3.3 is now needed


0.4.1
------
released: 2021-08-08

What changed until this release?
- Added [EffectFreezing](./wiki#freezing)
- Added ice Poketes ([Cubl](./wiki#cubl), [Spikl](./wiki#spikl)) and attacks ([freeze](./wiki#freeze), [Snow storm](./wiki#snow-storm), [Sword of ice](./wiki#sword-of-ice))
- Added some more new Poketes ([Confuso](./wiki#confuso), [Poisopla](./wiki#poisopla)) and attacks ([Confusion](./wiki#confusion), [Posion spores](./wiki#poison-spores), [Root slap](./wiki#root-slap))
- Added shiny Poketes
- Outsourced all map information to maps.py
- Added version checking to warn about data loss when downgrading
- Sorted the Poketes and attacks in the wiki by types
- Fixed the effectivity of [EffectBurning](./wiki#burning)
- Fixed logic bug in most effects, so that some types are not affected by some effects
- Added Pokete dex for the user to keep track of all Pokete 'races' they have ever caught regardless of wether or not the Poketes are in the deck or not
- Cleaned up save file to be more readable for humans
- Changed development flow


0.4.0
------
released: 2021-08-01

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


0.3.8
-------
released: 2021-07-07

What changed until this release?
- Added coloured type tags and attack labels
- Added ice type
- Added about
- Added a now Pokete
- Made some minor fixes and changes


0.3.7
-------
released: 2021-06-30

What changed until this release?
- Added trading with other players in the same network
- Simplified some code


0.3.6
-------
released: 2021-06-28

What changed until this release?
- scrap_engine 0.3.0 in now needed
- Added initiative attribute for Poketes to determine which Pokete attacks first
- Several minor fixed and additions

0.3.5
-------
released: 2021-06-25

What changed until this release?
- Compatibility with scrap_engine 0.2.0
- Added validation for pokete_data
- Added Intro

0.3.4
-------
released: 2021-06-21

What changed until this release?
- Added Changelog.md
- Added Route 6, bigmountain see and bigmountain cave
- Improved wiki.md
- Added Wolfiro
- Added saving Poketeballs
- Added some new attacks
- Fixed some bugs

0.3.3
-------
released: 2021-06-15

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

0.3.2
-------
released: 2021-06-08

What changed until this release?
- Added route 3
- Added route 4
- Added Deepest forest
- minor fixes
- Added pics
- Fixed some values
- Fixed some bugs with trainers

0.3.1
-------
released: 2021-06-04

What changed until this release?
- Added Abandoned village
- Added clampi
- Added more NPCs
- Added .desktop (MaFeLP) and logo
- Made additions to the item system

0.3.0
-------
released: 2021-05-30

This is the first real release of Pokete, because at this point most of the key game mechanics are implemented and most stuff that's still missing is just game content.
