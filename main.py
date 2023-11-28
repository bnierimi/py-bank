
import hashlib
import json
import os
import subprocess
from datetime import datetime
# from getpass import getpass

class Ichimonji:
    title     = "Ichimonji"
    author    = "t/bnierimi"
    version   = "0.10.0"
    currency  = "{i}"
    monjibase = ".monji.wado"
    about     = f"""
{title} {version} (tags/v{version}:0cca80d, Nov 28 2023, 04:23:39)
    A chain-like simple Banking system program
                  yours {author}
"""
    address_prefix = "0n"
    # Check if monjibase exists

    def __init__(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print()
        if self.IfDbExists() == 1:
            with open(self.monjibase) as opdb:
                contentToCheck = opdb.read()
            if len(contentToCheck) == 0:
                self.accounts = {}
                self.transactions = {}
        self.LoadDb()

    # CLi
    def Create(self, name, age, password):
        curTime = datetime.now().ctime()
        address = self.MkAddress([str(len(self.accounts)), name, str(age), curTime])
        self.accounts[address] = {
            "name": name,
            "age": age,
            "username": f"ji/{address}",
            "balance": 0,
            "datetime": curTime,
            "timestamp": datetime.timestamp(datetime.now()),
            "password": password,
        }
        self.DumpDb()
        return { "name": name, "address": address }

    # DB
    def IfDbExists(self):
        if not os.path.exists(self.monjibase):
            print("(*) Initialising Database...")
            json.dump({ "accounts": {}, "transactions": {} }, open(self.monjibase, "w"), indent=3)
            return False # Just created one
        return True # Exists already

    def LoadDb(self):
        "Read from Monjibase"
        totalContent = json.load(open(self.monjibase))
        self.accounts = totalContent["accounts"]
        self.transactions = totalContent["transactions"]
    
    def DumpDb(self):
        "Write to Monjibase"
        data = {
            "accounts": self.accounts,
            "transactions": self.transactions,
        }
        json.dump(data, open(self.monjibase, "w"), indent=3)

    # Methods
    def MkAddress(self, details):
        # hashValue = hash(f'%tcitrogg://{"~".join(details)}')
        address = self.address_prefix
        value = f'<%tcitrogg://{"~".join(details)}/>'
        address += hashlib.shake_128(str.encode(value)).hexdigest(8)
        return address
    
    def Cook(self, value):
        result = list(hashlib.sha3_512(str.encode(value)).hexdigest())
        result.reverse()
        return "".join(result)

    def Auth(self, address, password):
        pass
    
    # Account
    def GetAccountInfo(self, address):
        if address in self.accounts:
            account_info = self.accounts[address]
            return account_info
        else:
            return False
            # print(":( Oops! Address not found,\n Don't have an account? Create one with the command `create` or `!c`")

    def CheckBalance(self, address):
        account = self.GetAccountInfo(address)
        if account == False:
            print(":( Oops! An error occured, if it occurs again, kindly send a report to us!")
            return False
        return account["balance"]
    
    def Tranfer(self, sender_address, amount, receiver_address):
        if sender_address == f"{self.address_prefix}DEPOSIT" or self.CheckBalance(sender_address) < amount:
            sender_info = self.GetAccountInfo(sender_address)
            receiver_info = self.GetAccountInfo(receiver_address)
            sender_info["balance"] -= amount
            receiver_info["balance"] += amount
            self.accounts[sender_address] = sender_info
            self.accounts[receiver_address] = receiver_info
            self.DumpDb()
            self.AddTx({
                "sender": sender_address,
                "receiver": receiver_address,
                "amount": amount,
                # signature
            })
            return True
        else:
            print(f":( Oops! Insufficent Funds | You do not have up to {self.currency}{amount}")
            return False
        
    # Transaction
    def AddTx(self, transaction):
        tx_id = hashlib.sha1(str.encode(str(len(self.transactions)))).hexdigest()
        tx_extradetails = {
            "timestamp": datetime.timestamp(datetime.now())
        }
        self.transactions[tx_id] = transaction.update()
        self.DumpDb()

    def GetTx(self, tx_id):
        if tx_id in self.transactions:
            return self.transactions[tx_id]
        else:
            return False





# Read
# Write
# Update
# Delete

# While Logged in
def __login__(usrdetails):
    li_ji = Ichimonji()
    address = usrdetails["address"]
    account = li_ji.GetAccountInfo(address)
    logged_in = True
    print(f"--- {li_ji.title} : Welcome, {account["name"]} ---")
    while logged_in:
        print()
        li_cmd = input(f" ji/{address}> ").lower()
        if li_cmd in ["logout", "!q"]:
            logged_in = False
        else:
            if li_cmd in ["balance"]:
                balance = li_ji.CheckBalance(address)
                print(f" Balance: {li_ji.currency}{balance}")
            elif li_cmd in ["about"]:
                print(li_ji.about)
            elif li_cmd in ["profile"]:
                print(li_ji.GetAccountInfo(address))
            elif li_cmd in ["transfer"]:
                try:
                    amount = int(input("> Amount to tranfer: "))
                except ValueError as notIntError:
                    print(f"(x) Error: Amount has to be a number, {notIntError}")
                receiver = input("> Receiver's Address: ")
                response = li_ji.Tranfer(address, amount, receiver)
                if response:
                    print(f"(+) Success: Transferred `{li_ji.currency}{amount}` to `{li_ji.GetAccountInfo(receiver)["name"]}: {receiver}`")
                    print(f" Balance: {li_ji.GetAccountInfo(address)["balance"]}")
            elif address == f"{li_ji.address_prefix}tsurgeon" and li_cmd in ["deposit", "!d"]:
                try:
                    amount = int(input("> Amount to deposit: "))
                except ValueError as notIntError:
                    print(f"(x) Error: Amount has to be a number, {notIntError}")
                receiver = input("> Receiver's Address: ")
                response = li_ji.Tranfer(f"{li_ji.address_prefix}DEPOSIT", amount, receiver)
                if response:
                    print(f"(+) Success: Deposited `{li_ji.currency}{amount}` to `{receiver}`")
            elif li_cmd in ["help", "!h"]:
                print(f"""
-:- {li_ji.title} : {address} -:-
profile           View your account information
balance           View your account balance
tranfer           Tranfer some {'{Imonji}'} to another account
about,            About Ichimonji
delete_account    /!\\ Delete your Ichimonji account
download_data     Download your Ichimonji account data
logout, !q        Log out of this account session
help,   !h        Show this help dialog
""")
            else:
                print("(x) Error: Invaild command, use the `help` or `!h` command to get list of valid commands")





# CLI
running = True
ji = Ichimonji()

while running:
    
    cmd = input(f"{ji.title}> ").lower()
    if cmd in ["exit", "!q"]:
        running = False
    else:
        if cmd in ["create", "!c"]:
            name = input("> Enter your fullname: ")
            try:
                age = int(input("> Enter your age: "))
            except ValueError as notIntError:
                print("(x) Error: Your age has to be a number\n")
                continue
            password = ji.Cook(input("> Enter your password: "))
            confirm_password = ji.Cook(input("> Confirm your password: "))
            if password != confirm_password:
                print("(x) Error: Password mismatch\n")
                continue
            usrname_and_address = ji.Create(name, age, password)
            print(f"""
        Welcome to {ji.title}
 -----------
 | Name    | {usrname_and_address["name"]}
 | Address | {usrname_and_address["address"]}
 -----------
""")
        elif cmd in ["total_users"]:
            print(f" (i) Total Users: {len(ji.accounts)}")
        elif cmd in ["total_txs"]:
            print(f" (i) Total Transactions: {len(ji.transactions)}")
        
        elif cmd in ["about"]:
            print(ji.about)
        elif cmd in ["login", "!l"]:
            usraddress = input("> Enter your address: ")
            for each_account in ji.accounts:
                if usraddress == each_account:
                    account = ji.accounts[each_account]
                    break
            else:
                print(" :( Oops! Address not found,\n Don't have an account? Create one with the command `create` or `!c`\n")
                continue
            password = ji.Cook(input("> Enter your password: "))
            if password == account["password"]:
                del account["password"]
                del account["age"]
                del account["timestamp"]
                account["address"] = usraddress
            __login__(account)
        elif cmd in ["help", "!h"]:
            print(f"""
-:- {ji.title} : MonjiConsole -:-
about             About Ichimonji
create, !c        <yonko> Create new account
total_users       Show the total number of {ji.title} users.
total_txs         Show the total number of transactions performed.
login,  !l        Login to your {ji.title} account
exit,   !q        Exit MonjiConsole
help,   !h        Show this help dialog

<yonko>           Yonko priviledge, commands only permitted for admins
""")
        else:
            print("(x) Error: Invaild command, use the `help` or `!h` command to get list of valid commands")
    print()