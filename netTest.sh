#!/bin/bash

sleep 15

# running iperf with server as server and h1-5 as clients
# around 270 seconds (4.5 mins)

xdotool type --window "$(xdotool search --name 'Node: server')" 'iperf -i 10 -s' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: server')" Return

sleep 2

xdotool type --window "$(xdotool search --name 'Node: h1')" 'iperf -i 10 -t 60 -c 10.0.0.6' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h1')" Return

sleep 65

xdotool type --window "$(xdotool search --name 'Node: h2')" 'iperf -i 10 -t 60 -c 10.0.0.6' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h2')" Return

sleep 65

xdotool type --window "$(xdotool search --name 'Node: h3')" 'iperf -i 10 -t 60 -c 10.0.0.6' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h3')" Return

sleep 65

xdotool type --window "$(xdotool search --name 'Node: h4')" 'iperf -i 10 -t 60 -c 10.0.0.6' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h4')" Return

sleep 65

xdotool type --window "$(xdotool search --name 'Node: h5')" 'iperf -i 10 -t 60 -c 10.0.0.6' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h5')" Return

sleep 65

xdotool key --window "$(xdotool search --name 'Node: server')" ctrl+c

sleep 2


# running iperf with h1 as server and server, h2-5 as clients
# around 270 seconds (4.5 mins)


xdotool type --window "$(xdotool search --name 'Node: h1')" 'iperf -i 10 -s' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h1')" Return

sleep 2

xdotool type --window "$(xdotool search --name 'Node: server')" 'iperf -i 10 -t 60 -c 10.0.0.1' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: server')" Return

sleep 65

xdotool type --window "$(xdotool search --name 'Node: h2')" 'iperf -i 10 -t 60 -c 10.0.0.1' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h2')" Return

sleep 65

xdotool type --window "$(xdotool search --name 'Node: h3')" 'iperf -i 10 -t 60 -c 10.0.0.1' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h3')" Return

sleep 65

xdotool type --window "$(xdotool search --name 'Node: h4')" 'iperf -i 10 -t 60 -c 10.0.0.1' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h4')" Return

sleep 65

xdotool type --window "$(xdotool search --name 'Node: h5')" 'iperf -i 10 -t 60 -c 10.0.0.1' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h5')" Return

sleep 65

xdotool key --window "$(xdotool search --name 'Node: h1')" ctrl+c