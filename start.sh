#!/bin/bash

banner() {
    echo """
 ___  ___  ___  ___      ___ _______   ________  ________  ___  ________  ________  _______          
|\  \|\  \|\  \|\  \    /  /|\  ___ \ |\   __  \|\   __  \|\  \|\   ___ \|\   ____\|\  ___ \         
\ \  \\\  \ \  \ \  \  /  / | \   __/|\ \  \|\ /\ \  \|\  \ \  \ \  \_|\ \ \  \___|\ \   __/|        
 \ \   __  \ \  \ \  \/  / / \ \  \_|/_\ \   __  \ \   _  _\ \  \ \  \ \\ \ \  \  __\ \  \_|/__      
  \ \  \ \  \ \  \ \    / /   \ \  \_|\ \ \  \|\  \ \  \\  \\ \  \ \  \_\\ \ \  \|\  \ \  \_|\ \     
   \ \__\ \__\ \__\ \__/ /     \ \_______\ \_______\ \__\\ _\\ \__\ \_______\ \_______\ \_______\    
    \|__|\|__|\|__|\|__|/       \|_______|\|_______|\|__|\|__|\|__|\|_______|\|_______|\|_______|    
    """
}

banner
sudo docker compose up -d
echo "completed"