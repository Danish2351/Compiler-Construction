from colorama import Fore, Style, init
init(autoreset=True)

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor = 0
        self.current_token = tokens[0] if tokens else None
        self.scope = "Global"
        self.symbol_table = []

    def move_forward(self):
        self.cursor += 1
        if self.cursor < len(self.tokens):
            self.current_token = self.tokens[self.cursor]
        else:
            self.current_token = None

    def __peek(self):
        return self.current_token

    def match(self, token_type, value=None):
        if self.current_token is None:
            return False
        if self.current_token['type'] == token_type:
            if value is None or self.current_token['value'] == value:
                return True
        return False

    def add_to_symbol_table(self, lexeme, type_name, array_size=None):
        entry = {
            'lexeme': lexeme,
            'type': type_name,
            'scope': self.scope,
            'array_size': array_size if array_size else ''
        }
        self.symbol_table.append(entry)
        print(f"-> Symbol Table: Added {lexeme} ({type_name}, {self.scope})")

    def get_type(self):
        type_name = self.current_token['value']
        self.move_forward()
        return type_name

    def extract_type_from_tokens(self):
        if self.match("KEYWORD", "int"):
            return self.get_type()
        elif self.match("KEYWORD", "char"):
            return self.get_type()
        elif self.match("KEYWORD", "float"):
            return self.get_type()
        elif self.match("KEYWORD", "string"):
            return self.get_type()
        elif self.match("KEYWORD", "void"):
            return self.get_type()
        else:
            print(f"{Fore.RED}ERROR: Expected Type (int/char/void), got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None
        
    def parse_simple_declaration(self):
        type_name = self.extract_type_from_tokens()
        if type_name is None:
            return None

        identifiers = []

        if not self.match('IDENTIFIER'):
            print(f"{Fore.RED}ERROR: Expected identifier, got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None

        identifier = self.current_token['value']
        self.move_forward()

        array_size = None
        if self.match('PUNCTUATION', '['):
            self.move_forward()
            if self.match('INT_CONST'):
                array_size = self.current_token['value']
                self.move_forward()
            else:
                array_size = '0'
            if not self.match('PUNCTUATION', ']'):
                print(f"{Fore.RED}ERROR: Expected ']', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
                return None
            self.move_forward()

        identifiers.append({'name': identifier, 'array_size': array_size})
        self.add_to_symbol_table(identifier, type_name, array_size)

        while self.match('PUNCTUATION', ','):
            self.move_forward()

            if not self.match('IDENTIFIER'):
                print(f"{Fore.RED}ERROR: Expected identifier after comma, got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
                return None

            identifier = self.current_token['value']
            self.move_forward()

            array_size = None
            if self.match('PUNCTUATION', '['):
                self.move_forward()
                if self.match('INT_CONST'):
                    array_size = self.current_token['value']
                    self.move_forward()
                else:
                    array_size = '0'
                if not self.match('PUNCTUATION', ']'):
                    print(f"{Fore.RED}ERROR: Expected ']', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
                    return None
                self.move_forward()

            identifiers.append({'name': identifier, 'array_size': array_size})
            self.add_to_symbol_table(identifier, type_name, array_size)

        if not self.match('PUNCTUATION', ';'):
            print(f"{Fore.RED}ERROR: Expected semicolon, got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None

        self.move_forward()
        return {'type': type_name, 'identifiers': identifiers}

    def parse_function_declaration(self):
        function_type = self.extract_type_from_tokens()
        if not function_type:
            print(f"{Fore.RED}ERROR: Missing Function Type, got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None

        if not self.match("KEYWORD", "main"):
            print(f"{Fore.RED}ERROR: Expected 'main', found {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None

        function_identifier = self.current_token['value']
        self.add_to_symbol_table(function_identifier, "Function")
        self.move_forward()

        if not self.match('PUNCTUATION', '('):
            print(f"{Fore.RED}ERROR: Expected '(', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None
        self.move_forward()

        if not self.match('PUNCTUATION', ')'):
            print(f"{Fore.RED}ERROR: Expected ')', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None
        self.move_forward()

        if not self.match('PUNCTUATION', '{'):
            print(f"{Fore.RED}ERROR: Expected '{{', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None
        self.move_forward()

        self.scope = function_identifier

        while not self.match('PUNCTUATION', '}'):
            if self.current_token is None:
                print(f"{Fore.RED}ERROR: Unexpected end of file{Style.RESET_ALL}")
                return None
            self.parse_statement()

        if not self.match('PUNCTUATION', '}'):
            print(f"{Fore.RED}ERROR: Expected '}}', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None

        self.move_forward()
        return function_identifier

    def parse_statement(self):
        if self.match('KEYWORD') and self.current_token['value'] in ['int', 'char', 'float', 'string']:
            return self.parse_simple_declaration()

        elif self.match('KEYWORD', 'if'):
            return self.parse_condition_statement()

        elif self.match('KEYWORD', 'while') or self.match('KEYWORD', 'for'):
            return self.parse_loop_statement()

        elif self.match('PUNCTUATION', '}'):
            return None

        else:
            return self.parse_expression_statement()

    def parse_condition_statement(self):
        print("-> Parsing if/else statement")

        if not self.match('KEYWORD', 'if'):
            print(f"{Fore.RED}ERROR: Expected 'if', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None
        self.move_forward()

        if not self.match('PUNCTUATION', '('):
            print(f"{Fore.RED}ERROR: Expected '(', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None
        self.move_forward()

        while not self.match('PUNCTUATION', ')'):
            if self.current_token is None:
                print(f"{Fore.RED}ERROR: Unexpected end in if condition at line {self.current_token['line_no']}{Style.RESET_ALL}")
                return None
            self.move_forward()

        if not self.match('PUNCTUATION', ')'):
            print(f"{Fore.RED}ERROR: Expected ')', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None
        self.move_forward()

        if not self.match('PUNCTUATION', '{'):
            print(f"{Fore.RED}ERROR: Expected '{{', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None
        self.move_forward()

        while not self.match('PUNCTUATION', '}'):
            if self.current_token is None:
                print(f"{Fore.RED}ERROR: Unexpected end in if block at line {self.current_token['line_no']}{Style.RESET_ALL}")
                return None
            self.parse_statement()

        self.move_forward()

        if self.match('KEYWORD', 'else'):
            print("-> Parsing else block")
            self.move_forward()

            if not self.match('PUNCTUATION', '{'):
                print(f"{Fore.RED}ERROR: Expected '{{', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
                return None
            self.move_forward()

            while not self.match('PUNCTUATION', '}'):
                if self.current_token is None:
                    print(f"{Fore.RED}ERROR: Unexpected end in else block at line {self.current_token['line_no']}{Style.RESET_ALL}")
                    return None
                self.parse_statement()

            self.move_forward()

        return True

    def parse_loop_statement(self):
        loop_type = self.current_token['value']
        print(f"-> Parsing {loop_type} loop")
        self.move_forward()

        if not self.match('PUNCTUATION', '('):
            print(f"{Fore.RED}ERROR: Expected '(' after {loop_type}, got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None
        self.move_forward()

        while not self.match('PUNCTUATION', ')'):
            if self.current_token is None:
                print(f"{Fore.RED}ERROR: Unexpected end in {loop_type} condition at line {self.current_token['line_no']}{Style.RESET_ALL}")
                return None
            self.move_forward()

        self.move_forward()

        if not self.match('PUNCTUATION', '{'):
            print(f"{Fore.RED}ERROR: Expected '{{' after {loop_type}, got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None
        self.move_forward()

        while not self.match('PUNCTUATION', '}'):
            if self.current_token is None:
                print(f"{Fore.RED}ERROR: Unexpected end in {loop_type} block at line {self.current_token['line_no']}{Style.RESET_ALL}")
                return None
            self.parse_statement()

        self.move_forward()
        return True

    def parse_expression_statement(self):
        print("-> Parsing expression statement")

        while self.current_token and not self.match('PUNCTUATION', ';'):
            self.move_forward()

        if not self.match('PUNCTUATION', ';'):
            print(f"{Fore.RED}ERROR: Expected ';', got {self.current_token['value']} at {self.current_token['line_no']}{Style.RESET_ALL}")
            return None

        self.move_forward()
        return True

    def build_final_symbol_table(self):
        print("\n" + "=" * 70)
        print("SYMBOL TABLE")
        print("=" * 70)
        print(f"{'Lexeme':<20} {'Type':<15} {'Scope':<15} {'Array_size':<10}")
        print("-" * 70)
        for entry in self.symbol_table:
            print(f"{entry['lexeme']:<20} {entry['type']:<15} {entry['scope']:<15} {entry['array_size']:<10}")
        print("=" * 70)


def read_tokens(filename):
    tokens = []
    with open(filename, "r") as f:
        lines = f.readlines()[1:]
        for line in lines:
            parts = line.strip().split("\t")
            if len(parts) == 3:
                token_type = parts[0]
                lexeme = parts[1]
                line_no = parts[2]

                tokens.append({
                    "type": token_type,
                    "value": lexeme,
                    "line_no": line_no
                })
    return tokens


if __name__ == "__main__":
    tokens = read_tokens("output.txt")
    parser = SyntaxAnalyzer(tokens)
    parser.parse_function_declaration()
    parser.build_final_symbol_table()
