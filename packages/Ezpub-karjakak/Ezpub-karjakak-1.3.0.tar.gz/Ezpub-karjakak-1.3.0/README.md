# Ezpub [cli-environment]
## Tool to help developer to publish package to PyPI

## Installation
```
pip3 install Ezpub-karjakak
```
## Usage
**Create token for variable environment and save it for publish with twine [token key-in in tkinter simpledialog for showing in hidden].**
```
ezpub -t None
```
**Delete saved token.**
```
ezpub -t d
```
**Create save token.**
```
# Windows
ezpub -t %VARTOKEN%

# MacOS X
ezpub -t $VARTOKEN
```
**Building the package and create [build, dist, and package.egg-info] for uploading to PyPI.**  
```
# Window
ezpub -b "\package-path"

# MacOS X
ezpub -b /package_path
```
**TAKE NOTE:**
* **Ezpub will try to move existing [build, dist, and package.egg-info] to created archive folder and create new one.**
    * **If Exception occured, user need to remove them manually.**

**Pubish to PyPI.**
```
# For Windows only
ezpub -p \package-path\dist\*

# For MacOS X
ezpub -p "package_path/dist/*"
```
**TAKE NOTE:**
* **If token is not created yet, ~~it will start process "-t" automatically~~ user will be prompt to create first.**
* **Some firewall not allowed moving files to archive, you may exclude Ezpub from it.**
* **You can move the files manually and using `py -m build`  instead. [Please see the source code for assurance]**
* **MacOS X:**
    * **Extra secure with locking.**
* **Dependency:**
    * **twine**
    * **Clien**
    * **filepmon**
    * **filfla**
## Links
* **https://packaging.python.org/tutorials/packaging-projects/**
* **https://twine.readthedocs.io/en/latest/**