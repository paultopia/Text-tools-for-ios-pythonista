# text tools for iOS/Pythonista
Yak-shavey utilities for use in the pythonista app on ios.  Very simple little convenience scripts, largely designed to be put either on the lock screen/3d press (on iphone) or in the share sheet extension.  Mostly for quick and easy text manipulation, that kind of stuff.  

**buttonbox.py**: lazy boilerplate code for creating buttons, used as a module in other scripts. (Note: doesn't always seem to work right, should switch to just using console buttons.  Seems to generate glitches in some of the things using this.

**case_changer.py**: select text in some other app, share it via sharesheet into this, get it back converted to uppercase, lowercase, or some plausible facsimilie of title case (with arbitrary decisions made about whether to capitalize short words and such).  deposits converted text onto clipboard ready for pasting.

**clean_pasted_text.py**: Two functions.  first: you know how sometimes when you OCR or copy-paste text, the paragraph breaks are all weird and stupid?  this attempts to clean that up.  treats single line breaks as single continuations, double line breaks and linebreak + tab as real paragraph breaks. the cleanup line breaks function spits out paragraphs separated by double line breaks, markdown-style.  Second function: you know how sometimes punction comes in with unicode "smart quotes" and elipses and em-dashes and all the rest of that, but then that breaks other tools, like latex and python 2 and all the rest?  the dumbify punctuation function tries to catch as many of those as I can think of and replace them with boring ascii equivalents.  as before, input comes from selected text and ios sharing; output shows up on clipboard.

**convert_md.py**: share a markdown file from some other app (like byword etc.) into this via sharesheet.  will be passed through pandoc with the help of docverter.com (so, not for confidential stuff---gets passed to a third-party site via unencrypted http).  then will pop up another share sheet inviting you to put the converted file somewhere.  will have totally arbitrary file name, rename it yourself.

**merge_pdfs.py**: share pdf files one-by-one into it (using the "add to queue" option).  When you get to the last file, select the "finalize pdf" option instead.  It'll merge the pdf files in the order they were added and throw up an "open in" dialog to put the file somewhere.

**readzip.py**: quick and dirty script to download a compressed file and unzip it in memory to an appropriate folder, because it drives me crazy that ios has no built-in way to look at the contents of compressed files.  Can handle .tar.gzip and .zip files.  Just takes url as console input from running the script, because I'm lazy.

**risfile.py and zotero.py**: very much work-in-progress scripts to add data to zotero.

**zipimages.py**: select multiple images in the ios photos app and share them to this script, and it will shove them into a tar.gzip archive, which will then pop up in a share sheet on its own. For efficient uploading of a group of images to dropbox, onedrive, etc., emailing, and so forth.

more to be added as I make 'em.
