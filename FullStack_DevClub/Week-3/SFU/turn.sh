#socat -v TCP-LISTEN:19956,fork,reuseaddr STDOUT
#just Opening a port for checking FireWall


#Docker Setup

# Install Docker
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo apt install docker-compose -y

# Add your user to the docker group to run commands without sudo (optional, but recommended)
# You will need to log out and log back in for this to take effect.
sudo usermod -aG docker $USER
