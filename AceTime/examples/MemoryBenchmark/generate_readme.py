#!/usr/bin/python3
#
# Python script that regenerates the README.md from the embedded template. Uses
# ./generate_table.awk to regenerate the ASCII tables from the various *.txt
# files.

from subprocess import check_output

nano_results = check_output(
    "./generate_table.awk < nano.txt", shell=True, text=True)
micro_results = check_output(
    "./generate_table.awk < micro.txt", shell=True, text=True)
samd_results = check_output(
    "./generate_table.awk < samd.txt", shell=True, text=True)
stm32_results = check_output(
    "./generate_table.awk < stm32.txt", shell=True, text=True)
esp8266_results = check_output(
    "./generate_table.awk < esp8266.txt", shell=True, text=True)
esp32_results = check_output(
    "./generate_table.awk < esp32.txt", shell=True, text=True)
teensy32_results = check_output(
    "./generate_table.awk < teensy32.txt", shell=True, text=True)

print(f"""\
# Memory Benchmark

The `MemoryBenchmark.ino` was compiled with each `FEATURE_*` and the flash
memory and static RAM sizes were recorded. The `FEATURE_BASELINE` selection is
the baseline, and its memory usage  numbers are subtracted from the subsequent
`FEATURE_*` memory usage.

**Version**: AceTime v1.8.0

**DO NOT EDIT**: This file was auto-generated using `make README.md`.

## How to Regenerate

To regenerate this README.md:

```
$ make clean_benchmarks
$ make benchmarks
$ make README.md
```

The `make benchmarks` target uses `collect.sh` script which calls `auniter.sh`
(https://github.com/bxparks/AUniter) to invoke the Arduino IDE programmatically.
It produces a `*.txt` file with the flash and ram usage information (e.g.
`nano.txt`). It now takes about 16 minutes to generate the `*.txt` files on my
quad-core Intel Core i7-3840QM CPU @ 2.80GHz laptop.

The `make README.md` command calls the `generated_readme.py` Python script which
generates this `README.md` file. The ASCII tables below are generated by the
`generate_table.awk` script, which takes each `*.txt` file and converts it to an
ASCII table.

## Library Size Changes

In v1.3:
* The `BasicZoneManager` and `ExtendedZoneManager` classes were unified under a
  new parent interface `ZoneManager`. This seems to have caused the flash size
  to increase by around 1200 bytes on the AVR processors (Nano, Pro Micro),
  about 500 bytes on a SAMD, about 800 bytes on a ESP8266, 100 bytes on a ESP32,
  and 1400 bytes on a Teensy 3.2. The 8-bit processors suffer the most flash
  size increase proportional to their limited 32kB limit.
* Adding the `ZoneManager` interface simplifies a lot of the complexity with
  saving and restoring time zones using the `TimeZoneData` object, and I think
  it is worth the extra cost of flash size. The mitigating factor is that
  applications targetted towards 8-bit processors will normally have fixed
  number of timezones at compile time, so they can avoid using a `ZoneManager`,
  and avoid this penalty in flash size.

In v1.4.1+:
* Removed the `ZoneInfo::transitionBufSize` field from the `ZoneInfo` struct,
  which saves 1 byte on 8-bit processors (none on 32-bit processors due to
  4-byte alignment). We save 266 bytes for `BasicZoneManager` and 386 bytes for
  `ExtendedZoneManager` when all the zones are loaded into the zone registry.
* Incorporated zoneName compression causes flash/ram usage to increase by
  ~250/120 bytes when using only 1-2 zones, but *decreases* flash consumption by
  1200-2400 bytes when all the zones are loaded into the `ZoneManager`.

In v1.5+:
* Changing `ZoneProcessorCache::getType()` from a `virtual` to a non-virtual
  method saves 250-350 bytes of flash memory when using a `BasicZoneManager` or
  an `ExtendedZoneManager` on an 8-bit AVR processor. Unexpectedly, the flash
  memory consumption *increases* slightly (~0-50 bytes) for some ARM processors
  and the ESP32. Since those processors have far more flash memory, this seems
  like a good tradeoff.
* Changing `BasicZoneProcessor` and `ExtendedZoneProcessor` to be subclasses of
  the templatized `BasicZoneProcessorTemplate` and
  `ExtendedZoneProcessorTemplate` classes causes reduction of flash consumption
  by 250-400 bytes for 32-bit processors. Don't know why. (Very little
  difference for 8-bit AVR).
* Adding a `BrokerFactory` layer of indirection (to support more complex
  ZoneProcessors and Brokers) causes flash memory to go up by 100-200 bytes.

In v1.6:
* Added support for `LinkRegistry` to `BasicZoneManager` and
  `ExtendedZoneManager`. This increases the flash memory usage by 150-500 bytes
  when using one of these classes due to the code required by `LinkRegistrar`.
  This extra cost is incurred even if the `LinkRegistry` is set to 0 elements.
  Each `LinkEntry` consumes 8 bytes (2 x `uint32_t`). So a
  `zonedb::kLinkRegistry` with 183 elements uses 1464 extra bytes of flash; a
  `zonedbx::kLinkRegistry` with 207 elements uses 1656 extra bytes.

In v1.7:
* The virtual destructor on the `Clock` base class removed. This reduced the
  flash usage by 618 bytes on AVR processors , 328 bytes on the SAMD21, but only
  50-60 bytes on other 32-bit processors.
* The various `printShortNameTo()` or `printShortTo()` methods changed to
  replace the underscore in the zone names (e.g. `Los_Angeles`) with spaces
  (e.g. `Los Angeles`) to be more human friendly. This made little difference in
  the flash memory consumption, except on the ESP32 where it increased by
  200-300 bytes.

In v1.7.2
* The `SystemClock::clockMillis()` is now non-virtual, using compile-time
  polymorphism through C++ template, and incorporating the same techniques from
  AceRoutine v1.3. Saves about 20-40 bytes of flash.

In v1.7.5:
* `ExtendedZoneProcessor.compareTransitionToMatch()` was modified to
  detect an exact equality between a `Transition` and its `MatchingEra` if any
  of the 3 time stamp versions ('w', 's', 'u') are equal. Adds about 120-150
  bytes of flash on 8-bit and 32-bit processors. But removing
  `originalTransitionTime` from `Transition` decreases flash usage by about 20
  bytes.
* Upgrade ESP8266 Core from 2.7.4 to 3.0.2. Flash consumption increases by
  3-5 kB across the board.
* Upgrade Teensyduino from 1.54 to 1.55. Add memory consumed by `malloc()` and
  `free()` when using classes with virtual methods into baseline
  MemoryBenchmark, reducing the actual memory usage of various features by
  ~3kB.

In v1.8.0:
* Move Clock and SystemClock benchmarks into AceTimeClock v1.0.0.
* Extract thin links from BasicZoneManager and ExtendedZoneManager into
  new BasicLinkManager and ExtendedLinkManager classes.
    * Saves 200-500 bytes of flash for BasicZoneManager and ExtendedZoneManager.
    * Applications can decide whether to use thin links through the LinkManager
      (~2000 flash bytes for AVR) or use fat links through the
      `kZoneAndLinkRegistry` (~5000 flash bytes for AVR).
* Create various test objects as global variables instead of stack variables
  to get a more accurate measurement of their static memory consumption.

## Arduino Nano

* 16MHz ATmega328P
* Arduino IDE 1.8.16, Arduino CLI 0.19.2
* Arduino AVR Boards 1.8.3

```
{nano_results}
```

## Sparkfun Pro Micro

* 16 MHz ATmega32U4
* Arduino IDE 1.8.16, Arduino CLI 0.19.2
* SparkFun AVR Boards 1.1.13

```
{micro_results}
```

## SAMD21 M0 Mini

* 48 MHz ARM Cortex-M0+
* Arduino IDE 1.8.16, Arduino CLI 0.19.2
* Sparkfun SAMD Boards 1.8.4

```
{samd_results}
```

(SAMD compiler does not produce RAM usage numbers.)

## STM32 Blue Pill

* STM32F103C8, 72 MHz ARM Cortex-M3
* Arduino IDE 1.8.16, Arduino CLI 0.19.2
* STM32duino 2.0.0

```
{stm32_results}
```

An entry of `-1` indicates that the memory usage exceeded the maximum of the
microcontroller and the compiler did not generate the desired information.

## ESP8266

* NodeMCU 1.0, 80MHz ESP8266
* Arduino IDE 1.8.16, Arduino CLI 0.19.2
* ESP8266 Boards 3.0.2

```
{esp8266_results}
```

## ESP32

* ESP32-01 Dev Board, 240 MHz Tensilica LX6
* Arduino IDE 1.8.16, Arduino CLI 0.19.2
* ESP32 Boards 1.0.6

```
{esp32_results}
```

RAM usage remains constant as more objects are created, which indicates that an
initial pool of a certain minimum size is created regardless of the actual RAM
usage by objects.

## Teensy 3.2

* 96 MHz ARM Cortex-M4
* Arduino IDE 1.8.16, Arduino CLI 0.19.2
* Teensyduino 1.55

```
{teensy32_results}
```
""")
