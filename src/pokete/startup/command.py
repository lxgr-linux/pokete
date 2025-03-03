from pokete.release import CODENAME, SAVEPATH, VERSION
from pokete.util.command.command import Flag, RootCommand

class PoketeCommand:
    log_flag = Flag(["--log"], "Enables logging")
    mods_flag = Flag(["--no_mods"], "Disables mods")
    audio_flag = Flag(["--no_audio"], "Disables audio")

    def __init__(self, audio):
        self.do_logging = False
        self.load_mods = True
        audio.use_audio = True
        self.audio = audio

    def root_fn(self, ex: str, options: list[str],
                flags: dict[str, list[str]]):
        for flag in flags:
            if self.log_flag.is_flag(flag):
                self.do_logging = True
            elif self.mods_flag.is_flag(flag):
                self.load_mods = False
            elif self.audio_flag.is_flag(flag):
                self.audio.use_audio = False

    def run(self) -> tuple[bool, bool]:
        c = RootCommand(
            "Pokete", f"{CODENAME} v{VERSION}", self.root_fn,
            flags=[self.log_flag, self.mods_flag, self.audio_flag],
            additional_info=f"""All save and logfiles are located in ~{SAVEPATH}/
        Feel free to contribute.
        See README.md for more information.
        This software is licensed under the GPLv3, you should have gotten a
        copy of it alongside this software.""",
            usage=""
        )

        c.exec()

        return self.do_logging, self.load_mods
