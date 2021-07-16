"""
Try to set the table in a class

Need to handle fixed columns on left
"""

import PySimpleGUI as sg
from TableObj import PSGTable

sg.theme('Darkgrey')

def createColumns():
    columns = [
        {'text':'ID', 'width': 6, 'bg':'blue', 'fg':'white'},
        {'text':'Name', 'width': 20, 'bg':'blue', 'fg':'white'},
        {'text':'nickname', 'width': 10, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Level', 'width': 5, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Priority', 'width': 5, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'No Files', 'width': 6, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Pages', 'width': 5, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Col 1', 'width': 15, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Col 2', 'width': 15, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Col 3', 'width': 15, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Col 4', 'width': 15, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Col 5', 'width': 15, 'bg':'red', 'fg':'white', 'align':'center'},
        {'text':'Col 6', 'width': 15, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Col 7', 'width': 15, 'bg':'blue', 'fg':'white', 'align':'center'}
    ]
    return columns

# Temporary test data     
def create_data(rows, cols):
    data = [[f'({row}, {col})' for col in range(cols)]
        for row in range(rows)]
    #data[0].append('Test')
    data.append(['A'])
    return data

def drawCell(element, dataRow, dataColumn, value, table):
    # Used by table to display data
    if value == 'A':
        element.update(background_color='red')
    else:
        element.update(background_color='blue')
    element.update(value)

columns = createColumns()
table1 = PSGTable('A_', visibleRows=10, visibleColumns=10, colSpecs=columns, data=create_data(12,len(columns)), 
                   leftColLock=0, drawCell=drawCell) #    (50,20))

layout = [[sg.Text(text='Sample Text')], [sg.Frame('',table1.layout())],
[sg.Button('Exit')]]

window = sg.Window('Simulate Table 3', layout, use_default_focus=False,return_keyboard_events=True,
    finalize=True)
table1.initialize(window)



while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Exit':
        break
    elif event == table1.ID + 'V_Scrollbar':
        table1.vscroll(values[table1.ID + 'V_Scrollbar'])
    elif event == table1.ID + 'H_Scrollbar':
        table1.hscroll(values[table1.ID + 'H_Scrollbar'])
    elif event == table1.ID+'CELLCLICKED': # Example cell clicked process
        tableRow,tableCol, dataRow, dataCol = values[table1.ID+'CELLCLICKED']
        #print (tableRow,tableCol, dataRow, dataCol)
        if dataRow != None and dataCol != None:
            if table1.data[dataRow][dataCol] == 'ONE':
                c = 'TWO'
            else:
                c = 'ONE'
            table1.data[dataRow][dataCol] = c    
            table1.updateCells()
    else:
        print (event)
        print ( values)
        #table1.data[0][0] = '<0:0>'
        #table1.updateCells()

window.close()