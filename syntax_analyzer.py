class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor = 0
        self.current_token = tokens[0] if tokens else None

    def move_forward(self):
        self.cursor += 1
        if self.cursor < len(self.tokens):
            self.current_token = self.tokens[self.cursor]
        else:
            self.current_token = None
            
    def peek(self):
        return self.current_token
    
    def match(self, token_type, value=None):
        if self.current_token is None:
            return False
        if self.current_token['type'] == token_type:
            if value is None or self.current_token['value'] == value:
                return True
        return False
    
      
    def get_type(self):
        type_name = self.current_token['value']
        self.move_forward()
        return type_name
    
    def extract_type_from_tokens(self):
        if self.match("KEYWORD", "int"):
            get_type = self.get_type()
            return get_type
        elif self.match("KEYWORD", "char"):
            get_type = self.get_type()
            return get_type
        elif self.match("KEYWORD", "float"):
            get_type = self.get_type()
            return get_type
        elif self.match("KEYWORD", "string"):
            get_type = self.get_type()
            return get_type
        elif self.match("KEYWORD", "void"):
            get_type = self.get_type()
            return get_type    
        else:
            print(f"ERROR, Expected Type (int/char/void), got {self.current_token}")
            return None
    
    def parse_simple_declaration(self):
        
        type_name = self.extract_type_from_tokens()
        if type_name is None:
            return None
        
        identifiers = []  # Store all identifiers with their array info
        
        # Step 2: Get first identifier (required)
        if not self.match('IDENTIFIER'):
            print(f"ERROR: Expected identifier, got {self.current_token}")
            return None
        
        identifier = self.current_token['value']
        self.move_forward()
        
        # Step 2.5: Check for array brackets
        array_size = None
        if self.match('PUNCTUATION', '['):
            self.move_forward()  # Skip '['
            
            # Check if there's a number inside brackets
            if self.match('INT_CONST'):
                array_size = self.current_token['value']
                self.move_forward()
            else:
                array_size = '0'  # Empty brackets like d[]
            
            # Expect closing bracket
            if not self.match('PUNCTUATION', ']'):
                print(f"ERROR: Expected ']', got {self.current_token}")
                return None
            self.move_forward()
        
        identifiers.append({'name': identifier, 'array_size': array_size})
        
        # Step 3: Handle additional identifiers after commas
        while self.match('PUNCTUATION', ','):
            self.move_forward()  # Skip the comma
            
            # Now we expect another identifier
            if not self.match('IDENTIFIER'):
                print(f"ERROR: Expected identifier after comma, got {self.current_token}")
                return None
            
            identifier = self.current_token['value']
            self.move_forward()
            
            # Check for array brackets again
            array_size = None
            if self.match('PUNCTUATION', '['):
                self.move_forward()  # Skip '['
                
                # Check if there's a number inside brackets
                if self.match('INT_CONST'):
                    array_size = self.current_token['value']
                    self.move_forward()
                else:
                    array_size = '0'  # Empty brackets
                
                # Expect closing bracket
                if not self.match('PUNCTUATION', ']'):
                    print(f"ERROR: Expected ']', got {self.current_token}")
                    return None
                self.move_forward()
            
            identifiers.append({'name': identifier, 'array_size': array_size})
        
        # Step 4: Check for semicolon
        if not self.match('PUNCTUATION', ';'):
            print(f"ERROR: Expected semicolon, got {self.current_token}")
            return None
        
        self.move_forward()
        
        print(f"Successfully parsed declaration:")
        for item in identifiers:
            if item['array_size']:
                print(f"  {type_name} {item['name']}[{item['array_size']}]")
            else:
                print(f"  {type_name} {item['name']}")
        
        return {'type': type_name, 'identifiers': identifiers}
    
    def parse_function_declaration(self):
        # Parse the function body and enters into local/lexical scope
        pass
    
    def parse_condition_statement(self):
        # Parse the if/else block
        pass
    
    def parse_loop_statement(self):
        # Parse the for/while loop
        pass
    
    def build_final_symbol_table(self):
        # Construct the symbol table finally
        pass
    
    
def read_tokens(filename):
    tokens = []
    with open(filename, "r") as f:
        lines = f.readlines()[1:]
        for line in lines:
            parts = line.strip().split("\t")
            if len(parts) == 3:
                token_type = parts[0]
                lexeme = parts[1]
                line = parts[2]
                
                tokens.append({
                    "type": token_type,
                    "value": lexeme,
                    "line_no": line
                })
                
    return tokens

    
# Testing purposes
# test_tokens = [
#     {'type': 'KEYWORD', 'value': 'int', 'line_no': '1'},
#     {'type': 'IDENTIFIER', 'value': 'x', 'line_no': '1'},
#     {'type': 'PUNCTUATION', 'value': ';', 'line_no': '1'},
# ]
        
tokens = read_tokens("output.txt")
parser = SyntaxAnalyzer(tokens)
result = parser.parse_simple_declaration()
print(result)