from requests import get


def main() -> None:
    page = get(
        "https://robertsspaceindustries.com/en/download",
        timeout=15,
    ).text.splitlines()
    for line in page:
        if "install.robertsspaceindustries.com" in line:
            print(line)


if __name__ == "__main__":
    main()
