#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        cmdDefs = ui.commandDefinitions

        # Create a button command definition.
        buttonExample = cmdDefs.addButtonDefinition('VPUI_CmdID2', 'ViaPointUI','UI to add ViaPoints')

        # Connect to the command created event.
        #buttonExampleCreated = adsk.core.CommandCreatedEventHandler()
        #buttonExample.commandCreated.add(buttonExampleCreated)
        #handlers.append(buttonExampleCreated)

        # Get the ADD-INS panel in the model workspace. 
        addInsPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')

        # Add the button to the bottom.
        buttonControl = addInsPanel.controls.addCommand(buttonExample)

        # Make the button available in the panel.
        buttonControl.isPromotedByDefault = True
        buttonControl.isPromoted = True
        ui.messageBox('Hello addin')

        # Get the UserInterface object and the CommandDefinitions collection.
        ui = app.userInterface
        cmdDefs = ui.commandDefinitions

        # Delete the button definition.
        buttonExample = ui.commandDefinitions.itemById('MyButtonDefId')
        if buttonExample:
            buttonExample.deleteMe()
            
        # Get panel the control is in.
        addInsPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')

        # Get and delete the button control.
        buttonControl = addInsPanel.controls.itemById('MyButtonDefId')
        if buttonControl:
            buttonControl.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))