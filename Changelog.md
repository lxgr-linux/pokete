0.4.1
------
released: 2021-08-08

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
