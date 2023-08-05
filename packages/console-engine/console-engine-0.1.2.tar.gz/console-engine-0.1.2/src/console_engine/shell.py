# Copyright (c) 2021 LightningV1p3r

####################
#Libs
####################

from . import lexer,parser,interpreter

import colorama
import getpass

####################
#Shell
####################

class Shell:

    def __init__(self, config, header=None, banner=None) -> None:
        self.config = config
        self.banner = banner
        self.keywords = list(self.config['keywords'])

        if header == None:
            self.header = '>> '
        else:
            self.header = header

    def prompt(self):
        
        user_input = input(self.header)

        lexer_ = lexer.Lexer(user_input)
        tokens = lexer_.tokenize()

        parser_ = parser.Parser(tokens, self.keywords)
        ast = parser_.parse()

        interpreter_ = interpreter.Interpreter(ast, self.config)
        inst, count = interpreter_.gen_inst_stack()

        return inst, count

    def prompt_secret(self):
        
        prefix = f'[⚿]'
        secret = getpass(prefix)

        return secret

    def prompt_passthrough(self):
        
        user_input = input(self.header)

        return user_input

    def update_header(self, val):
        self.header = val

    def out(self, output, prefix=None):
        
        if prefix == 'sucess':
            out = f'[{colorama.Fore.GREEN}✓{colorama.Fore.RESET}]'
            print(out)
        elif prefix == 'warning':
            out =  f'[{colorama.Fore.YELLOW}⚠{colorama.Fore.RESET}]'
            print(out)
        elif prefix == 'failed':
            out = f'[{colorama.Fore.RED}✖{colorama.Fore.RESET}]'
            print(out)
        else:
            print(output)