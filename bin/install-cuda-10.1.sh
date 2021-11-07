# Basic CUDA 10.1 Installer, from https://developer.nvidia.com/cuda-10.1-download-archive-update2?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1804&target_type=deblocal
# and the corresponding site https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu-installation

echo "Step 1: Checking if a CUDA NVIDIA device is found:"
lspci | grep -i nvidia

echo ""
echo "Step 2: Check for a supported version of linux:"
uname -m && cat /etc/*release

echo ""
echo "Step 3: GCC installed?"
gcc --version

echo ""
echo "Step 4: Check if kernel-headers are up to date:"
sudo apt-get install linux-headers-$(uname -r)

echo "Step 5: Install CUDA by .deb"
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget http://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda-repo-ubuntu1804-10-1-local-10.1.243-418.87.00_1.0-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804-10-1-local-10.1.243-418.87.00_1.0-1_amd64.deb
sudo apt-key add /var/cuda-repo-10-1-local-10.1.243-418.87.00/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda