---
draft: false
title: "Before Turing, There Was Rejewski"
date: 2026-11-09
summary: "Everyone knows Alan Turing broke Enigma. Fewer people know that three Polish mathematicians did it first."
genre: explainer
math: false
tags:
  - history
  - data
---

Today I came across the word *bomba*, Polish for "bomb", and learnt that it was the name of a machine built in 1938 by a Polish mathematician called Marian Rejewski to break the German Enigma cipher. My first reaction was confusion. If the Poles had a machine to break Enigma in 1938, then what was Alan Turing doing? I grew up thinking Turing broke Enigma, full stop. It turns out the real story is a relay race, and the Poles ran the first and hardest leg.

## Enigma was never just one machine

Enigma looked like a typewriter in a wooden box. Every time you pressed a key, an electrical signal passed through a set of rotating wheels called rotors and a panel of plug cables, and a different letter lit up. Then the rotors turned, so pressing the same key again gave a completely different letter. With all the possible rotor orders, starting positions and plug connections, the number of ways to set up the machine ran into the trillions and beyond, and the Germans changed the settings every day.

{{< photo src="enigma.jpg" alt="A German Enigma machine in a wooden case with a keyboard and lamp board, on display behind glass" caption="A German Army and Air Force Enigma machine on display at Bletchley Park." by="Vintage Fan 5678" source="https://commons.wikimedia.org/wiki/File:German_Army_and_Luftwaffe_Enigma_Machine_-_A16991_in_Bletchley_Park.jpg" license="CC BY 4.0" license_url="https://creativecommons.org/licenses/by/4.0/" >}}

What I did not realise is that Enigma was not one fixed machine that someone broke once. The Germans kept changing the hardware and the rules for using it, and every change meant the codebreakers had to break it again. The story makes much more sense as a series of versions, each one harder than the last.

## Version one, broken by a repeated word

{{< photo float="right" src="rejewski.jpg" alt="Black and white portrait of Marian Rejewski in a military uniform and round glasses" caption="Marian Rejewski." source="https://commons.wikimedia.org/wiki/File:Marian_Rejewski.jpg" license="public domain" >}}

Poland had good reason to worry about Germany, so in 1932 its Cipher Bureau hired three young mathematicians, Marian Rejewski, Jerzy Różycki and Henryk Zygalski. Towards the end of that year Rejewski was given the Enigma problem to work on.

The Germans had a habit that turned out to be fatal. At the start of every message, the operator picked a three-letter "message key", which told the receiver where to set the rotors, and typed it twice in a row to protect against typing errors. So the first six letters of every message were the same three letters, encrypted twice. Since every operator on the network did this with the same daily settings, those first six letters were tied together in a predictable way, and Rejewski saw that he could describe that pattern as equations using permutation theory, a branch of abstract mathematics. Combined with some German documents obtained by a French spy, he [reconstructed the internal wiring of the military Enigma by the end of 1932](https://en.wikipedia.org/wiki/Marian_Rejewski), without ever having seen one. The historian David Kahn wrote that it "elevates him to the pantheon of the greatest cryptanalysts of all time."

For the rest of the 1930s, the three of them built tools to find each day's settings, including a card catalogue of more than 100,000 entries and a set of perforated paper sheets invented by Zygalski. Poland was quietly reading German military messages.

## Version two, and the bomba

In [September 1938](https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma), the Germans changed the rules so that each operator chose their own starting position for every message, and the old card catalogue stopped working. They were still typing the message key twice, though, and Rejewski used exactly that. Within about two months he had designed the [bomba](https://en.wikipedia.org/wiki/Bomba_%28cryptography%29), Polish for "bomb", an electrically powered machine that combined six Enigmas and ran through rotor positions hunting for the repeated key. Six bombas were ready by mid-November 1938, and each could find a day's key in about two hours.

A quick note on names, because they get mixed up a lot. The Polish machine was the bomba. The British machine that came later, which most people have heard of, was the Bombe. They are related, but they are not the same machine.

## Versions three and four, and things get out of hand

The bomba worked for barely a month. In December 1938 the Germans gave operators five rotors to choose from instead of three, which took the number of possible rotor orders from 6 to 60. The Poles would have needed ten times as many bombas and ten times as many perforated sheets, and Poland simply did not have the money. In January 1939 the Germans also added more plug cables. There is no evidence that the Germans knew the Poles were reading their messages. As far as historians can tell, they were just tightening security, and even after the war German officers believed Enigma had never been broken.

The final blow came in [May 1940](https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma), when the Germans stopped typing the message key twice. Every Polish method, the bomba included, depended on that one repetition, and with it gone they were useless.

## Handing it over

By the summer of 1939 the Poles knew war was coming and that they could not keep up alone. So in late July 1939 they invited British and French intelligence officers to a secret meeting in a forest near Warsaw and handed over everything, their methods, their mathematics and even replica Enigma machines. [About five weeks later](https://en.wikipedia.org/wiki/Marian_Rejewski), Germany invaded Poland.

Alan Turing was not at that meeting, but he was about to inherit everything that came out of it. He had been working part-time for Britain's codebreaking agency since 1938 and reported to Bletchley Park on 4 September 1939, the day after Britain declared war. In January 1940 he travelled to France to [spend several days with the Polish codebreakers](https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma), who had escaped there.

## So what was Turing doing?

Turing was not an unknown codebreaker who got lucky. In 1936, at the age of 24, he had published a paper called "[On Computable Numbers](https://en.wikipedia.org/wiki/Alan_Turing)", which described an imaginary machine that could carry out any calculation by following simple rules. We now call it a Turing machine, and it is still the basic model of what a computer is. In the same paper he proved that some problems can never be solved by any machine, however clever, the most famous example being that no program can decide in advance whether every other program will eventually stop. He then did a PhD at Princeton under the logician Alonzo Church. Among mathematicians, he was already someone to watch.

What he brought to Enigma was a way of breaking it that did not depend on the Germans making a mistake. Instead of hunting for the repeated message key, his machine used "cribs", short pieces of text the codebreakers could guess, like a weather report that always started the same way. The Bombe then tested rotor settings against the crib and threw out every setting that led to a logical contradiction, leaving only a handful of possibilities to check by hand. This is why the Bombe kept working after May 1940, when the Polish methods died.

{{< photo src="bombe.jpg" alt="The back of a large machine covered in rows of round rotating drums" caption="A working rebuild of the Turing–Welchman Bombe at Bletchley Park. Each set of drums imitates an Enigma machine." by="Mike Peel" source="https://commons.wikimedia.org/wiki/File:Bletchley_Park_Bombe_2.jpg" license="CC BY-SA 4.0" license_url="https://creativecommons.org/licenses/by-sa/4.0/" >}}

The first [Bombe](https://en.wikipedia.org/wiki/Bombe) was installed in March 1940. Turing's colleague Gordon Welchman then added a component called the diagonal board, which cut down the number of settings to check enormously, and from August 1940 every Bombe had it. This is why the machine is often called the Turing–Welchman Bombe. Around 200 were built by the end of the war.

Turing also took on the hardest version of all, the Enigma used by the German navy and its U-boats, and developed a statistical method called [Banburismus](https://en.wikipedia.org/wiki/Banburismus) to attack it. The historian Harry Hinsley later estimated that the intelligence from Bletchley Park shortened the war by at least two years.

So the Poles broke Enigma first and showed that it could be done. Turing's contribution was making it breakable even after the Germans fixed their mistakes, and that is why he is remembered.

## The people history forgot

What happened to the Polish team afterwards is the part that stayed with me. When Poland fell, the codebreakers escaped through Romania to France, where they kept working on Enigma until France fell too. Różycki died in January 1942 when the [passenger ship he was travelling on sank](https://en.wikipedia.org/wiki/Jerzy_R%C3%B3%C5%BCycki) in the Mediterranean. Rejewski and Zygalski escaped over the Pyrenees into Spain, where they were jailed for months, and finally reached Britain in August 1943. By then, Enigma had become a British and American operation, and the two men who had cracked it first were [kept away from it](https://en.wikipedia.org/wiki/Marian_Rejewski), working instead on lesser ciphers.

After the war, Rejewski went back to communist Poland, where he was investigated by the security services for nearly a decade. Because the whole Enigma story stayed classified until the 1970s, almost nobody knew what he had done. Most of the honours came only after he died in 1980, including a monument in Poznań and, in 2021, the Enigma Cipher Centre, a museum in the same city dedicated to the Polish codebreakers.

So the next time someone says Alan Turing broke Enigma, it is worth adding that he was standing on the shoulders of three young Polish mathematicians who got there first.
