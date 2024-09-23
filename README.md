# Simple currency converter for the command line

- Note: optimized between yen and euro
- No requirements, just python3 standard library

## Why?
It takes a lot of effort to write all the zeros for example when using large numbers. 
Additionally, Google doesn't work robustly when using the Japanese letters in numbers such as 万.

## Summary
Converts yen to other currencies.
Automatically parses "man", "sen", "hyaku"
so it is possible to input i.e. <50man4sen3hyaku>

If converting from other currency to yen, automatically shows the 
yen with 万 counter (also 千, 百 is specified)

First rates.csv is checked for conversion rates, and if no recent rate is found, today's rate is fetched from an API and saved to .csv

Windows batch scripts can be found from /bat_scripts

## Example usage
From command line:
```
>> python converter.py 55man -s jpy -t eur

============== Currency converter (¥->€) | 2024-09-23 23:08 =============
Rate (1¥ -> €) 0.0062071957  | Inverse rate (1€ -> ¥): 161.1033465563201

550000.00 jpy  (55万円) -> 3413.96 eur
```

With windows batch script:
```
>> y2e 55man

============== Currency converter (¥->€) | 2024-09-23 23:08 =============
Rate (1¥ -> €) 0.0062071957  | Inverse rate (1€ -> ¥): 161.1033465563201

550000.00 jpy  (55万円) -> 3413.96 eur
```

Additionally getting the monthly value after conversion by supplying --m or --monthly flag (--yearly is also possible):
```
>> y2e 500man m

============== Currency converter (¥->€) | 2024-09-23 23:09 =============
Rate (1¥ -> €) 0.0062071957  | Inverse rate (1€ -> ¥): 161.1033465563201

5000000.00 jpy  (500万円) -> 31035.98 eur

Monthly: 2586.33 eur
```