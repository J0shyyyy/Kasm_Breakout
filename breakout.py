import requests
import json
import webbrowser
import time
import sys
if len(sys.argv) == 1:
	print("Please input a URL as an arguement (e.g. python3 breakout.py https://Kasm.local/)")
	exit()
requests.packages.urllib3.disable_warnings()
host_url = sys.argv[1]
api_url= host_url + "api/public/"
api_key = "API_KEY"
api_secret = "API_SECRET"

def request_kasm(imageid, name):
	response = ""
	payload = {
	"api_key": api_key,
	"api_key_secret": api_secret,
	"image_id": imageid
	}
	#Checks to see if kasm is already running
	print("Checking if image is already running...\n")
	get_kasms(name, "")
	print("Retrieving new session...\n")
	res = requests.post(api_url + "request_kasm", json=payload, verify=False)
	try:
		response_json = res.json()
		kasm_url = response_json["kasm_url"]
		user_id = response_json["user_id"]
		kasm_id = response_json["kasm_id"]
		if name[0:5] == "Kiosk":
			inp = input("Do you want the Easy(0) or Hard(1) version?")
			if inp == "1":
				print("Booting Hard Kiosk Breakout... ")
				webbrowser.open_new(host_url + kasm_url + "?disable_control_panel=1")
				exec_cmd(kasm_id,user_id,"xterm -e /bin/bash -c \"xmodmap -e 'remove control = Control_L'\"")
				exec_cmd(kasm_id,user_id,"xterm -e /bin/bash -c \"xmodmap -e 'remove control = Control_R'\"")
				print("Done!")
			else:
				#Opens new kasm in web browser
				webbrowser.open_new(host_url + kasm_url)
				print("Kasm Successfully Deployed!")
		else:
			#Opens new kasm in web browser
			webbrowser.open_new(host_url + kasm_url)
			print("Kasm Successfully Deployed!")
	except:
		print("An error has occurred! Try Destroying some active sessions.")


def get_images(option, choice):
	response = ""
	payload = {
	"api_key": api_key,
	"api_key_secret": api_secret
	}
	res = requests.post(api_url + "get_images", json=payload, verify=False)
	response_json = res.json()
	if option == "0":
		#If option 0 is used, prints all available boxes
		for i in range(len(response_json["images"])):
			print("Box " + str(i) + " : " + str(response_json["images"][i]["friendly_name"]))
	if option == "1":
		#When option 1 is supplied, grabs the specified box's image id and feeds it into request_kasm
			image_id = response_json["images"][int(choice)]["image_id"]
			name = response_json["images"][int(choice)]["friendly_name"]
			request_kasm(image_id, name)


def get_kasms(name, option):
#Checks to see if Box selected is already running
	response = ""
	payload = {
	"api_key": api_key,
	"api_key_secret": api_secret
	}
	
	res = requests.post(api_url + "get_kasms", json=payload, verify=False)
	response_json = res.json()
	if option == "2":
		print("Currently running Boxes: \n")
	for i in range(len(response_json["kasms"])):
		if option == "1":
			#Destroys all running boxes
			kasm_id = response_json["kasms"][i]["kasm_id"]
			user_id = response_json["kasms"][i]["user_id"]
			print("Destroying " + str(response_json["kasms"][i]["image"]["friendly_name"]) + " Session...")
			destroy_kasm(user_id, kasm_id)
			print("Done!")
		elif option == "2":
			#Prints all running boxes currently
			print(str(response_json["kasms"][i]["image"]["friendly_name"]) + "\n")
		else:
			if response_json["kasms"][i]["image"]["friendly_name"] == name:
				kasm_id = response_json["kasms"][i]["kasm_id"]
				user_id = response_json["kasms"][i]["user_id"]
				print("Active Session found, Deleting active session...\n")
				destroy_kasm(user_id, kasm_id)


def destroy_kasm(userid, kasmid):
#Destroys running session
    payload = {
    "api_key": api_key,
    "api_key_secret": api_secret,
    "kasm_id": kasmid,
    "user_id": userid
    }
    res = requests.post(api_url + "destroy_kasm", json=payload, verify=False)


def exec_cmd(kasmid, userid, cmd):
	#Meant to execute command, does not work
    payload = {
	"api_key": api_key,
	"api_key_secret": api_secret,
	"kasm_id": kasmid,
	"user_id": userid,
	"exec_config":
    {
        "cmd": cmd
        }
	}
    res = requests.post(api_url + "exec_command_kasm", json=payload, verify=False)


def main():
	print("Welcome to kasm breakout testing!")
	choice1 = input("Would you like to Connect to a Box (0)\nDelete all running sessions (1)\n")
	if choice1 == "0":
		print("Which box would you like to select: (Input the number) \n")
		#Call of get images to print all available images to screen
		get_images("0", "")
		choice2 = input()
		#Call of get images to grab image id of picked box and start it
		get_images("1",choice2)
	elif choice1 == "1":
		#Call of get_kasms prints all running sessions
		get_kasms("", "2")
		choice3 = input("Are you sure you want to destroy these sessions? (y/n)")
		if choice3 == "y" or choice3 == "Y":
			#Call of get kasms to destroy all running sessions
			get_kasms("", "1")

main()
