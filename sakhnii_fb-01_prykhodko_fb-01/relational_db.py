# Практично повноцінна реалізація основної структури даних.
# [Ii][Nn][Dd][Ee][Xx][Ee][Dd]
# from ctypes.wintypes import BOOL
import re
import os
from prettytable import PrettyTable

pattern_create = re.compile("^[Cc][Rr][Ee][Aa][Tt][Ee]\s+[a-zA-Z][a-zA-Z0-9_]*\s+\(\s*[a-zA-Z][a-zA-Z0-9_]*(\s+[Ii][Nn][Dd][Ee][Xx][Ee][Dd])*(\s*,\s*[a-zA-Z][a-zA-Z0-9_]*(\s+[Ii][Nn][Dd][Ee][Xx][Ee][Dd])*)*\s*\)\s*;\s*$")
pattern_insert = re.compile("^[Ii][Nn][Ss][Ee][Rr][Tt](\s+[Ii][Nn][Tt][Oo])?\s+[a-zA-Z][a-zA-Z0-9_]*\s+\(\s*\".+\"(\s*,\s*\".+\")*\s*\)\s*;\s*$")
pattern_select = re.compile("^[Ss][Ee][Ll][Ee][Cc][Tt]\s+[Ff][Rr][Oo][Mm]\s+[a-zA-Z][a-zA-Z0-9_]*(\s+[Ww][Hh][Ee][Rr][Ee]\s+[a-zA-Z][a-zA-Z0-9_]*\s+[><=]\s+(([a-zA-Z][a-zA-Z0-9_]*)|(\".+\")))?\s*;\s*$")
pattern_exit = re.compile("^[Ee][Xx][Ii][Tt]\s*;\s*$")
pattern_clear = re.compile("^[Cc][Ll][Ee][Aa][Rr]\s*;\s*$")
patterns = [pattern_create, pattern_insert, pattern_select, pattern_exit, pattern_clear]
print("Welcome to our program, which was created by students of group FB-01: Prykhodko Ihor and Sakhnii Nazar \n\n"
      "To test relational database, please ENTER basic query commands (To finish type \"EXIT\")")
tables = {}
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
                  "Try to make query in next format ↓\n"
                  "> CREATE {table_name} ({column_name_№1} [,..., {column_name_№n}]);\n")
        elif bool(re.match("^[Ii][Nn][Ss][Ee][Rr][Tt]", command)):
            print('Incorrect \"INSERT\" syntax.\n'
                  'Try to make query in next format ↓\n'
                  '> INSERT [INTO] {table_name} ("{value_№1}" [,..., "{value_№n}"]);\n')
        elif bool(re.match("^[Ss][Ee][Ll][Ee][Cc][Tt]", command)):
            print("Incorrect \"SELECT\" syntax.\n"
                  "Try to make query in next format ↓\n"
                  "> SELECT FROM {table_name}\n"
                  ".   [WHERE {condition}]\n"
                  ".   [ORDER_BY {column_name_№1} [(ASC|DESC)] [,..., {column_name_№n}] ];\n")
        elif bool(re.match("^[Ee][Xx][Ii][Tt]", command)):
            print("Incorrect \"EXIT\" syntax.\n"
                  "Format of \"EXIT\" command: EXIT;\n")
        elif bool(re.match("^[Cc][Ll][Ee][Aa][Rr]", command)):
            print("Incorrect \"CLEAR\" syntax.\n"
                  "Format of \"CLEAR\" command: CLEAR;\n")
        else:
            print("Unknown command :-(")
    else:
        if result == 0:
            tokens_create = re.findall("[a-zA-Z][a-zA-Z0-9_]*", command)
            # print("Tokens of \"CREATE\" command:")
            # print(tokens_create)
            if tokens_create[1] in tables:
                print("Error! Table with this name is already exist ¯\_(ツ)_/¯\n")
                continue
            else:
                column_names = []
                error_check = 0
                for token in tokens_create[2:]:
                    if bool(re.match("[Ii][Nn][Dd][Ee][Xx][Ee][Dd]", token)):
                        pass  # Will be added in the near future
                    else:
                        if token in column_names:
                            print("Error. Can not create table with 2 similar names of columns ¯\_(ツ)_/¯\n")
                            error_check = 1
                            break
                        column_names.append(token)
                if error_check:
                    continue
                tables[tokens_create[1]] = [column_names]
                print("Tables:", tables)
                print("◘ 'Table", tokens_create[1], "has been created'\n")
        elif result == 1:
            tokens_insert_values = re.findall("\".+?\"", command)
            tokens_insert_name = re.findall("[a-zA-Z][a-zA-Z0-9_]*(?=(?:[^\"]*\"[^\"]*\")*[^\"]*\Z)", command)
            # print("Tokens of \"INSERT\" command:")
            # print(tokens_insert_values)
            # print(tokens_insert_name)
            table_name = tokens_insert_name[-1]
            if table_name not in tables:
                print("Error! No such table ¯\_(ツ)_/¯\n")
                continue
            table = tables[table_name]
            if len(tokens_insert_values) != len(table[0]):
                print("Error! Number of tokens not matching the number of columns ¯\_(ツ)_/¯\n")
                continue
            table.append(tokens_insert_values)
            print("Tables:", tables)
            print("◘ '1 row has been inserted into ", table_name, "'\n", sep="")
        elif result == 2:
            tokens_select = re.findall("[a-zA-Z][a-zA-Z0-9_]*(?=(?:[^\"]*\"[^\"]*\")*[^\"]*\Z)", command)
            # print("Tokens of \"SELECT\" command:")
            # print(tokens_select)
            table_name = tokens_select[2]
            table = tables[table_name]
            output_table = PrettyTable()
            output_table.field_names = table[0]
            if len(tokens_select) == 3:
                output_table.add_rows(table[1:])
                print(output_table)
            else:
                if bool(re.match("[Ww][Hh][Ee][Rr][Ee]", tokens_select[3])):
                    def check_condition(condition: str, parameter_1: str, parameter_2: str) -> bool:
                        if condition == ">":
                            if parameter_1 > parameter_2:
                                return True
                        elif condition == "<":
                            if parameter_1 < parameter_2:
                                return True
                        else:
                            if parameter_1 == parameter_2:
                                return True
                        return False

                    parameter_1 = tokens_select[4]
                    index_1 = table[0].index(parameter_1)
                    condition = re.search("[<>=]", command).group()
                    parameter_2 = re.findall("\".+?\"", command)
                    if not parameter_2:
                        parameter_2 = tokens_select[5]
                        index_2 = table[0].index(parameter_2)
                        for row in table[1:]:
                            if check_condition(condition, row[index_1], row[index_2]):
                                output_table.add_row(row)
                    else:
                        parameter_2 = parameter_2[0]
                        for row in table[1:]:
                            if check_condition(condition, row[index_1], parameter_2):
                                output_table.add_row(row)
                    print(output_table)
                else:
                    pass  # "Order by" will be added soon
        elif result == 3:
            break
        elif result == 4:
            os.system('cmd /c "cls"')
# create test (a,b,c);
# insert test ("a","b","c");
# insert test ("1","2","3");
# insert test ("r","t","f");
# insert test ("ab","bc","cd");
# select from test where b > "b";
