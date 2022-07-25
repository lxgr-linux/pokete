## Build

UNIX
```
go build -buildmode=c-shared -o ./libplaysound.so
```

Windows
```
GOOS=windows CGO_ENABLED=1 CC=x86_64-w64-mingw32-cc go build -buildmode=c-shared -o ./libplaysound.dll
```

