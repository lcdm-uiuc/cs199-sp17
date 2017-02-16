# Lab 3: Hadoop Map/Reduce on "Real" Data

## Introduction
In the past 2 labs, you were introduced to the concept of Map/Reduce and how we can execute Map/Reduce Python scripts on Hadoop with Hadoop Streaming.

This week, we'll give you access to a modestly large (~60GB) Twitter dataset. You'll be using the skills you learned in the last two weeks to perform some more complex transformations on this dataset.

Like in the last lab, we'll be using Python to write mappers and reducers. We've included a helpful shell script to make running mapreduce jobs easier. The script is in your `bin` folder, so you can just run it as `mapreduce`, but we've included the source in this lab so you can see what it's doing.

Here's the usage for that command:

```
Usage: ./mapreduce map-script reduce-scripe hdfs-input-path hdfs-output-path

Example: ./mapreduce mapper.py reducer.py /tmp/helloworld.txt /user/quinnjarr
```

## The Dataset

The dataset is located in `/shared/snapTwitterData` in HDFS. You'll find these files: 

```
/shared/snapTwitterData/tweets2009-06.tsv
/shared/snapTwitterData/tweets2009-07.tsv
/shared/snapTwitterData/tweets2009-08.tsv
/shared/snapTwitterData/tweets2009-09.tsv
/shared/snapTwitterData/tweets2009-10.tsv
/shared/snapTwitterData/tweets2009-11.tsv
/shared/snapTwitterData/tweets2009-12.tsv
```

Each file is a `tsv` (tab-separated value) file. The schema of the file is as follows:

```
POST_DATETIME <tab> TWITTER_USER)URL <tab> TWEET_TEXT
```

Example:

```
2009-10-31 23:59:58	http://twitter.com/sometwitteruser	Wow, CS199 is really a good course
```
	
## Lab Activities
**Lab 3 is due on Thursday, Febuary 16nd, 2017 at 11:55PM.**

Please zip your source files for the following exercises and upload it to Moodle (learn.illinois.edu).

**NOTE:** Place your Hadoop output in your HDFS home directory under the folder `~/twitter/`. (i.e. Problem 1 output should map to `~/twitter/`

**EDIT:** Due to resource constraints on the cluster, please run your map/reduce jobs on only 1 twitter file (`tweets2009-06.tsv`). If you've already run your code on the whole dataset, that is fine.

1. Write a map/reduce program to determine the the number of @ replies each user received.
2. Write a map/reduce program to determine the user with the most Tweets for every given day in the dataset. (If there's a tie, break the tie by sorting alphabetically on users' handles)
3. Write a map reduce program to determine which Twitter users have the largest vocabulary - that is, users whose number of unique words in their tweets is maximized.

### Don't lose your progress!

Hadoop jobs can take a very long time to complete. If you don't take precautions, you'll lose all your progress if something happens to your SSH session.

To mitigate this, we have installed `tmux` on the cluster. Tmux is a tool that lets us persist shell sessions even when we lose SSH connection.

1. Run `tmux` to enter into a tmux session.
2. Run some command that will take a long time (`ping google.com`)
3. Exit out of your SSH session.
4. Log back into the server and run `tmux attach` and you should find your session undisturbed.

### Suggested Workflow

We've provided you with a `sample` command that streams out a random 1% sample of the text file. This is useful for testing, as you won't want to use the entire dataset while developing your map/reduce scripts.

1. Write your map/reduce and test it with regular unix commands:

	```
	sample /mnt/volume/snapTwitterData/tweets2009-06.tsv | ./<MAPPER>.py | sort | ./<REDUCER>.py
	```

2. Test your map/reduce with a single Tweet file on Hadoop:

	```
	hdfs dfs -mkdir -p twitter
	hdfs dfs -rm -r twitter/out
	mapreduce <MAPPER>.py <REDUCER>.py /shared/snapTwitterData/tweets2009-06.tsv twitter/out
	```
	
3. Run your map/reduce on the full dataset:
	```
	hdfs dfs -mkdir -p twitter
	hdfs dfs -rm -r twitter/out
	mapreduce <MAPPER>.py <REDUCER>.py /shared/snapTwitterData/*.tsv twitter/out
	```
