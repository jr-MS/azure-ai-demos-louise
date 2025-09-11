# Guide: Using Flux Model with ComfyUI on Azure VM

## 1. Create an Azure Virtual Machine (VM)

- Recommended OS: Ubuntu 22.04.
- Recommended GPU: NVIDIA A10/A100.
- Configure inbound port: Open port 8188 (for ComfyUI web service).
- Disk: At least 1TB SSD is recommended.

## 2. Install NVIDIA Driver and CUDA Toolkit

> You can install these in later steps. After installation, reboot the VM (`sudo reboot`).

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-4
sudo apt-get install -y nvidia-driver-550
```

## 3. Connect to VM via SSH

```bash
ssh -i /Users/louise/MSFT/Code/flux/flux-aus-east_key.pem azureuser@<VM_IP>
```
> Replace `<VM_IP>` with your VM's public IP address.

## 4. Install Basic Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git python3-pip python3-venv -y
```

## 5. Install ComfyUI

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Create Model Directories

```bash
mkdir -p models/unet models/vae models/clip
```

## 7. Download Kontext Model

```bash
sudo apt install git-lfs
git lfs install
git clone https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev
```
> When downloading the model for the first time, log in to Hugging Face and accept the model license. Enter your username and access token as prompted.

## 8. Copy Model File to ComfyUI

```bash
cp FLUX.1-Kontext-dev/flux1-kontext-dev.safetensors ~/ComfyUI/models/unet/
```

## 9. Download Other Models (Python Script)

Create a file named `download_models.py` in the ComfyUI directory with the following content:

```python
from huggingface_hub import hf_hub_download

vae_file = hf_hub_download(
    repo_id="black-forest-labs/FLUX.1-dev",
    filename="ae.safetensors",
    local_dir="/home/azureuser/ComfyUI/models/vae"
)

clip_l_file = hf_hub_download(
    repo_id="comfyanonymous/flux_text_encoders",
    filename="clip_l.safetensors",
    local_dir="/home/azureuser/ComfyUI/models/clip"
)

t5_file = hf_hub_download(
    repo_id="comfyanonymous/flux_text_encoders",
    filename="t5xxl_fp16.safetensors",
    local_dir="/home/azureuser/ComfyUI/models/clip"
)

print("Download complete:")
print("VAE:", vae_file)
print("CLIP L:", clip_l_file)
print("T5 XXL:", t5_file)
```

Run:

```bash
source venv/bin/activate
python download_models.py
```

## 10. Start ComfyUI Service

```bash
cd ~/ComfyUI
source venv/bin/activate
python main.py --listen --port 8188 --cuda-device 0
```

## 11. Access the Web Service

Open your browser and visit:

```
http://<VM_IP>:8188/
```
> Replace `<VM_IP>` with your VM's public IP address.

---

## References

1. [Flux Kontext Model Documentation](https://comfyanonymous.github.io/ComfyUI_examples/flux/#flux-kontext-image-editing-model)
2. [Flux.1-Solution-Test Example](https://github.com/xinyuwei-david/david-share/tree/master/Multimodal-Models/Flux.1-Solution-Test)
3. [Hugging Face FLUX.1-Kontext-dev](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev)

> It is recommended to check for errors after each step. If you encounter issues, refer to the official documentation or community discussions.

## Sample Image
Microsoft FTE Only: [link](https://microsoftapc-my.sharepoint.com/:p:/g/personal/jingruhan_microsoft_com/ERbCrEWu4NdJgiHX3JiNgZABCJa_QoK7PLVn-aSBtc7new?e=68WD5B)