import adsk.core
import adsk.fusion
import adsk.cam
import traceback

## Global variable used to maintain a reference to all event handlers.
handlers = []
## global variable to maintain reference to the fusion ui
ui = None
## global variable to maintain reference to the fusion application
app = None
## global varibale to keep track of how many table rows are created
rowNumber = 0
## global variable to specify how many via points can be input in the dialog window
numberViaPoints = 3
## global variable to specify the links that can be choosen
links = ['Link 1','Link 2']

## This is a helper function that adds rows to the dialog windows table.
def addRow(tableInput,i):
    tableChildInputs = tableInput.commandInputs
    # add input for via point number
    childTableNumberInput = tableChildInputs.addIntegerSpinnerCommandInput(tableInput.id + '_number{}'.format(rowNumber), 'Via-Point Number', 0 , 50 , 1, i)
    # add input for link name
    childTableLinkInput =  tableChildInputs.addDropDownCommandInput(tableInput.id + '_link{}'.format(rowNumber), 'Select Link Name', adsk.core.DropDownStyles.LabeledIconDropDownStyle);
    dropdownItems = childTableLinkInput.listItems
    # TODO: rigidGroupSupport
    # add a dropdown item for every link
    global links
    for lin in links:
        dropdownItems.add(lin, False, '')
    # add selection inputs to select the via point position
    childTableSelectInput =  tableChildInputs.addDropDownCommandInput(tableInput.id + '_select{}'.format(rowNumber), 'Select Point Number', adsk.core.DropDownStyles.LabeledIconDropDownStyle);
    dropdownItemsSelect = childTableSelectInput.listItems
    global numberViaPoints
    for j in range(0,numberViaPoints):
        dropdownItemsSelect.add('Select Number ' + str(j), False, '')
    
    row = tableInput.rowCount
    tableInput.addCommandInput(childTableNumberInput, row, 0)
    tableInput.addCommandInput(childTableLinkInput, row, 1)
    tableInput.addCommandInput(childTableSelectInput, row, 2)
    global rowNumber
    rowNumber = rowNumber + 1

## Event handler for the commandCreated event.
# 
# This event is called as soon as the button is created. It defines how the
# dialog window is displayed and what functions it has. 
class ButtonCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        cmd = args.command
        inputs = cmd.commandInputs
        commandId = "xyz"

        # Create tab 'add'
        tabCmdInput1 = inputs.addTabCommandInput(commandId + '_tab_1', 'Add');
        tab1ChildInputs = tabCmdInput1.children;

        # Create input to select myoMuscle number
        tab1ChildInputs.addIntegerSpinnerCommandInput(commandId + '_muscle', 'MyoMuscle Number', 0 , 500 , 1, 0)

        # Create table to input ViaPoint number, link name and which selection belongs to the provided info
        tableInput = tab1ChildInputs.addTableCommandInput(commandId + '_table', 'Via-Points', 3, '1:1:2')
        tableInput.tablePresentationStyle = 2
        global numberViaPoints
        tableInput.maximumVisibleRows = numberViaPoints + 1

        # create table inputs
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

        # add <numberViaPoints> rows to the table and <numberViaPoints> selection inputs
        for i in range(0,numberViaPoints):
            addRow(tableInput,i)

            # Create selection input to select position of viaPoint
            selectionInput = tab1ChildInputs.addSelectionInput(commandId + '_selection' + str(i), 'Select Point ' + str(i), 'Select a circle for the via-point.')
            selectionInput.setSelectionLimits(1, 1)
            selectionInput.addSelectionFilter("CircularEdges")

        # connect execute event handler
        onExecuteEvent = MyExecuteEventHandler()
        cmd.execute.add(onExecuteEvent)
        handlers.append(onExecuteEvent)

## Event handler for the execute event.
# 
# This event is called when the 'OK' button in the dialog window is clicked.
# It then starts to create constuction points with a decent naming, so that
# the SDFusion exporter can then parse this information into an SDF file.
class MyExecuteEventHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandEventArgs.cast(args)
        try:
            command = eventArgs.firingEvent.sender                
            inputs = command.commandInputs
            commandId = "xyz"
            # get the mcoMuscle number
            muscleInput = inputs.itemById(commandId + '_muscle')
            muscle = muscleInput.value
            tableInput = inputs.itemById(commandId + '_table')
            global numberViaPoints
            edges = []
            # first safe all the selections, because they get lost during the following operations
            # due to some Fusion internal thingy
            for i in range(0,numberViaPoints):
                edge = adsk.fusion.BRepEdge.cast(inputs.itemById(commandId + '_selection' + str(i)).selection(0).entity)
                edges.append(edge)
            # get all via point information
            for i in range(1,numberViaPoints):
                # get via point number
                numberInput = tableInput.getInputAtPosition(i, 0).id
                numberInput = inputs.itemById(numberInput)
                number = numberInput.value
                # get link name
                linkInput = tableInput.getInputAtPosition(i, 1)
                link = linkInput.selectedItem.name
                # get via point position
                selectionInput = tableInput.getInputAtPosition(i, 2)
                selection = selectionInput.selectedItem.name
                edge = edges[int(selection[-1:])-1]
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
                point.name = "VP_motor"+ str(muscle) + "_" + link + "_" + str(number)
          
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

## This function handles what happens as soon as the addin is started.
# 
# This function creates the button in Fusions UI. It connects the event
# that is called when the button is created.
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

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

## This function cleans up the document when the addin is stopped.
#
# To clean up the button in Fusions UI is removed.
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
