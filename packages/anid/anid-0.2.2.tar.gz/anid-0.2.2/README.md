anid
====

[![Pypi](https://img.shields.io/pypi/v/anid.svg?style=plastic)](https://pypi.org/project/anid/)

`anid` is a cli to download animes from [animefire.net](https://animefire.net)

Instalation
-----------

``` code:sh
pip install anid
```

Usage
-----

To use you need to pass the anime name, the number of episodes and optionally the episode to start the download

``` code:sh
Usage: anid [OPTIONS] ANIME

Options:
  -e, --episodes INTEGER  Number of episodes  [required]
  -s, --start INTEGER     Number of episodes
  --help                  Show this message and exit.
```

If you want download a anime you will search in the [animefire.net](http://animefire.net) and open the url with player and copy the anime name in url

In this exemple https://animefire.net/animes/mob-psycho-100/1 you will copy "mod-psycho-100" and put in the command, and the number of episodes, like this:

In mod pyscho 100 case: https://animefire.net/animes/mob-psycho-100/1
Copy "mod-psycho-100" and put in command, and the number of episodes, like this:

``` code:sh
anid "mob-psycho-100" -e 12
```

License
-------

This project use MIT **license**

About Me
--------

Telegram: [@exebixel](https://t.me/exebixel)

Email: ezequielnat7@gmail.com