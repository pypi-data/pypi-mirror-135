# frash

Juggling with hex numbers. 

With `frash` you can convert integers and floats to their hexadecimal equivalent.

Below you can find some examples.

## Install

`pip install frash`

## Usage

```console
bash> frash 255
$ 0xff

bash> frash 255.
$ 0x1.fep7

bash> frash 98.2
$ 0x1.88ccccccccccdp6

bash> frash -r 0x1.88ccccccccccdp6
$ 98.2

bash> frash -r 0x2.p7
$ 256

bash> frash -r 1.8p0
$ 1.5

bash> frash -r 1.8
$ 1.5

bash> frash -r 0x1.8
$ 1.5

bash> frash -r 0x1.8p+1
$ 3

bash> frash -r 0x1.8p-2
$ 0.375

bash> frash -r .de
$ 0.867188

bash> frash -r abap1
$ 5492

bash> frash -r ABAP1
$ 5492

bash> frash 1e3
$ 0x1.f4p9

bash> frash 1e-4
$ 0x1.a36e2eb1c432dp-14
```
