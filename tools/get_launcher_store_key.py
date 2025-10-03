from shutil import rmtree
from subprocess import run


def main():
    dest = "./launcher"
    run(
        [
            R"C:\Program Files\nodejs\npx.cmd",
            "asar",
            "extract",
            R"C:\Program Files\Roberts Space Industries\RSI Launcher\resources\app.asar",
            dest,
        ],
        check=True,
    )

    with open(Rf"{dest}\lib\main.js") as f:  # fmt: skip # pylint: disable=unspecified-encoding
        contents = f.read()
        i = contents.index("encryptionKey")
        key = contents[i + 15 : i + 59]
        print(key)

    rmtree(dest)


if __name__ == "__main__":
    main()
