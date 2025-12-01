import re


PATTERNS = {
    "keywords": ["const", "char", "int", "string", "float", "double", "bool", "if", "else", "for", "while", "do", "public", "static", "void", "main", "args"],
    "operators": ["+", "-", "*", "/", "=", "%", "<", ">", ">=", "<=", "!=", "!"],
    "punctuation": [",", ";", "(", ")", "{", "}"]
}

TOKEN_PATTERNS = [
    ("FLOAT_CONST", r"^[+-]*[0-9]*\.[0-9]*$"),
    ("INT_CONST", r"^[0-9]+$"),
    ("CHAR_CONST", r"^'[^']'$"),
    ("STRING_CONST", r'^"[^"\n]*"$'),
    ("COMMENT", r"/\*.*?\*/"),
    ("IDENTIFIER", r"^[a-zA-Z][a-zA-Z0-9_]*$"),
]

def split_into_tokens(line, patterns):
    tokens = []
    current = ""
    start = 0

    while start < len(line):

        # SKIP SINGLE-LINE COMMENT
        if line[start:start+2] == "//":
            break  # ignore the rest of the line
        # SKIP MULTI-LINE COMMENT
        if line[start:start+2] == "/*":
            end = line.find("*/", start+2)
            if end == -1:  # comment not closed
                return tokens  # skip full line
            start = end + 2
            continue

        char = line[start]
        # print(char)
        if char.isspace():
            if current:
                tokens.append(current)
                current = ""
            start += 1
            continue
        
        if char in patterns["operators"] or char in patterns["punctuation"]:
            if current:
                tokens.append(current)
                current = ""
            tokens.append(char)
            start += 1
            continue

        if char == '"':
            if current:
                tokens.append(current)
                current = ""
            j = start + 1
            while j < len(line) and line[j] != '"':
                j += 1
            if j < len(line):
                tokens.append(line[start:j+1])
                start = j + 1
            else:
                tokens.append(line[start:])
                start = len(line)
            continue


        if char == "'":
            if current:
                tokens.append(current)
                current = ""
            if start+2 < len(line) and line[start+2] == "'":
                tokens.append(line[start:start+3])
                start += 3
            else:
                tokens.append(line[start:])  # invalid char constant
                start = len(line)
            continue
        
        current += char
        start += 1

    if current:
        tokens.append(current)

    return tokens

def classify_tokens(token, line_no):
    if token in PATTERNS["keywords"]:
        return ("KEYWORD", token, line_no)
    
    if token in PATTERNS["operators"]:
        return ("OPERATOR", token, line_no)
    
    if token in PATTERNS["punctuation"]:
        return ("PUNCTUATION", token, line_no)

    for name, pattern in TOKEN_PATTERNS:
        if re.match(pattern, token):
            return (name, token, line_no)
    
    return ("ERROR", token, line_no)

def main():
    with open("code.txt", "r") as f:
        lines = f.readlines()

    with open("output.txt", "w") as out:
        out.write("Token\tLexeme\tLine No\n")
        for line_no, line in enumerate(lines, start=1):
            raw_tokens = split_into_tokens(line.strip(), PATTERNS)
            for t in raw_tokens:
                token_type, lexeme, ln = classify_tokens(t, line_no)
                out.write(f"{token_type}\t{lexeme}\t{ln}\n")

if __name__ == "__main__":
    main()
