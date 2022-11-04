# Практично повноцінна реалізація інтерфейсу командного рядка (взаємодія із користувачем) і парсеру команд.
import re
import os

pattern_create = re.compile("^[Cc][Rr][Ee][Aa][Tt][Ee]\s+[a-zA-Z][a-zA-Z0-9_]*\s+\(\s*[a-zA-Z][a-zA-Z0-9_]*(\s*,\s*[a-zA-Z][a-zA-Z0-9_]*)*\s*\)\s*;\s*$")
pattern_insert = re.compile("^[Ii][Nn][Ss][Ee][Rr][Tt](\s+[Ii][Nn][Tt][Oo])?\s+[a-zA-Z][a-zA-Z0-9_]*\s+\(\s*\".+\"(\s*,\s*\".+\")*\s*\)\s*;\s*$")
pattern_select = re.compile("^[Ss][Ee][Ll][Ee][Cc][Tt]\s+[Ff][Rr][Oo][Mm]\s+[a-zA-Z][a-zA-Z0-9_]*\s*;\s*$")
pattern_exit = re.compile("^[Ee][Xx][Ii][Tt]\s*;\s*$")
pattern_clear = re.compile("^[Cc][Ll][Ee][Aa][Rr]\s*;\s*$")
patterns = [pattern_create, pattern_insert, pattern_select, pattern_exit, pattern_clear]
print("◙ Welcome to our program, which was created by students of group FB-01: Prykhodko Ihor and Sakhnii Nazar 🙂\n\n"
      "♦ To test the command line interface, please ENTER basic database query commands ↓ (To finish type \"EXIT\")")

while True:
    command = ""
    i = 0
    while True:
        if i == 0:
           line = input(">>> ")
        else:
            line = input("... ")
        i += 1
        command += (line + "\n")
        if ";" in line:
            break
    result = -1
    for i in range(len(patterns)):
        if patterns[i].match(command):
            result = i
            break
    if result == -1:
        if bool(re.match("^[Cc][Rr][Ee][Aa][Tt][Ee]", command)):
            print("Incorrect \"CREATE\" syntax.\n"
                  "Try to make query in next format → CREATE {table_name} ({column_name_№1} [,..., {column_name_№n}]);")
        elif bool(re.match("^[Ii][Nn][Ss][Ee][Rr][Tt]", command)):
            print("Incorrect \"INSERT\" syntax. \n"
                  "Try to make query in next format → INSERT [INTO] {table_name} ('{value_№1}' [,..., '{value_№n}']);")
        elif bool(re.match("^[Ss][Ee][Ll][Ee][Cc][Tt]", command)):
            print("Incorrect \"SELECT\" syntax. \n"
                  "Try to make query in next format → SELECT FROM {table_name};")
        elif bool(re.match("^[Ee][Xx][Ii][Tt]", command)):
            print("Incorrect \"EXIT\" syntax. \n"
                  "Format of \"EXIT\" command: EXIT;")
        elif bool(re.match("^[Cc][Ll][Ee][Aa][Rr]", command)):
            print("Incorrect \"CLEAR\" syntax. \n"
                  "Format of \"CLEAR\" command: CLEAR;")
        else:
            print("Unknown command :-(")
    else:
        if result == 0:
            tokens_create = re.findall("[a-zA-Z][a-zA-Z0-9_]*", command)  
            print("Tokens of \"CREATE\" command:")
            print(tokens_create)
        elif result == 1:
            tokens_insert = re.findall("(\".+?\")|([a-zA-Z][a-zA-Z0-9_]*)", command)
            print("Tokens of \"INSERT\" command:")
            print(tokens_insert)
        elif result == 2:
            tokens_select = re.findall("[a-zA-Z][a-zA-Z0-9_]*", command)
            print("Tokens of \"SELECT\" command:")
            print(tokens_select)
        elif result == 3:
            break
        elif result == 4:
            os.system("cmd /c cls")
       
