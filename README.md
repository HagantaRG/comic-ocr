# Jelly's Manga Reading Thingy.
This is my own rendition of the excellent [Mokuro](https://github.com/kha-white/mokuro) project, made mostly just to do it.
That being said, if you have any suggestions, please give me a heads-up and I will be happy to implement it. Probably.
## Installation
To install, you should only need to run:
```
pip install comic-ocr-reader
```
Once that it is installed (it may take some time, there are large dependencies in there) you should then run:
```
comic_ocr_reader
```
Or if that doesn't work:
```
python3 -m comic_ocr_reader
```
## Usage
1. Prepare a folder containing the images you would like to process. As of v.0.0.1 the images in this folder must be named the page number you would like that image to be.
   (e.g. the PNG image you would like to use as the second page should be titled "2.png")
   The name of the folder will be the name of the resultant HTML file. (e.g. if your folder is titled "Naruto" the output HTML file will be "Naruto.html" )
2. Run comic-reader-ocr and enter the "folder" command.
3. Enter the absolute path of the folder from step 1 and wait for comic-reader-ocr to process all the images.
4. Once finished, the resulting HTML file will be placed within the folder from step 1.
5. Open the resulting HTML using your web browser of choice.
### Notes
- You *will* need to keep the HTML file within the same folder as all the rest of the pages. Otherwise, the images will not load.
- Depending on your hardware, it may take quite some time to fully process all pages. On my laptop, it took roughly ~8s/page. I imagine on something with an actual GPU it would be faster though.
## FAQs (as decided by Myself)
1. Is this a worse version of various other projects (e.g. [Mokuro](https://github.com/kha-white/mokuro))?

   - Yes.

2. Do you know how to like. Write things. That work?

   - No.

3. Why did you do this?

   - As a learning exercise, mostly. Plus, I like trying to reinvent wheels.

4. Can I make suggestions?

   - Yes. 

5. Did you use AI for this?

   - Yes. Most of the HTML and JS was AI generated, as unfortunately I really *really* don't like looking at either of those things.

6. Are you going to try to make this a webapp because that probably makes a lot of sense or just. Like. Something that isn't Python so that it's easier to distribute or something?

   - Yes. I'll probably try to rewrite this in Rust or do something like the [mokuro-reader](https://github.com/Gnathonic/mokuro-reader) project.
