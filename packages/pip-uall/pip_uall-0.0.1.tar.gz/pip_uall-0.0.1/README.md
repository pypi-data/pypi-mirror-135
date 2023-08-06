# pip_uall
This project is a little tool for updating `pip`-packages. I wrote this tool because `pip` doesn' have an option for updating all packages.

## Installation
You can install this package with git or `pip`.

### Git
- Clone the repository with  
  ```
  git clone https://github.com/ClasherKasten/pip_uall.git
  ```  
  or download the zipped sources.

- Navigate to the folder where you cloned the repository or where you unzipped the sources.
- Run  
  ```
  pip install .
  ```

### Pip
- Just run ```pip install pip_uall```

## Usage
- Create a file called `.pipuall.ini` in your home directory and add the section `[pip_uall]`. Then under the `pip_commands` option you can specify which pip versions should be used for updating and in the `excluded` option you can specify which packages should not be updated.
- run `pip_uall`