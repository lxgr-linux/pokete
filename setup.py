#!/usr/bin/env python3

import os
import shutil
from setuptools import setup


def package_file_to_pokete(file: str) -> None:
    print(f"  Packaging {file} ...")
    replace_paths = [
        ("import pokete_data as p_data", "import pokete.pokete_data as p_data"),
        ("from pokete_data", "from pokete.pokete_data"),
        ("import pokete_classes", "import pokete.pokete_classes"),
        ("from pokete_classes", "from pokete.pokete_classes"),
        ("from pokete_general_use_fns import",
            "from pokete.pokete_general_use_fns import"),
        ("from release import", "from pokete.release import")
    ]

    with open(file, 'r') as f:
        data = f.read()

    for text, replace in replace_paths:
        data = data.replace(text, replace)

    if file == "pokete.py":
        data = data.replace('if __name__ == "__main__":', 'if True:')

    with open(os.path.join('pokete', file), 'w') as f:
        f.write(data)


def main():
    for directory in ["pokete_data", "pokete_classes"]:
        print(f"Processing directory '{directory}'...")
        os.makedirs(os.path.join("pokete", directory), exist_ok=True)
        for file in os.listdir(directory):
            file = os.path.join(directory, file)
            if os.path.isfile(file):
                package_file_to_pokete(file)

    print("Packaging root file scripts...")
    for file in ["pokete.py", "pokete_general_use_fns.py", "release.py"]:
        package_file_to_pokete(file)

    print("Packaging new '__init__.py' file...")
    with open(os.path.join("pokete", "__init__.py"), 'w') as f:
        f.write("""def run_pokete():
    import pokete.pokete

if __name__ == "__main__":
    run_pokete()
""")

    print("Packaging assets...")
    asset_path = os.path.join("assets", "music")
    os.makedirs(os.path.join("pokete", asset_path), exist_ok=True)
    for file in os.listdir(asset_path):
        file = os.path.join(asset_path, file)
        if os.path.isfile(file):
            print(f"  Packaging '{file}'...")
            shutil.copyfile(file, os.path.join("pokete", file))

    setup()
    # For setuptools<44.0 uncomment the following lines instead
    #setup(
    #    name="pokete",
    #    version="0.7.3",
    #    description="A terminal based Pokemon like game",
    #    author="lxgr-linux",
    #    author_email="lxgr@protonmail.com",
    #    license="GPL-3.0",
    #    packages=["pokete", "pokete.pokete_data", "pokete.pokete_classes"],
    #    entry_points={
    #        'console_scripts': [
    #            'pokete = pokete:run_pokete'
    #        ]
    #    },
    #    install_requires=[
    #        "scrap_engine >= 1.2.0",
    #        "playsound",
    #        "pygobject",
    #        "pynput"
    #    ],
    #    include_package_data=True
    #)


if __name__ == "__main__":
    main()
