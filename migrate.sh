echo "This will migrate your data from ~/.cache/pokete to ~/.local/share/pokete. Press enter to continue."

read -r n

cp -r -i ~/.cache/pokete ~/.local/share/pokete
