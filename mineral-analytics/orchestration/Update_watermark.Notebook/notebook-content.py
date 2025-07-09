# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "b1e1c8cd-a958-4f59-9822-1dc27ec46183",
# META       "default_lakehouse_name": "LH_Minerals",
# META       "default_lakehouse_workspace_id": "b0973323-41d3-4fc8-8a3b-326e68ad1340",
# META       "known_lakehouses": [
# META         {
# META           "id": "b1e1c8cd-a958-4f59-9822-1dc27ec46183"
# META         }
# META       ]
# META     }
# META   }
# META }

# PARAMETERS CELL ********************

lastModified = ""

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from notebookutils import mssparkutils
import json

payload = json.dumps({"lastModified": lastModified}, indent=2)

folder = "Files/watermarks"
file   = f"{folder}/Watermark.json"

mssparkutils.fs.mkdirs(folder)
mssparkutils.fs.put(file, payload, overwrite=True)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
