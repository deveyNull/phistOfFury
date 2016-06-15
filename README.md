# p.h.i.s.t.
##Perceptual Hashing Image Similarity Tool

MD5 sucks for identifying similar images. This is a fact.

I was writing a tool to do identify REDACTED based on reused REDACTED and MD5 just wasn't cutting it. After a bit of looking for better options I found out about perceptual hashing. This link will explain it better than I can <html> http://www.hackerfactor.com/blog/?/archives/432-Looks-Like-It.html</html>. A perceptual hash is a function that is able to transform a given image into a hash of a specified length based off of the image's visual properties, which means that similar images return similar hashes and visually identical images return matching hashes. Queries to a database of these hashes returns the hash of the image that is most similar to the queried one. 

This is great if you only want to find exact matches, make a giant hashtable, but if you want to find similar images which do not hash to the same string in any sort of reasonable time, you're going to need a multi-dimensional data structure. This will give you log(n) lookups, which isn't bad, but it will start getting ugly, real fast, limiting you to a pretty small target database.

My method of storing the database allows a constant time lookup for 17 million-ish images which do not hash to the same exact string, allowing perceptual hashing to be implemented at scale. I have plans to do a few more shenanigans in the backend which will allow me to say constant time lookups to 170 million-ish with a straighter face. 

What this all means is that this method can find similar images in a database significantly faster than any other method *that I know of*. Of course, this is python.

So what is this? 

This is a mature proof of concept python library that can be applied to any problem related to fuzzy image matching. It is meant to demonstrate the power of perceptual hashing, coupled with my wildly non-proprietary block mean based matrix reduction clustering(the secret sauce). Damn that will be a cool paper once I write it. It is intended to be thrown on top of existing frameworks to replace MD5 checks. It was designed to search a directory of images but is capable of handling real time queries fairly well. 

Applications Include:
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

Limitations Include:
* Crops 
  *    Breaks everything perceptual hashes rely on
* Rotations and Reflections:
  *    Trivial to rotate/reflect image and requery
  *    Hashes are binary arrays, should be able to implement rotation/reflection at that level
* Major Edits

Practical Limitations Include:
* Proof of Concept, Written in Python
  *    Nuff Said.
* Speed/Size Tradeoff
  *    I went for speed. Hashtables required are extensive. 
* "Database" is a flat file which I serialize and re-load as needed
  *   If anyone can think of a better way to do this, let me know
    
Future Development:
* Baselining and testing
* Add the ability to update a temporary db alongside primary db and query both
* Implement k-d trees in buckets instead of lists
* Get more people using this
  * Tell your friends

This is a side-project, a labor of love, but it's a damn good time.
Email me at <html>d.m.devey@gmail.com</html> if you have any questions or comments.

###Quick description of each file:

**phist.py** = The guts of the tool, an absolute pile of functions that make everything else work

**phistTerminal.py** = A terminal wrapper for the phist functions, just to demonstrate how easy it is to integrate them
