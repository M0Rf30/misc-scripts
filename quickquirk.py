#!/usr/bin/env python

import configparser
import dmidecode
import os
import sys
import requests


def print_warnings():
    warn = dmidecode.get_warnings()
    if warn:
        print("### WARNING: %s" % warn)
        dmidecode.clear_warnings()


def is_connected():
    try:
        response = requests.get("http://www.google.com")
        print("response code: " + str(response.status_code) + "\n")
    except requests.ConnectionError:
        print("Could not connect")
        quit()


def read_values():
    # Check if running as root .... provide a warning if not
    root_user = (os.getuid() == 0 and True or False)
    if not root_user:
        print("####  NOT RUNNING AS ROOT")
        sys.exit()

    if root_user:
        dmixml = dmidecode.dmidecodeXML()
        dmixml.SetResultType(dmidecode.DMIXML_DOC)
        xmldoc = dmixml.QuerySection('system')

        tree = xmldoc.xpathNewContext()

# What to look for - XPath expressions
        vendorpath = "/dmidecode/SystemInfo/Manufacturer"
        productpath = "/dmidecode/SystemInfo/ProductName"

        vendorlist = tree.xpathEval(vendorpath)
        productlist = tree.xpathEval(productpath)
        vendor = vendorlist[0].get_content()
        product = productlist[0].get_content()
        print_warnings()
        return(vendor, product)


def search_notebook(vendor, product):
    branch = "master"
    dburl = "https://raw.githubusercontent.com/M0Rf30/quickquirk_db/" + \
            branch + "/" + vendor + "/" + product
    quirks = requests.get(dburl)
    return quirks


def print_quirks(quirks):
    parser = configparser.ConfigParser()
    parser.read_string(quirks)


is_connected()
vendor, product = read_values()
quirks = search_notebook(vendor.rstrip(' '), product.rstrip(' '))
print_quirks(quirks.text)
