## Build

### Linux
```shell
go build -ldflags "-s -w" -buildmode=c-shared -o ./libplaysound.x86_64.so
```

### Windows
```shell
GOOS=windows CGO_ENABLED=1 CC=x86_64-w64-mingw32-cc go build -ldflags "-s -w" -buildmode=c-shared -o ./libplaysound.x86_64.dll
```

### OSX
x86
```shell
build -ldflags "-s -w" -buildmode=c-shared -o ./libplaysound.x86_64.osx.so
```

arm64
```shell
GOOS=darwin GOARCH=arm64 go build -ldflags "-s -w" -buildmode=c-shared -o ./libplaysound.arm64.osx.so
```
