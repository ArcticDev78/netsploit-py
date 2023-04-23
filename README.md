# netsploit-py
### This is a project to help you use nmap and similar network tools easily and efficiently.


#### NOTE:
- This is a work-in-progress project. Surely many things can be improved here and there, so feel free to open an issue about it.
- If something doesn't work on your platform, please feel free to open an issue about it.
- This project is made targeted for Linux platform. So there it might not work on other platforms. It might work on macOS with some changes.

Install required `pip` packages:

```
pip install simple-colors

pip install pickleDB

pip install tabulate
```

### REQUIRED FOR SETUP:
> You must create folders for logging:
```sh
# First make sure that you are in the git repository folder of netsploit
mkdir logs/
cd logs/
mkdir device-info network-scanner os-guesser oui-lookup port-scanner vuln-scanner
```