dest=$1

install -Dv assets/com.github.lxgr-linux.pokete.desktop "$dest/share/applications/com.github.lxgr-linux.pokete.desktop"
install -Dvm644 assets/com.github.lxgr-linux.pokete.svg "$dest/share/icons/hicolor/scalable/apps/com.github.lxgr-linux.pokete.svg"
install -Dv assets/pokete.metainfo.xml "$dest/share/metainfo/com.github.lxgr_linux.pokete.metainfo.xml"
install -Dv LICENSE "$dest/share/licenses/com.github.lxgr_linux.pokete/LICENSE"
install -dv "$dest/bin/"
find . | grep -E "\.py$|\.so$|\.mp3$" | while read file
do
    install -Dv "$file" "$dest/share/pokete/$file"
done
ln -s "../share/pokete/pokete.py" "$dest/bin/"
