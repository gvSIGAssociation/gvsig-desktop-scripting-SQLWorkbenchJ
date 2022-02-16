# encoding: utf-8

import gvsig

from gvsig import getResource

from java.io import File
from org.gvsig.andami import PluginsLocator
from org.gvsig.app import ApplicationLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.swing.api import ToolsSwingLocator

from addons.SQLWorkbenchJ.sqlworkbenchj import SQLWorkbenchJ

class SQLWorkbenchJExtension(ScriptingExtension):
  def __init__(self):
    pass

  def canQueryByAction(self):
    return True

  def isEnabled(self,action):
    return True

  def isVisible(self,action):
    return True
    
  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "tool-sqlworkbenchj":
      SQLWorkbenchJ().showForm()

def selfRegister():
  application = ApplicationLocator.getManager()

  #
  # Registramos las traducciones
  i18n = ToolsLocator.getI18nManager()
  i18n.addResourceFamily("text",File(getResource(__file__,"i18n")))

  #
  # Registramos los iconos en el tema de iconos
  icon = File(getResource(__file__,"images","sqlworkbenchj.png")).toURI().toURL()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  iconTheme.registerDefault("scripting.SQLWorkbenchJExtension", "action", "tool-sqlworkbenchj", None, icon)

  #
  # Creamos la accion 
  extension = SQLWorkbenchJExtension()
  actionManager = PluginsLocator.getActionInfoManager()
  action = actionManager.createAction(
    extension, 
    "tool-sqlworkbenchj", # Action name
    u"SQLWorkbenchJ", # Text
    "tool-sqlworkbenchj", # Action command
    "tool-sqlworkbenchj", # Icon name
    None, # Accelerator
    650700601, # Position 
    u"SQLWorkbenchJ" # Tooltip
  )
  action = actionManager.registerAction(action)
  application.addMenu(action, u"tools/SQLWorkbenchJ")
      
def main(*args):
   selfRegister()
