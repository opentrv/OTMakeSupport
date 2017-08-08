#!/usr/bin/python3
"""
Copyright [2017] [Deniz Erbilgin]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This program:
    reads in log files in OpenTRV frame format and decodes
    requires a csv file containing decryption keys
"""

import pipes  # TODO replace with argparse (see utils/trvdecode.py)
import sys

# ANSI Colour Escape Patterns.
COLOUR_END="\033[0m"

# List of nodes
REV10_NODES = { "83 82 b9 8c": "\033[90m\033[102m",  # REV10 w/ assocs is highligted green
                "c5 97 d0 a9": "\033[90m\033[101m" }  # REV10 w/o assocs is higlighted red
rev7_nodes = {}

if sys.argv[1] == '-h':
    print("\
Script for printing colour coded node data \
\n \
\nUsage: \
\n- Arg1: Shell command to process file with. \
\n- Arg2: File to process. \
\nExample: \
\nprint_tests.py 'tail -f' log_to_print.log \
")

# Set up pipe.
pipe_in = pipes.Template()
pipe_in.append(sys.argv[1], '--')

# Get file path.
file_path = sys.argv[2]

# Avoid printing error message on exit.
try:
    with pipe_in.open(file_path, 'r') as file:
        print("\033[90m\033[107mdate          time        ctr    node id    \033[0m")
        for line in file:
            # Avoid printing error message on empty lines.
            try:
                # Split date-time, ip address and message body.
                split_line = line.rstrip().split(',')
                date = split_line[0][0:10]
                time = split_line[0][11:]
                ip = split_line[1]
                node_ctr = split_line[2][6:7]
                node_id = split_line[2][9:20]
                colour = ""
                # Highlight if member of REV10_NODES dict, otherwise assume REV7 and assign a colour
                if node_id in REV10_NODES:
                    colour = REV10_NODES[node_id]
                else:
                    if node_id not in rev7_nodes:
                        # Only have 8 colours to choose from so wrap around.
                        rev7_nodes[node_id] = "\033[{}m".format((len(rev7_nodes) % 8) + 90)
                    colour = rev7_nodes[node_id]
                print("{0}{1}    {2}    {3}      {4}{5}".format(
                                                                colour,
                                                                date,
                                                                time,
                                                                node_ctr,
                                                                node_id,
                                                                COLOUR_END))
            except IndexError:
                pass
except KeyboardInterrupt:
    exit(0)
