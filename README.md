# bias-statistics
Grabs current top stories from New York Times, BBC, CNN, and Breitbart, and tests them for bias using sentence - keyword matching.
Liberal and Conservative keywords come from "liberal.txt" and "conservative.txt" files, respectively.
The files "flip.txt" and "double.txt" are used to modify values determined by the program.
For example, the word "obamacare" has a natural liberal connotation. But, if the scraper detects the word "abysmal" next to "obamacare",
the article will get points towards being more conservative than liberal.
If words from double.txt are detected in the same way, the points value towards liberal/conservative is increased.

This is a first project with python so the code is disgusting.
