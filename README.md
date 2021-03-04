# ES200G-Decoder-Analysis
Experimentation in decoding serial UART for the ES200G battery—only the battery, not the scooter's communications to it.


### Running this notebook from a different drive
If storing this Jupyter Notebook on a drive other than C:/, load from Anaconda Prompt this way.

```
jupyter notebook --notebook-dir=D:/
```

### Data Column Notes
1. _[0x3A]_
2. _[0x16]_
3. _[0x20]_
4. Some state [0x02], [0x03], [0x0E], [0x1D], [0x2F], [0x0F]
  > __This is acting like a state for possibly an indicator light__

  * These code are flashed as follows
    * [0x02] On and Discharging
      * Seems to be the default value given when discharging
    * [0x0E] About to start charging (????? LOAD)
    * [0x1D] About to start charging (NO LOAD)
      * Seems to be given when charging begins up after BMS low-power shutdown
    * [0x2F] On and Charging (NO LOAD)
      * Seems to be the default Value given when charging
    * [0x0F] Fully Charged (NO LOAD)
      * Seems to be given when charging cycling when fully charged. It's specifically given when there is < 1 amp total current on charge (Might need to test with a load during test to see what happens.)
    * Alternating [0x0F][0x2F] this seems to happen when charge is at 100% and current draw starts bouncing between 1 to 0 amps respectively. This could be used to alert the user the charge has slowed down to a trickle before it turns off.
5. _[0x00]_
6. Energy Gauge (0-100)
7. Unknown A (0-100) ??
8. Celsius Temp A
9. Celsius Temp B
10. Celsius Temp C
11. Celsius Temp D
12. Unknown B [0x24], [0x25]
  * Data shared from another hacker shows the following values. Need to figure out what was happening concurrently to help extrapolate meaning
    * [0x01], [0x21], [0x22], [0x29], [0x2E], [0x33], [0x36], [0x39], [0x3A], [0x3B]
    > Order is sequential only because I placed them that way. The analyzed data records are not ordered and seem to flutter about. Maybe that's a sign of non-liner values like temperature, draw and the like, but more a state or a code parameter.

13. _[0x00]_
14. Some state [0x00], [0x19], [0x7C]
  > __This is acting like a state that could be used to in relation to the charger being engaged__

  * [0x00] Seems to be the default state while on and discharging (LOAD)
  * [0x19] Seems to be given when charging begins, similar timing to #4 (NO LOAD)
  * [0x7C] Seems to be given when charging, similar to #4 but does _**not**_ fluctuate when nearing full/slow charge. (NO LOAD)
15. _[0x0F]_
16. _[0x00]_
17. _[0x00]_
18. Some state [0x00], [0x01], [0x03]
  * This one seems to also be changing with the charge state.
      * [0x00] Seems to be given when discharging (LOAD)
      * [0x01] Seems to be given when charging (NO LOAD)
      * [0x03] Seems to be given when charging begins, similar timing to #4 (NO LOAD)
19. _[0x00]_
20. [0x00], [0x20], [0x60]
  * [0x00] Seems to be given when discharging (LOAD)
  * [0x20] Seems to be given when discharging (LOAD)
  * [0x60] Seems to be given when charging (NO LOAD) -- Maybe not? Seeing it on discharge, no charging.
21. [0x00], [0x40]
  * [0x40] Seems to be given when discharging (LOAD) -- Maybe not?
  * [0x00] Seems to be given when charging (NO LOAD)
22. Total Voltage (LSB)
23. Total Voltage (MSB)
24. _[0x00]_
25. _[0x00]_
26. Total Current (LSB)
27. Total Current (MSB)
28. [0x00], [0xFF]
  * Charge State A — Possibly used to allow motor or lighting based on whether the battering is charging or not (binary state)
      * [0xFF] When battery is ON there  _**not**_ charging
29. [0x00], [0xFF]
  * Charge State B — Possibly used to allow motor or lighting based on whether the battering is charging or not (binary state)
      * [0xFF] When on and _**not**_ charging
30. Cell Voltage Highest (LSB)
31. Cell Voltage Highest (MSB)
32. Cell Voltage Lowest (LSB)
33. Cell Voltage Lowest (MSB)
34. _[0x52]_
35. _[0x2C]_
36. CRC8/Maxim

> Data columns 28 and 29 could be a float (2 bytes) but why? Likely two states for two discrete functions even though they seem to be in sync.

> Data columns 34 and 35 could be a float _[11.35]_ or two integers of _[82]_ _[44]_ or ASCII _[,]_ _[R]_

### Commit Notes
> Before committing, clear cell and widget states to reduce the size of the notebook.



### Contributed Information from Jonathan Sperb
```
Comand sent:
(byte) -
(0) - 0x32 (read ?)
(1) - 0x13 (?)
(2) - 0x01 (num of bytes ?)
(3) - 0x16 (address ?)
(4) - Maxim Checksum8

Comand received:
(byte) -
(0) - 0x32 Comand (read (?))
(1) - 0x16 Address (?)
(2) - 0x20 Num of bytes (without checksum (?))
(3) - Status bits
                            0 0 0 0  0 0 1 0  [0x02]
                            0 0 0 0  0 0 1 1  [0x03]
                            0 0 0 0  0 0 0 0  [0x0E]
                            0 0 0 0  0 0 0 0  [0x1D]
                            0 0 1 0  1 1 1 1  [0x2F]
                            0 0 0 0  1 1 1 1  [0x0F]
                        ? ──┘ │ │ │  │ │ │ │
                        ? ────┘ │ │  │ │ │ │
            Charging bulk ──────┘ │  │ │ │ │
       Cell under-voltage ────────┘  │ │ │ │
         Charger Okay (?) ───────────┘ │ │ │
          Charge Detected ─────────────┘ │ │
 Discharge MOSFET enabled ───────────────┘ │
    Charge MOSFET enabled ─────────────────┘

(4) -
(5) - State of charge
(6) -
(7) - Max Cell temp
(8) - Avg Cell temp
(9) - discharge mosfet temperature
(10) - microcontroller Temperature
(12-11) - Charge Cycle count
(13) - Charger OnOff (?)
(14) -
(15) -
(16) - Overvoltage (?)
(17) - Low Power/Standby (?)
(18) - Overtemp (?)
(19) -
(20) -
(22-21) - Pack Voltage
(23) -
(24) -
(26-25) - Pack Current
(27) - Discharging (?)
(28) - Discharging (?)
(30-29) - Highest Cell Voltage
(32-31) - Lowest Cell Voltage
(33) -
(34) -
(35) - Maxim Checksum8
```


## Thank you to
* Jehu Garcia and the DIY community he's fostered.

## Special thanks to these other DIYers
* Daniel Esparza
* Jonathan Sperb
* Justin Sutcliff [https://github.com/DookieSheets/OKAI-Battery-Lib]
