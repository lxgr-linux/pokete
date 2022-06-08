v0.7.2

# Pokete wiki
This wiki/documentation is a compilation of all Poketes/attacks/types present in the Pokete game.
This wiki can be generated using ```$ ./gen_wiki.py```.

Use ```$./gen_wiki.py help``` to get more information about different wikis.

You can find different versions of this wiki:

- A single-page version can be found [here](wiki.md)
- A multi-page version can be found [here](https://lxgr-linux.github.io/pokete/wiki-multi/)

## Table of contents
1. [Poketes](#poketes)
   1. [Electro Poketes](#electro-poketes)
       1. [Electrode](#electrode)
   2. [Fire Poketes](#fire-poketes)
       1. [Wolfior](#wolfior)
       2. [Wolfiro](#wolfiro)
   3. [Flying Poketes](#flying-poketes)
       1. [Bato](#bato)
       2. [Bator](#bator)
       3. [Mothor](#mothor)
       4. [Ostri](#ostri)
       5. [Owol](#owol)
       6. [Schmetterling](#schmetterling)
       7. [Vogli](#vogli)
       8. [Voglo](#voglo)
       9. [Voglus](#voglus)
   4. [Ground Poketes](#ground-poketes)
       1. [Corcos day](#corcos-day)
       2. [Corcos night](#corcos-night)
       3. [Dicki](#dicki)
       4. [Dicko](#dicko)
       5. [Lil nut](#lil-nut)
       6. [Raupathor day](#raupathor-day)
       7. [Raupathor night](#raupathor-night)
       8. [Rollator](#rollator)
   5. [Ice Poketes](#ice-poketes)
       1. [Cubl](#cubl)
       2. [Spikl](#spikl)
   6. [Normal Poketes](#normal-poketes)
       1. [Hornita](#hornita)
       2. [Horny](#horny)
       3. [Mowcow](#mowcow)
       4. [Ratatat](#ratatat)
       5. [Rato](#rato)
   7. [Plant Poketes](#plant-poketes)
       1. [Bushy](#bushy)
       2. [Megapois](#megapois)
       3. [Poisopla](#poisopla)
       4. [Rosi](#rosi)
       5. [Treenator](#treenator)
       6. [Wheeto](#wheeto)
   8. [Poison Poketes](#poison-poketes)
       1. [Choka](#choka)
       2. [Würgos](#würgos)
   9. [Stone Poketes](#stone-poketes)
       1. [Bigstone](#bigstone)
       2. [Diamondos](#diamondos)
       3. [Lilstone](#lilstone)
       4. [Poundi](#poundi)
       5. [Steini](#steini)
   10. [Undead Poketes](#undead-poketes)
       1. [Angrilo](#angrilo)
       2. [Confuso](#confuso)
       3. [Gobost](#gobost)
       4. [Saugh](#saugh)
   11. [Water Poketes](#water-poketes)
       1. [Blub](#blub)
       2. [Clampi](#clampi)
       3. [Crabbat](#crabbat)
       4. [Karpi](#karpi)
       5. [Rustacean](#rustacean)
2. [Attacks](#attacks)
   1. [Electro attacks](#electro-attacks)
       1. [Charging](#charging)
       2. [Mega arch](#mega-arch)
       3. [Shock](#shock)
   2. [Fire attacks](#fire-attacks)
       1. [Ash throw](#ash-throw)
       2. [Fire ball](#fire-ball)
       3. [Fire bite](#fire-bite)
       4. [Flame throw](#flame-throw)
   3. [Flying attacks](#flying-attacks)
       1. [Brooding](#brooding)
       2. [Eye pick](#eye-pick)
       3. [Flying](#flying)
       4. [Pick](#pick)
       5. [Power pick](#power-pick)
       6. [Schmetter](#schmetter)
       7. [Storm gust](#storm-gust)
       8. [Wind blow](#wind-blow)
       9. [Wing hit](#wing-hit)
   4. [Ground attacks](#ground-attacks)
       1. [Dick energy](#dick-energy)
       2. [Earch quake](#earch-quake)
       3. [Ground hit](#ground-hit)
       4. [Hiding](#hiding)
       5. [Power roll](#power-roll)
       6. [Toe Breaker](#toe-breaker)
   5. [Ice attacks](#ice-attacks)
       1. [Freeze](#freeze)
       2. [Snow storm](#snow-storm)
       3. [Spikes](#spikes)
       4. [Sword of ice](#sword-of-ice)
   6. [Normal attacks](#normal-attacks)
       1. [Bite](#bite)
       2. [Choker](#chocer)
       3. [Cry](#cry)
       4. [Meat skewer](#meat-skewer)
       5. [Power bite](#power-bite)
       6. [Snooze](#snooze)
       7. [Supercow power](#supercow-power)
       8. [Tackle](#tackle)
       9. [Tail wipe](#tail-wipe)
   7. [Plant attacks](#plant-attacks)
       1. [Apple drop](#apple-drop)
       2. [Bark hardening](#bark-hardening)
       3. [Branch stab](#branch-stab)
       4. [Leaf storm](#leaf-storm)
       5. [Poison spores](#poison-spores)
       6. [Root slap](#root-slap)
       7. [Root strangler](#root-strangler)
       8. [Special smell](#special-smell)
       9. [Sucker](#sucker)
       10. [Super sucker](#super-sucker)
       11. [The old roots hit](#the-old-roots-hit)
   8. [Poison attacks](#poison-attacks)
       1. [Poison bite](#poison-bite)
       2. [Poison thorn](#poison-thorn)
   9. [Stone attacks](#stone-attacks)
       1. [Brick throw](#brick-throw)
       2. [Dazzle](#dazzle)
       3. [Dia spikes](#dia-spikes)
       4. [Dia stab](#dia-stab)
       5. [Pepple fire](#pepple-fire)
       6. [Politure](#politure)
       7. [Rock smash](#rock-smash)
       8. [Sand throw](#sand-throw)
   10. [Undead attacks](#undead-attacks)
       1. [Confusion](#confusion)
       2. [Heart touch](#heart-touch)
       3. [Mind blow](#mind-blow)
   11. [Water attacks](#water-attacks)
       1. [Bubble bomb](#bubble-bomb)
       2. [Bubble gun](#bubble-gun)
       3. [Bubble shield](#bubble-shield)
       4. [Shell pinch](#shell-pinch)
       5. [Wet slap](#wet-slap)
3. [Types](#types)
4. [Items](#items)
   1. [AP potion](#ap-potion)
   2. [Healing potion](#healing-potion)
   3. [Hyperball](#hyperball)
   4. [Poketeball](#poketeball)
   5. ['Shut the fuck up' stone](#shut-the-fuck-up-stone)
   6. [Super potion](#super-potion)
   7. [Superball](#superball)
   8. [Treat](#treat)
5. [Effects](#effects)
   1. [Paralyzation](#paralyzation)
   2. [Sleep](#sleep)
   3. [Burning](#burning)
   4. [Poison](#poison)
   5. [Confusion](#confusion)
   6. [Freezing](#freezing)

## Poketes
In the following all Poketes with their attributes are displayed.

### Electro Poketes
#### Electrode
A small floating ball that will give you a shock.

```
           
    (+)    
           
           

```

- Type: [Electro](#types)
- Health points: 20
- Attack factor: 5
- Defense factor: 2
- Initiative: 4
- Missing chance: 0
- Rarity: 0.8
- Loosing experience: 3
- Attacks:
   + [Shock](#shock)
   + [Charging](#charging)
   + [Mega arch](#mega-arch)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve

### Fire Poketes
#### Wolfior
A fiery wolf straight from hell, that likes to burn 11 years old butts of.

```
   ^---^   
   (* *)   
   >(.)<   
           

```

- Type: [Fire](#types)
- Health points: 20
- Attack factor: 6
- Defense factor: 3
- Initiative: 4
- Missing chance: 0
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Fire bite](#fire-bite)
   + [Ash throw](#ash-throw)
- Active: Always
- Can be found in:
   + Route 1
   + Sunnydale
   + Sunnydale Lake
   + Route 3
- Evolves to [Wolfiro](#wolfiro) at level 25

#### Wolfiro
A fiery wolf from hell on steroids.

```
   \^-^/   
   {* *}   
   >{.}<   
           

```

- Type: [Fire](#types)
- Health points: 25
- Attack factor: 7
- Defense factor: 4
- Initiative: 5
- Missing chance: 0
- Rarity: 1
- Loosing experience: 4
- Attacks:
   + [Tackle](#tackle)
   + [Fire bite](#fire-bite)
   + [Ash throw](#ash-throw)
   + [Fire ball](#fire-ball)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve

### Flying Poketes
#### Bato
An annoying flying rat.

```
    ___    
WW\/* *\/WW
   \v-v/   
           

```

- Type: [Flying](#types)
- Health points: 20
- Attack factor: 3
- Defense factor: 1
- Initiative: 6
- Missing chance: 0
- Rarity: 1.3
- Loosing experience: 3
- Attacks:
   + [Bite](#bite)
   + [Cry](#cry)
- Active: Always
- Can be found in:
   + Nice Town cave
   + Mysterious cave
   + Dark cave
   + Big mountain cave
- Evolves to [Bator](#bator) at level 20

#### Bator
A chongus flying rat.

```
    ___    
WW\/o o\/WW
   |v-v|   
   \___/   

```

- Type: [Flying](#types)
- Health points: 25
- Attack factor: 4
- Defense factor: 2
- Initiative: 8
- Missing chance: 0
- Rarity: 0.2
- Loosing experience: 4
- Attacks:
   + [Bite](#bite)
   + [Cry](#cry)
   + [Poison bite](#poison-bite)
   + [Wing hit](#wing-hit)
- Active: Always
- Can be found in:
   + Mysterious cave
- Does not evolve


#### Mothor
A dark butterfly that will schmetter you away.

```
 .__`o´__. 
  \_\|/_/  
  /_/'\_\  
 ´       ` 

```

- Type: [Flying](#types)
- Health points: 20
- Attack factor: 6
- Defense factor: 2
- Initiative: 4
- Missing chance: 0.1
- Rarity: 1
- Loosing experience: 4
- Attacks:
   + [Schmetter](#schmetter)
   + [Wing hit](#wing-hit)
- Active: Night
- Can be found in:
   + Nowhere
- Does not evolve


#### Ostri
A very aggressive bird Pokete that lives near deserts and will try to pick out your eyes.

```
   !       
  >´)      
    \www'  
     ||    

```

- Type: [Flying](#types)
- Health points: 20
- Attack factor: 8
- Defense factor: 0
- Initiative: 7
- Missing chance: 0
- Rarity: 0.6
- Loosing experience: 4
- Attacks:
   + [Tackle](#tackle)
   + [Eye pick](#eye-pick)
   + [Brooding](#brooding)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve


#### Owol
A night active Pokete, that is looking for lil children as a midnight snack.

```
   ,___,   
   {o,o}   
   /)_)    
    ""     

```

- Type: [Flying](#types)
- Health points: 20
- Attack factor: 7
- Defense factor: 2
- Initiative: 3
- Missing chance: 0
- Rarity: 0.5
- Loosing experience: 2
- Attacks:
   + [Pick](#pick)
   + [Wing hit](#wing-hit)
   + [Cry](#cry)
- Active: Night
- Can be found in:
   + Abandoned village
   + Route 3
   + Route 4
   + Deepens forest
   + Route 5
   + Route 6
- Does not evolve


#### Schmetterling
A butterfly that will schmetter you away.

```
 .__ o __. 
  \_\|/_/  
  /_/'\_\  
           

```

- Type: [Flying](#types)
- Health points: 20
- Attack factor: 5
- Defense factor: 2
- Initiative: 4
- Missing chance: 0.1
- Rarity: 1
- Loosing experience: 3
- Attacks:
   + [Schmetter](#schmetter)
   + [Wing hit](#wing-hit)
- Active: Day
- Can be found in:
   + Nowhere
- Does not evolve


#### Vogli
A very common bird Pokete that lives everywhere.

```
    A      
   <')     
    www*   
    ||     

```

- Type: [Flying](#types)
- Health points: 20
- Attack factor: 6
- Defense factor: 1
- Initiative: 6
- Missing chance: 0
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Power pick](#power-pick)
- Active: Always
- Can be found in:
   + Nice Town
   + Route 4
   + Deepens forest
- Evolves to [Voglo](#voglo) at level 20

#### Voglo
A very aggressive bird Pokete that can only be found in the woods.

```
    ?      
   >´)     
    www*   
    ||     

```

- Type: [Flying](#types)
- Health points: 20
- Attack factor: 7
- Defense factor: 1
- Initiative: 7
- Missing chance: 0
- Rarity: 0.8
- Loosing experience: 3
- Attacks:
   + [Tackle](#tackle)
   + [Power pick](#power-pick)
   + [Wing hit](#wing-hit)
   + [Brooding](#brooding)
- Active: Always
- Can be found in:
   + Route 1
   + Sunnydale
   + Sunnydale Lake
   + Route 2
   + Route 3
   + Route 4
   + Deepens forest
   + Route 5
   + Route 6
   + Mowcow meadow
   + The fields of Agrawos
   + Agrawos
- Evolves to [Voglus](#voglus) at level 35

#### Voglus
A very aggressive and hard to find bird Pokete.

```
    /      
   >´}     
    WWW'   
    ||     

```

- Type: [Flying](#types)
- Health points: 25
- Attack factor: 9
- Defense factor: 3
- Initiative: 8
- Missing chance: 0
- Rarity: 0.2
- Loosing experience: 5
- Attacks:
   + [Tackle](#tackle)
   + [Power pick](#power-pick)
   + [Storm gust](#storm-gust)
   + [Brooding](#brooding)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve

### Ground Poketes
#### Corcos day
A small heavy thing, that can be found on the ground, but that may reveal something wonderful later.

```
           
    |\     
    |'\    
    \_|    

```

- Type: [Ground](#types)
- Health points: 15
- Attack factor: 2
- Defense factor: 5
- Initiative: 1
- Missing chance: 0
- Rarity: 1
- Loosing experience: 1
- Attacks:
   + [Tackle](#tackle)
   + [Hiding](#hiding)
- Active: Day
- Can be found in:
   + Abandoned village
- Evolves to [Raupathor day](#raupathor_day) at level 20

#### Corcos night
A small heavy thing, that can be found on the ground, but that may reveal something wonderful later.

```
           
    |\     
    |'\    
    \_|    

```

- Type: [Ground](#types)
- Health points: 15
- Attack factor: 2
- Defense factor: 5
- Initiative: 1
- Missing chance: 0
- Rarity: 1
- Loosing experience: 1
- Attacks:
   + [Tackle](#tackle)
   + [Hiding](#hiding)
- Active: Night
- Can be found in:
   + Abandoned village
- Evolves to [Raupathor night](#raupathor_night) at level 20

#### Dicki
A little what ever, that sticks out of the ground.

```
           
    __     
   ('')    
   |  |    

```

- Type: [Ground](#types)
- Health points: 20
- Attack factor: 2
- Defense factor: 4
- Initiative: 2
- Missing chance: 0.1
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Dick energy](#dick-energy)
   + [Hiding](#hiding)
   + [Ground hit](#ground-hit)
- Active: Always
- Can be found in:
   + Nowhere
- Evolves to [Dicko](#dicko) at level 55

#### Dicko
An even bigger what ever, that sticks out of the ground.

```
    __     
   ('')    
   |  |    
   |  |    

```

- Type: [Ground](#types)
- Health points: 25
- Attack factor: 3
- Defense factor: 5
- Initiative: 3
- Missing chance: 0.1
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Dick energy](#dick-energy)
   + [Hiding](#hiding)
   + [Ground hit](#ground-hit)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve


#### Lil nut
A very small what ever, that sticks out of the ground.

```
           
           
    __     
   ('')    

```

- Type: [Ground](#types)
- Health points: 20
- Attack factor: 1
- Defense factor: 3
- Initiative: 1
- Missing chance: 0.1
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Ground hit](#ground-hit)
- Active: Always
- Can be found in:
   + The fields of Agrawos
- Evolves to [Dicki](#dicki) at level 35

#### Raupathor day
A small caterpillar found on leafs.

```
           
  .__.__.  
 ()__)__)}´
  '  '  '  

```

- Type: [Ground](#types)
- Health points: 20
- Attack factor: 3
- Defense factor: 4
- Initiative: 3
- Missing chance: 0.1
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Hiding](#hiding)
- Active: Day
- Can be found in:
   + Route 7
- Evolves to [Schmetterling](#schmetterling) at level 30

#### Raupathor night
A small caterpillar found on leafs.

```
           
  .__.__.  
 ()__)__)}´
  '  '  '  

```

- Type: [Ground](#types)
- Health points: 20
- Attack factor: 3
- Defense factor: 4
- Initiative: 3
- Missing chance: 0.1
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Hiding](#hiding)
- Active: Night
- Can be found in:
   + Route 7
- Evolves to [Mothor](#mothor) at level 30

#### Rollator
A big chunk of stone and dirt, that roles around.

```
   _____   
  / o o \  
  | ___ |  
  \_____/  

```

- Type: [Ground](#types)
- Health points: 25
- Attack factor: 2
- Defense factor: 5
- Initiative: 3
- Missing chance: 0
- Rarity: 0.5
- Loosing experience: 3
- Attacks:
   + [Tackle](#tackle)
   + [Power roll](#power-roll)
- Active: Always
- Can be found in:
   + Route 2
   + Dark cave
   + Big mountain see
- Does not evolve

### Ice Poketes
#### Cubl
A small ice cube.

```
  /-----\  
   |* *|   
  \-----/  
           

```

- Type: [Ice](#types)
- Health points: 20
- Attack factor: 3
- Defense factor: 3
- Initiative: 1
- Missing chance: 0.1
- Rarity: 1.2
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Freeze](#freeze)
   + [Snow storm](#snow-storm)
- Active: Always
- Can be found in:
   + Nowhere
- Evolves to [Spikl](#spikl) at level 30

#### Spikl
A block of ice.

```
 /-------\ 
  | * * |  
 \-------/ 
           

```

- Type: [Ice](#types)
- Health points: 25
- Attack factor: 4
- Defense factor: 4
- Initiative: 2
- Missing chance: 0.1
- Rarity: 0.9
- Loosing experience: 4
- Attacks:
   + [Tackle](#tackle)
   + [Freeze](#freeze)
   + [Snow storm](#snow-storm)
   + [Sword of ice](#sword-of-ice)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve

### Normal Poketes
#### Hornita
An majestic horse that is always looking for something to pick with its horn.

```
 \         
 =')~      
   (¯¯¯¯)~ 
   //¯¯\\  

```

- Type: [Normal](#types)
- Health points: 20
- Attack factor: 6
- Defense factor: 2
- Initiative: 3
- Missing chance: 0
- Rarity: 1
- Loosing experience: 3
- Attacks:
   + [Tackle](#tackle)
   + [Meat skewer](#meat-skewer)
   + [Tail wipe](#tail-wipe)
- Active: Always
- Can be found in:
   + Route 1
   + Sunnydale
   + Sunnydale Lake
   + Route 5
   + Route 6
- Does not evolve


#### Horny
A teenage unicorn in the middle of puberty.

```
  ,        
 =')       
   (¯¯¯)~  
   //¯\\   

```

- Type: [Normal](#types)
- Health points: 20
- Attack factor: 5
- Defense factor: 1
- Initiative: 4
- Missing chance: 0.2
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Meat skewer](#meat-skewer)
- Active: Always
- Can be found in:
   + Nice Town
- Evolves to [Hornita](#hornita) at level 20

#### Mowcow
A cow-like creature found on meadows.

```
    ^__^   
    (oo)   
    (__)   
           

```

- Type: [Normal](#types)
- Health points: 20
- Attack factor: 2
- Defense factor: 3
- Initiative: 2
- Missing chance: 0
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
- Active: Always
- Can be found in:
   + Mowcow meadow
   + The fields of Agrawos
   + Agrawos
- Does not evolve


#### Ratatat
A damn dangerous and enourmous rat, that will bite of your leg.

```
   ^---^   
   \* */   
   >VvV<   
    ^^^    

```

- Type: [Normal](#types)
- Health points: 25
- Attack factor: 7
- Defense factor: 3
- Initiative: 7
- Missing chance: 0
- Rarity: 0.7
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Tail wipe](#tail-wipe)
   + [Power bite](#power-bite)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve


#### Rato
An annoying rat.

```
   ^---^   
   \o o/   
   >\./<   
           

```

- Type: [Normal](#types)
- Health points: 20
- Attack factor: 4
- Defense factor: 2
- Initiative: 6
- Missing chance: 0
- Rarity: 1.3
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Tail wipe](#tail-wipe)
- Active: Always
- Can be found in:
   + Nice Town
   + Nice Town cave
   + Route 1
   + Sunnydale
   + Sunnydale Lake
   + Abandoned house
   + Route 4
   + Deepens forest
   + Big mountain see
- Evolves to [Ratatat](#ratatat) at level 25
### Plant Poketes
#### Bushy
A bush, and just a bush. But watch out!

```
           
    (()    
   (()))   
           

```

- Type: [Plant](#types)
- Health points: 25
- Attack factor: 2
- Defense factor: 1
- Initiative: 1
- Missing chance: 0
- Rarity: 1
- Loosing experience: 1
- Attacks:
   + [Tackle](#tackle)
   + [Bark hardening](#bark-hardening)
- Active: Always
- Can be found in:
   + Route 2
   + Route 7
   + Mowcow meadow
- Evolves to [Treenator](#treenator) at level 20

#### Megapois
A very unsuspicious plant.

```
    w w    
  w |/.    
.__\|/|    
 \_\||/    

```

- Type: [Plant](#types)
- Health points: 25
- Attack factor: 3
- Defense factor: 5
- Initiative: 2
- Missing chance: 0.1
- Rarity: 0.9
- Loosing experience: 6
- Attacks:
   + [Root slap](#root-slap)
   + [Poison spores](#poison-spores)
   + [Leaf storm](#leaf-storm)
   + [Poison thorn](#poison-thorn)
- Active: Always
- Can be found in:
   + The fields of Agrawos
   + Agrawos
- Does not evolve


#### Poisopla
A unsuspicious plant.

```
           
     w .   
 .__ |/|   
  \_\||/   

```

- Type: [Plant](#types)
- Health points: 20
- Attack factor: 3
- Defense factor: 3
- Initiative: 1
- Missing chance: 0.1
- Rarity: 0.9
- Loosing experience: 6
- Attacks:
   + [Root slap](#root-slap)
   + [Poison spores](#poison-spores)
   + [Leaf storm](#leaf-storm)
- Active: Always
- Can be found in:
   + Route 7
- Evolves to [Megapois](#megapois) at level 20

#### Rosi
A plant Pokete, that's often mistaken for a normal flower.

```
           
    (@)    
     |     
    \|/    

```

- Type: [Plant](#types)
- Health points: 20
- Attack factor: 0
- Defense factor: 1
- Initiative: 3
- Missing chance: 0
- Rarity: 0.8
- Loosing experience: 2
- Attacks:
   + [Sucker](#sucker)
   + [Super sucker](#super-sucker)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve


#### Treenator
A scary an dangerous apple tree.

```
    (()    
   (()))   
     H     
     H     

```

- Type: [Plant](#types)
- Health points: 25
- Attack factor: 2
- Defense factor: 2
- Initiative: 2
- Missing chance: 0
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Apple drop](#apple-drop)
   + [Bark hardening](#bark-hardening)
   + [Branch stab](#branch-stab)
   + [Root strangler](#root-strangler)
- Active: Always
- Can be found in:
   + Route 7
- Does not evolve


#### Wheeto
A plant Pokete found in Agrawos, with special 'Powers'.

```
    \ /    
    \|/    
    \|/    
     |     

```

- Type: [Plant](#types)
- Health points: 20
- Attack factor: 3
- Defense factor: 2
- Initiative: 2
- Missing chance: 0.1
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Root slap](#root-slap)
   + [Special smell](#special-smell)
- Active: Always
- Can be found in:
   + Agrawos
- Does not evolve

### Poison Poketes
#### Choka
A fucking dangerous and enormous snake Pokete.

```
 _______   
/____ * \  
 (   \   \ 
\______   \

```

- Type: [Poison](#types)
- Health points: 25
- Attack factor: 5
- Defense factor: 1
- Initiative: 4
- Missing chance: 0
- Rarity: 0.5
- Loosing experience: 4
- Attacks:
   + [Choker](#chocer)
   + [Bite](#bite)
   + [Poison bite](#poison-bite)
   + [Power bite](#power-bite)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve


#### Würgos
A dangerous snake Pokete.

```
  >'({{{   
  }}}}}}}  
 {{{{{{{{{ 
           

```

- Type: [Poison](#types)
- Health points: 20
- Attack factor: 3
- Defense factor: 0
- Initiative: 3
- Missing chance: 0
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Choker](#chocer)
   + [Bite](#bite)
   + [Poison bite](#poison-bite)
- Active: Always
- Can be found in:
   + Route 5
   + Route 6
   + Big mountain see
   + Sunny Beach
- Evolves to [Choka](#choka) at level 30
### Stone Poketes
#### Bigstone
A big and heavy stone made from one of the hardest stones.

```
+---------+
|  o   o  |
|   ---   |
+---------+

```

- Type: [Stone](#types)
- Health points: 30
- Attack factor: 2
- Defense factor: 13
- Initiative: 5
- Missing chance: 0
- Rarity: 0.3
- Loosing experience: 5
- Attacks:
   + [Snooze](#snooze)
   + [Politure](#politure)
   + [Brick throw](#brick-throw)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve


#### Diamondos
A precious diamond, that can only be found in the darkest caves.

```
           
    /\^/   
   <o o>   
   <_-_>   

```

- Type: [Stone](#types)
- Health points: 20
- Attack factor: 2
- Defense factor: 15
- Initiative: 2
- Missing chance: 0.1
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Politure](#politure)
   + [Dazzle](#dazzle)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve


#### Lilstone
A small but powerful stone Pokete that lives in the mountains.

```
           
   _____   
   |'ᵕ'|   
   ‾‾‾‾‾   

```

- Type: [Stone](#types)
- Health points: 20
- Attack factor: 1
- Defense factor: 2
- Initiative: 3
- Missing chance: 0
- Rarity: 1
- Loosing experience: 2
- Attacks:
   + [Tackle](#tackle)
   + [Politure](#politure)
   + [Pepple fire](#pepple-fire)
- Active: Always
- Can be found in:
   + Nice Town cave
   + Dark cave
   + Big mountain cave
- Evolves to [Bigstone](#bigstone) at level 25

#### Poundi
A powerful and heavy stone Pokete that lives in mountain caves.

```
   A-A-A   
  < o o >  
  < --- >  
   VvVvV   

```

- Type: [Stone](#types)
- Health points: 25
- Attack factor: 2
- Defense factor: 3
- Initiative: 4
- Missing chance: 0
- Rarity: 0.7
- Loosing experience: 4
- Attacks:
   + [Tackle](#tackle)
   + [Politure](#politure)
   + [Earch quake](#earch-quake)
- Active: Always
- Can be found in:
   + Big mountain see
   + Big mountain cave
- Does not evolve


#### Steini
A squared stone that can casually be found on the ground.

```
 +-------+ 
 | o   o | 
 |  www  | 
 +-------+ 

```

- Type: [Stone](#types)
- Health points: 25
- Attack factor: 2
- Defense factor: 4
- Initiative: 5
- Missing chance: 0
- Rarity: 1
- Loosing experience: 3
- Attacks:
   + [Tackle](#tackle)
   + [Politure](#politure)
   + [Brick throw](#brick-throw)
- Active: Always
- Can be found in:
   + Nice Town cave
   + Route 1
   + Sunnydale
   + Sunnydale Lake
   + Mysterious cave
   + Route 2
   + Dark cave
   + Route 3
   + Big mountain cave
- Does not evolve

### Undead Poketes
#### Angrilo
A ghost Pokete that will scare your pants off.

```
 .░░░░░░░. 
 ░░\░░░/░░ 
 .░░( )░░. 
.         .

```

- Type: [Undead](#types)
- Health points: 25
- Attack factor: 3
- Defense factor: 2
- Initiative: 7
- Missing chance: 0
- Rarity: 0.6
- Loosing experience: 4
- Attacks:
   + [Tackle](#tackle)
   + [Mind blow](#mind-blow)
   + [Wet slap](#wet-slap)
   + [Heart touch](#heart-touch)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve


#### Confuso
A ball floating around in dark woods and caves, that will confuse the shit out of you.

```
       }}  
     _{{   
    (_)}   
           

```

- Type: [Undead](#types)
- Health points: 20
- Attack factor: 1
- Defense factor: 1
- Initiative: 2
- Missing chance: 0.1
- Rarity: 0.5
- Loosing experience: 6
- Attacks:
   + [Confusion](#confusion)
- Active: Always
- Can be found in:
   + Route 7
- Does not evolve


#### Gobost
A scary ghost Pokete that lives in caves and old houses.

```
 .░░░░░░░. 
 ░░o░░░o░░ 
 ░░░░░░░░░ 
 ░ ░ ░ ░ ░ 

```

- Type: [Undead](#types)
- Health points: 20
- Attack factor: 2
- Defense factor: 1
- Initiative: 6
- Missing chance: 0
- Rarity: 1
- Loosing experience: 3
- Attacks:
   + [Tackle](#tackle)
   + [Mind blow](#mind-blow)
   + [Heart touch](#heart-touch)
- Active: Always
- Can be found in:
   + Dark cave
   + Abandoned village
   + Abandoned house
   + Route 7
- Evolves to [Angrilo](#angrilo) at level 25

#### Saugh
The dark firy souls of those who got burned to death by the hot sun!

```
           
    .,     
  ,*..*.   
 ...,..,.  

```

- Type: [Undead](#types)
- Health points: 20
- Attack factor: 4
- Defense factor: 2
- Initiative: 5
- Missing chance: 1
- Rarity: 0.5
- Loosing experience: 4
- Attacks:
   + [Mind blow](#mind-blow)
   + [Fire ball](#fire-ball)
   + [Sand throw](#sand-throw)
- Active: Always
- Can be found in:
   + Sunny Beach
- Does not evolve

### Water Poketes
#### Blub
Very delicious and low fat water Pokete.

```
  _____    
 / o   \   
 >   v  >< 
 \_____/   

```

- Type: [Water](#types)
- Health points: 20
- Attack factor: 2
- Defense factor: 1
- Initiative: 1
- Missing chance: 0
- Rarity: 1
- Loosing experience: 5
- Attacks:
   + [Tackle](#tackle)
   + [Bubble bomb](#bubble-bomb)
   + [Bubble shield](#bubble-shield)
- Active: Always
- Can be found in:
   + Sunnydale Lake
   + Big mountain see
   + Rock-ville
   + Sunny Beach
- Does not evolve


#### Clampi
A shell that lives deep in the see or near bays, that's pretty hard to crack.

```
    ___    
  -/ * \-  
  -\___/-  
           

```

- Type: [Water](#types)
- Health points: 25
- Attack factor: 2
- Defense factor: 7
- Initiative: 3
- Missing chance: 0
- Rarity: 0.8
- Loosing experience: 5
- Attacks:
   + [Tackle](#tackle)
   + [Bubble bomb](#bubble-bomb)
   + [Shell pinch](#shell-pinch)
- Active: Always
- Can be found in:
   + Route 3
   + Big mountain see
   + Sunny Beach
- Evolves to [Crabbat](#crabbat) at level 20

#### Crabbat
A crusty Pokete that loves to pinch big toes.

```
 (  ___  ) 
  \-* *-/  
   ^   ^   
           

```

- Type: [Water](#types)
- Health points: 30
- Attack factor: 3
- Defense factor: 8
- Initiative: 4
- Missing chance: 0
- Rarity: 0.8
- Loosing experience: 5
- Attacks:
   + [Tackle](#tackle)
   + [Bubble gun](#bubble-gun)
   + [Earch quake](#earch-quake)
   + [Shell pinch](#shell-pinch)
- Active: Always
- Can be found in:
   + Sunny Beach
- Evolves to [Rustacean](#rustacean) at level 40

#### Karpi
A very harmless water Pokete that can be found everywhere.

```
           
           
  <°))))>< 
           

```

- Type: [Water](#types)
- Health points: 15
- Attack factor: 0
- Defense factor: 0
- Initiative: 0
- Missing chance: 0
- Rarity: 3
- Loosing experience: 1
- Attacks:
   + [Tackle](#tackle)
- Active: Always
- Can be found in:
   + Sunnydale Lake
   + Route 3
   + Big mountain see
   + Rock-ville
   + Sunny Beach
- Does not evolve


#### Rustacean
A crusty Pokete that will pinch your toe, and check whether or not you borrowed something.

```
 {  ^^^  } 
  \-* *-/  
   ^   ^   
           

```

- Type: [Water](#types)
- Health points: 35
- Attack factor: 4
- Defense factor: 9
- Initiative: 5
- Missing chance: 0
- Rarity: 0.5
- Loosing experience: 5
- Attacks:
   + [Toe Breaker](#toe-breaker)
   + [Bubble gun](#bubble-gun)
   + [Earch quake](#earch-quake)
   + [Shell pinch](#shell-pinch)
- Active: Always
- Can be found in:
   + Nowhere
- Does not evolve


## Attacks
Those are all attacks present in the game.

### Electro attacks
#### Shock
Gives the enemy a shock.

- Type: [Electro](#types)
- Minimum Level: 0
- Attack factor: 1.5
- Missing chance: 0.2
- Attack points: 30
- Effect: None

#### Charging
Charges the Pokete.

- Type: [Electro](#types)
- Minimum Level: 10
- Attack factor: 0
- Missing chance: 0
- Attack points: 15
- Effect: None

#### Mega arch
Gives the enemy heavy a shock.

- Type: [Electro](#types)
- Minimum Level: 15
- Attack factor: 5
- Missing chance: 0
- Attack points: 10
- Effect: [Paralyzation](#paralyzation)

### Fire attacks
#### Fire bite
Burns and bites the enemy at the same time.

- Type: [Fire](#types)
- Minimum Level: 0
- Attack factor: 2
- Missing chance: 0.2
- Attack points: 15
- Effect: [Burning](#burning)

#### Ash throw
Throws ashes in the enemy's eyes.

- Type: [Fire](#types)
- Minimum Level: 15
- Attack factor: 0.5
- Missing chance: 0
- Attack points: 15
- Effect: None

#### Flame throw
Hans get ze Flammenwerfer!

- Type: [Fire](#types)
- Minimum Level: 15
- Attack factor: 2.5
- Missing chance: 0
- Attack points: 10
- Effect: [Burning](#burning)

#### Fire ball
Casts a fireball at the enemy.

- Type: [Fire](#types)
- Minimum Level: 25
- Attack factor: 4
- Missing chance: 0
- Attack points: 10
- Effect: None

### Flying attacks
#### Flying
Gives the Pokete the abbility to fly you around.

- Type: [Flying](#types)
- Minimum Level: 0
- Attack factor: 1.5
- Missing chance: 0.1
- Attack points: 30
- Effect: None

#### Pick
A pick at the enemy's weakest spot.

- Type: [Flying](#types)
- Minimum Level: 0
- Attack factor: 1.7
- Missing chance: 0.1
- Attack points: 30
- Effect: None

#### Wind blow
Casts a wind blow at the enemy.

- Type: [Flying](#types)
- Minimum Level: 0
- Attack factor: 2
- Missing chance: 0
- Attack points: 20
- Effect: None

#### Storm gust
Casts a strong and fast storm gust full of rain and hail that hits the enemy at it's weakest spots and makes it wanting to die.

- Type: [Flying](#types)
- Minimum Level: 0
- Attack factor: 6
- Missing chance: 0
- Attack points: 10
- Effect: None

#### Schmetter
Schmetters the enemy away.

- Type: [Flying](#types)
- Minimum Level: 0
- Attack factor: 1.7
- Missing chance: 0.1
- Attack points: 30
- Effect: None

#### Eye pick
Picks out one of the enemy's eyes.

- Type: [Flying](#types)
- Minimum Level: 0
- Attack factor: 2.5
- Missing chance: 0.6
- Attack points: 10
- Effect: None

#### Wing hit
Hits the enemy with a wing.

- Type: [Flying](#types)
- Minimum Level: 0
- Attack factor: 2.5
- Missing chance: 0.5
- Attack points: 10
- Effect: None

#### Brooding
Regenerates 2 HP.

- Type: [Flying](#types)
- Minimum Level: 15
- Attack factor: 0
- Missing chance: 0
- Attack points: 10
- Effect: None

#### Power pick
A harsh picking on the enemy's head.

- Type: [Flying](#types)
- Minimum Level: 0
- Attack factor: 2
- Missing chance: 0.4
- Attack points: 10
- Effect: None

### Ground attacks
#### Earch quake
Brings the earth to shift.

- Type: [Ground](#types)
- Minimum Level: 0
- Attack factor: 4
- Missing chance: 0
- Attack points: 10
- Effect: None

#### Power roll
Rolls over the enemy.

- Type: [Ground](#types)
- Minimum Level: 0
- Attack factor: 2.5
- Missing chance: 0.2
- Attack points: 15
- Effect: None

#### Toe Breaker
Breaks the enemys toes.

- Type: [Ground](#types)
- Minimum Level: 0
- Attack factor: 2.5
- Missing chance: 0.3
- Attack points: 20
- Effect: None

#### Ground hit
Damages the enemy with an unpredictable hit out of the ground.

- Type: [Ground](#types)
- Minimum Level: 0
- Attack factor: 3
- Missing chance: 0.1
- Attack points: 10
- Effect: None

#### Dick energy
Collects a great amount of energy in the Poketes tip.

- Type: [Ground](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0
- Attack points: 15
- Effect: None

#### Hiding
Makes the Pokete hide under the ground to minimize damage.

- Type: [Ground](#types)
- Minimum Level: 20
- Attack factor: 0
- Missing chance: 0
- Attack points: 15
- Effect: None

### Ice attacks
#### Freeze
Freezes the enemy.

- Type: [Ice](#types)
- Minimum Level: 10
- Attack factor: 0
- Missing chance: 0.1
- Attack points: 10
- Effect: [Freezing](#freezing)

#### Snow storm
Summons a snow storm full of ice spikes onto the enemy.

- Type: [Ice](#types)
- Minimum Level: 0
- Attack factor: 2.5
- Missing chance: 0
- Attack points: 20
- Effect: None

#### Sword of ice
Stabs a giant ice spike into the enemy.

- Type: [Ice](#types)
- Minimum Level: 20
- Attack factor: 5
- Missing chance: 0.3
- Attack points: 10
- Effect: None

#### Spikes
Stabs the enemy with an some ice spikes.

- Type: [Ice](#types)
- Minimum Level: 0
- Attack factor: 1.75
- Missing chance: 0
- Attack points: 30
- Effect: None

### Normal attacks
#### Tackle
Tackles the enemy very hard.

- Type: [Normal](#types)
- Minimum Level: 0
- Attack factor: 1.5
- Missing chance: 0.2
- Attack points: 30
- Effect: None

#### Cry
So loud, it confuses the enemy.

- Type: [Normal](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0
- Attack points: 10
- Effect: None

#### Bite
A hard bite the sharp teeth.

- Type: [Normal](#types)
- Minimum Level: 0
- Attack factor: 1.75
- Missing chance: 0.1
- Attack points: 30
- Effect: None

#### Power bite
The hardest bite you can think of.

- Type: [Normal](#types)
- Minimum Level: 30
- Attack factor: 8
- Missing chance: 0.1
- Attack points: 5
- Effect: None

#### Choker
Chokes the enemy and makes it weaker.

- Type: [Normal](#types)
- Minimum Level: 0
- Attack factor: 1
- Missing chance: 0.2
- Attack points: 15
- Effect: [Paralyzation](#paralyzation)

#### Tail wipe
Wipes through the enemy's face.

- Type: [Normal](#types)
- Minimum Level: 10
- Attack factor: 2.5
- Missing chance: 0.5
- Attack points: 10
- Effect: None

#### Meat skewer
Drills a horn deep in the enemy's flesh.

- Type: [Normal](#types)
- Minimum Level: 0
- Attack factor: 3.5
- Missing chance: 0.7
- Attack points: 10
- Effect: None

#### Snooze
Makes the enemy sleepy.

- Type: [Normal](#types)
- Minimum Level: 15
- Attack factor: 0
- Missing chance: 0.2
- Attack points: 15
- Effect: [Sleep](#sleep)

#### Supercow power
Makes the Pokete angry and strong.

- Type: [Normal](#types)
- Minimum Level: 10
- Attack factor: 0
- Missing chance: 0
- Attack points: 10
- Effect: None

### Plant attacks
#### Special smell
Spreads a special smell that will make the enemy confused and very happy.

- Type: [Plant](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0
- Attack points: 10
- Effect: [Confusion](#confusion)

#### Apple drop
Lets an apple drop on the enemy's head.

- Type: [Plant](#types)
- Minimum Level: 0
- Attack factor: 1.7
- Missing chance: 0.3
- Attack points: 30
- Effect: None

#### Super sucker
Sucks 2 HP from the enemy and adds it to it's own.

- Type: [Plant](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0
- Attack points: 10
- Effect: None

#### Sucker
Sucks 1 HP from the enemy and adds it to it's own.

- Type: [Plant](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0
- Attack points: 20
- Effect: None

#### Root strangler
Uses old and crusty roots to strangle the enemy.

- Type: [Plant](#types)
- Minimum Level: 20
- Attack factor: 1
- Missing chance: 0.2
- Attack points: 15
- Effect: [Paralyzation](#paralyzation)

#### Root slap
Uses old and crusty roots to slap the enemy.

- Type: [Plant](#types)
- Minimum Level: 0
- Attack factor: 1.5
- Missing chance: 0.2
- Attack points: 30
- Effect: None

#### The old roots hit
An ancient attack that summons the deepest and oldest roots from old times, laying deep in the grounds, to defeat the enemy.

- Type: [Plant](#types)
- Minimum Level: 0
- Attack factor: 50
- Missing chance: 0
- Attack points: 1
- Effect: None

#### Leaf storm
Blasts a bunch of spiky leafs at the enemy.

- Type: [Plant](#types)
- Minimum Level: 20
- Attack factor: 5
- Missing chance: 0
- Attack points: 10
- Effect: None

#### Bark hardening
Hardens the bark to protect it better.

- Type: [Plant](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0
- Attack points: 15
- Effect: None

#### Poison spores
Ejects some poisonous spores onto the enemy.

- Type: [Plant](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0
- Attack points: 15
- Effect: [Poison](#poison)

#### Branch stab
Stabs the enemy with a branch, preferably in the enemy's eyes.

- Type: [Plant](#types)
- Minimum Level: 15
- Attack factor: 4
- Missing chance: 0.2
- Attack points: 10
- Effect: None

### Poison attacks
#### Poison bite
Makes the enemy weaker.

- Type: [Poison](#types)
- Minimum Level: 0
- Attack factor: 1
- Missing chance: 0.3
- Attack points: 10
- Effect: [Poison](#poison)

#### Poison thorn
Stabs a venomous thorn in the enemy's flesh.

- Type: [Poison](#types)
- Minimum Level: 15
- Attack factor: 2.75
- Missing chance: 0.1
- Attack points: 20
- Effect: [Poison](#poison)

### Stone attacks
#### Pepple fire
Fires pepples at the enemy and makes it blind.

- Type: [Stone](#types)
- Minimum Level: 0
- Attack factor: 1
- Missing chance: 0
- Attack points: 5
- Effect: None

#### Sand throw
Throws sand at the enemy and makes it blind.

- Type: [Stone](#types)
- Minimum Level: 0
- Attack factor: 1
- Missing chance: 0
- Attack points: 5
- Effect: None

#### Politure
Upgrades defense and attack points.

- Type: [Stone](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0
- Attack points: 15
- Effect: None

#### Brick throw
Throws an euler brick at the enemy.

- Type: [Stone](#types)
- Minimum Level: 15
- Attack factor: 2
- Missing chance: 0.3
- Attack points: 20
- Effect: None

#### Rock smash
Pounds the enemy with the Poketes full weight.

- Type: [Stone](#types)
- Minimum Level: 15
- Attack factor: 5
- Missing chance: 0.1
- Attack points: 5
- Effect: None

#### Dia stab
Stabs the enemy with an giant diamond spike.

- Type: [Stone](#types)
- Minimum Level: 15
- Attack factor: 5
- Missing chance: 0.1
- Attack points: 5
- Effect: None

#### Dazzle
Shines a bright light at the enemy and dazzles them.

- Type: [Stone](#types)
- Minimum Level: 10
- Attack factor: 1.5
- Missing chance: 0.2
- Attack points: 20
- Effect: [Paralyzation](#paralyzation)

#### Dia spikes
Throws a heck lot of diamond spikes at the enemy.

- Type: [Stone](#types)
- Minimum Level: 20
- Attack factor: 2
- Missing chance: 0
- Attack points: 20
- Effect: None

### Undead attacks
#### Heart touch
Touches the enemy's heard with its' cold ghost claws.

- Type: [Undead](#types)
- Minimum Level: 20
- Attack factor: 4
- Missing chance: 0
- Attack points: 10
- Effect: None

#### Confusion
Confuses the enemy.

- Type: [Undead](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0.2
- Attack points: 40
- Effect: [Confusion](#confusion)

#### Mind blow
Causes confusion deep in the enemy's mind.

- Type: [Undead](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0
- Attack points: 15
- Effect: [Confusion](#confusion)

### Water attacks
#### Bubble gun
Fires some bubbles at the enemy.

- Type: [Water](#types)
- Minimum Level: 0
- Attack factor: 2
- Missing chance: 0.2
- Attack points: 20
- Effect: None

#### Bubble bomb
A deadly bubble.

- Type: [Water](#types)
- Minimum Level: 0
- Attack factor: 6
- Missing chance: 0
- Attack points: 10
- Effect: None

#### Bubble shield
Creates a giant bubble that protects the Pokete.

- Type: [Water](#types)
- Minimum Level: 0
- Attack factor: 0
- Missing chance: 0
- Attack points: 10
- Effect: None

#### Wet slap
Gives the enemy a wet and cold slap in the face.

- Type: [Water](#types)
- Minimum Level: 10
- Attack factor: 2.5
- Missing chance: 0.1
- Attack points: 15
- Effect: None

#### Shell pinch
Pinches the enemy with its strong shells.

- Type: [Water](#types)
- Minimum Level: 15
- Attack factor: 2.5
- Missing chance: 0.1
- Attack points: 20
- Effect: None

## Types
Those are all the Pokete/Attack types that are present in the game with all their (in)effectivities against other types.

|Type|Effective against|Ineffective against|
|---|---|---|
|Normal|||
|Stone|Flying, Fire|Plant|
|Plant|Stone, Ground, Water|Fire, Ice|
|Water|Stone, Flying, Fire|Plant, Ice|
|Fire|Flying, Plant, Undead, Ice|Stone, Water|
|Ground|Normal|Flying, Ice|
|Electro|Stone, Flying|Ground|
|Flying|Plant|Stone|
|Undead|Normal, Ground, Plant, Water, Poison|Fire|
|Ice|Water, Plant, Ground|Fire|
|Poison|Normal|Undead|

## Items
Those are all items present in the game, that can be traded or found.

### AP potion
Refills the Poketes attack APs.

- Price: 100
- Can be used in fights: Yes

### Healing potion
Heals a Pokete with 5 HP

- Price: 15
- Can be used in fights: Yes

### Hyperball
For catching Poketes with a waaay higher chance

- Price: None
- Can be used in fights: Yes

### Poketeball
A ball you can use to catch Poketes

- Price: 2
- Can be used in fights: Yes

### 'Shut the fuck up' stone
Makes trainer leaving you alone

- Price: None
- Can be used in fights: No

### Super potion
Heals a Pokete with 15 HP

- Price: 25
- Can be used in fights: Yes

### Superball
A ball you can use to catch Poketes with an increased chance

- Price: 10
- Can be used in fights: Yes

### Treat
Upgrades a Pokete by a whole level.

- Price: None
- Can be used in fights: No

## Effects
Those effects can be given to a Pokete through an attack.

### Paralyzation
Paralyses the enemy and stops it from attacking. This is reverted randomly.

### Sleep
Makes the enemy fall asleep and stops it from attacking. This is reverted randomly.

### Burning
Sets the enemy on fire and damages them with 2 HP every round. This is reverted randomly.

### Poison
Poisons the enemy and damages the enemy with 1 HP every round. This is reverted randomly.

### Confusion
Makes the enemy hurt it self. This is reverted randomly.

### Freezing
Freezes the enemy and stops it from attacking. This is reverted randomly.
