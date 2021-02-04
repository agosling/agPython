## Guides:


### GATE:  

[http://wiki.opengatecollaboration.org/index.php/Installation_Guide_V8.0](http://wiki.opengatecollaboration.org/index.php/Installation_Guide_V8.0)

[http://wiki.opengatecollaboration.org/index.php/Compilation_Instructions_V8.0](http://wiki.opengatecollaboration.org/index.php/Compilation_Instructions_V8.0)


### Geant4:  

[http://geant4-userdoc.web.cern.ch/geant4-userdoc/UsersGuides/InstallationGuide/fo/BookInstalGuide.pdf](http://geant4-userdoc.web.cern.ch/geant4-userdoc/UsersGuides/InstallationGuide/fo/BookInstalGuide.pdf)


### UCL Radiotherapy installation guide wiki:

[https://wiki.ucl.ac.uk/pages/viewpage.action?pageId=82446093](https://wiki.ucl.ac.uk/pages/viewpage.action?pageId=82446093)


# CURRENT INSTALL LOG


## Prior to installation (Mac specific)


### HomeBrew

for terminal installation of packages - [https://brew.sh/](https://brew.sh/)


```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```



### cmake


```
brew install cmake
```



### X11

X11 is no longer distributed with Mac OSX.  Also not accessible through port.

Download from [https://www.xquartz.org/](https://www.xquartz.org/) and install using .dmg/.pkg.  Alternately, can install with brew


```
brew cask install xquartz
```



### OpenGL

[https://stackoverflow.com/questions/23450334/opengl-3-3-4-1-on-mac-osx-10-9-using-glfw-library](https://stackoverflow.com/questions/23450334/opengl-3-3-4-1-on-mac-osx-10-9-using-glfw-library)

[https://jslvtr.com/using-opengl-in-mac-os-x/](https://jslvtr.com/using-opengl-in-mac-os-x/)

I will suggest installing glfw via homebrew [http://brew.sh/](http://brew.sh/) The advantage being you can always uninstall it neatly by doing `brew uninstall glfw3`!

Once Homebrew is installed, open the terminal and run


```
brew update
brew tap homebrew/versions
```


`brew install glfw3` for glfw3


```
brew install glew
```



## Geant4

**REMEMBER:  must install Genat4 10.3 **rather than the most up to date version as GATE works on this legacy version and isn’t setup to work on the most recent version of Geant4


```
sudo mkdir /usr/local/geant4
cd /usr/local/geant4
sudo cp ~/Downloads/geant4.10.03.p03.tar.gz .
sudo tar -xvf geant4.10.03.p03.tar.gz
sudo mkdir geant4.10.03.p03-build geant4.10.03.p03-install
cd geant4.10.03.p03-build
sudo cmake -DCMAKE_INSTALL_PREFIX=/usr/local/geant4/geant4.10.03.p03-install -DGEANT4_BUILD_MULTITHREADED=ON -DGEANT4_INSTALL_DATA=ON -DGEANT4_INSTALL_DATADIR=/usr/local/geant4/geant4.10.03.p03-data -DGEANT4_USE_OPENGL_X11=ON /usr/local/geant4/geant4.10.03.p03
```


~~Removed installation options~~

~~-DGEANT4_USE_QT=ON~~


```
sudo make -j3
sudo make install
cd /usr/local/geant4/geant4.10.03.p03-install/bin
source geant4.sh
```



## Root

Root is required for the GATE installation.  Version installed is Root-6.12.06.  Installing the pre-compiled tar-ball for simplicity but to have some control over setup and file location

Download `root_v6.12.06.macosx64-10.13-clang90.tar.gz` from [https://root.cern.ch/content/release-61206](https://root.cern.ch/content/release-61206)


```
cd /usr/local
sudo mkdir root
cd root
sudo cp ~/Downloads/root_v6.12.06.macosx64-10.13-clang90.tar.gz .
sudo tar -xvf root_v6.12.06.macosx64-10.13-clang90.tar.gz
sudo mv root root_v6.12.06
```


Before running ROOT, need to set the environment variable ROOTSYS and change PATH to include root/bin and library variables. These go into the file ~/.bash_profile Please note: the syntax is for bash, if you are running tcsh you will have to use setenv instead of export.

[https://root.cern.ch/root/htmldoc/guides/users-guide/ROOTUsersGuide.html#installing-root](https://root.cern.ch/root/htmldoc/guides/users-guide/ROOTUsersGuide.html#installing-root)

After install completes, need to setup the environment to be ready to run in future.  Place the following lines in `~/.bash_profile`


```
export ROOTSYS=/usr/local/root/root_v6.12.06
export PATH=$PATH:$ROOTSYS/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ROOTSYS/lib
```


~~Alternately for a particular instance you can use the included script:~~


```
source /usr/local/root/root_v6.XX.YY/bin/thisroot.sh
```



## GATE

**Installing GATE v8.0 **(newer versions available) as this mirrors the install in UCLH


```
sudo mkdir /usr/local/gate
cd /usr/local/gate/
sudo cp ~/Downloads/gate_v8.0.tar.gz .
sudo tar -xvf gate_v8.0.tar.gz
sudo mkdir gate_v8.0-build gate_v8.0-install
cd gate_v8.0-build/
sudo cmake -DBUILD_TESTING=OFF -DCMAKE_BACKWARDS_COMPATIBILITY=2.4 -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local/gate/gate_v8.0-install -DGATE_DOWNLOAD_BENCHMARKS_DATA=ON -DGATE_USE_ECAT7=OFF -DGATE_USE_GEANT4_UIVIS=ON -DGATE_USE_ITK=OFF -DGATE_USE_OPTICAL=OFF -DGATE_USE_STDC11=ON -DGeant4_DIR=/usr/local/geant4/geant4.10.03.p03-install/lib/Geant4-10.3.3 /usr/local/gate/gate_v8.0
```


Had numerous errors when trying to cmake with -DBUILD_TESTING=ON so set to OFF

Testing to see whether ITK is strictly necessary (to reduce install burden).  Have set -DGATE_USE_ITK=OFF (previously =ON) and will test, may need to re-install


```
sudo make -j3
sudo make install
```


After install completes, need to setup the environment to be ready to run in future.  Place the following lines in `~/.bash_profile`:


```
source /usr/local/geant4/geant4.10.03.p03-install/bin/geant4.sh
source /usr/local/root/root_v6.12.06/bin/thisroot.sh
export PATH=$PATH:/usr/local/gate/gate_v8.0-install/bin
