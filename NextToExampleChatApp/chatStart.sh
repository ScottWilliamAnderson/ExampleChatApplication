sleep 15

xdotool type --window "$(xdotool search --name 'Node: server')" './serverBoot.sh' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: server')" Return

sleep 2

xdotool type --window "$(xdotool search --name 'Node: h1')" './aliceBoot.sh' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h1')" Return

sleep 3

xdotool type --window "$(xdotool search --name 'Node: h2')" './bobBoot.sh' 
sleep 1
xdotool key --window "$(xdotool search --name 'Node: h2')" Return

for i in $(seq 0 1 1000); do
	sleep 2
	xdotool type --window "$(xdotool search --name 'Node: h1')" 'ping!'
	xdotool key --window "$(xdotool search --name 'Node: h1')" Return
	sleep 2
	xdotool type --window "$(xdotool search --name 'Node: h2')" 'pong!'
	xdotool key --window "$(xdotool search --name 'Node: h2')" Return
done