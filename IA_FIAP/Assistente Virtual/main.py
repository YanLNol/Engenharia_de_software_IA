import os
import json


from chatterbot import ChatBot
from rich.console import Console
from chatterbot.trainers import ChatterBotCorpusTrainer

class cli():
    def __init__(self, name):
        self.chatbot = ChatBot(name)
        self.console = Console(width=100)

    def treiner(self):
        ChatterBotCorpusTrainer(self.chatbot).train("chatterbot.corpus.portuguese")

    def start(self):
        loop = True
        self.treiner()
        os.system('clear')
        self.console.print(f"""\n[blue b] Hello World [/]\n\n""", justify="center")
        USERNAME = self.console.input("[black bold]    >>> What's the username? [/]")
        os.system('clear')
        self.console.print(f"""\n[blue b] Hello World [/]\n\n""", justify="center")
        while loop:
            MESSAGE = self.console.input(f"[green bold]   {USERNAME} >>> [/]")
            res = self.chatbot.get_response(MESSAGE)
            self.console.print(f"[red bold]   Kali >>> {res}[/]")
            
                
if __name__ == "__main__":
    cli = cli('kali')
    cli.start()