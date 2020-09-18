import xmltodict
from csv import DictReader
from collections import OrderedDict
from string import Template
comment_template = Template("""*********************************************************************************
${line1}
${line2}
*********************************************************************************""")

# Join in middle
def jim(join_text, template, iterator):
    return join_text.join(template.format(i) for i in iterator)

if __name__ == '__main__':
    with open('Rungs.L5X', 'r') as f:
        rungs = xmltodict.parse(f.read())
    with open('input.csv', 'r') as f:
        input_values = [row for row in DictReader(f)]
    output_rungs = list()
    for v in input_values:
        text = 'AOI_DigInput({0},{1},SIM_ENABLE,{0}.DisagreeAlarm,{0}.DisagreeAlarmAck);'.format(v['Name'], v['Point'])
        comment = comment_template.substitute(line1=v['Name'], line2=v['Description'])
        output_rungs.append(OrderedDict([('@Use', 'Target'), ('@Number', '0'), ('@Type', 'N'), ('Comment', comment), ('Text', text)]))
    rungs['RSLogix5000Content']['Controller']['Programs']['Program']['Routines']['Routine']['RLLContent']['Rung'] = output_rungs
    xmltodict.unparse(rungs, open('output.L5X', 'w'))

