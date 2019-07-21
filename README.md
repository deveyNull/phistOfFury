<img src="https://raw.githubusercontent.com/deveyNull/phistOfFury/master/resources/phistBlueRibbon.png" alt="drawing" width="300"/> 

# p.h.i.s.t. 
## Perceptual Hashing Image Similarity Tool (Codename: Pedos and Terrorists)

### What is perceptual hashing?

MD5 sucks for identifying similar images. This is a fact.

I was writing a tool to do identify ~~REDACTED~~ based on reused ~~REDACTED~~ on various platforms and MD5 just wasn't cutting it. After a bit of looking for better options I found out about perceptual hashing. This link explains it very well. <html> http://www.hackerfactor.com/blog/?/archives/432-Looks-Like-It.html</html>. 

A perceptual hash is a function that is able to transform a given image into a hash of a specified length based off of the image's visual properties, which means that similar images return similar hashes and visually identical images return matching hashes. Queries to a database of these hashes returns the hash of the image that is most similar to the queried one. 

### These Images All Return Matches
<img src="https://github.com/deveyNull/phistOfFury/raw/master/resources/goat.jpg" alt="drawing" width="400"/> <img src="https://github.com/deveyNull/phistOfFury/raw/master/resources/bills.JPG" alt="drawing" width="400"/>

It is trivial to find near-exact matches, make a giant hashtable just like if you were using MD5, but if you want to find similar images which do not hash to the same string in any sort of reasonable time, you're going to need a multi-dimensional data structure (multi-vantage point trees a la <html>http://www.phash.org/</html>, k-dimensional trees a la <html> https://www.microsoft.com/en-us/photodna </html>, or any other manner of academic shenaniganery). This will give you log(n) lookups, which isn't terrible, depending who you are talking to, but it will get ugly once you get up to internet scale, limiting perceptual hashing to a sideshow in the real world. 

My main contribution to the field of perceptual hashing is a hashing and storage pipeline that results in a constant time lookup for ~170 million hashes, allowing perceptual hashing to be implemented at internet scale. The code in here is a standalone python file, no database setup required, that only gets you up to ~17 million hashes, which is probably good enough for whatever use you are looking through Github for. Here is my slide deck I went on a roadshow with if you want to [learn more](https://github.com/deveyNull/phistOfFury/raw/master/resources/perceptualHashingFinal.pdf).

What this all means is that my wildly non-proprietary block mean based matrix reduction clustering can find similar images at scale significantly faster than any other method. If you disagree with this statement, please let me know. The clustering is the secret sauce, let me know if you need me to explain how it works, and yes, I will write the paper eventually. For now, 90% of what you need to rip off my stuff is in [this document](https://github.com/deveyNull/phistOfFury/raw/master/resources/phistPaper.pdf). If I ever wind up needing to get a PHD for anything I am just going to do this project. 

And of course, this code is all in python, so don't expect the hashing function to be anywhere as fast as something written in assembly, cough photoDNA apologists. p.h.i.s.t. is a POC that makes its money on the database lookup, not the hash function. There are plenty of C and C# perceptual hashing implementations out there, if you're doing this for real modify one of them to copy what this python does and then send the results to the lookup function.

### So what can I use this for?

This is a mature proof of concept python library that can be applied to any problem related to fuzzy image matching. It is meant to demonstrate the power of perceptual hashing, coupled with my wildly non-proprietary block mean based matrix reduction clustering. p.h.i.s.t. is intended to be thrown on top of existing frameworks to replace MD5 checks. It was designed to search a directory of images but is capable of handling real time queries fairly well.  

### Applications Include:
* Scraping 
  *    Social Media
  *   Websites
* Forensics
* De-Duplication
* Whitelisting
* Upload Checking
  *   Social Media
  *   Cloud Sharing
* Identifying phising landing pages (shouts to wik)
* Video Screenshotting

### Limitations Include:
* Crops 
  *    Breaks everything perceptual hashes rely on
* Rotations and Reflections:
  *    Trivial to rotate/reflect image and requery
  *    Hashes are binary arrays, trivial to implement rotation/reflection at that level, almost no added overhead
* Major Edits

### Practical Limitations Include:
* Single File, Standalone Proof of Concept, Written in Python
  *   'Nuff Said.
* Speed/Size Tradeoff
  *    I went for speed. Hashtables required are extensive. 
* "Database" is a flat file which I serialize and re-load as needed
  *   If anyone can think of a better way to do this in a standalone python file, let me know
  *   It goes without saying, if you are actually using this, don't use a pickled python flat file as your database
    
### Future Development:
* Implement k-d trees in buckets instead of lists
  * This is how you would increase your constant time lookup to 170 million images 
  * I never did this in python because the serialized flat file doesn't make sense to store a few hundred million hashes in it
* Add the ability to update a temporary db alongside primary db and query both

#### Author's note:
<img src="https://github.com/deveyNull/phistOfFury/blob/master/resources/a11.jpg?raw=true" alt="drawing" width="250"/> <img src="https://github.com/deveyNull/phistOfFury/raw/master/resources/phistIsis.png" alt="drawing" width="300"/> <img src="https://github.com/deveyNull/phistOfFury/blob/master/resources/a20.jpg?raw=true" alt="drawing" width="250"/> 

This was a side-project I did back at school that wound up being way more fun, and way less fun, than I could have ever imagined. It was a real labor of love, but it was a damn good time figuring out how to turn perceptual hashing into something we can use to solve problems in the real world. Email me at <html>d.m.devey@gmail.com</html> if you have any questions or comments. I will implement it or provide full support free of charge for you if your problem has anything to do with pedos or terrorists. 

### Quick description of each file:

**phist.py** = The guts of the tool, an absolute pile of functions that make everything else work

**phistTerminal.py** = A terminal wrapper for the phist functions, just to demonstrate how easy it is to integrate them
