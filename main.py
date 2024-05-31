import re

FILE_NAME = 'sales'

COMMANDS = [
    ('help', 'Show all commands with descriptions'),
    ('add', 'Add an entry to the sales report'),
    ('delete', 'Delete an entry from the sales report'),
    ('update', 'Update the number of sold units for a product'),
    ('chart', 'Draw a chart of the data'),
    ('exit', 'Finish program execution')
]


def is_empty(file_name):
    file = open(file_name, 'r')
    return file.read() == ''


def get_line_data(line):
    comma_index = line.index(',')
    name = line[:comma_index]
    sold = line[comma_index + 1:]
    return str(name), int(sold)


def format_line(name, sold, name_justify_width, sold_justify_width):
    formatted_name = name.rjust(name_justify_width, ' ')
    sales_number = f' ({str(sold).rjust(sold_justify_width, "0")}): '
    bars = '#' * sold
    return formatted_name + sales_number + bars


def get_longest_name_and_sold(lines):
    longest_name = ''
    largest_sold = 0
    for l in lines:
        name, sold = get_line_data(l)
        if len(longest_name) < len(name):
            longest_name = name
        if sold > largest_sold:
            largest_sold = sold

    return longest_name, largest_sold


def chart(file_name, date):
    print()
    if is_empty(file_name):
        print('No products to show!')
        print()
        return

    sales_data = open(file_name, 'r')
    lines = sales_data.readlines()
    longest_name, largest_sold = get_longest_name_and_sold(lines)

    print('SALES REPORT for ' + date)
    print('==================')
    for line in lines:
        name, sold = get_line_data(line.strip())
        print(format_line(name, sold, len(longest_name), len(str(largest_sold))))
    print()


def show_commands():
    print()
    for c in COMMANDS:
        print(c[0], '|', c[1])
    print()


def add_entry(file_name):
    file = open(file_name, 'r')
    lines = file.read().split('\n')
    if lines[0] == '':
        lines = []
    name = input('Product name: ')
    quantity = input('Quantity sold: ')
    lines.append(f'{name},{quantity}')
    file = open(file_name, 'w')
    file.write('\n'.join(lines))
    file.close()
    print(f'Added {name}, {quantity} units')


def delete_entry(file_name):
    print()
    if is_empty(file_name):
        print('No products to delete. Consider adding them first.')
        print()
        return

    product_name = input('What product do you want to delete? ')
    file = open(file_name, 'r')
    lines = file.read().split('\n')
    has_product = False
    for i in range(0, len(lines)):
        name = get_line_data(lines[i])[0]
        if name == product_name:
            has_product = True
            lines.remove(lines[i])
            break

    if has_product:
        file = open(file_name, 'w')
        file.write('\n'.join(lines))
        file.close()
        print('deleted ' + product_name)
    else:
        print('No product named \'' + product_name + '\' was found')

    print()


def update_entry(file_name):
    print()
    if is_empty(file_name):
        print('No products to update. Consider adding them first.')
        print()
        return
    product_name = input('What product do you want to update? ')
    file = open(file_name, 'r')
    lines = file.read().split('\n')
    has_product = False
    for i in range(0, len(lines)):
        name = get_line_data(lines[i])[0]
        if name == product_name:
            new_quantity = input('What is the new quantity? ')
            lines[i] = name + ',' + new_quantity
            has_product = True
            break

    if has_product:
        file = open(file_name, 'w')
        file.write('\n'.join(lines))
        file.close()
        print('updated ' + product_name)
    else:
        print('No product named \'' + product_name + '\' was found')

    print()


def interpret_command(command, file_name, date):
    match command:
        case 'help':
            show_commands()
        case 'add':
            add_entry(file_name)
        case 'delete':
            delete_entry(file_name)
        case 'update':
            update_entry(file_name)
        case 'chart':
            chart(file_name, date)
        case 'exit':
            print('Finishing')
            exit()
        case _:
            print(f'Unknown command \'{command}\', please try another one')


def main():
    print('Initiating')
    date = ''
    while re.search('^\\d{4}-\\d{2}-\\d{2}$', date) == None:
        print('Which date would you like to work on?')
        date = input('Use the format YYYY-MM-DD, like 2024-01-02 (January 2nd, 2024): ').strip()

    file_name = date + '_' + FILE_NAME + '.txt'
    open(file_name, 'a')

    print('Type help for all available commands')
    while True:
        command = input('Waiting for command: ')
        interpret_command(command, file_name, date)


main()
