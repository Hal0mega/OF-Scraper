r"""
                                                             
        _____                                               
  _____/ ____\______ ________________    ____   ___________ 
 /  _ \   __\/  ___// ___\_  __ \__  \  /  _ \_/ __ \_  __ \
(  <_> )  |  \___ \\  \___|  | \// __ \(  <_> )  ___/|  | \/
 \____/|__| /____  >\___  >__|  (____  /\____/ \___  >__|   
                 \/     \/           \/            \/         
"""

import logging
import re

from rich import print
from rich.console import Console

import ofscraper.utils.profiles.data as profile_data

log = logging.getLogger("shared")
console = Console()
currentData = None
currentProfile = None


def print_profiles() -> list:
    print_current_profile()
    console.print("\n\nCurrent Profiles\n")
    profile_fmt = "Profile: [cyan]{}"
    for name in profile_data.get_profile_names():
        console.print(profile_fmt.format(name))


def print_current_profile():
    current_profile = profile_data.get_active_profile()
    log.info("Using profile: [cyan]{}[/cyan]".format(current_profile))


def profile_name_fixer(input):
    return f"{re.sub('_profile','', input)}_profile" if input else None
