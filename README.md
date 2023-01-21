![Build Status](https://travis-ci.com/pereferrera/chinese_checkers.svg?branch=master)

## I did it just to beat my wife at chinese checkers

Let's face it, I'm very bad at chinese checkers. And my wife is pretty good at it.
So I got very frustrated and decided to write an AI to beat her just once.
From a transhumanist point of view, the AI that I wrote is an extension to myself.

So it is fair to say that now I can also beat my wife at chinese checkers.

(23/07/20: The final match is still to be played, but she actually defeated a work-in-progress version of the AI once...)
(21/01/23: There was a never a final match, she continued winning all subsequent games and I decided to act as if those games never happened)

### The "AI"

Sorry, this is not as exciting as GPT-3. I did this while on parental leave.
You can't get too fancy with a baby crying.

This is just a very simple engine that uses the typical min-max tree with alpha-beta 
pruning, plus a transposition table to speed up things.
But the code was profiled and optimized quite a bit.

### Can you beat me at chinese checkers?

You will need Python >= 3.8

(if on linux - maybe a bunch of libraries as a requirement to pygame like `apt-get install python-dev libfreetype6-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev`)

```
make create_env
make run
```

Mouse input through pygame is a bit rusty, so you might have to repeat sometimes 
the move that is intended.

### Here a bunch of papers for you (always nice to link some papers, isn't it?):

* [one](http://cs229.stanford.edu/proj2016spr/report/003.pdf)
* [two](https://core.ac.uk/download/pdf/48835733.pdf)
* [three](https://pdfs.semanticscholar.org/30ea/b0836cdc488196f1638d7660aad90883a91f.pdf)
