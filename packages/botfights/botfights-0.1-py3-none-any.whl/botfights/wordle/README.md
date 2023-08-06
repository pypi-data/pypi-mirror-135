wordle
======

This is a harness to write bots that play wordle.

See:

https://www.powerlanguage.co.uk/wordle/

To play against the computer:

```
$ python wordle.py human
```

To test a bot named `play` in `sample-bot.py` against 100 words in `wordlist.txt`:

```
$ wordle sample --num 100
```

To write a bot, write a function `play` in a python file that takes a
string `state`. `state` looks like:

```-----:00000,arose:31112,amend:31211```

That is, state is a comma-delimited list of guess, feedback pairs.
Your first guess was `arose`, your second guess was `amend`, the secret word
is `abbey`. For `amend`, the first letter was correct
(indicated by a `3`), the third letter is in the wrong place (`2`),
and the second, fourth, and fifth letters do not appear in the secret word (`1`).

To "score" your bot:

```
$ python wordle.py bot wordlist.txt sample-bot.play 10 | grep WORD
WORD    1       elect   sample-bot.play 8       8.000   0.064   0.064
WORD    2       neemb   sample-bot.play 21      14.500  0.130   0.097
WORD    3       ylems   sample-bot.play 24      17.667  0.146   0.113
WORD    4       heeds   sample-bot.play 10      15.750  0.068   0.102
WORD    5       talaq   sample-bot.play 9       14.400  0.056   0.093
WORD    6       visas   sample-bot.play 11      13.833  0.081   0.091
WORD    7       beery   sample-bot.play 18      14.429  0.105   0.093
WORD    8       imbar   sample-bot.play 10      13.875  0.075   0.091
WORD    9       lawks   sample-bot.play 19      14.444  0.089   0.091
WORD    10      kraal   sample-bot.play 25      15.500  0.195   0.101
```

Here `sample-bot` solved 10 words in an average of 15.5 guesses per word.

Once you've written your bot, you can compete against other bots at
[botfights.io](https://botfights.io/).

To play your bot on botfights.io in the `test` event, where `XXXX` and `YYYYYYYYY`
are your credentials:

```
$ python wordle.py botfights sample-bot.play XXXXX YYYYYYYYYY test
```

To fight `sample-bot` in the [botfights_i](https://botfights.io/event/botfights_i) event:

```
$ python wordle.py botfights sample-bot.play XXXXX YYYYYYYYYY botfights_i
```

