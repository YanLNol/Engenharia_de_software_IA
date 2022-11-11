import requests
import threading

from os import *
from sys import *
from time import sleep
from rich.console import Console

KEY = "4042ce7973721b98b37d2a21c9caa74ca2bcdcea4af2709a85b88deb293b44e8e24651ba9bd16d444e55c6e0f70618f63367342e9753e6ef0784f437b4a300f5"
console = Console()
CSI = "\x1b["

class cli():
    def __init__(self, url, startID=0):
        self.url = url
        self.currID = startID
        self.account = False
        self.startTS = None

    def errorMessage(self, message):
        system('clear')
        print(self.account)
        console.print(f"    [white bold]>>>[/] [red bold]{message}[/]")
        return exit()

    def checkRestart(self, messages):
            First = messages["0"]
            TS = First[1]

            if self.startTS is None: 
                self.startTS = TS
                return

            if TS != self.startTS: 
                self.startTS = TS
                self.currID = 0
   
    def messageSend(self, Username, Password, Message):
        res = requests.post(self.url + "/message/send", json={
            "key": KEY,
            "username": Username,
            "password": Password,
            "message": Message, 
		}).json()

        if res['fault'] == True:
            self.errorMessage(res['message'])

    def messagePush(self, Username, Password):
        res = requests.post(self.url + "/message/push", json={
            "key": KEY,
            "username": Username,
            "password": Password,
        }).json()
        
        self.checkRestart(res)
		
        while str(self.currID) in res:
            yield res[str(self.currID)]
            self.currID += 1

    def login2(self):
            system('clear')
            console.print(f"""\n[blue b]LOGIN PAGE[/]""", justify="left")   
            LOGIN = True
            while LOGIN:
                try:
                    USERNAME = console.input("[black bold]    >>> What's the username? [/]")
                    PASSWORD = console.input("[black bold]    >>> What's the password? [/]")
                    CONFIRM = console.input("[black bold]    >>> Do you really want to login? [/]")

                    if CONFIRM == "y" or CONFIRM == "yes" or CONFIRM == "Y" or CONFIRM == "YES":
                        res = requests.post(self.url + "/login", json={
                            "key": KEY,
                            "username": USERNAME,
                            "password": PASSWORD,
                        }).json()

                        if res['fault'] == True:
                            system('clear')
                            console.print(f"""\n[red b] {res['message']} [/]""", justify="left")
                            pass
                        else:
                            self.account = { 
                                "password": PASSWORD, 
                                "username": USERNAME
                            }
                            LOGIN = False
                            self.start()

                    else:
                        system('clear')
                        LOGIN = False
                        console.print(f"    [white bold]>>>[/] [green bold]Goodbye![/]")
                        return exit()
                except KeyboardInterrupt:
                    LOGIN = False
                    system('clear')
                    console.print(f"    [white bold]>>>[/] [green bold]Goodbye![/]")
                    return exit()

    def sinup(self):
            system('clear')
            console.print(f"""\n[blue b]SINUP PAGE[/]""", justify="left")   
            SINUP = True
            while SINUP:
                try:
                    USERNAME = console.input("[black bold]    >>> What's the username? [/]")
                    PASSWORD = console.input("[black bold]    >>> What's the password? [/]")
                    CONFIRM = console.input("[black bold]    >>> Do you really want to register? [/]")

                    if CONFIRM == "y" or CONFIRM == "yes" or CONFIRM == "Y" or CONFIRM == "YES":
                        res = requests.post(self.url + "/signup", json={
                            "key": KEY,
                            "username": USERNAME,
                            "password": PASSWORD,
                        }).json()

                        if res['fault'] == True:
                            system('clear')
                            console.print(f"""\n[blue b]SINUP PAGE[/]""", justify="left")   
                            console.print(f"""\n[red b] {res['message']} [/]""", justify="left")
                            pass
                        else:
                            SINUP = False
                            self.login2()
                    else:
                        system('clear')
                        SINUP = False
                        console.print(f"    [white bold]>>>[/] [green bold]Goodbye![/]")
                        return exit()
                except KeyboardInterrupt:
                    SINUP = False
                    system('clear')
                    console.print(f"    [white bold]>>>[/] [green bold]Goodbye![/]")
                    return exit()
    
    def login(self):
        if self.account == False:
            system('clear')
            console.print(f"""\n[blue b]If you want to login 1 if you want to register 2[/]""", justify="left")   
            loop = True
            while loop:
                OPT = console.input()
                if OPT == "1":
                    loop = False
                    self.login2()
                elif OPT == "2":
                    loop = False
                    self.sinup()
                else:
                    system('clear')
                    console.print(f"""\n[red b]invalid option[/]""", justify="left")   
        else:
            pass

    def messagePrint(self):
        loop = True
        while loop:
            for message in self.messagePush(self.account['username'], self.account['password']):
                    console.print(message[1])
            sleep(0.1)
        loop = False

    def start(self):
        loop = True
        system('clear')
        self.login()

        thread = threading.Thread(target=self.messagePrint)
        thread.start()

        self.messageSend("Dem0n", self.account['password'], f"[red]   [ [i b]Dem0n[/] ] • [b i]Welcome back {self.account['username']}[/][/]")

        while loop:
            try:
                TEXT = input()
                print(f"{CSI}A{CSI}K", end="", flush=True)

                if TEXT == "" or TEXT == " ":
                    OwO=0
                elif TEXT == "exit":
                    self.messageSend("Dem0n", "", f"[red]   [ [i b]Dem0n[/] ] • [b i]{self.account['username']} left.[/][/]")
                    thread.join()
                    loop = False
                    system('clear')
                    console.print(f"    [white bold]>>>[/] [green bold]Goodbye![/]")
                    return exit()
                else:
                    self.messageSend(self.account['username'], self.account['password'], f"[yellow]   [ [i b]{self.account['username']}[/] ] • [b i]{TEXT}[/][/]")
            
            except KeyboardInterrupt:
                self.messageSend("Dem0n", "", f"[red]   [ [i b]Dem0n[/] ] • [b i]{self.account['username']} left.[/][/]")
                thread.join()
                loop = False
                system('clear')
                console.print(f"    [white bold]>>>[/] [green bold]Goodbye![/]")
                return exit()

if __name__ == "__main__":
    cli = cli("http://localhost:3000")
    cli.start()