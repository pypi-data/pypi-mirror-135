# discolib

A python library which implements the DISCo protocol to communicate with DISCo-enabled devices.

## Installation
`$ python3 -m pip install discolib`

## Getting started
To start a DISCo-enabled python project:  
`$ python3 -m discolib --init <type>`  
Right now the supported types are:  
- serial
- tcp
- stub

This will generate a `disco.json` config starter file, as well as a `main.py` file which implements the bare-minimum required to use the library to communicate with the device.

## Code gen
To generate code containing knowledge of your desired DISCo attributes, run the following in a directory containing a valid `disco.json` file:  
`$ python3 -m discolib --codegen <language>`  
Right now the supported languages are:  
- C

This whill generate a `disco` directory containing the DISCo source files specifying your attributes. See [examples](../../examples) to see how to build and interface with the code in specific use cases.
