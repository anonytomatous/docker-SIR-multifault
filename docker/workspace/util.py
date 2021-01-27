import os
import re

source_file_names = {
    'gzip': 'allfile.c',
    'grep': 'grep.c',
    'sed': 'sed.c',
    'flex': 'flex.c'
}

linking_command_pattern = {
    'gzip': 'gcc -o allfile allfile.o',
    'grep': 'gcc $(COMPILE_PARAMETERS) -I. -o  grep.exe grep.c',
    'sed': 'gcc -o sed.exe',
    'flex': '$(CC) -o flex.exe flex.o'
}

def string2number(name: str) -> int:
    number = int(''.join([s for s in name if s.isdigit()]))
    return number

def sort_string_by_number(l: list) -> list:
    return sorted(l, key=lambda x: string2number(x))

def get_test_cases(original_output_path):
            return [tc for tc in os.listdir(original_output_path) if re.match(r'(?:test|t)[0-9]+', tc) != None]

def get_test_number(test_name):
    digits = ''
    for c in test_name:
        if c.isdigit():
            digits = digits + c
    
    return int(digits)