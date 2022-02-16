# encoding: utf-8

import gvsig
from gvsig import getResource
from gvsig.libs.formpanel import FormPanel

import thread
import os.path
import subprocess
import shutil

from java.lang import System
from java.io import File
from java.io import FileInputStream
from java.io import FileOutputStream
from java.util import Properties

from org.apache.commons.io import FileUtils
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.scripting.swing.api import ScriptingSwingLocator, JScriptingComposer
from org.gvsig.tools import ToolsLocator
from org.gvsig.fmap.dal.swing import DALSwingLocator
from  org.gvsig.tools.swing.api import ToolsSwingLocator
from  org.gvsig.tools.swing.api.windowmanager import WindowManager_v2

import javax.swing.ImageIcon
import javax.imageio.ImageIO
from javax.swing import AbstractAction, Action
from org.gvsig.scripting import ScriptingLocator


class SQLWorkbenchJ(FormPanel):
    def __init__(self):
        FormPanel.__init__(self,gvsig.getResource(__file__,"sqlworkbenchj.xml"))
        self.pickerConn = DALSwingLocator.getDataSwingManager().createJDBCConnectionPickerController(self.cboConexion, self.btnConexion)
        
    def actionPerformed(self, *args):
        if self.dialog.getAction()==WindowManager_v2.BUTTON_OK:
            conn = self.pickerConn.get()
            url = conn.getUrl()
            name = self.cboConexion.getSelectedItem().toString()
            provider = conn.getProviderName()
            user = conn.getUser()
            password = conn.getPassword()
            # jdbc:h2:tcp://127.0.1.1:9123//home/jjdelcerro/datos/devel/org.gvsig.desktop/org.gvsig.desktop.plugin/org.gvsig.h2spatial/org.gvsig.h2spatial.h2gis132/org.gvsig.h2spatial.h2gis132.provider/target/test-dbs/test_ars1-1642756338518-001;MODE=PostgreSQL;SCHEMA=PUBLIC;ALLOW_LITERALS=ALL
            # jdbc:h2:file:/home/jjdelcerro/dbs/srv1;MODE=PostgreSQL;SCHEMA=PUBLIC;ALLOW_LITERALS=ALL
            if self.chkShareConnection.isSelected():
              if url.startswith("jdbc:h2:file:"):
                url = url.replace("jdbc:h2:file:","jdbc:h2:tcp://127.0.0.1:9123/")
              elif url.startswith("jdbc:h2:split:"):
                url = url.replace("jdbc:h2:split:","jdbc:h2:tcp://127.0.0.1:9123/split:")
            launch(url, name, provider, user, password)
            
    def showForm(self):
        self.dialog = ToolsSwingLocator.getWindowManager().createDialog(self.asJComponent(), "Select database", None, WindowManager_v2.BUTTONS_OK_CANCEL)
        self.dialog.addActionListener(self.actionPerformed)
        self.dialog.show(WindowManager_v2.MODE.WINDOW)
  
def getDataFolder():
  return ScriptingLocator.getManager().getDataFolder("sqlworkbenchj").getAbsolutePath()

def launch0(url, name, provider, user, password):
  if password == None:
    password = ""
  pluginsManager = PluginsLocator.getManager()
  appfolder = pluginsManager.getApplicationFolder().getAbsolutePath().replace("\\","/")
  
  java = os.path.join( System.getProperties().getProperty("java.home"), "bin", "java")

  apphome = getResource(__file__, "app", "Workbench-Build127").replace("\\","/")
  configdir = getDataFolder()

  CP = apphome+"/sqlworkbench.jar"
  try:
    os.unlink(configdir+"/Default.wksp")
  except:
    pass
  wbdrivers = getResource(__file__, "app", "templates","WbDrivers.xml").replace("\\","/")
  f = open(wbdrivers,"r")
  s = f.read()
  s = s.replace("${GVSIG_INSTALL_DIR}", appfolder)
  target = open(configdir+"/WbDrivers.xml", "w")
  target.write(s)
  target.close()
  

  profiles = getResource(__file__, "app", "templates", provider,"wb-profiles.properties").replace("\\","/")
  f = open(profiles,"r")
  s = f.read()
  s = s.replace("${DATABASE_NAME}", name)
  s = s.replace("${DATABASE_URL}", url)
  s = s.replace("${DATABASE_USER}", user)
  s = s.replace("${DATABASE_PASSWORD}", password)
  f.close()
  target = open(configdir+"/wb-profiles.properties", "w")
  target.write(s)
  target.close()
  
  
  cmd = [
    java,
    "-jar",CP,
    "-configDir="+configdir,
    "-profile="+name
  ]
  print cmd
  
  subprocess.call(cmd)


def launch(url, name, provider, user, password):
  thread.start_new_thread(launch0,(url, name, provider, user, password))
  
def main(*args):
  #launch()

  SQLWorkbenchJ().showForm()
    
