---
draft: false
title: "Zip It"
date: 2026-11-21
summary: "How ZIP stores repeated text, using BANANA as an example, and how ZIP differs from TAR and HDF5."
cover_credit: "Luca Florio, CC BY-SA 3.0, via Wikimedia Commons"
cover_credit_url: "https://commons.wikimedia.org/wiki/File:Bright_colored_pencils_revealed_behind_a_zipper_(190001157).jpg"
genre: rabbit-hole
math: false
tags:
  - technology
  - data
---

I zip and unzip files almost every day, and I work with `.h5` files full of gravitational wave data, but until recently I had no idea what happened when a file got "compressed". A computer cannot just throw data away and hope you will not notice, because when you unzip your thesis you need every single comma back. So how does a file get smaller without losing anything? You can see both steps in the word BANANA.

## Trick one, short codes for common letters

Computers store everything as 0s and 1s, called bits. Normally, every letter gets the same number of bits, usually 8. The letter A, for example, is stored as 01000001 and B as 01000010. So BANANA, with its six letters, takes 6 × 8 = 48 bits.

That is fair, but wasteful, because the letters are not equally common. BANANA has three A's, two N's and only one B, yet the B gets just as much space as the A. What if the letters you use most got shorter codes and the rare ones got longer codes? Samuel Morse had the same idea in the 1830s, which is why in Morse code the most common letter in English, E, is a single dot.

The problem is doing this without creating confusion. Say we gave A the code 1 and B the code 11. When the computer later reads 11, it has no way of knowing if that is one B or two A's. So the codes need a special property, that no code can be the start of another code.

In 1951, an MIT student named David Huffman found a method he could prove was the best possible way to do this. It is now called [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding), and it is still in use more than seventy years later.

Here is how it works for BANANA, step by step.

1. Count the letters. A appears 3 times, N twice and B once.
2. Take the two rarest, B and N, and join them into a small branch. Together they appear 1 + 2 = 3 times.
3. Now there are two things left, A with 3 and the B–N branch with 3. Join those two into the top of the tree.
4. To find each letter's code, start at the top and walk down to it. Every step to the left is a 0 and every step to the right is a 1.

{{< inline-svg src="huffman.svg" caption="Huffman coding for BANANA. A is common, so it sits near the top with the one-bit code 0. B and N are rarer, so they sit lower down with two-bit codes. The word shrinks from 48 bits to 9." >}}

That gives A the code 0, N the code 10 and B the code 11, and BANANA becomes 11 0 10 0 10 0, just 9 bits instead of 48. To read it back, the computer goes from left to right. It sees 1, which is not a full code yet, then 1 again, and 11 is B. Next is 0, which is A. Then 1, then 0, and 10 is N, and so on. Because no code is the start of another, there is only ever one way to read the string, and no spaces are needed in between.

The file does have to carry this little table of codes along with it, so for a single word the saving is tiny. For a long document, where letters like e and the space between words appear thousands of times, giving them short codes saves a lot.

## Trick two, don't repeat yourself

Huffman coding looks at one letter at a time, but real files are full of whole chunks that repeat, like words, phrases, and the same lines of code over and over. In 1977, two Israeli computer scientists, Abraham Lempel and Jacob Ziv, came up with a way to use that.

The idea is simple. Whenever something appears that has already appeared earlier in the file, you do not write it out again. Instead, you leave a short note pointing back to the first time, saying how far back to go and how many letters to copy.

Take the phrase "to be or not to be". The first "to be" has to be written out in full, because the computer has never seen it before. But by the time it reaches the second "to be", it has seen those exact five characters (the space counts as one) 13 characters earlier. So instead of writing "to be" again, it writes a note that says "go back 13, copy 5".

{{< inline-svg src="lz77.svg" caption="Lempel–Ziv compression. The second \"to be\" is replaced by a note pointing back to the first one." >}}

When the file is unzipped, the computer reads the note, jumps back 13 characters, copies the 5 it finds there, and the phrase is rebuilt exactly. In this short example, the note saves only a couple of letters. But in a long text file where "the" appears thousands of times, or a spreadsheet where the same column names repeat on every row, these notes replace huge amounts of repeated text with a few small numbers.

## Put them together and you get .zip

Most of the zip files you have ever opened use a method called [DEFLATE](https://en.wikipedia.org/wiki/Deflate), designed by Phil Katz for his PKZIP program in the late 1980s, and it uses both methods in sequence.

First comes trick two. The computer scans through the file and, every time it finds something it has seen before, swaps it for a "go back and copy" note. It looks up to 32 kilobytes into the past, which is roughly the last ten pages of text. What is left is a mix of letters that appeared for the first time and lots of these notes.

Then comes trick one. The computer counts which letters and which notes appear most often, builds a Huffman tree, and gives the most common ones the shortest codes. The result is written into the zip file. Unzipping runs both steps backwards. The same method is inside every `.gz` file and every PNG image.

This also explains why zipping a zip file does nothing. After both tricks, the repetition and the uneven letter counts are gone, and what is left looks almost random. There is nothing left to squeeze. In fact, no compression method can shrink every possible file, because there are fewer short files than long ones, so some files have to stay the same size or get bigger. Compression only works because real data, like text, code and images, is full of patterns.

Push that idea to the extreme and you get a zip bomb. The famous [42.zip](https://en.wikipedia.org/wiki/Zip_bomb) is about 42 kilobytes, but it contains five layers of zip files nested inside each other, and if you unzipped all of it, you would get about 4.5 petabytes of data, enough to fill thousands of laptops.

## So what are .tar and .h5?

{{< inline-svg src="archives.svg" caption="A .tar.gz compresses the whole archive. A .zip compresses files individually. An .h5 file stores datasets in groups." >}}

A [.tar](https://en.wikipedia.org/wiki/Tar_%28computing%29) file does not compress anything at all. The name stands for tape archive, and it dates back to Unix in 1979, when backups were written to long reels of magnetic tape. It stores files one after another in a single archive. To make it smaller, you then run the whole bundle through a compressor like gzip, which is why you see names like `.tar.gz`. Because the compressor sees all the files at once, it can find repeats across different files and often compresses better than zip. The downside is that, like a tape, it has to be read from start to finish, so getting one file out of a huge `.tar.gz` means unpacking everything before it.

A [.zip](https://en.wikipedia.org/wiki/ZIP_%28file_format%29) file does the opposite. It compresses each file on its own and adds an index at the very end saying where each one starts. That makes it a little less efficient, but you can pull out a single file without touching the rest.

An `.h5` file is something else altogether. [HDF5](https://en.wikipedia.org/wiki/Hierarchical_Data_Format), which stands for Hierarchical Data Format, is not really an archive. It is more like a whole file system inside one file, with groups that work like folders and datasets that hold large arrays of numbers, each with its own labels and notes attached. Scientists love it because you can read just the slice of data you need without loading the rest, and individual datasets can be compressed too. It is the format the LIGO and Virgo gravitational wave detectors use to [share their data](https://gwosc.org/o2_details) with the public, which is how I ended up using it in the first place.

So the next time you right-click a folder and hit "compress", there is a little tree and a lot of "go back and copy" notes being written for you, all based on an idea a student came up with in 1951.
