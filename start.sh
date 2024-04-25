docker build -t dl_hw2_image .;
docker run -it --gpus all --rm dl_hw2_image

# sudo groupadd docker
# sudo usermod -aG docker $USER
# sudo systemctl restart docker
# sudo docker pull liangchenhsun/dl_images:dl_hw2_240425
# sudo docker run -it --gpus all --rm liangchenhsun/dl_images:dl_hw2_240425
