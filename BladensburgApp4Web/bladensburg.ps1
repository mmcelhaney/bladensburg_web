# Install WSL and Ubuntu
Write-Host "Installing WSL and Ubuntu..."
Invoke-Expression -Command "wsl --install"
Invoke-Expression -Command "wsl --set-version Ubuntu 2"

# Update Ubuntu and install required packages
Write-Host "Updating Ubuntu and installing required packages..."
Invoke-Expression -Command "sudo apt-get update -y"
Invoke-Expression -Command "sudo apt-get upgrade -y"
Invoke-Expression -Command "sudo apt-get install -y python3.10 python3.10-venv python3.10-dev build-essential cython3"

# Verify installations
Write-Host "Verifying Python installation..."
Invoke-Expression -Command "python3.10 --version"
Write-Host "Verifying Cython installation..."
Invoke-Expression -Command "cython3 --version"

# Create and activate virtual environment
Write-Host "Creating virtual environment..."
Invoke-Expression -Command "python3.10 -m venv sdaenv"
Write-Host "Activating virtual environment..."
Invoke-Expression -Command "source sdaenv/bin/activate"

# Install setuptools, Kivy, and SQLite3 in the virtual environment, ignoring SSL modules
Write-Host "Installing setuptools, Kivy, and SQLite3..."
Invoke-Expression -Command "pip install setuptools kivy pysqlite3 --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org"

# Moving the BladensburgAppwKivy folder
Write-Host "Moving BladensburgAppwKivy folder..."
Invoke-Expression -Command "mv /mnt/c/Users/Downloads/BladensburgAppwKivy ~/BladensburgAppwKivy"

# Navigate to the project folder
Write-Host "Navigating to the project folder..."
Invoke-Expression -Command "cd ~/BladensburgAppwKivy"

# Creating buildozer.spec file with specified configurations
Write-Host "Creating buildozer.spec file..."
Invoke-Expression -Command "
cat <<EOF > buildozer.spec
[app]
title = Bladensburg SDA
package.name = bladensburgapp
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec
source.include_patterns = assets/*,images/*,fonts/*
source.exclude_dirs = tests, bin, venv
requirements = python3,kivy,pysqlite3,cython==0.29.24,setuptools
android.arch = armeabi-v7a
buildozer.spec should placed on the new folder and make the Application name 'Bladensburg SDA' and the apk's name 'bladensburgapp.apk'
EOF
"

# Generate APK using buildozer
Write-Host "Installing buildozer..."
Invoke-Expression -Command "pip install buildozer"
Write-Host "Initializing buildozer..."
Invoke-Expression -Command "buildozer init"
Write-Host "Building APK..."
Invoke-Expression -Command "buildozer -v android debug"

Write-Host "APK generation process complete. Your APK is ready in the bin directory."
