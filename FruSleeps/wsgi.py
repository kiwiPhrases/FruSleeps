#from FruSleeps import create_app



import sys
#sys.path.extend([WORKING_DIR_AND_PYTHON_PATHS])
from flask.cli import ScriptInfo
from FruSleeps import create_app
import FruSleeps as app
locals().update(ScriptInfo(create_app=create_app).load_app().make_shell_context())
print("Python %s on %s\nApp: %s\nInstance: %s" % (sys.version, sys.platform, app.import_name, app.instance_path))