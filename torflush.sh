#!/bin/sh
{
sleep 3
echo 'AUTHENTICATE "jinglebell"'
sleep 3
echo "signal NEWNYM"
sleep 3
echo "quit"
} | telnet 127.0.0.1 9151
