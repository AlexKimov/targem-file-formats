from inc_noesis import *

ANIM_EVAL_FRAMERATE = 20.0

def registerNoesisTypes():
    handle = noesis.register( \
        "BattleMages (2004) model with animations", ".sam")
        
    noesis.setHandlerTypeCheck(handle, bmsModelCheckType)
    noesis.setHandlerLoadModel(handle, bmsModelLoadModel)
        
    return 1 
    
    
class Vector4F:
    def __init__(self, reader): 
        self.reader = reader
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0
        
    def read(self):
        self.x, self.y, self.z, self.w = noeUnpack("ffff", self.reader.readBytes(16)) 
        
    def getStorage(self):
        return (self.x, self.y, self.z, self.w)    
    
    
class Vector2F:
    def __init__(self, reader): 
        self.reader = reader
        self.x = 0
        self.y = 0
        
    def read(self):
        self.x, self.y = noeUnpack("ff", self.reader.readBytes(8))
 
    def getStorage(self):
        return (self.x, self.y)  
        
        
class Vector3UI16:
    def __init__(self, reader): 
        self.reader = reader
        self.x = 0
        self.y = 0
        self.z = 0
        
    def read(self):
        self.x, self.y, self.z = noeUnpack("HHH", self.reader.readBytes(6))
        
    def getStorage(self):
        return (self.x, self.y, self.z)
        
        
class Vector3F:
    def __init__(self, reader): 
        self.reader = reader
        self.x = 0
        self.y = 0
        self.z = 0
        
    def read(self):
        self.x, self.y, self.z = noeUnpack("fff", self.reader.readBytes(12))
        
    def getStorage(self):
        return (self.x, self.y, self.z) 
    
 
class BMsVertex:
    def __init__(self, reader, type):
        self.reader = reader
        self.pos = Vector3F(self.reader)
        self.normal = Vector3F(self.reader) 
        self.uv = Vector2F(self.reader)
        self.weights = []
        self.type = type
        
    def readWeights(self):
        num = self.reader.readUShort()    
        for i in range(num):
            vertexWeight = BMsVertexWeight(self.reader)
            vertexWeight.read()
            self.weights.append(vertexWeight)  
     
    def read(self):
        self.pos.read()
        self.normal.read()
        self.uv.read()
        if self.type == 2:
            self.readWeights()
        
        
class BMsFace:
    def __init__(self, reader): 
        self.reader = reader
        self.indexes = Vector3UI16(self.reader)
        
    def read(self):
        self.indexes.read()
    
    
class BMsVertexWeight:
    def __init__(self, reader): 
        self.reader = reader
        self.index = 0
        self.weight = 0
        
    def read(self):    
        self.index = self.reader.readUShort() 
        self.weight = self.reader.readFloat()   
        
        
class BMsModelMesh:
    def __init__(self, reader):
        self.reader = reader
        self.name = ""
        self.vertexes = []        
        self.faces = []              
          
    def readHeader(self):
        self.name = self.reader.readBytes(40).split(b"\x00")[0].decode("ascii")
        self.vertexNum = self.reader.readUShort()
        self.faceNum = self.reader.readUShort()
        self.un1 = self.reader.readUShort()
        self.un2 = self.reader.readUShort()
    
    def readVertexes(self):
        for i in range(self.vertexNum):   
            vertex = BMsVertex(self.reader, self.un2)
            vertex.read()
            self.vertexes.append(vertex)
            
    def readFaces(self):
        for i in range(self.faceNum):  
            face = BMsFace(self.reader)
            face.read()
            self.faces.append(face)            
     
    def read(self):
        self.readHeader()      
        self.readVertexes()        
        self.readFaces()         
        
  
class BMsModelBone:
    def __init__(self, reader): 
        self.reader = reader
        self.pos = Vector3F(self.reader)
        self.rot = Vector4F(self.reader)
        self.parentIndex = 0
        self.transMatrix = NoeMat43()
        self.name = ""
        
    def read(self):
        self.name = self.reader.readBytes(40).split(b"\x00")[0].decode("ascii")  
        self.index = self.reader.readUShort()        
        self.parentIndex = self.reader.readShort()

        self.pos.read()
        self.rot.read()            
        
    def getTransMat(self):
        rotQuat = NoeQuat(self.rot.getStorage())
        transMatrix = rotQuat.toMat43()
        transMatrix[3] = self.pos.getStorage()

        return transMatrix                              
    
    
class BMsAnimationBonePose:    
    def __init__(self, reader):  
        self.reader = reader    
        self.pos = Vector3F(self.reader)
        self.orientation = Vector4F(self.reader)  
        self.index = 0
        
    def read(self):
        self.pos.read()
        self.orientation.read() 
        self.index = self.reader.readUShort()  
        
        
class BMsAnimationFrame:
    def __init__(self, reader, num):
        self.reader = reader    
        self.num =  num
        self.bposes = []
        
    def read(self):
        for i in range(self.num):
            bpos = BMsAnimationBonePose(self.reader)
            bpos.read()
            self.bposes.append(bpos)        
         
    
class BMsAnimation:
    def __init__(self, reader, boneNum):
        self.reader = reader
        self.boneNum = boneNum
        self.frameNum = 0
        self.unk1 = 0
        self.unk2 = 0
        self.name = ""
        self.frames = []
        
    def readHeader(self):  
        self.frameNum = self.reader.readUShort() 
        self.size = self.reader.readUShort() 
        self.unk = self.reader.readUShort() 
        self.index = self.reader.readUShort() 
        self.name = self.reader.readBytes(27).split(b"\x00")[0].decode("ascii") 
        
        self.reader.seek(self.unk * 8, NOESEEK_REL)   
        
    def readFrames(self):  
        for i in range(self.frameNum):
            frame = BMsAnimationFrame(self.reader, self.boneNum)
            frame.read()
            self.frames.append(frame)            
            
    def read(self):
        self.readHeader()
        self.readFrames()
        
        
class BMsModel:
    def __init__(self, reader): 
        self.reader = reader
        self.boneNum = 0
        self.bonesOffset = 0
        self.bones = []
        self.meshes = []
        self.animations = []
        
    def readHeader(self):
        self.reader.seek(36, NOESEEK_ABS)
        self.bonesOffset = self.reader.readUInt() 
        self.reader.seek(108, NOESEEK_ABS)
        self.boneNum = self.reader.readUShort() 
        self.meshNum = self.boneNum - self.reader.readUShort() 
        self.reader.seek(118, NOESEEK_ABS)
        self.animationNum = self.reader.readUShort() 
        self.reader.seek(120, NOESEEK_ABS)
        self.matName = self.reader.readBytes(40).split(b"\x00")[0].decode("ascii") 
        
    def readMeshes(self):
        for i in range(self.meshNum):    
            mesh = BMsModelMesh(self.reader)
            mesh.read()
            self.meshes.append(mesh)
            
    def readBones(self):
        self.reader.seek(self.bonesOffset, NOESEEK_ABS)    
        for i in range(self.boneNum):
            bone = BMsModelBone(self.reader)
            bone.read()
            self.bones.append(bone)
            
    def readAnimations(self):
        self.bNum = self.reader.readUShort() 
        for i in range(self.animationNum):
            animation = BMsAnimation(self.reader, self.bNum)
            animation.read()
            self.animations.append(animation)        
        
    def read(self):
        self.readHeader()
        self.readBones()
        self.readMeshes()
        self.readAnimations()
     
        
def bmsModelCheckType(data):

    return 1     
    

def bmsModelLoadModel(data, mdlList):
    #noesis.logPopup()
    model = BMsModel(NoeBitStream(data))
    model.read()
    
    ctx = rapi.rpgCreateContext()

    for msh in model.meshes:  
        for i in range(msh.faceNum):
            rapi.rpgSetName(msh.name)
            rapi.rpgSetMaterial(model.matName)
            face = msh.faces[i]
            rapi.immBegin(noesis.RPGEO_TRIANGLE)
            for k in range(3):              
                vIndex = face.indexes.getStorage()[k] 
                rapi.immUV2(msh.vertexes[vIndex].uv.getStorage())  
                rapi.immNormal3(msh.vertexes[vIndex].normal.getStorage())  
                
                if msh.vertexes[vIndex].weights:
                    indexes = [vertexWeight.index for vertexWeight in msh.vertexes[vIndex].weights]
                    weights = [vertexWeight.weight for vertexWeight in msh.vertexes[vIndex].weights]

                    rapi.immBoneIndex(indexes)
                    rapi.immBoneWeight(weights)
                    
                rapi.immVertex3(msh.vertexes[vIndex].pos.getStorage())      
        
            rapi.immEnd()     
    
    # show skeleton
    bones = []
    for bone in model.bones:
        boneName = bone.name
        
        if bone.parentIndex >= 0:
            parentMat = model.bones[bone.parentIndex].transMatrix
            boneMat = bone.getTransMat() * parentMat
            bone.transMatrix = boneMat
            
            parentName = model.bones[bone.parentIndex].name
            bones.append(NoeBone(bone.index, boneName, boneMat, parentName, bone.parentIndex))             
        else:         
            bone.transMatrix = bone.getTransMat()
            boneMat = bone.transMatrix
      
            bones.append(NoeBone(bone.index, boneName, boneMat, "", -1))

    kfBones = []
    anims = []
    frameToTime = 1.0 / ANIM_EVAL_FRAMERATE
    for animation in model.animations:        
        for bone in bones: 
            keyFramedBone = NoeKeyFramedBone(bone.index)
            rkeys = []
            pkeys = []   
                              
            boneFramePoses = [frame.bposes[bone.index] for frame in animation.frames]
            
            for index, bfp in enumerate(boneFramePoses):                           
                rkeys.append(NoeKeyFramedValue(index * frameToTime, NoeQuat(bfp.orientation.getStorage())))           
                pkeys.append(NoeKeyFramedValue(index * frameToTime, NoeVec3(bfp.pos.getStorage())))
            
            keyFramedBone.setRotation(rkeys)          
            keyFramedBone.setTranslation(pkeys)
    
            kfBones.append(keyFramedBone)   

        anims.append(NoeKeyFramedAnim(animation.name, bones, kfBones) )    
        break
           
    mdl = rapi.rpgConstructModelSlim() 
    mdl.setAnims(anims)  
    mdl.setBones(bones)
    mdlList.append(mdl)
    
    rapi.setPreviewOption("setAngOfs", "0 -90 0")
    rapi.setPreviewOption("setAnimSpeed", "30.0")
	
    return 1        