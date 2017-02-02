# Lab 2: Introduction to Map/Reduce on Hadoop

## Introduction

In this lab, we introduce the map/reduce programming
paradigm. Simply put, this approach to computing breaks tasks down into
a map phase (where an algorithm is mapped onto data) and a reduce phase,
where the outputs of the map phase are aggregated into a concise output.
The map phase is designed to be parallel, and to move the computation to
the data, which, when using HDFS, can be widely distributed. In this
case, a map phase can be executed against a large quantity of data very
quickly. The map phase identifies keys and associates with them a value.
The reduce phase collects keys and aggregates their values. The standard
example used to demonstrate this programming approach is a word count
problem, where words (or tokens) are the keys) and the number of
occurrences of each word (or token) is the value.

As this technique was popularized by large web search companies like
Google and Yahoo who were processing large quantities of unstructured
text data, this approach quickly became popular for a wide range of
problems.  Of course, not every problem can be transformed into a
map-reduce approach, which is why we will explore Spark in several
weeks. The standard MapReduce approach uses Hadoop, which was built
using Java. Rather than switching to a new language, however, we will
use Hadoop Streaming to execute Python code. In the rest of this
lab, we introduce a simple Python WordCount example code. We first
demonstrate this code running at the Unix command line, before switching to running the code by using Hadoop Streaming.

### Mapper: Word Count

The first Python code we will write is the map Python program. This
program simply reads data from `STDIN`, tokenizes each line into words and
outputs each word on a separate line along with a count of one. Thus our
map program generates a list of word tokens as the keys and the value is
always one.

```python
#!/usr/bin/env python3

# These examples are based off the blog post by Michale Noll:
# 
# http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
#

import sys

# We explicitly define the word/count separator token.
sep = '\t'

# We open STDIN and STDOUT
with sys.stdin as fin:
    with sys.stdout as fout:
    
        # For every line in STDIN
        for line in fin:
        
            # Strip off leading and trailing whitespace
            line = line.strip()
            
            # We split the line into word tokens. Use whitespace to split.
            # Note we don't deal with punctuation.
            
            words = line.split()
            
            # Now loop through all words in the line and output

            for word in words:
                fout.write("{0}{1}1\n".format(word, sep))
```

### Reducer: Word Count

The second Python program we write is our reduce program. In this code,
we read key-value pairs from `STDIN` and use the fact that the Hadoop
process first sorts all key-value pairs before sending the map output to
the reduce process to accumulate the cumulative count of each word. The
following code could easily be made more sophisticated by using `yield`
statements and iterators, but for clarity we use the simple approach of
tracking when the current word becomes different than the previous word
to output the key-cumulative count pairs.

```python
#!/usr/bin/env python3

import sys

# We explicitly define the word/count separator token.
sep = '\t'

# We open STDIN and STDOUT
with sys.stdin as fin:
    with sys.stdout as fout:
    
        # Keep track of current word and count
        cword = None
        ccount = 0
        word = None
   
        # For every line in STDIN
        for line in fin:
        
            # Strip off leading and trailing whitespace
            # Note by construction, we should have no leading white space
            line = line.strip()
            
            # We split the line into a word and count, based on predefined
            # separator token.
            #
            # Note we haven't dealt with punctuation.
            
            word, scount = line.split('\t', 1)
            
            # We will assume count is always an integer value
            
            count = int(scount)
            
            # word is either repeated or new
            
            if cword == word:
                ccount += count
            else:
                # We have to handle first word explicitly
                if cword != None:
                    fout.write("{0:s}{1:s}{2:d}\n".format(cword, sep, ccount))
                
                # New word, so reset variables
                cword = word
                ccount = count
        else:
            # Output final word count
            if cword == word:
                fout.write("{0:s}{1:s}{2:d}\n".format(word, sep, ccount))
```

### Testing Python Map-Reduce

Before we begin using Hadoop, we should first test our Python codes out
to ensure they work as expected. First, we should change the permissions
of the two programs to be executable, which we can do with the Unix
`chmod` command.

```sh
chmod u+x /path/to/lab2/mapper.py
chmod u+x /path/to/lab2/reducer.py
```

#### Testing Mapper.py

To test out the map Python code, we can run the Python `mapper.py` code
and specify that the code should redirect STDIN to read the book text
data. This is done in the following code cell, we pipe the output into
the Unix `head` command in order to restrict the output, which would be
one line per word found in the book text file. In the second code cell,
we next pipe the output of  `mapper.py` into the Unix `sort` command,
which is done automatically by Hadoop. To see the result of this
operation, we next pipe the result into the Unix `uniq` command to count
duplicates, pipe this result into a new sort routine to sort the output
by the number of occurrences of a word, and finally display the last few
lines with the Unix `tail` command to verify the program is operating
correctly.

With these sequence of Unix commands, we have (in a single-node)
replicated the steps performed by Hadoop MapReduce: Map, Sort, and
Reduce.




```sh
cd /path/to/lab2

./mapper.py <  book.txt | wc -l
```

```sh
cd /path/to/lab2

./mapper.py <  book.txt | sort -n -k 1 | \
 uniq -c | sort -n -k 1 | tail -10
```

#### Testing Reducer.py

To test out the reduce Python code, we run the previous code cell, but
rather than piping the result into the Unix `tail` command, we pipe the
result of the sort command into the Python `reducer.py` code. This
simulates the Hadoop model, where the map output is key sorted before
being passed into the reduce process. First, we will simply count the
number of lines displayed by the reduce process, which will indicate the
number of  unique _word tokens_ in the book. Next, we will sort the
output by the number of times each word token appears and display the
last few lines to compare with the previous results.


```sh
cd /path/to/lab2

./mapper.py <  book.txt | sort -n -k 1 | \
./reducer.py | wc -l
```

```sh
cd /path/to/lab2

./mapper.py <  book.txt | sort -n -k 1 | \
./reducer.py | sort -n -k 2 | tail -10
```

## Python Hadoop Streaming

**IMPORTANT:** Before doing the following activities, run the following command to setup the Hadoop environment correctly. If you don't, it's likely that these instructions **will not work**.

```
source ~/hadoop.env
```

### Introduction

We are now ready to actually run our Python codes via Hadoop Streaming.
The main command to perform this task is `hadoop`.

Running this Hadoop command by supplying the `-help` flag will provide
a useful summary of the different options. Note that `jar` is short for
Java Archive, which is a compressed archive of compiled Java code that
can be executed to perform different operations. In this case, we will
run the Java Hadoop streaming jar file to enable our Python code to work
within Hadoop.


```sh
# Run the Map Reduce task within Hadoop
hadoop --help
```

    Usage: hadoop [--config confdir] [COMMAND | CLASSNAME]
      CLASSNAME            run the class named CLASSNAME
     or
      where COMMAND is one of:
      fs                   run a generic filesystem user client
      version              print the version
      jar <jar>            run a jar file
                           note: please use "yarn jar" to launch
                                 YARN applications, not this command.
      checknative [-a|-h]  check native hadoop and compression libraries availability
      distcp <srcurl> <desturl> copy file or directories recursively
      archive -archiveName NAME -p <parent path> <src>* <dest> create a hadoop archive
      classpath            prints the class path needed to get the
      credential           interact with credential providers
                           Hadoop jar and the required libraries
      daemonlog            get/set the log level for each daemon
      trace                view and modify Hadoop tracing settings
    
    Most commands print help when invoked w/o parameters.


For our map/reduce Python example to
run successfully, we will need to specify five flags:

1. `-files`: a comma separated list of files to be copied to the Hadoop cluster.
2. `-input`: the HDFS input file(s) to be used for the map task.
3. `-output`: the HDFS output directory, used for the reduce task.
4. `-mapper`: the command to run for the map task.
5. `-reducer`: the command to run for the reduce task.

Given our previous setup, we will eventually run the full command as follows:

```
	# DON'T RUN ME YET!
    hadoop $STREAMING -files mapper.py,reducer.py -input wc/in \
        -output wc/out -mapper mapper.py -reducer reducer.py 
```
When this command is run, a series of messages will be displayed to the
screen (via STDERR) showing the progress of our Hadoop Streaming task.
At the end of the stream of information messages will be a statement
indicating the location of the output directory as shown below. Note, we
can append Bash redirection to ignore the Hadoop messages, simply by
appending `2> /dev/null` to the end of any Hadoop command, which sends
all STDERR messages to a non-existent Unix device, which is akin to
nothing. 

For example, to ignore any messages from the `hdfs dfs -rm -r -f wc/out`
command, we would use the following syntax:

```bash
hdfs dfs -rm -r -f wc/out 2> /dev/null
```

Doing this, however, does hide all messages, which can make debugging
problems more difficult. As a result, you should only do this when your
commands work correctly.

### Putting files in HDFS
In order for Hadoop to be able to access our raw data (the book text) we first have to copy it into the file system that Hadoop uses natively, HDFS.

To do this, we'll run a series of HDFS commands that will copy our local `book.txt` into the distributed file system.

```
# Make a directory for our book data
hdfs dfs -mkdir -p wc/in

# Copy our book to our new folder
hdfs dfs -copyFromLocal book.txt wc/in/book.txt

# Check to see that our book has made it to the folder
hdfs dfs -ls wc/in
hdfs dfs -tail wc/in/book.txt
```

### Running the Hadoop Job
Now that our data is in Hadoop HDFS, we can actually execute the streaming job that will run our word count map/reduce.

```sh
# Delete output directory (if it exists)
hdfs dfs -rm -r -f wc/out

# Run the Map Reduce task within Hadoop
hadoop jar $STREAMING \
    -files mapper.py,reducer.py -input wc/in \
    -output wc/out -mapper mapper.py -reducer reducer.py
```

### Hadoop Results

In order to view the results of our Hadoop Streaming task, we must use
HDFS DFS commands to examine the directory and files generated by our
Python Map/Reduce programs. The following list of DFS commands might
prove useful to view the results of this map/reduce job.

```bash
# List the wc directory
hdfs dfs -ls wc

# List the output directory
hdfs dfs -ls wc/out

# Do a line count on our output
hdfs dfs -count -h wc/out/part-00000

# Tail the output
hdfs dfs -tail wc/out/part-00000
```

Note that these
Hadoop HDFS commands can be intermixed with Unix commands to perform
additional text processing. The important point is that direct file I/O
operations must use HDFS commands to work with the HDFS file system.

The output should match the Python
only map-reduce approach.

### Hadoop Cleanup

Following the successful run of our map/reduce Python programs, we have
created a new directory `wc/out` in the HDFS, which contains two files. If we wish
to rerun this Hadoop Streaming map/reduce task, we must either specify a
different output directory, or else we must clean up the results of the
previous run. To remove the output directory, we can simply use the HDFS
`-rm -r -f wc/out` command, which will immediately delete the `wc/out`
directory. The successful completion of this command is indicated by
Hadoop, and this can also be verified by listing the contents of the
`wc` directory.

```sh
hdfs dfs -r -f wc/out
```

### Student Activity

In the preceding cells, we introduced Hadoop map/reduce by using a
simple word count task. Now that you have run the lab, go back and
make the following changes to see how the results change.

1. We ignored punctuation, modify the original mapper Python code to
token on white space or punctuation. How does this change the Python
map-reduce output?
2. Try downloading a different text from Project Gutenberg. Can you make your map-reduce application run across multiple texts?
3. Can you make your map-reduce code compute bi-grams instead of
unigrams?
