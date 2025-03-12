from config import Config


class Args(Config):
    debug: bool
    file: str | None
    quit_on_eof: bool
    replay: int | bool
    verbose: int

    version: None
    update: None
