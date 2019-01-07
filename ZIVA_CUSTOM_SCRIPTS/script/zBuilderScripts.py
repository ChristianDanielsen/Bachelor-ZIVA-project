import zBuilder.builders.ziva as zva
# STORE ZIVA NODES
z = zva.Ziva()
z.retrieve_from_scene()

# DELETE ZIVA NODES 
import zBuilder.zMaya as mz
mz.clean_scene()

# BUILD AGAIN
z.build()

# WRITE ZIVA NODES TO DISC
z.write('S:/student/3DDA_17/users/Anders Lund Dick/Sem03/Rigging/1SemesterRig/data/test3.zBuilder')

# READ ZIVA NODES FROM FILE
import zBuilder.builders.ziva as zva
z = zva.Ziva()
# Use the same path here that you used above.
z.retrieve_from_file('S:/student/3DDA_17/users/Anders Lund Dick/Sem03/Rigging/1SemesterRig/data/test3.zBuilder')

# MIRROR ZIVA SETUP
import zBuilder.builders.ziva as zva
z = zva.Ziva()
z.retrieve_from_scene()
z.string_replace('^l_','r_')