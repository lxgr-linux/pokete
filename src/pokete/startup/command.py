import logging
from pathlib import Path
import sys
from pokete.release import CODENAME, SAVEPATH, VERSION, SAVEPATH
from pokete.util.command.command import Flag, RootCommand

class PoketeCommand:
    log_flag = Flag(["--log"], "Enables logging")
    mods_flag = Flag(["--no_mods"], "Disables mods")
    audio_flag = Flag(["--no_audio"], "Disables audio")
    save_dir_flag = Flag(["--save_dir"], f"Sets the path for save-files and logs, default is: {SAVEPATH}")

    def __init__(self, audio):
        self.do_logging = False
        self.load_mods = True
        audio.use_audio = True
        self.audio = audio
        self.save_dir:Path = SAVEPATH

    def root_fn(self, ex: str, options: list[str],
                flags: dict[str, list[str]]):
        for flag, values in flags.items():
            if self.log_flag.is_flag(flag):
                self.do_logging = True
            elif self.mods_flag.is_flag(flag):
                self.load_mods = False
            elif self.audio_flag.is_flag(flag):
                self.audio.use_audio = False
            elif self.save_dir_flag.is_flag(flag):
                if len(values) != 1:
                    logging.error("Flag '%s' takes exactly one argument", flag)
                    sys.exit(1)
                self.save_dir = Path(flags[flag][0])

    def run(self) -> tuple[bool, bool, Path]:
        c = RootCommand(
            "Pokete", f"{CODENAME} v{VERSION}", self.root_fn,
            flags=[self.log_flag, self.mods_flag, self.audio_flag, self.save_dir_flag],
            additional_info=f"""All save and logfiles are located in ~{SAVEPATH}/
        Feel free to contribute.
        See README.md for more information.
        This software is licensed under the GPLv3, you should have gotten a
        copy of it alongside this software.""",
            usage=""
        )

        c.exec()

        return self.do_logging, self.load_mods, self.save_dir
