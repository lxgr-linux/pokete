from pathlib import Path
import json

def main():
    lang_path = Path(__file__).parent / "lang"
    lang_file = lang_path / "en_US.json"
    schema_file = lang_path / "schema.json"

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "title": "Pokete Translation File Schema",
        "properties": {}
    }

    if not lang_file.is_file():
        print(f"en_US.json file not found in directory {lang_file} Abort.")
        return

    with open(lang_file) as en_US:
        data = json.load(en_US)

        for key in data:
            if key == "$schema":
                continue

            schema["properties"][key] = {
                "type": "string"
            }

    with open(schema_file, "w") as schema_file:
        json.dump(schema, schema_file, indent=2)


if __name__ == '__main__':
    main()
