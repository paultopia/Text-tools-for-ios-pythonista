# ipad_tools
Yak-shavey utilities for use in the pythonista app on ios.  Very simple little convenience scripts, largely designed to be put either on the lock screen/3d press (on iphone) or in the share sheet extension.  Mostly for quick and easy text manipulation, that kind of stuff.  

**buttonbox.py**: lazy boilerplate code for creating buttons, used as a module in other scripts.

**case_changer.py**: select text in some other app, share it via sharesheet into this, get it back converted to uppercase, lowercase, or some plausible facsimilie of title case (with arbitrary decisions made about whether to capitalize short words and such).  deposits converted text onto clipboard ready for pasting.

**convert_md.py**: share a markdown file from some other app (like byword etc.) into this via sharesheet.  will be passed through pandoc with the help of docverter.com (so, not for confidential stuff---gets passed to a third-party site via unencrypted http).  then will pop up another share sheet inviting you to put the converted file somewhere.  will have totally arbitrary file name, rename it yourself.

more to be added as I make 'em.
