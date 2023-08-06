# Mikrotik HTML Dumper

---

This is a small project written since my team worked with mikrotiks and we sometimes needed to present audits of the configuration for upper manangement in a quick and easy to read format.

## Installing

You can use pip to install this script

```pip install mikrotik_html_documentation```

## General Use

One installed, you can see the options available to you by running the help parameter

```bash
mt-html --help
Usage: mt-html [OPTIONS] COMMAND [ARGS]...

  This simple tool logins to a Mikrotik and creats an HTML dump

Options:
  --help  Show this message and exit.

Commands:
  dump
  env
```

## Requirements

You'll need to setup a .env file for the username and password. You can do so by running the following command

```mt-html generate-env```

It will then ask you to enter the username and password which will be stored in a .env file for you from the current working directory of the script.


# Usage

---

To use the script, simply run the following

```mt-html html-dump -f <firewall>```

It will then ask you to enter the IP or FQDN of the firewall and dump out HTML code so you can easily upload to markup language supported documentation systems, or simply share it as a web file.
Files are created and can be located in your home directory

```~/mikrotik_html_dump```

# License

---

Apache-2.0




