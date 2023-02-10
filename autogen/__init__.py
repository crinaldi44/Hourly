import glob
import importlib
import os

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
models = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]
print(models)
for model in models:
    importlib.import_module("autogen.server.release.openapi_server.models." + model)