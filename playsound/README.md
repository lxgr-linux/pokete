## Build

Linux
```shell
go build -ldflags "-s -w" -buildmode=c-shared -o ./libplaysound.so
```

Windows
```shell
GOOS=windows CGO_ENABLED=1 CC=x86_64-w64-mingw32-cc go build -ldflags "-s -w" -buildmode=c-shared -o ./libplaysound.dll
```

OSX
```shell
go build -ldflags "-s -w" -buildmode=c-shared -o ./libplaysound.osx.so
```

