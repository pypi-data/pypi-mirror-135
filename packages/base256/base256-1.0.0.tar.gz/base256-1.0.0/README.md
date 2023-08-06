# base256

When base64 just isn't enough

## Installation

### From PyPI

```sh
pip3 install base256
```

### From GitHub

```sh
pip3 install git+https://github.com/donno2048/base256
```

## Usage

Please only use even-length hexadecimal values.

### In Python

```py
from os import remove
from base256 import encode, decode, encode_hex, decode_hex, encode_file, decode_file, encode_string, decode_string
print(encode('123456789abcdef0'))
print(decode('ĒĴŖŸƚƼǞǰ'))
print(encode_hex(0x123456789abcdef0))
print(decode_hex('ĒĴŖŸƚƼǞǰ'))
print(hex(decode_hex('ĒĴŖŸƚƼǞǰ')))
print(encode_file('README.md'))
print(decode_file('ģĠŢšųťĲĵĶĊĊŗŨťŮĠŢšųťĶĴĠŪŵųŴĠũųŮħŴĠťŮůŵŧŨĊĊģģĠŉŮųŴšŬŬšŴũůŮĊĊģģģĠņŲůŭĠŐŹŐŉĊĊŠŠŠųŨĊŰũŰĳĠũŮųŴšŬŬĠŢšųťĲĵĶĊŠŠŠĊĊģģģĠņŲůŭĠŇũŴňŵŢĊĊŠŠŠųŨĊŰũŰĳĠũŮųŴšŬŬĠŧũŴīŨŴŴŰųĺįįŧũŴŨŵŢĮţůŭįŤůŮŮůĲİĴĸįŢšųťĲĵĶĊŠŠŠĊĊģģĠŕųšŧťĊĊŐŬťšųťĠůŮŬŹĠŵųťĠťŶťŮĭŬťŮŧŴŨĠŨťŸšŤťţũŭšŬĠŶšŬŵťųĮĊĊģģģĠŉŮĠŐŹŴŨůŮĊĊŠŠŠŰŹĊŦŲůŭĠůųĠũŭŰůŲŴĠŲťŭůŶťĊŦŲůŭĠŢšųťĲĵĶĠũŭŰůŲŴĠťŮţůŤťĬĠŤťţůŤťĬĠťŮţůŤťşŨťŸĬĠŤťţůŤťşŨťŸĬĠťŮţůŤťşŦũŬťĬĠŤťţůŤťşŦũŬťĬĠťŮţůŤťşųŴŲũŮŧĬĠŤťţůŤťşųŴŲũŮŧĊŰŲũŮŴĨťŮţůŤťĨħıĲĳĴĵĶķĸĹšŢţŤťŦİħĩĩĊŰŲũŮŴĨŤťţůŤťĨħǄƒǄƴǅƖǅƸǆƚǆƼǇƞǄƏħĩĩĊŰŲũŮŴĨťŮţůŤťşŨťŸĨİŸıĲĳĴĵĶķĸĹšŢţŤťŦİĩĩĊŰŲũŮŴĨŤťţůŤťşŨťŸĨĩĩĊŰŲũŮŴĨťŮţůŤťşŦũŬťĨħŒŅŁńōŅĮŭŤħĩĩĊŰŲũŮŴĨŤťţůŤťşŦũŬťĨĬĠħŴťŭŰħĩĩĊŲťŭůŶťĨħŴťŭŰħĩĊŰŲũŮŴĨťŮţůŤťşųŴŲũŮŧĨħňťŬŬůĬĠŷůŲŬŤġħĩĩĊŰŲũŮŴĨŤťţůŤťşųŴŲũŮŧĨħħĩĩĊŠŠŠĊĊģģģĠŉŮĠŴŨťĠţůŭŭšŮŤĠŬũŮťĊĊŠŠŠųŨĊŢšųťĲĵĶĊŠŠŠĊ', 'temp'))
remove('temp')
print(encode_string('Hello, world!'))
print(decode_string('ňťŬŬůĬĠŷůŲŬŤġ'))
```

### In the command line

```sh
base256
```
