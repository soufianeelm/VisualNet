
# Network Traffic Flow Visualizer Project

As part of the LU3IN033 Networking course, taught in the 3rd year of the Computer Science degree at Sorbonne University, we developed a Python program that allows the visualization of one or more network traffic flows. 
This application takes as input a text file, called a trace, containing the bytes captured on an Ethernet network.
Details on the input file format will be provided later.

We used the tkinter module, which is part of Python’s standard library, to create the graphical interface.

## Installation

Instructions to install our program on major operating systems

### Step 1 (Linux Users)

Ensure that development libraries are installed:

```bash
sudo apt-get install python3-dev
```

### Step 2 (Linux, Mac, Windows Users)

Use the [pip](https://pip.pypa.io/en/stable/) module to install pyinstaller: 

```bash
pip3 install pyinstaller
```

### Step 3 (Linux, Mac, Windows Users)

Navigate to the folder containing the source code and run:

```bash
pyinstaller codesource.py --onefile
```

This command creates a "dist" folder containing the executable along with other necessary files for the program to run.

### Step 4 

Move the "logo.png" and "test.txt" files into the folder containing the executable.

## Usage

After following the installation instructions, go to the "dist" folder and launch the executable by double-clicking the file, or by using the command:

Windows :

```bash
start codesource.exe
```

The program will launch and a graphical interface will appear.

![alt text](https://github.com/soufianeelm/Reseau/blob/main/image_2022-12-09_230907208.png?raw=true)

To launch the visualization of a trace, drag the file containing the trace into the folder where the executable is located.

Then, enter the name of the file (without the extension) in the input field.

A new window will appear, showing the visualization of the network traffic flows captured in the trace.

![alt text](https://github.com/soufianeelm/Reseau/blob/main/image_2022-12-09_231532572.png?raw=true)

To filter the searches, use the input field and search button at the bottom of the window.

Insert the desired filter, then click the "search" button.

To cancel the filtering, run the search with an empty filter.

## Questions

Answers to some potential questions from users.

### What format is supported for the input file?

The program supports the following format:

- A raw text file (.txt)
- For each frame, each line begins with an offset variable, represented by 4 hexadecimal digits, which is equal to the address of the first byte on the line.
- For each line, the bytes are separated from the offset and the ASCII characters at the end of the line by 3 spaces.
- Bytes are separated by a single space between them.
- Frames are separated by a blank line. 
     
### What filters are available?

There are a total of 17 filters.

For IP address filters, they follow this form (e.g., 0.0.0.0):

- 0.0.0.0 (the source IP or destination IP can be equal to 0.0.0.0)
- 0.0.0.0 and 1.1.1.1 (either source IP = 0.0.0.0 and destination IP = 1.1.1.1, or vice versa)
- ip.src == 0.0.0.0 (the source IP must be equal to 0.0.0.0)
- ip.dst == 0.0.0.0 (the destination IP must be equal to 0.0.0.0)
- ip.src == 0.0.0.0 and ip.dst == 1.1.1.1 (the source IP must be equal to 0.0.0.0 and the destination IP must be equal to 1.1.1.1)

For protocol filters, only 2 filters are available:

- tcp
- http

The remaining filters are combinations of IP address filters and protocol filters:

- [IP filter] and [protocol filter]
