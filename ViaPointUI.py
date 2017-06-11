#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

# Global variable used to maintain a reference to all event handlers.
handlers = []
ui = None
app = None
rowNumber = 0

def addRow(tableInput):
    tableChildInputs = tableInput.commandInputs
    childTableNumberInput = tableChildInputs.addIntegerSpinnerCommandInput(tableInput.id + '_number{}'.format(rowNumber), 'Via-Point Number', 0 , 50 , 1, 0)
    childTableLinkInput =  tableChildInputs.addDropDownCommandInput(tableInput.id + '_link{}'.format(rowNumber), 'Select Link Name', adsk.core.DropDownStyles.LabeledIconDropDownStyle);
    dropdownItems = childTableLinkInput.listItems
    # TODO: rigidGroupSupport
    dropdownItems.add('Link 1', False, '')
    dropdownItems.add('Link 2', False, '')
    childTableSelectInput =  tableChildInputs.addDropDownCommandInput(tableInput.id + '_select{}'.format(rowNumber), 'Select Point Number', adsk.core.DropDownStyles.LabeledIconDropDownStyle);
    dropdownItemsSelect = childTableSelectInput.listItems
    for i in range(1,10):
        dropdownItemsSelect.add('Select Number ' + str(i), False, '')
    
    row = tableInput.rowCount
    tableInput.addCommandInput(childTableNumberInput, row, 0)
    tableInput.addCommandInput(childTableLinkInput, row, 1)
    tableInput.addCommandInput(childTableSelectInput, row, 2)
    
    global rowNumber
    rowNumber = rowNumber + 1

# Event handler for the commandCreated event.
class ButtonCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        cmd = args.command
        inputs = cmd.commandInputs
        commandId = "xyz"

        # Create tab input 1
        tabCmdInput1 = inputs.addTabCommandInput(commandId + '_tab_1', 'Add');
        tab1ChildInputs = tabCmdInput1.children;

        # Create integer spinner input
        tab1ChildInputs.addIntegerSpinnerCommandInput(commandId + '_spinnerInt', 'MyoMuscle Number', 0 , 500 , 1, 0)

        # Create table input
        tableInput = tab1ChildInputs.addTableCommandInput(commandId + '_table', 'Via-Points', 3, '1:1:2')
        tableInput.tablePresentationStyle = 2
        #tableInput.minimumVisibleRows = 10
        tableInput.maximumVisibleRows = 11

        tableChildInputs = tableInput.commandInputs
        childTableNumberInput = tableChildInputs.addTextBoxCommandInput(tableInput.id + '_textBox1{}'.format(rowNumber), 'Via-Point Number', 'Via-Point Number', 1, True)
        childTableLinkInput = tableChildInputs.addTextBoxCommandInput(tableInput.id + '_textBox2{}'.format(rowNumber), 'Link Name', 'Link Name', 1, True)
        childTablePointInput = tableChildInputs.addTextBoxCommandInput(tableInput.id + '_textBox3{}'.format(rowNumber), 'Select Point Number', 'Select Point Number', 1, True)
        row = tableInput.rowCount
        tableInput.addCommandInput(childTableNumberInput, row, 0)
        tableInput.addCommandInput(childTableLinkInput, row, 1)
        tableInput.addCommandInput(childTablePointInput, row, 2)
        global rowNumber
        rowNumber = rowNumber + 1

        addRow(tableInput)

        for i in range(1,9                              ):
            addRow(tableInput)

            # Create selection input
            selectionInput = tab1ChildInputs.addSelectionInput(commandId + '_selection' + str(i), 'Select Point ' + str(i), 'Select a circle for the via-point.')
            selectionInput.setSelectionLimits(1, 1)
            selectionInput.addSelectionFilter("CircularEdges")

        #onSelectionEvent = MySelectionEventHandler()
        #cmd.selectionEvent.add(onSelectionEvent)
        #handlers.append(onSelectionEvent)

        onExecuteEvent = MyExecuteEventHandler()
        cmd.execute.add(onExecuteEvent)
        handlers.append(onExecuteEvent)

        #onInputChanged = MyCommandInputChangedHandler()
        #cmd.inputChanged.add(onInputChanged)
        #handlers.append(onInputChanged) 

class MyCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
           command = args.firingEvent.sender   
           cmdInput = args.input                   
           inputs = command.commandInputs
           
           commandId = "xyz"
           tableInput = inputs.itemById(commandId + '_table')
           if cmdInput.id == tableInput.id + '_add':
               addRow(tableInput)
           elif cmdInput.id == tableInput.id + '_delete':
               if tableInput.selectedRow == -1:
                   ui.messageBox('Select one row to delete')
               else:
                   tableInput.deleteRow(tableInput.selectedRow)
          
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Event handler for the execute event.
class MyExecuteEventHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandEventArgs.cast(args)
        try:
            command = eventArgs.firingEvent.sender   
            #cmdInput = eventArgs.input                   
            inputs = command.commandInputs

            commandId = "xyz"

            for i in range(1,9):
                selInput = inputs.itemById(commandId + '_selection' + str(i))
                #if cmdInput.id == selInput.id:
                if selInput is None:
                    global ui
                    ui.messageBox("nay")
                
                sel = selInput.selection(0)
                edge = adsk.fusion.BRepEdge.cast(sel.entity)
                global ui
                ui.messageBox("yay")
                # Get construction points
                global app
                product = app.activeProduct
                design = adsk.fusion.Design.cast(product)
                # get root component in this design
                rootComp = design.rootComponent
                conPoints = rootComp.constructionPoints
                # Create construction point input
                pointInput = conPoints.createInput()
                # Create construction point by center
                pointInput.setByCenter(edge)
                point = conPoints.add(pointInput)
                point.name = "asdfghjkl" + str(i)
          
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


        # Code to react to the event.
        ui.messageBox('In MyExecuteHandler event handler.')

# Event handler for the selectionEvent event.
class MySelectionEventHandler(adsk.core.SelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.SelectionEventArgs.cast(args)
        #sel = eventArgs.selection(0)
        #edge = adsk.fusion.BRepEdge.cast(sel.entity)

        global ui
        ui.messageBox("Edge")

        # Code to react to the event.
        ui.messageBox('In MySelectionEventHandler event handler.')

def run(context):
    ui = None
    try:
        global app
        app = adsk.core.Application.get()
        global ui
        ui  = app.userInterface
        cmdDefs = ui.commandDefinitions

        # Create a button command definition.
        button = cmdDefs.itemById('ViaPointButtonID')
        if not button:
            button = cmdDefs.addButtonDefinition('ViaPointButtonID', 'Via-Points','Via-Points', './/Resources//Viapoints')

        # Connect to the command created event.
        ButtonCommandCreated = ButtonCommandCreatedHandler()
        button.commandCreated.add(ButtonCommandCreated)
        handlers.append(ButtonCommandCreated)

        # Create new panel
        ViaPointPanel = ui.workspaces.itemById('FusionSolidEnvironment').toolbarPanels.itemById('ViaPointPanelId')
        if not ViaPointPanel:
            ViaPointPanel = ui.workspaces.itemById('FusionSolidEnvironment').toolbarPanels.add('ViaPointPanelId', 'VIA-POINTS')
        buttonControl = ViaPointPanel.controls.addCommand(button, 'ViaPointButtonID')
        buttonControl.isPromoted = True
        #buttonControl.isPromotedByDefault = True

        # Delete the button definition.
        #buttonExample = ui.commandDefinitions.itemById('VPUI_CmdID')
        #if buttonExample:
        #    buttonExample.deleteMe()
            
        # Get panel the control is in.
        #addInsPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')

        # Get and delete the button control.
        #buttonControl = addInsPanel.controls.itemById('VPUI_CmdID')
        #if buttonControl:
        #    buttonControl.deleteMe()

        # Prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        #adsk.autoTerminate(False)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    global ui
    try:
        # Clean up the command.
        global ui
        addInsPanel = ui.allToolbarPanels.itemById('ViaPointPanelId')
        cntrl = addInsPanel.controls.itemById('ViaPointButtonID')
        if cntrl:
            cntrl.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
