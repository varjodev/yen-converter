import argparse
import urllib.request
import json
import csv
from pathlib import Path
from datetime import datetime

currency_symbol_table = {"eur":"€",
                         "jpy":"¥", # "円"
                         "usd": "$"
                         }


def num_to_yen(num, remainder=False):
    """
        Converts a number into yen with 万 sign denoting 10000s
    """
    man = num//10000
    rem = num % 10000

    man_string = f"{man:.0f}万" if man > 0 else ''
    remainder_string = f"{rem:.0f}" if remainder else ''
    return f"{man_string}{remainder_string}円"


def parse_yen(amount_string):
    """
        Parses for Japanese words "man", "sen", "hyaku" and numbers in a string
        and makes it into a float i.e. 32man9sen3hyaku23 -> 329323.0

        Typically used only with "man", i.e. 32man9323 -> 329323.0
    """
    total = 0

    if "man" in amount_string:
        temp_list = amount_string.split("man")
        man = int(temp_list[0].replace(" ",""))
        amount_string = temp_list[1]
        total += man*10000

    if "sen" in amount_string:
        temp_list = amount_string.split("sen")
        sen = int(temp_list[0].replace(" ",""))
        amount_string = temp_list[1]
        total += sen*1000

    if "hyaku" in amount_string:
        temp_list = amount_string.split("hyaku")
        hyaku = int(temp_list[0].replace(" ",""))
        amount_string = temp_list[1]
        total += hyaku*100

    amount_string = amount_string.replace(" ", "")
    amount_string = amount_string.replace(",", ".")

    total += float(amount_string) if amount_string else 0

    return total

def get_rate(src,target):
    """
        Tries to find today's rate from local database
        If not found fetch from API
    """
    csvfile_path = Path(__file__).parent.absolute().joinpath('rates.csv')
    with open(csvfile_path, 'r') as f:
        ratereader = csv.reader(f, delimiter=',')
        header = next(ratereader) # src, target, rate, date
        rows=[]
        for row_i, row in enumerate(ratereader):
            if row[0] == src and row[1] == target:
                if row[3] == datetime.today().strftime("%Y-%m-%d"):
                    return float(row[2]) # rate found
                else:
                    continue
            if row != "":
                rows.append(row)
            
    print("Fetching rate...")
    # Api source https://github.com/fawazahmed0/exchange-api
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{src}.json"
    res = urllib.request.urlopen(url)
    rates = json.loads(res.read().decode('utf-8'))
    rate = rates[src][target]

    rows.append([src,target,rate, datetime.today().strftime("%Y-%m-%d")])

    with open(csvfile_path, 'w', newline='') as f:
        ratewriter = csv.writer(f, delimiter=',')
        ratewriter.writerow(header)
        for row in rows:
            ratewriter.writerow(row)

    return rate
    
def currency_string(num,currency):
    """
        Formats an amount of money and currency into a string
        JPY gets formatted with 万 amount in brackets
    """
    return f"{num:.2f} {currency} {'' if currency != "jpy" else ' (' + num_to_yen(num) + ')'}"


if __name__=="__main__":
    print(__file__)
    parser = argparse.ArgumentParser(
                        prog='Currency Converter',
                        description='Converts currencies (optimized for euro<->yen)')

    parser.add_argument('amount', help="Amount of currency to be converted")
    parser.add_argument('-s', '--source_currency', help="Source currency code, i.e. jpy,eur,usd")
    parser.add_argument('-t', '--target_currency', help="Source currency code, i.e. jpy,eur,usd")
    parser.add_argument('--monthly', action='store_true', help="Returns additionally the converted amount divided by 12") 
    parser.add_argument('--yearly', action='store_true', help="Returns additionally the converted amount multiplied by 12") 
    parser.add_argument('-r', '--rate', help="exchange rate, if empty fetch today's rate from an API or local database")

    args = parser.parse_args()

    amount_string = str(args.amount)
    src_currency = args.source_currency
    target_currency = args.target_currency

    if args.rate is None:
        rate = get_rate(src_currency,target_currency)
    else:
        rate = float(args.rate) # fixed rate set with the -r argument

    if src_currency == "jpy":
        amount = parse_yen(amount_string)
    else:
        amount = float(amount_string)

    total_target = amount*rate

    src_symb = currency_symbol_table[src_currency] if src_currency in currency_symbol_table else src_currency
    target_symb = currency_symbol_table[target_currency] if target_currency in currency_symbol_table else target_currency

    print(f"\n============== Currency converter ({src_symb}->{target_symb}) | {datetime.today().strftime('%Y-%m-%d %H:%M')} =============")
    print(f"Rate (1{src_symb} -> {target_symb}) {rate}  | Inverse rate (1{target_symb} -> {src_symb}): {1/rate} ")
    print()
    print(f"{currency_string(amount,src_currency)} -> {currency_string(total_target,target_currency)}")

    if args.monthly:
        print()
        print(f"Monthly: {currency_string(total_target/12,target_currency)}")

    if args.yearly:
        print()
        print(f"Yearly: {currency_string(total_target*12,target_currency)}")
