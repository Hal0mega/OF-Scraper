r"""
                                                             
        _____                                               
  _____/ ____\______ ________________    ____   ___________ 
 /  _ \   __\/  ___// ___\_  __ \__  \  /  _ \_/ __ \_  __ \
(  <_> )  |  \___ \\  \___|  | \// __ \(  <_> )  ___/|  | \/
 \____/|__| /____  >\___  >__|  (____  /\____/ \___  >__|   
                 \/     \/           \/            \/         
"""

import json
import logging

from humanfriendly import parse_size

import ofscraper.prompts.prompts as prompts
import ofscraper.utils.binaries as binaries
import ofscraper.utils.config.context as config_context
import ofscraper.utils.config.file as config_file
import ofscraper.utils.config.schema as schema
import ofscraper.utils.console as console_
import ofscraper.utils.paths.common as common_paths

console = console_.get_shared_console()
log = logging.getLogger("shared")


def read_config(update=True):
    with config_context.config_context():
        config = config_file.open_config()
        if update and schema.config_diff(config):
            config = config_file.auto_update_config(config)
        if config.get("config"):
            config = config["config"]
        return config


def update_config(field: str, value):
    p = common_paths.get_config_path()
    with open(p, "r") as f:
        config = json.load(f)

    config["config"].update({field: value})

    config_file.write_config(config)


def edit_config():
    with config_context.config_context():
        config = config_file.open_config()
        updated_config = prompts.config_prompt()
        config = update_config_full(config, updated_config)
        config_file.write_config(config)
        console.print("`config.json` has been successfully edited.")


def edit_config_advanced():
    with config_context.config_context():
        config = config_file.open_config()
        updated_config = prompts.config_prompt_advanced()
        config = update_config_full(config, updated_config)
        config_file.write_config(config)
        console.print("`config.json` has been successfully edited.")


def update_config_full(config, updated_config):
    config = config_file.open_config()
    if config.get("config"):
        config = config["config"]
    if updated_config.get("config"):
        updated_config = updated_config["config"]
    config.update(updated_config)
    return config


def update_mp4decrypt():
    config = {"config": read_config()}
    if prompts.auto_download_mp4_decrypt() == "Yes":
        config["config"]["mp4decrypt"] = binaries.mp4decrypt_download()
    else:
        config["config"]["mp4decrypt"] = prompts.mp4_prompt(config["config"])
    config_file.write_config(config)


def update_ffmpeg():
    config = {"config": read_config()}
    if prompts.auto_download_ffmpeg() == "Yes":
        config["config"]["ffmpeg"] = binaries.ffmpeg_download()
    else:
        config["config"]["ffmpeg"] = prompts.ffmpeg_prompt((config["config"]))
    config_file.write_config(config)
