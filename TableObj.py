
import PySimpleGUI as sg

class PSGTable:
    def __init__(self, tableID, visibleRows=0, visibleColumns=0, colSpecs=[], data=None, leftColLock=0,
                 drawCell=None, headerBG='green') -> None:
        self.ID = tableID
        self.visibleRows = visibleRows # Not including column header - maybe set automatically if not supplied?
        self.colSpecs = colSpecs # Name, widths, colors, justification
        self.headerBG = headerBG
        self.visibleColumns = visibleColumns  # maybe set automatically if not supplied?
        self.gap = 2
        self.topDataRow = 0   # Modified when scrolling
        self.leftDataCol = 0  # Adjusted when scroling horizontally
        self.leftColLock = leftColLock # Columns that do not scroll horizontally
        self.isVScroll = True # Changed when data analyzed (setData())
        self.isHScroll = True # Changed when data analyzed (setData())
        self.data = data
        self.setData(data)
        self.window = None # Set in initialize()
        # Set table rows and columns (visible) if not specified, from the data rows and the number of columns
        if not self.visibleRows:
            self.visibleRows = len(data)
        if not self.visibleColumns:
            self.visibleColumns = len(colSpecs)
        if drawCell: # Replace
            self.drawCell = drawCell
    # ---------------------------------------------------------------------------------------------------
    # Install data matrix and associated variables
    # ---------------------------------------------------------------------------------------------------
    def setData(self, data):
        self.data = data # So it can be used after the object is instantiated
        self.dataRows = len(data)
        cols = 0
        for row in data: # In case of sparse data, find the longest row
            cols = max(cols, len(row))
        self.dataColumns = cols
        self.topDataRow = 0
        self.leftDataCol = 0
        # With V scroll, it works to just make it invisible
        # With H scroll making it invisible leaves a space, so remove the creation during layout
        # If not needed
        if self.dataRows <= self.visibleRows:
            self.isVScroll=False
        if self.dataColumns <= self.visibleColumns:
            self.isHScroll = False
    # ---------------------------------------------------------------------------------------------------
    # Table layout
    # ---------------------------------------------------------------------------------------------------
    def layout(self):
        # V & H Scrollbar issues
        # Below we provide the vertical range, but we might not know this when layout created
        # Without the data we do not know how many columns of data there is 
        table = self.cellLayout()
        vHeight = self.visibleRows * 1.15
        # Calculate horizontal width for scroll bar - initial value set, cannot be changed when horizontally scrolling
        w = 0
        for col in self.colSpecs[:self.visibleColumns]:
            w += col['width']
        w = w *.95
        option2 = {'resolution':1, 'pad':(0, 0), 'disable_number_display':True,
        'enable_events':True}
        layout = []
        layout.append([sg.Column(table, background_color='black', pad=(0, 0), key='Table'),
             sg.Slider(range=(1, len(self.data)-self.visibleRows),    size=(vHeight, 24), orientation='v',
             **option2, key=self.ID+'V_Scrollbar', visible=True)])
        if self.isHScroll:
            layout.append([sg.Slider(range=(0, self.dataColumns-self.visibleColumns), size=(w, 25), orientation='h',
                **option2, key=self.ID+'H_Scrollbar', visible=True)])
        return layout

    def cellLayout(self):
        table = []
        line = []
        for i in range(self.visibleColumns):
            col = self.colSpecs[i]
            line.append(sg.Text(col['text'], size=(col['width'],1),background_color=self.headerBG, pad=(self.gap,1),
            justification=col.get('align', 'left'), key=self.ID+'Col_'+str(i)))
        table.append(line)
        for y in range(0, self.visibleRows):
            line = []
            for x in range(0, self.visibleColumns):
                #x_pad = (self.gap, self.gap) if x==self.visibleColumns-1 else (self.gap, 0)
                #y_pad = (self.gap, self.gap) if y==self.visibleRows-1 else (self.gap, 0)
                #pad = (x_pad, y_pad)
                #bg = 'green' if (x == 0 or y == 0) else 'blue'
                line.append(
                    sg.Text(' ', size=(self.colSpecs[x]['width'], 1), pad=(self.gap,1), 
                        justification=self.colSpecs[x].get('align','left'), # enable_events=True,
                        text_color=self.colSpecs[x]['fg'], background_color=self.colSpecs[x]['bg'], key=self.ID + str((y, x)))
                )
            table.append(line)
        return table
    # ---------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------------
    def updateCells(self):
        # Get columns that need to be displayed
        temp = [i for i in range(self.dataColumns)]
        displayCols = temp[:self.leftColLock] + temp[self.leftColLock+self.leftDataCol:self.visibleColumns+self.leftDataCol]
        displayCols = self.displayColumns()
        count = 0 # Text box column
        for i in displayCols: # Resize column headers, i = display column
            element = self.window[self.ID + 'Col_' + str(count)]
            element.update(self.colSpecs[i]['text'])
            element.set_size((self.colSpecs[i]['width'],1))
            count += 1
        for row in range(self.visibleRows):
            colCount = 0 # The taxt box column
            for colNo in displayCols: # The data to display
                element = self.window[self.ID+str((row, colCount))]
                element.set_size((self.colSpecs[colNo]['width'],1))
                if row < self.dataRows:
                    if colNo < len(self.data[row+self.topDataRow]): # Draw data
                        #element.update(self.data[row+self.topDataRow][colNo])
                        self.drawCell(element, row+self.topDataRow,colNo, self.data[row+self.topDataRow][colNo], self)
                    else: # Blank cell
                        element.update(' ')
                else: # Blank row
                    element.update(' ')
                colCount += 1
        self.window.refresh()

    # Replace in main program if required
    def drawCell(self, element, dataRow, dataColumn, value, table): # In case we need to change the data
        element.update(value)

    def displayColumns(self):
        temp = [i for i in range(self.dataColumns)]
        return temp[:self.leftColLock] + temp[self.leftColLock+self.leftDataCol:self.visibleColumns+self.leftDataCol]

    def vscroll(self, event):
        if not self.isVScroll:
            return
        if type(event) is float: # Using scroll bar
            self.topDataRow = self.dataRows - self.visibleRows - int(event) + 1
        else:                    # Using mouse wheel
            delta = int(event.delta/120)
            self.topDataRow = min(max(0, self.topDataRow-delta), self.dataRows - self.visibleRows)
        self.updateCells()
        self.window[self.ID+'V_Scrollbar'].update(value=self.dataRows - self.visibleRows - self.topDataRow+1)
        self.window.refresh()

    def hscroll(self, event):
        if not self.isHScroll:
            return
        if type(event) is float: # Using scroll bar
            self.leftDataCol = int(event) # self.dataColumns - self.visibleColumns - int(event) + 1
        else:
            delta = int(event.delta/120)
            self.leftDataCol = min(max(0, self.leftDataCol-delta), self.dataColumns-self.visibleColumns)
        self.updateCells()
        self.window[self.ID+'H_Scrollbar'].update(value=self.leftDataCol) # self.dataColumns - self.visibleColumns - self.leftDataCol+1)
        self.window.refresh()

    def clicked(self, x, row, col,): # x is needed, but not used
        # Row and column are the textbox row and column, not the data
        dataRow = self.topDataRow + row
        if dataRow >= len(self.data):
            dataRow = None
            dataColumn = None
        else:
            displayCols = self.displayColumns()
            dataColumn = displayCols[col]
            if dataColumn >= len(self.data[dataRow]):
                dataColumn = None
        self.window.write_event_value(self.ID+ 'CELLCLICKED', (row,col, dataRow, dataColumn)) # This appears in main window loop as an event

    # ---------------------------------------------------------------------------------------------------
    # Complete the linking of events to mousewheel, scroll bars
    # ---------------------------------------------------------------------------------------------------
    def initialize(self, window):
        for y in range(self.visibleRows):
            for x in range(self.visibleColumns):
                element = window[self.ID+str((y, x))]
                element.Widget.configure(takefocus=0)
                element.Widget.bind('<MouseWheel>', self.vscroll)
                element.Widget.bind('<Shift-MouseWheel>', self.hscroll)
                element.Widget.bind('<Button-1>', lambda eff='s', a=y, b=x: self.clicked(eff, a, b)) # PDH - Not sure what eff does? (Space for the event?)
                element.ParentRowFrame.bind('<MouseWheel>', self.vscroll)
                element.ParentRowFrame.bind('<Shift-MouseWheel>', self.hscroll)
        window[self.ID+'V_Scrollbar'].update(value=len(self.data)-self.visibleRows) # 0 is at the bottom of the slider!
        if self.isHScroll:
            window[self.ID+'H_Scrollbar'].update(value=0) #self.dataColumns) # 0 is at the bottom of the slider!
        if len(self.data) <= self.visibleRows: # Vertical scroll not needed
            window[self.ID+'V_Scrollbar'].update(visible=False)
        self.window = window
        self.updateCells()
        window.refresh()
    # ---------------------------------------------------------------------------------------------------

