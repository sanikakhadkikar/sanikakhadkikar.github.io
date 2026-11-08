---
draft: false
title: "A New Cold War"
date: 2026-11-06
summary: "Hackers are breaking into supermarket fridges, and the Pentagon wants to know if they got into the ones on US military bases too."
genre: explainer
math: false
tags:
  - technology
  - politics
---

Of all the headlines I expected to read this year, "hackers are attacking refrigerators" was not one of them. But here we are. Freezers at US military commissaries mysteriously defrosted, hundreds of supermarkets in France had their fridges cranked up to oven temperatures overnight, and yesterday the US government issued an official warning about it. Apparently fridges are the new frontier of cyberwarfare.

## The commissary mystery

Commissaries are the grocery stores on US military bases, run by the Defense Commissary Agency. In late August, within days of each other, the refrigeration at [at least six commissaries](https://www.stripes.com/theaters/us/2026-09-01/army-cid-investigates-commissary-refrigerator-outages-22721718.html) failed, at Fort Irwin and Travis Air Force Base in California, F.E. Warren in Wyoming, Fort Huachuca in Arizona, Naval Station Newport in Rhode Island and Columbus Air Force Base in Mississippi. Some of the appliances had switched themselves into defrost mode, spoiling thousands of dollars of meat, dairy, produce and frozen food. The stores stayed open, but only for dry goods.

At first it just sounded like bad luck. But Army and Air Force criminal investigators opened cases, and the Pentagon is now [treating the outages as a possible cyberattack](https://fortune.com/2026/11/01/hackers-pushed-freezers-at-hundreds-of-french-supermarkets-to-122-degrees-pentagon-investigating-us-military-bases/). Officials have not confirmed that anyone actually got into the systems, but the timing of what happened next in Europe made a lot of people suspicious.

## Meanwhile, in France

On the night of October 11, someone broke into the refrigeration controllers of [up to 700 French supermarkets](https://en.wikipedia.org/wiki/2026_French_supermarket_refrigerator_hack), including hundreds of Intermarché, Carrefour and Coopérative U stores, and switched them all into defrost mode with the food still inside. The alarms were disabled first, so nobody noticed until staff showed up the next morning. Fridges had reached about 50°C, one store in Normandy reported 80°C, and some equipment actually melted or caught fire. Whole aisles of food went in the bin, with damage estimated at €10 million or more.

Then on November 2 it happened again, this time at supermarkets across Belgium, Luxembourg, the Netherlands, Sweden, Germany, Ireland, Estonia and Portugal. Worst of all, attackers also targeted three French blood banks and tried to heat stored plasma to 110°C. Thankfully their monitoring alarms worked and staff stepped in before anything was destroyed.

## How do you even hack a fridge?

This is the part that got me. Big commercial fridges are not like the one in your kitchen. They are run by small computers called controllers, which let a store manage the temperature of every freezer from one place, often remotely over the internet. The attacks targeted controllers made by Danfoss, a major supplier, and some of the models involved are ancient by computer standards. One reached its end of life in 2016 and another in 2021, meaning they no longer get security updates. Security researchers at Claroty had already reported in 2025 that some of these controllers could be logged into with the username "admin" and a hidden daily code that could be worked out from the device's own date. Many of them were simply sitting on the open internet for anyone to find.

The US military seems to have the same problem. NPR reported that commissaries use [older Danfoss controllers](https://www.npr.org/2026/11/03/nx-s1-6026676/cold-war-hackers-fridges), including some from the mid-2000s that can no longer be updated with secure software.

## Who did it?

Nobody knows yet. US officials reportedly suspect Iran-linked hackers were behind the commissary outages, and one industry analyst said the pattern [closely matches Iranian groups](https://www.defenseone.com/threats/2026/11/warn-refrigerator-hacks-attacks-military/417076/). But no government has officially named anyone, and one security expert in France even suggested it could have been kids messing around. When the door is left this wide open, it does not take a nation state to walk through it.

## Why this is not actually funny

It is easy to laugh at the idea of a fridge being hacked, and I did at first. But refrigeration keeps a lot more than ice cream cold. Food supplies, medicines, vaccines and blood all depend on it, which is exactly why the blood bank attack is so chilling (sorry). Yesterday, CISA, the FBI and the Departments of Health, Agriculture and Transportation issued a [joint warning](https://www.defenseone.com/threats/2026/11/warn-refrigerator-hacks-attacks-military/417076/) telling businesses to take refrigeration controls off the public internet, change default passwords, install updates and retire equipment that is no longer supported. And the head of the UK's National Cyber Security Centre warned that this is just the beginning, since AI now makes it much easier to find and exploit old, forgotten technology like this.

So the next time someone tells you their smart fridge is the future, maybe ask them when it last got a security update.
