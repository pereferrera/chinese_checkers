[![Build Status](https://travis-ci.com/pereferrera/chinese_checkers.svg?branch=master)]

## I did it just to beat my wife at chinese checkers

Let's face it, I'm very bad at chinese checkers. And my wife is pretty good at it.
So I got very frustrated and decided to write an AI to beat her just once.
From a transhumanist point of view, the AI that I wrote is an extension to myself.

So it is fair to say that now I can also beat my wife at chinese checkers.

### The "AI"

I was on parental leave with almost no time for computers, so I couldn't
get too fancy with it.

This is just a very simple engine that uses the typical min-max tree with alpha-beta 
pruning, plus a transposition table to speed up things.

### Can you beat me at chinese checkers?

You will need Python 3.7!

```
make create_env
make run
```

Mouse input through pygame is a bit rusty, so you might have to repeat sometimes 
the move that inted to do.

### These papers were of help:

* [one](http://cs229.stanford.edu/proj2016spr/report/003.pdf)
* [two](https://core.ac.uk/download/pdf/48835733.pdf)
* [three](https://pdfs.semanticscholar.org/30ea/b0836cdc488196f1638d7660aad90883a91f.pdf)
