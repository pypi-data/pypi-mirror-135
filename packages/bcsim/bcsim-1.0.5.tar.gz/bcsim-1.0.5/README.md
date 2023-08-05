![GitHub](https://img.shields.io/github/license/geozeke/bcsim)
![PyPI](https://img.shields.io/pypi/v/bcsim)
![PyPI - Status](https://img.shields.io/pypi/status/bcsim)
![GitHub last commit](https://img.shields.io/github/last-commit/geozeke/bcsim)
![GitHub issues](https://img.shields.io/github/issues/geozeke/bcsim)
![PyPI - Downloads](https://img.shields.io/pypi/dm/bcsim)
![GitHub repo size](https://img.shields.io/github/repo-size/geozeke/bcsim)
![Lines of code](https://img.shields.io/tokei/lines/github/geozeke/bcsim)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bcsim)

<br>

<img src="https://drive.google.com/uc?export=view&id=1H04KVAA3ohH_dLXIrC0bXuJXDn3VutKc" width="120"/>

# Ball Clock Simulator

## Installation

The Ball Clock Simulator is lightweight, pure Python, with no third-party dependencies.

```shell
pip3 install bcsim  
```

## Usage

To display the help menu, run:

```shell
bcsim -h
```

## Documentation

See: [Ball Clock API Documentation](https://geozeke.github.io/bcsim)
## What Is A Ball Clock?

Start with this [YouTube video](https://www.youtube.com/watch?v=F7K6GIBWPQw) that describes exactly what a Ball Clock is. It gives you a good overview of how it works.

## What Does This Program Do?

I have one of the clocks shown in the video (I also have one of [these clocks](https://www.idle-tyme.com/)).

One day, I was staring at it and I thought: *When the clock shows 1:00 and all the balls are in the input tray (what I call the reservoir) they're in a certain order. I wonder how long the clock has to run before the balls return to that same ordering again.*

It turns out I'm not even close to the first person to ask this question. The [Ball Clock Problem](http://www.chilton.com/~jimw/ballclk.html) has been rattling around the internet as at least as far back as 1995. Just go to GitHub, type "Ball Clock", and you'll get lots of hits. Like those simulations, my program runs the clock and counts the number of days that pass until the balls all return to their original starting order in the reservoir.

## How Is This Ball Clock Simulator Different?

It's written in Python.

In the [YouTube video](https://www.youtube.com/watch?v=F7K6GIBWPQw), starting around 2:10, you'll hear a description of a little plastic lever (what I call the "cam") that prevents the balls in the 5-min rail from colliding with the balls in the hr-rail when the clock strikes 1:00. The physical clock would have issues if that cam were not present, but there's no need for it in a virtual clock. I've been able to reproduce the results of others, which assume the cam is not present, but the combinatorics are radically different when the cam is there. In that regard my simulation is a little unique.

Besides choosing to model the cam, I noticed another variation on how some other simulators assume the clock mechanics work.

There seems to broad consensus about how the clock mechanics work until you go from 12:59 to 1:00. All the other simulators I've seen assume that the last ball to drop between 12:59 and 1:00 comes back into the reservoir last. After observing my own clock carefully and stepping through the YouTube video, I feel confident that the last ball to drop between 12:59 and 1:00 actually cycles back to the reservoir just ***before*** the balls in the hour rail. To see what I mean, set the playback speed on [the video]((https://www.youtube.com/watch?v=F7K6GIBWPQw)) to 0.25x, advance it to the 4:00 mark, and press play. I found it fascinating that this one little difference also had a massive effect on the simulation results.

The simulator allows you to concurrently run different scenarios from 27 (the minimum number of balls required to run the clock) up to 1,000 balls, and you can save your results to a csv file for later analysis. It uses multiprocessing to concurrently cycle *n* clocks at a time, where *n* is the number of available CPUs on your computer. In addition to utilizing multiprocessing, the simulator takes advantage of a unique repeating pattern to further speed up calculations.

At each 12-hr interval, all the balls in the clock are in the reservoir. If you start with a fresh clock and brute-force cycle it for 720 minutes (12-hrs), then you get what I call a permutation vector in the reservoir. You can now treat each ball number in the reservoir as an index (position) for the movement of the balls every 12-hrs.

For example: if cycling a fresh clock 12-hrs results in ball #10 ending up in position #2, that means every 12-hrs the ball in position #10 will migrate to position #2. Using two Python lists, we can now cycle the clock for 12-hrs each "tick", rather then 1-minute for each "tick". The speed gains in clock cycling are dramatic.

I also found that several clocks will cycle back to the initial condition in a fractional number of days -- 18.5 days in the case of a clock with 38 balls. This may have something to do with the way I've modeled the clock mechanics, but I couldn't find another solution to the Ball Clock problem that cycled a given clock on the 12-hr boundary; they all cycled for a whole number of days.

## Peer(less) Review

Writing this simulator gave me some great practice with Python programming topics: argument parsing, classes, multiprocessing, inter-process communication, queues and project packaging (pypi). While not required to use the program, I also included detailed API documentation for those who are interested.

It's not really practical to validate my assumptions using a physical clock -- in some cases it takes billions of simulated days to cycle back to the starting position. I would love it if someone coded this up independently, using the same clock mechanics I describe, and validated or invalidated the program's results.

## Version History

* 1.0.5 (2022-01-17)
	* Code/documentation linting and cleanup.<br><br>
* 1.0.4 (2022-01-09)
	* Fixed a display glitch in the window that counts the number of clocks in queue.<br><br>
* 1.0.3 (2022-01-03)
	* Adjusted display width to support counting days with up to three digits in the trillions column: 999,999,999,999,999.<br><br>
* 1.0.2 (2021-12-23)
	* Documentation cleanup.
	* Added site logo to README.md file.<br><br>
* 1.0.1 (2021-12-13)
	* Initial release
