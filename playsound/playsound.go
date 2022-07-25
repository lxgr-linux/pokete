package main

import (
	"C"
	"fmt"
	"os"
	"time"

	"github.com/hajimehoshi/go-mp3"
	"github.com/hajimehoshi/oto/v2"
)

//export playsound
func playsound(file *C.char) {
	fmt.Println("1")
	f, err := os.Open(C.GoString(file))
	if err != nil {
		panic(err)
	}
	defer f.Close()

	fmt.Println("2")
	d, err := mp3.NewDecoder(f)
	if err != nil {
		fmt.Println(err)
		panic(err)
	}

	fmt.Println("3")
	c, ready, err := oto.NewContext(d.SampleRate(), 2, 2)
	if err != nil {
		fmt.Println(err)
		panic(err)
	}
	<-ready

	fmt.Println("4")
	p := c.NewPlayer(d)
	defer p.Close()
	p.Play()

	fmt.Println("5")
	fmt.Printf("Length: %d[bytes]\n", d.Length())
	for {
		time.Sleep(time.Second)
		if !p.IsPlaying() {
			break
		}
	}
}

func main() {
}
