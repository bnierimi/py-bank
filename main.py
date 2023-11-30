
import hashlib
import json
import os
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
        self.ReadWholeDb()

    def LoadFl(self, filename, ftype="json", mode="r"):
        if ftype in ["f", "file"]:
            with open(filename, mode) as opfl:
                content = opfl.read()
            return content
        else:
            return json.load(open(filename, mode))

    def DumpFl(self, filename, content, ftype="json", mode="w", indent=3):
        if ftype in ["f", "file"]:
            with open(filename, mode) as opfl:
                opfl.write(content)
        else:
            json.dump(content, open(filename, mode), indent=indent)

    # CLi
    def Create(self, name, age, password, username=""):
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
        self.WriteToDb()
        return { "name": name, "address": address }

    # DB
    def IfDbExists(self):
        if not os.path.exists(self.monjibase):
            print("(*) Initialising Database...")
            json.dump({ "accounts": {
                "0ntsurgeon": {
                    "name": "&tsurgeon",
                    "age": 0,
                    "username": "tsurgeon",
                    "balance": 1_000_000_000,
                    "timestamp": datetime.timestamp(datetime.now()),
                    "password": self.Cook("yonko::eri")
                }}, "transactions": {} }, open(self.monjibase, "w"), indent=3)
            # self.Create("&tsurgeon", username="tsurgeon", age=0, password=self.Cook("yonko::eri"))
            return False # Just created one
        return True # Exists already

    def ReadWholeDb(self):
        "Read from Monjibase"
        totalContent = json.load(open(self.monjibase))
        self.accounts = totalContent["accounts"]
        self.transactions = totalContent["transactions"]
    
    def WriteToDb(self):
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

    def GetAccountInfoByUsername(self, username):
        for each_account in self.accounts:
            if username == each_account["username"]:
                return each_account
            else:
                return False

    def CheckBalance(self, address):
        account = self.GetAccountInfo(address)
        if account == False:
            print(":( Oops! An error occured, if it occurs again, kindly send a report to us!")
            return False
        return account["balance"]
    
    def Tranfer(self, sender_address, amount, receiver_address):
        if sender_address == f"{self.address_prefix}DEPOSIT" or self.CheckBalance(sender_address) > amount:
            sender_info = self.GetAccountInfo(sender_address)
            receiver_info = self.GetAccountInfo(receiver_address)
            sender_info["balance"] -= amount
            receiver_info["balance"] += amount
            self.accounts[sender_address] = sender_info
            self.accounts[receiver_address] = receiver_info
            self.WriteToDb()
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
        self.WriteToDb()

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
        li_cmd = input(f" ji/{address}> ").lower().strip()
        if li_cmd in ["logout", "!q"]:
            logged_in = False
        else:
            if li_cmd in ["balance"]:
                balance = li_ji.CheckBalance(address)
                print(f" Balance: {li_ji.currency}{balance}")
            elif li_cmd in ["about"]:
                print(li_ji.about)
            # elif li_cmd in ["set_username"]:
            #     username = input("> Enter username: ")
            elif li_cmd in ["profile"]:
                profile = li_ji.GetAccountInfo(address)
                del profile["password"]
                del profile["timestamp"]
                longest_word = ""
                for each_info in profile:
                    if len(each_info) > len(longest_word):
                        longest_word = each_info
                for each_info in profile:
                    print(" | {}: {}".format(each_info.title().ljust(len(longest_word)+1, " "), profile[each_info]))
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
            elif address == f"{li_ji.address_prefix}tsurgeon" and li_cmd in ["getuser"]:
                username_or_address = input("> By [u]sername or [a]ddress: ")
                if username_or_address in ["a", "address"]:
                    address = input("")
                    response = li_ji.GetAccountInfoByUsername(address)
                    if response == False:
                        print(f"(x) Error: No such address as `{address}`")
                        continue
                elif username_or_address in ["u", "username"]:
                    usrname = input("")
                    response = li_ji.GetAccountInfoByUsername(usrname)
                    if response == False:
                        print(f"(x) Error: No such username as `{usrname}`")
                        continue
                else:
                    print("(x) Unknown Command, try again")
                    continue
                profile = li_ji.GetAccountInfo(address)
                del profile["password"]
                del profile["timestamp"]
                longest_word = ""
                for each_info in profile:
                    if len(each_info) > len(longest_word):
                        longest_word = each_info
                for each_info in profile:
                    print(" | {}: {}".format(each_info.title().ljust(len(longest_word)+1, " "), profile[each_info]))
            elif li_cmd in ["download_data"]:
                password = li_ji.Cook(input("> Enter password: "))
                account = li_ji.GetAccountInfo(address)
                li_ji.DumpFl(f"{address}-info.json", account)
                print(f"(+) Downloaded account data as `{address}-info.json`")
                # if password == account["password"]:
                #     del account["password"]
                    # account["datetime"] = datetime.fromtimestamp(account["timestamp"])
                    # del account["timestamp"]
                # else:
                #     print("(x) Wrong password")
            elif li_cmd in ["help", "!h"]:
                print(f"""
-:- {li_ji.title} : {address} -:-
profile           View your account information
balance           View your account balance{"" if address == f"{li_ji.address_prefix}tsurgeon" else "\ntranfer           Tranfer some {'{Imonji}'} to an address"}{"\ndeposit           <yonko> Deposit some {Imonji} to an address" if address == f"{li_ji.address_prefix}tsurgeon" else ""}
about,            About Ichimonji{"\ngetuser           <yonko> Get user's profile by address or username" if address == f"{li_ji.address_prefix}tsurgeon" else ""}
download_data     Download your Ichimonji account data{"" if address == f"{li_ji.address_prefix}tsurgeon" else "\ndelete_account    /!\\ Delete your Ichimonji account"}
logout, !q        Log out of this account session
help,   !h        Show this help dialog

{"<yonko>           Yonko priviledge, commands only permitted for admins" if address == f"{li_ji.address_prefix}tsurgeon" else ""}
""")
            else:
                print("(x) Error: Invaild command, use the `help` or `!h` command to get list of valid commands")





# CLI
running = True
ji = Ichimonji()

while running:
    
    cmd = input(f"{ji.title}> ").lower().strip()
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
 | Name     | {usrname_and_address["name"]}
 | Address  | {usrname_and_address["address"]}
 | Username | {usrname_and_address["username"]}
 -----------

 ! Login to update your username
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
create, !c        Create new account
total_users       Show the total number of {ji.title} users.
total_txs         Show the total number of transactions performed.
login,  !l        Login to your {ji.title} account
exit,   !q        Exit MonjiConsole
help,   !h        Show this help dialog
""")
        else:
            print("(x) Error: Invaild command, use the `help` or `!h` command to get list of valid commands")
    print()