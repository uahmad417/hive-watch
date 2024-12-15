#!/bin/bash

BLUE="\e[34m"
GREEN="\e[33m"
NC="\e[0m"


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

show_help() {
    echo "Usage: start.sh [command] [options]"
    echo
    echo "Commands:"
    echo "  create         starts the platform services"
    echo "  destroy        shuts down the platform service"
    echo "  help          Show this help message."
    echo
    echo "Options:"
    echo "  -h, --help    Show help for a specific command."
}

create() {
    echo "Starting up services..."
    echo -e "${BLUE}Starting mosquitto${NC}"
    echo ""
    oc create -f mosquitto.yml
    echo ""
    
    echo -e "${BLUE}Starting elasticsearch${NC}"
    oc create -f elasticsearch.yml
    echo ""

    echo -e "${BLUE}Starting kibana${NC}"
    oc create -f kibana.yml
    echo ""

    echo "Sleeping for 10 seconds to allow services to start"
    sleep 10

    echo -e "${BLUE}Starting enrichment${NC}"
    oc create -f enrichment.yml
    echo ""

    echo -e "${BLUE}Starting storage${NC}"
    oc create -f storage.yml
    echo ""

    echo -e "${BLUE}Starting docker compose${NC}"
    sudo docker compose up -d
    echo ""

    echo -e "${GREEN}Completed!${NC}"
}

destroy() {
    echo "Shutting  down services..."
    echo -e "${BLUE}Shutting down mosquitto$NC"
    echo ""
    oc delete -f mosquitto.yml
    echo ""
    
    echo -e "${BLUE}Shutting down elasticsearch${NC}"
    oc delete -f elasticsearch.yml
    echo ""

    echo -e "${BLUE}Shutting down kibana${NC}"
    oc delete -f kibana.yml
    echo ""

    echo -e "${BLUE}Shutting down enrichment${NC}"
    oc delete -f enrichment.yml
    echo ""

    echo -e "${BLUE}Shutting down storage${NC}"
    oc delete -f storage.yml
    echo ""

    echo -e "${BLUE}Shutting down docker compose services${NC}"
    sudo docker compose down -v
    echo ""

    echo -e "${GREEN}Completed!${NC}"

}

banner
echo "HiveBridge Threat Deception Platform"
sleep 3

case $1 in 
    create)
        create
        ;;
    destroy)
        destroy
        ;;
    help|-h|--help)
        show_help
        ;;
    *)
        echo "Unkown command $1"
        show_help
esac