## Hardxor

`hardxor` is a tool to xor a file byte by byte. 

```bash
bash> hexdump inputfile.hex
$ 0000000 69 6d 70 6f 72 74 20 70 61 74 68 6c 69 62 0a 66
  0000010 72 6f 6d 20 73 65 74 75 70 74 6f 6f 6c 73 20 69

bash> python3 -m hardxor inputfile.hex -k 0xe4 -o outputfile.hex

bash> hexdump outputfile.hex
$ 0000000 8d 89 94 8b 96 90 c4 94 85 90 8c 88 8d 86 ee 82
  0000010 96 8b 89 c4 97 81 90 91 94 90 8b 8b 88 97 c4 8d
```
