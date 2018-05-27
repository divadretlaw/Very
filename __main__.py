#!/usr/bin/env python3
# coding: utf-8

import datetime
import sys

from configuration import Configuration
from osHelper import OSHelper
from printer import Printer
from updater import Updater

config = Configuration()


def additional_command(command):
    cmd = config.get_additional_commands_of(command)

    if cmd is not None:
        packages = ""

        if len(sys.argv) < 3:
            print(u'\U0001F6AB' + " No subcommand provided for '" + sys.argv[1] + "'")
            return

        for x in range(3, len(sys.argv)):
            packages += " " + sys.argv[x]

        if sys.argv[2] in cmd and cmd[sys.argv[2]] != "":
            OSHelper.run(cmd[sys.argv[2]] + packages)
        else:
            print(u'\U0001F6AB' + " Unknown subcommand of '" + sys.argv[1] + "'")

    return


def arguments_from(from_):
    arguments = ""
    for x in range(from_, len(sys.argv)):
        arguments += " " + sys.argv[x]
    return arguments


def install():
    packages = arguments_from(2)

    main = config.get_main_package_manager()
    if main is not None:
        print(u'\U00002795' + " Installing packages using '" + main["command"] + "'...")
        OSHelper.run(main["install"] + packages)
    return


def remove():
    packages = arguments_from(2)

    main = config.get_main_package_manager()
    if main is not None:
        print(u'\U00002796' + " Removing packages using '" + main["command"] + "'...")
        OSHelper.run(main["remove"] + packages)
    return


def search():
    packages = arguments_from(2)

    main = config.get_main_package_manager()
    if main is not None:
        OSHelper.run(main["search"] + packages)
    return


def ls():
    packages = arguments_from(2)

    main = config.get_main_package_manager()
    if main is not None:
        OSHelper.run(main["list"] + packages)
    return


def clean():
    print(u'\U0000267B\U0000fe0f' + "  Cleaning system...")
    main = config.get_main_package_manager()
    OSHelper.run_if(main["command"], main["clean"])

    for packageManger in config.get_additional():
        OSHelper.run_if(packageManger["command"], packageManger["clean"])

    print(u'\U0001f5d1' + "  Emptying trash...")

    if sys.platform == "darwin":
        OSHelper.run("rm -rf $HOME/.Trash/*")
    else:
        OSHelper.run("rm -rf $HOME/.local/share/Trash/files/*")
        OSHelper.run("rm -rf $HOME/.local/share/Trash/info/*.trashinfo")

    return


def additional_clean():
    print(u'\U0000267B\U0000fe0f' + "  Running additional clean commands...")

    for x in config.data["additional_clean_commands"]:
        print("Running '" + x + "'...")
        OSHelper.run(x)


def update():
    for p in config.get_package_mangers():
        if OSHelper.has_package(p["command"]):
            print(u'\U0001f4e6' + " Updating packages using '" + p["command"] + "'...")
            OSHelper.run(p["update"])
            OSHelper.run(p["upgrade"])

    for x in config.get_additional():
        if OSHelper.has_package(x["command"]):
            if x["update"] != "":
                print(u'\U0001f4e6' + " Updating packages using '" + x["command"] + "'...")
                OSHelper.run(x["update"])
                OSHelper.run(x["upgrade"])
    return


def upgrade():
    print(u'\U0001f504' + " Upgrading System...")
    for p in config.get_package_mangers():
        OSHelper.run_if(p["command"], p["system_upgrade"])
    return


def ip():
    OSHelper.run("curl " + config.get_sources()["ip"])
    return


def ping():
    print(u'\U0001F310' + " Starting ping test...")
    OSHelper.run("ping " + config.get_sources()["ping"])
    return


def download():
    print(u'\U00002b07\U0000fe0f' + "  Starting download test...")
    OSHelper.run("curl _sLko /dev/null " + config.get_sources()["downloadtest"])
    return


def hosts():
    hosts = config.get_sources()["hosts"]
    sudo = ""
    if hosts["sudo"]:
        sudo = "sudo"

    target = hosts["target"]

    print(u'\U0001F4DD' + " Updating '" + target + "' from '" + hosts["source"] + "'...")

    OSHelper.run("echo '# Last updated: {:%Y-%m-%d %H:%M:%S}".format(
        datetime.datetime.now()) + "\n' | " + sudo + " tee " + target + " > /dev/null")

    if hosts["defaults"]:
        OSHelper.run(
            "echo '127.0.0.1 localhost\n::1 localhost\n255.255.255.255 broadcasthost\n127.0.0.1 "
            + OSHelper.name()
            + "\n' | "
            + sudo + " tee -a "
            + target + " > /dev/null")

    OSHelper.run("curl -#SLk " + hosts[
        "source"] + " | grep '^[^#]' | grep 0.0.0.0 | " + sudo + " tee -a " + target + " > /dev/null")
    return


def wallpaper():
    print(u'\U00002b07\U0000fe0f' + "  Downloading Wallpaper from '" + config.get_sources()["wallpaper"] + "'...")
    OSHelper.run("curl -#SLko $HOME/Pictures/Wallpaper.jpg " + config.get_sources()["wallpaper"])

    print(u'\U0001f5bc' + " Setting wallpaper...")
    if sys.platform == "darwin":
        OSHelper.run(
            "sqlite3 ~/Library/Application\ Support/Dock/desktoppicture.db "
            + "\"update data set value = '~/Pictures/Wallpaper.jpg'\" && killall Dock")
    elif sys.platform.startswith('linux'):
        if OSHelper.has_package("gsettings"):
            OSHelper.run("gsettings set org.gnome.desktop.background picture-uri file://$HOME/Pictures/Wallpaper.jpg")
            OSHelper.run("gsettings set org.gnome.desktop.screensaver picture-uri file://$HOME/Pictures/Wallpaper.jpg")
    return


def update_very():
    print(u'\U00002935\U0000fe0f' + "  Updating 'very'...")
    Updater.update_file("updater.py")
    OSHelper.run("python3 updater.py")
    return


def very():
    if len(sys.argv) < 2:
        Printer.error_message(sys.argv[0])
        exit()
    else:
        if sys.argv[1] == "very":
            config.get_config()
            exit()
        elif sys.argv[1] == "install":
            install()
        elif sys.argv[1] == "remove":
            remove()
        elif sys.argv[1] == "search":
            search()
            exit()
        elif sys.argv[1] == "list" or sys.argv[1] == "ls":
            ls()
            exit()
        elif sys.argv[1] == "clean":
            clean()
        elif sys.argv[1] == "wow-clean":
            clean()
            additional_clean()
        elif sys.argv[1] == "update":
            update()
        elif sys.argv[1] == "system-update":
            upgrade()
        elif sys.argv[1] == "much-update":
            update()
            upgrade()
        elif sys.argv[1] == "ip":
            ip()
            exit()
        elif sys.argv[1] == "ping":
            ping()
        elif sys.argv[1] == "download":
            download()
        elif sys.argv[1] == "hosts":
            hosts()
        elif sys.argv[1] == "wallpaper":
            wallpaper()
        elif sys.argv[1] == "very-update":
            update_very()
        elif any(sys.argv[1] in additional["id"] for additional in config.get_additional()):
            additional_command(sys.argv[1])
            exit()
        else:
            print(u'\U0001F6AB' + " Unknown command '" + sys.argv[1] + "'\n")
            Printer.error_message(sys.argv[0])
            exit()
        print(u'\U00002705' + " Done.")


if __name__ == "__main__":
    very()
