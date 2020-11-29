import argparse
import csv
import jinja2
import sys

parser = argparse.ArgumentParser()
parser.add_argument('input_file', nargs='?', type=argparse.FileType('r', encoding='utf-8'), default=sys.stdin)
parser.add_argument('output_file', nargs='?', type=argparse.FileType('w', encoding='utf-8'), default=sys.stdout)
args = parser.parse_args()

index = {
    'family-name': 1,
    'first-name': 2,
    'family-name-kana': 3,
    'first-name-kana': 4,
    'id': 5,
    'mail-address': 6,
    'group': 17,
}

members_by_group = {}

rows = csv.reader(args.input_file, delimiter='\t')
for row in rows:
    member = {
        'name': row[index['family-name']] + ' ' + row[index['first-name']],
        'data': [
            row[index['family-name']],
            row[index['first-name']],
            row[index['family-name-kana']],
            row[index['first-name-kana']],
            row[index['mail-address']],
            row[index['id']],
        ]
    }

    members_by_group.setdefault(row[index['group']], []).append(member)


template = '''\
@NoteHotkey = ^+y,400
{%- for group, members in members_by_group.items() %}
+{{ group }}
    {%- for member in members %}
    +{{ member.name }}
        {%- for item in member.data %}
        {{ item }}
        {%- endfor %}
    ..
    {%- endfor %}
..
{%- endfor %}
'''


env = jinja2.Environment(loader = jinja2.DictLoader({'template.txt.j2': template}))
template = env.get_template('template.txt.j2')
context = { 'members_by_group': members_by_group }
result = template.render(context)

args.output_file.write(result)
