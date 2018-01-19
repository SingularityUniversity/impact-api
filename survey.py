import csv
from collections import OrderedDict

# with open('impact.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print(row["StartDate"])
#         a.append(row['StartDate'] + row['Q6'])
# print(a)
#
# with open('new_impact.csv', 'w', newline='') as newfile:
#     writer = csv.writer(newfile, delimiter=' ')
#     for line in a:
#         writer.writerow(line)


def write_in(my_list, question_no, my_string):

    if my_list[question_no] == "Yes":
        my_list[question_no + 1] = my_string
        pull_in(my_list, 22, 19)


def pull_in(my_list, question_no, col):
    my_list.insert(question_no + 1, "")
    my_list[question_no + 1] = my_list[col]


def insert_new_columns(matrix, question_no, columns):
    for row in matrix:
        for x in range(len(columns)):
            row.insert(question_no + x + 1, "")

    for x in range(len(columns)):
        matrix[0][question_no + x + 1] = columns[x]





def fill_matrix_with_csv():
    matrix = []
    with open('impact.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            matrix.append(row)
    return matrix


def fill_csv_from_matrix(matrix):
    with open('new_impact.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in matrix:
            write_in(row, 22, 'New Organization')
            writer.writerow(row)


def main():
    my_matrix = fill_matrix_with_csv()
    insert_new_columns(my_matrix, 22, ["Email", "Impact_Initiative_Type"])
    fill_csv_from_matrix(my_matrix)


def fill_dict_matrix_from_csv(csvfile='impact.csv'):
    matrix = []
    with open(csvfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            matrix.append(row)
    return matrix


def insert_into_ordered_dict(my_dict, key_index, new_key):
    new_dict = my_dict.__class__()
    for key, value in my_dict.items():
        new_dict[key] = value
        if key == key_index:
            new_dict[new_key] = ""
    my_dict.clear()
    my_dict.update(new_dict)


def dict_insert_new_columns(matrix, columns):
    columns.reverse()

    for x in range(len(columns)):
        question = columns[x].split('-')[0]
        print(question)
        for an_ordered_dict in matrix:
            insert_into_ordered_dict(an_ordered_dict, question, columns[x])


column_logic = (
    {'Name': 'Q6', 'Check': 'Yes', '#Email': 'Q2_3', '@Impact_Initiative_Type': 'New Organization'},
)

column_logic = fill_dict_matrix_from_csv('logic.csv')

column_names = ['Email', 'Impact_Initiative_Type', 'Name', 'One-liner', 'Subtype',	'Year_founded',
                'Program_Affiliation', 'GGC_Focus', 'Tech_Focus', 'Num_Employees', 'Scale',
                'Influence']

def get_column_names(column_names, column_logig):
    names = []
    for row_dict in column_logic:
        for col in column_names:
            col_name = row_dict['Name'] + '-' + col
            names.append(col_name)
    return names

column_names = get_column_names(column_names, column_logic)


def process_question(my_dict, question_dict):
    for key, value in question_dict.items():
        if key.startswith('#'):
            column_name = question_dict['Name'] + '-' + key[1:].strip()
            try:
                my_dict[column_name] = my_dict[question_dict[key].strip()]
            except KeyError:
                print('Key Error')
        elif key.startswith('@'):
            column_name = question_dict['Name'] + '-' + key[1:].strip()
            my_dict[column_name] = question_dict[key].strip()


def process_all_questions(my_dict, column_logic=column_logic):
    for question_dict in column_logic:
        if question_dict['Name']:
            if my_dict[question_dict['Name']] == question_dict['Check']:
                print('processing question', question_dict['Name'])
                process_question(my_dict, question_dict)


def transform_matrix(matrix):
    dict_insert_new_columns(matrix, column_names)
    for my_dict in matrix:
        print('processing row')
        process_all_questions(my_dict)


def get_headers(matrix):
    headers = []
    for k, v in matrix[0].items():
        headers.append(k)
    return headers


def fill_csv_from_dict_matrix(matrix, csvfile='new_dict_impact.csv'):
    fieldnames = get_headers(matrix)
    with open(csvfile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in matrix:
            writer.writerow(row)

my_dict_matrix = fill_dict_matrix_from_csv('impact.csv')
print('matrix created')
transform_matrix(my_dict_matrix)
print('matrix transformed')
fill_csv_from_dict_matrix(my_dict_matrix)








