dest=$1
app_id="com.github.lxgr_linux.pokete"

install -Dv "assets/$app_id.desktop" "$dest/share/applications/$app_id.desktop"
install -Dvm644 "assets/$app_id.svg" "$dest/share/icons/hicolor/scalable/apps/$app_id.svg"
install -Dv assets/pokete.metainfo.xml "$dest/share/metainfo/$app_id.metainfo.xml"
install -Dv LICENSE "$dest/share/licenses/$app_id/LICENSE"
install -dv "$dest/bin/"
find . | grep -E "\.py$|\.so$|\.mp3$" | while read file
do
    install -Dv "$file" "$dest/share/pokete/$file"
done
ln -s "../share/pokete/pokete.py" "$dest/bin/"
