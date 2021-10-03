<h1 id="pokete----grey-edition">Pokete -- Grey Edition</h1>
<p><img src="assets/ss/ss01.png" alt="Example" /></p>
<p><a href="assets/pics.md">See more example pics</a></p>
<h2 id="what-is-it">What is it?</h2>
<p>Pokete is a small terminal based game in the style of a very popular and old game by Gamefreak.</p>
<h2 id="installation">Installation</h2>
<p>For Linux just do this:</p>
<pre class="shell"><code># pip install scrap_engine
$ git clone https://github.com/lxgr-linux/pokete.git
$ ./pokete/pokete.py
</code></pre>
<p>You can also install it from the AUR:</p>
<pre class="shell"><code>$ buildaur -S pokete-git
</code></pre>
<p>For windows first install pynput and then do a Windows equivalent to the above.</p>
<h2 id="how-to-play">How to play?</h2>
<p>Imagine your a Pokete-Trainer and your goal is it to run around in the world and catch/train as many Poketes as possible and to get the best trainer.</p>
<p>First of all you get a starter Pokete (Steini), that you can use to fight battles with other Poketes. The controls are w a s d to walk around.</p>
<p>When entering the high grass (;), you may be attacked by a wild Pokete. By pressing 1 you can choose between the attacks (as long their AP is over 0) your Pokete got, by pressing the according number, or navigating the "*"-cursor to the attack and pressing enter. The wild Pokete will fight back, you can kill it and gain XP to level up your Pokete or you can catch it to let it fight for you. To catch a Pokete you have to first weaken the enemy and then throw a Poketeball. And with a bit luck you can catch it. Pressing the "1" key you can take a look at your current deck, see the detailed information of your Pokete and your attacks or rearrange them. Changes will only be saved by quitting the game using the exit function.</p>
<p>Since your a Pokete-Trainer, you can also fight against other trainers, the one other "a", that's staying in the middle of the landscape will start a fight with you, when you go into his way. You can not escape from such a trainer fight, you either have to win, or lose. Those trainer fights give double the XP.</p>
<p>In case one of your Poketes dies, or is too weak, you can heal it by going into the house, aka, Pokete-Center, talk the the person there and choose the healing option. There you can also take a look at all your Poketes, and not just the first six. The ones marked with an "o" are the ones in your deck.</p>
<p>By pressing "e" you can get into a menu where player name and later other settings, can be changed.</p>
<p>The red balls all over the map, are Poketeballs, you need to catch Poketes. Stepping on such a ball adds it to your inventory.</p>
<p>See <a href="HowToPlay.md">How to play</a>.</p>
<h2 id="game-depth">Game depth</h2>
<p>Not only are there Poketes that are stronger than others, but also Poketes with different types, which are effective against some types and ineffective against others.</p>
<table>
<thead>
<tr class="header">
<th>Type</th>
<th>Effective against</th>
<th>Ineffective against</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Normal</td>
<td></td>
<td></td>
</tr>
<tr class="even">
<td>Stone</td>
<td>Flying, Fire</td>
<td>Plant</td>
</tr>
<tr class="odd">
<td>Plant</td>
<td>Stone, Ground, Water</td>
<td>Fire, Ice</td>
</tr>
<tr class="even">
<td>Water</td>
<td>Stone, Flying, Fire</td>
<td>Plant, Ice</td>
</tr>
<tr class="odd">
<td>Fire</td>
<td>Flying, Plant, Undead, Ice</td>
<td>Stone, Water</td>
</tr>
<tr class="even">
<td>Ground</td>
<td>Normal</td>
<td>Flying</td>
</tr>
<tr class="odd">
<td>Electro</td>
<td>Stone, Flying</td>
<td>Ground</td>
</tr>
<tr class="even">
<td>Flying</td>
<td>Plant</td>
<td>Stone</td>
</tr>
<tr class="odd">
<td>Undead</td>
<td>Normal, Ground, Plant, Water</td>
<td>Fire</td>
</tr>
<tr class="even">
<td>Ice</td>
<td>Water, Plant</td>
<td>Fire</td>
</tr>
</tbody>
</table>
<p>For additional information you can see <a href="./wiki.html">wiki</a>.</p>
<h2 id="tips">Tips</h2>
<ul>
<li>In conversations you can very easily skip the text printing by pressing any key</li>
<li>When you want to see the next text in a conversation, also just press any key</li>
<li>Don't play on full-screen, the game then starts to be overseeable</li>
<li>Don't be offended by the other trainers, they may swear at you</li>
</ul>
<h2 id="todo">TODO</h2>
<ul>
<li>[x] Add a wizard to set name and choose starter Pokete at the start</li>
<li>[ ] Add More maps</li>
<li>[x] Add types for attacks and Poketes</li>
<li>[x] Add evolving</li>
<li>[ ] Add more than one Pokete for trainers</li>
<li>[x] Coloured Poketes</li>
<li>[x] A store to buy Poketeballs</li>
<li>[x] Add potions</li>
<li>[x] Add Intro</li>
<li>[x] Add trading</li>
<li>[x] Add Poketedex</li>
<li>[x] Effects</li>
<li>[x] Add color codes for types</li>
</ul>
<h2 id="dependencies">Dependencies</h2>
<p>Pokete depends on python3 and the scrap_engine module. On windows pynput has to be installed too.</p>
<h2 id="documentation">Documentation</h2>
<p><a href="https://lxgr-linux.github.io/pokete/doc/pokete_classes/index.html">Documentation for pokete_classes</a> <a href="https://lxgr-linux.github.io/pokete/doc/pokete_data/index.html">Documentation for pokete_data</a> <a href="https://lxgr-linux.github.io/pokete/doc/gen-wiki.html" title="gen-wiki.py">Documentatio for the gen-wiki file</a> <a href="https://lxgr-linux.github.io/pokete/doc/pokete.html" title="pokete.py">Documentation for the main file "pokete.py"</a></p>
<h2 id="releases">Releases</h2>
<p>For release information see <a href="./Changelog.html">Changelog</a>.</p>
<h2 id="contributing">Contributing</h2>
<p>Feel free to contribute what ever you want to this game. New Pokete contributions are especially welcome, those are located in /pokete_data/poketes.py</p>
<p>After adding new Poketes and/or Attacks you may want to run</p>
<pre class="shell"><code>$ ./gen-wiki.py
</code></pre>
<p>to regenerate the wiki and adding them to it.</p>
<p><a href="https://github.com/lxgr-linux/pokete/actions/workflows/main.yml"><img src="https://github.com/lxgr-linux/pokete/actions/workflows/main.yml/badge.svg" alt="Wiki" /></a> <a href="https://github.com/lxgr-linux/pokete/actions/workflows/main_validate.yml"><img src="https://github.com/lxgr-linux/pokete/actions/workflows/main_validate.yml/badge.svg" alt="Code-Validation" /></a> <a href="https://github.com/lxgr-linux/pokete/actions/workflows/documentation.yml"><img src="https://github.com/lxgr-linux/pokete/actions/workflows/documentation.yml/badge.svg" alt="GitHub-Pages Build" /></a></p>
<h1 id="pokete----grey-edition">Pokete -- Grey Edition</h1>
<p><img src="assets/ss/ss01.png" alt="Example" /></p>
<p><a href="assets/pics.md">See more example pics</a></p>
<h2 id="what-is-it">What is it?</h2>
<p>Pokete is a small terminal based game in the style of a very popular and old game by Gamefreak.</p>
<h2 id="installation">Installation</h2>
<p>For Linux just do this:</p>
<pre class="shell"><code># pip install scrap_engine
$ git clone https://github.com/lxgr-linux/pokete.git
$ ./pokete/pokete.py
</code></pre>
<p>You can also install it from the AUR:</p>
<pre class="shell"><code>$ buildaur -S pokete-git
</code></pre>
<p>For windows first install pynput and then do a Windows equivalent to the above.</p>
<h2 id="how-to-play">How to play?</h2>
<p>Imagine your a Pokete-Trainer and your goal is it to run around in the world and catch/train as many Poketes as possible and to get the best trainer.</p>
<p>First of all you get a starter Pokete (Steini), that you can use to fight battles with other Poketes. The controls are w a s d to walk around.</p>
<p>When entering the high grass (;), you may be attacked by a wild Pokete. By pressing 1 you can choose between the attacks (as long their AP is over 0) your Pokete got, by pressing the according number, or navigating the "*"-cursor to the attack and pressing enter. The wild Pokete will fight back, you can kill it and gain XP to level up your Pokete or you can catch it to let it fight for you. To catch a Pokete you have to first weaken the enemy and then throw a Poketeball. And with a bit luck you can catch it. Pressing the "1" key you can take a look at your current deck, see the detailed information of your Pokete and your attacks or rearrange them. Changes will only be saved by quitting the game using the exit function.</p>
<p>Since your a Pokete-Trainer, you can also fight against other trainers, the one other "a", that's staying in the middle of the landscape will start a fight with you, when you go into his way. You can not escape from such a trainer fight, you either have to win, or lose. Those trainer fights give double the XP.</p>
<p>In case one of your Poketes dies, or is too weak, you can heal it by going into the house, aka, Pokete-Center, talk the the person there and choose the healing option. There you can also take a look at all your Poketes, and not just the first six. The ones marked with an "o" are the ones in your deck.</p>
<p>By pressing "e" you can get into a menu where player name and later other settings, can be changed.</p>
<p>The red balls all over the map, are Poketeballs, you need to catch Poketes. Stepping on such a ball adds it to your inventory.</p>
<p>See <a href="HowToPlay.md">How to play</a>.</p>
<h2 id="game-depth">Game depth</h2>
<p>Not only are there Poketes that are stronger than others, but also Poketes with different types, which are effective against some types and ineffective against others.</p>
<table>
<thead>
<tr class="header">
<th>Type</th>
<th>Effective against</th>
<th>Ineffective against</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Normal</td>
<td></td>
<td></td>
</tr>
<tr class="even">
<td>Stone</td>
<td>Flying, Fire</td>
<td>Plant</td>
</tr>
<tr class="odd">
<td>Plant</td>
<td>Stone, Ground, Water</td>
<td>Fire, Ice</td>
</tr>
<tr class="even">
<td>Water</td>
<td>Stone, Flying, Fire</td>
<td>Plant, Ice</td>
</tr>
<tr class="odd">
<td>Fire</td>
<td>Flying, Plant, Undead, Ice</td>
<td>Stone, Water</td>
</tr>
<tr class="even">
<td>Ground</td>
<td>Normal</td>
<td>Flying</td>
</tr>
<tr class="odd">
<td>Electro</td>
<td>Stone, Flying</td>
<td>Ground</td>
</tr>
<tr class="even">
<td>Flying</td>
<td>Plant</td>
<td>Stone</td>
</tr>
<tr class="odd">
<td>Undead</td>
<td>Normal, Ground, Plant, Water</td>
<td>Fire</td>
</tr>
<tr class="even">
<td>Ice</td>
<td>Water, Plant</td>
<td>Fire</td>
</tr>
</tbody>
</table>
<p>For additional information you can see <a href="./wiki.html">wiki</a>.</p>
<h2 id="tips">Tips</h2>
<ul>
<li>In conversations you can very easily skip the text printing by pressing any key</li>
<li>When you want to see the next text in a conversation, also just press any key</li>
<li>Don't play on full-screen, the game then starts to be overseeable</li>
<li>Don't be offended by the other trainers, they may swear at you</li>
</ul>
<h2 id="todo">TODO</h2>
<ul>
<li>[x] Add a wizard to set name and choose starter Pokete at the start</li>
<li>[ ] Add More maps</li>
<li>[x] Add types for attacks and Poketes</li>
<li>[x] Add evolving</li>
<li>[ ] Add more than one Pokete for trainers</li>
<li>[x] Coloured Poketes</li>
<li>[x] A store to buy Poketeballs</li>
<li>[x] Add potions</li>
<li>[x] Add Intro</li>
<li>[x] Add trading</li>
<li>[x] Add Poketedex</li>
<li>[x] Effects</li>
<li>[x] Add color codes for types</li>
</ul>
<h2 id="dependencies">Dependencies</h2>
<p>Pokete depends on python3 and the scrap_engine module. On windows pynput has to be installed too.</p>
<h2 id="documentation">Documentation</h2>
<p><a href="https://lxgr-linux.github.io/pokete/doc/pokete_classes/index.html">Documentation for pokete_classes</a> <a href="https://lxgr-linux.github.io/pokete/doc/pokete_data/index.html">Documentation for pokete_data</a> <a href="https://lxgr-linux.github.io/pokete/doc/gen-wiki.html" title="gen-wiki.py">Documentatio for the gen-wiki file</a> <a href="https://lxgr-linux.github.io/pokete/doc/pokete.html" title="pokete.py">Documentation for the main file "pokete.py"</a></p>
<h2 id="releases">Releases</h2>
<p>For release information see <a href="./Changelog.html">Changelog</a>.</p>
<h2 id="contributing">Contributing</h2>
<p>Feel free to contribute what ever you want to this game. New Pokete contributions are especially welcome, those are located in /pokete_data/poketes.py</p>
<p>After adding new Poketes and/or Attacks you may want to run</p>
<pre class="shell"><code>$ ./gen-wiki.py
</code></pre>
<p>to regenerate the wiki and adding them to it.</p>
