from inc_noesis import *


ANIM_EVAL_FRAMERATE = 20.0


def registerNoesisTypes():
    handle = noesis.register( \
        "ExMachina (2004) model with animations", ".gam")
        
    noesis.setHandlerTypeCheck(handle, exmModelCheckType)
    noesis.setHandlerLoadModel(handle, exmModelLoadModel)
        
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
    
class Vector4B:    
    def __init__(self, reader): 
        self.reader = reader
        self.r = 0
        self.g = 0
        self.b = 0
        self.a = 0
        
    def read(self):
        self.r, self.g, self.b, self.a = noeUnpack("bbbb", self.reader.readBytes(4)) 
        
    def getStorage(self):
        return (self.r, self.g, self.b, self.a) 
        
    
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
    
    
class Matrix4x4:
    def __init__(self, reader): 
        self.reader = reader
        self.x = Vector4F(self.reader)
        self.y = Vector4F(self.reader)
        self.z = Vector4F(self.reader)    
        self.pos = Vector4F(self.reader)  
        
    def read(self):
        self.x.read()        
        self.y.read()        
        self.z.read()        
        self.pos.read()   

    def getStorage(self):
        return (self.x.getStorage(), self.y.getStorage(), self.z.getStorage(), self.pos.getStorage())         
    
 
class ExMVertex:
    def __init__(self, reader, type):
        self.reader = reader
        self.type = type
        self.pos = Vector3F(self.reader)
        self.posXYZW = Vector4F(self.reader)        
        self.normal = Vector3F(self.reader)
        self.color = Vector4B(self.reader)  
        self.tangent = Vector4F(self.reader) 
        self.uvw = Vector3F(self.reader)        
        self.uv = Vector2F(self.reader)
        self.uv1 = Vector2F(self.reader)
        self.uv2 = Vector2F(self.reader)
     
    def read(self):
        if self.type == 0:
            self.pos.read()        
        if type == 1:
            self.pos.read()
            self.uv.read()        
        if self.type == 2:
            self.pos.read()
            self.color.read()       
        if self.type == 3:
            self.posXYZW.read()
            self.color.read()
            self.uv.read()       
        if self.type == 4:
            self.posXYZW.read()
            self.normal.read()
            self.uv.read()      
        if self.type == 5:
            self.pos.read()
            self.normal.read()
            self.color.read()       
        if self.type == 6:
            self.pos.read()
            self.color.read()
            self.uv.read()          
        if self.type == 7:
            self.pos.read()
            self.normal.read()
            self.uv.read()         
        if self.type == 8:
            self.pos.read()
            self.normal.read()            
            self.color.read()
            self.uv.read()         
        if self.type == 9:
            self.pos.read()
            self.normal.read()            
            self.color.read()
            self.uv.read()          
            self.uv1.read()          
        if self.type == 10:
            self.pos.read()
            self.normal.read()            
            self.uv.read()          
            self.uv1.read()          
        if self.type == 11:
            self.pos.read()
            self.normal.read()            
            self.uv.read()         
            self.uv1.read()         
            self.uv2.read()         
        if self.type == 12:
            self.pos.read()          
            self.color.read()
            self.uvw.read()         
        if self.type == 13:
            self.pos.read()
            self.normal.read()            
            self.color.read()
            self.uvw.read()          
            self.uv.read()          
        if self.type == 14:
            self.pos.read()
            self.normal.read()            
            self.color.read()
            self.uv.read()          
            self.uv1.read()          
        if self.type == 15:
            self.pos.read()
            self.normal.read()            
            self.uv.read()  
            self.tangent.read()            
        if self.type == 16:
            self.pos.read()
            self.normal.read()
            self.color.read()
            self.uv.read()
            self.tangent.read()

        
class ExMFace:
    def __init__(self, reader): 
        self.reader = reader
        self.indexes = Vector3UI16(self.reader)
        
    def read(self):
        self.indexes.read()
    
    
class ExMVertexWeight:
    def __init__(self, reader): 
        self.reader = reader
        self.index = 0
        self.weight = 0
        
    def read(self):    
        self.index = self.reader.readUShort() 
        self.weight = self.reader.readFloat()   
    
    
class ExMVertexData:
    def __init__(self, reader): 
        self.reader = reader
        self.weights = []
        self.offsets = []
        self.normals = []
        self.vertNum = 0
        
    def read(self):  
        self.vertNum = self.reader.readUShort() 
        for k in range(self.vertNum):
            weight = ExMVertexWeight(self.reader)
            weight.read() 
            self.weights.append(weight)
            
            self.reader.seek(24, NOESEEK_REL)
        self.reader.seek((4 - self.vertNum) * 30, NOESEEK_REL)            
        
        
class ExMModelMesh:
    def __init__(self, reader):
        self.reader = reader
        self.boneIndex = -1
        self.matIndex = 0
        self.name = ""
        self.vertices = []        
        self.doubleVertices = []        
        self.faces = []
        self.vertexData = []       
          
    def readHeader(self):
        self.name = self.reader.readBytes(40).split(b"\x00")[0].decode("ascii")
        self.meshType = self.reader.readUInt()
        self.boneIndex = self.reader.readUInt()        
        self.matGroupIndex = self.reader.readUInt() 
        self.matIndex = self.reader.readUInt()
        self.size = self.reader.readUInt()
        self.vertexType = self.reader.readUInt()
        self.vertexNum = self.reader.readUInt()
        self.faceNum = self.reader.readUInt()      
        
    def readVertices(self):
        for i in range(self.vertexNum):   
            vertex = ExMVertex(self.reader, self.vertexType)
            vertex.read()
            self.vertices.append(vertex)
            
        if self.meshType == 1:    
            for i in range(self.vertexNum):   
                vertex = ExMVertex(self.reader, self.vertexType)
                vertex.read()
                self.doubleVertices.append(vertex)   
        
    def readFaces(self):
        for i in range(self.faceNum):  
            face = ExMFace(self.reader)
            face.read()
            self.faces.append(face)   
            
    def readVertexdata(self):
        for i in range(self.vertexNum):
            vxData = ExMVertexData(self.reader)
            vxData.read()
            self.vertexData.append(vxData)               
        
    def read(self):
        self.readHeader()      
        self.readVertices()
        
        if self.meshType == 2:
            self.readVertexdata()
            
        self.readFaces()                    
  
  
class ExMModelBone:
    def __init__(self, reader): 
        self.reader = reader
        self.parentIndex = 0
        self.pos = Vector3F(self.reader)
        self.rot = Vector4F(self.reader)
        self.matrix = Matrix4x4(self.reader)
        self.transMatrix = None
        self.name = ""
        
    def read(self):
        self.name = self.reader.readBytes(40).split(b"\x00")[0].decode("ascii")                   
        self.parentIndex = self.reader.readInt()
        self.pos.read()
        self.rot.read() 
        self.matrix.read()       
        
    def getTransMat(self):
        rotQuat = NoeQuat(self.rot.getStorage())
        transMatrix = rotQuat.toMat43().inverse()
        transMatrix[3] = self.pos.getStorage()

        mat = NoeMat44()
        mat[0] = NoeVec4(self.matrix.getStorage()[0])
        mat[1] = NoeVec4(self.matrix.getStorage()[1])
        mat[2] = NoeVec4(self.matrix.getStorage()[2])
        mat[3] = self.matrix.getStorage()[3]

        return transMatrix   
    
    
class ExMAnimationKey:    
    def __init__(self, reader):  
        self.reader = reader    
        self.pos = Vector3F(self.reader)
        self.orientation = Vector4F(self.reader)  
        self.index = 0
        
    def read(self):
        self.index = self.reader.readUShort()      
        self.pos.read()
        self.orientation.read() 
 
    def __repr__(self):
        return repr((self.pos.getStorage(), self.orientation.getStorage()))
        
        
class ExMAnimationFrame:
    def __init__(self, reader, num):
        self.reader = reader    
        self.num =  num
        self.keys = {}
        
    def read(self):
        for i in range(self.num):
            key = ExMAnimationKey(self.reader)
            key.read()
            self.keys[key.index] = key


class ExMAnimation:
    def __init__(self, reader):
        self.reader = reader
        self.frameNum = 0
        self.boneIndexes = []
        self.name = ""
        self.frames = []
        
    def readHeader(self):   
        self.name = self.reader.readBytes(25).split(b"\x00")[0].decode("ascii")
        self.frameNum = self.reader.readUShort() 
        self.fps = self.reader.readUShort() 
        self.next = self.reader.readUShort() 
        self.changeNum = self.reader.readUShort()  
        self.keyNum =  self.reader.readUShort()   
        self.action =  self.reader.readUInt()   
        
        for i in range(self.changeNum):
            self.current = self.reader.readUShort()    
            self.type =  self.reader.readUInt()   
            self.new =  self.reader.readUShort()             
        
    def readFrames(self):  
        for i in range(self.frameNum):
            frame = ExMAnimationFrame(self.reader, self.keyNum)
            frame.read()
            self.frames.append(frame)       
            
    def read(self):
        self.readHeader()
        self.readFrames()
        
        
class ExMTexture: 
    def __init__(self, reader):
        self.reader = reader    
        self.name = ""
        self.uvIndex = 0
        self.type = 0
        
    def read(self):   
        self.name = self.reader.readBytes(40).split(b"\x00")[0].decode("ascii")        
        self.uvIndex = self.reader.readUInt() 
        self.type = self.reader.readUInt() 
     
     
class ExMMaterialColor():
    def __init__(self, reader):
        self.reader = reader       
        self.r = 0 
        self.g = 0 
        self.b = 0 
        self.a = 0
        
    def read(self):
        self.r, self.g, self.b, self.a = noeUnpack("ffff", self.reader.readBytes(16))   
        
    def getStorage(self):
        return (self.r, self.g, self.b, self.a)        
     
     
class ExMMaterial:
    def __init__(self, reader):
        self.reader = reader
        self.name = ""
        self.diffuse = ExMMaterialColor(self.reader)
        self.ambient = ExMMaterialColor(self.reader)
        self.specular = ExMMaterialColor(self.reader)
        self.emmisive = ExMMaterialColor(self.reader)
        self.power = 0
        
        self.textures = []
        
    def read(self):
        self.diffuse.read()
        self.ambient.read()
        self.specular.read()
        self.emmisive.read()
        self.power = self.reader.readFloat()
        
        texureNum = self.reader.readUInt()        
        self.name = self.reader.readBytes(100).split(b"\x00")[0].decode("ascii")

        for i in range(texureNum):
            texture = ExMTexture(self.reader)
            texture.read()
            self.textures.append(texture) 
        
        
class ExMModel:
    def __init__(self, reader): 
        self.reader = reader
        self.boneNum = 0
        self.bonesOffset = 0
        self.bones = []
        self.animatedMeshes = []
        self.skinnedMeshes = []
        self.staticMeshes = []
        self.animations = []
        self.materials = []
        
    def readHeader(self):
        self.reader.seek(8, NOESEEK_ABS)
        sectionsNum = self.reader.readUInt() 
        
        while sectionsNum:
            type = self.reader.readUInt()
            size = self.reader.readUInt()
            if type == 2:
               self.bonesOffset = self.reader.readUInt() 
            elif type == 4:
               self.meshesOffset = self.reader.readUInt() 
            elif type == 8:
               self.animationsOffset = self.reader.readUInt()                
            elif type == 15:
               self.matsOffset = self.reader.readUInt() 
            else:   
               self.reader.seek(4, NOESEEK_REL)
            self.reader.seek(4, NOESEEK_REL)
                
            sectionsNum -= 1
           
        self.animatedMeshNum = self.reader.readUShort()
        self.skinnedMeshNum = self.reader.readUShort()
        self.staticMeshNum = self.reader.readUShort()
        
        self.animationsNum = self.reader.readUShort()
        self.matNum = self.reader.readUShort()
        self.boneNum = self.reader.readUShort()
        self.reader.seek(4, NOESEEK_REL)
        
    def readMeshes(self):
        self.reader.seek(self.meshesOffset, NOESEEK_ABS)    
      
        for i in range(self.animatedMeshNum):    
            mesh = ExMModelMesh(self.reader)
            mesh.read() 
            mesh.name = "Animated: {name}".format(name=mesh.name)            
            self.animatedMeshes.append(mesh)
            
        for i in range(self.skinnedMeshNum):    
            mesh = ExMModelMesh(self.reader)
            mesh.read()
            mesh.name = "Skinned: {name}".format(name=mesh.name)             
            self.skinnedMeshes.append(mesh)  
            
        for i in range(self.staticMeshNum):    
            mesh = ExMModelMesh(self.reader)
            mesh.read()
            mesh.name = "Static: {name}".format(name=mesh.name)             
            self.staticMeshes.append(mesh)              

    def readBones(self):
        self.reader.seek(self.bonesOffset, NOESEEK_ABS)        
        for i in range(self.boneNum):
            bone = ExMModelBone(self.reader)
            bone.read()
            self.bones.append(bone)           
            
    def readAnimations(self):   
        self.reader.seek(self.animationsOffset, NOESEEK_ABS)    
        for i in range(self.animationsNum):
            animation = ExMAnimation(self.reader)
            animation.read()
            self.animations.append(animation)   
         
    def readMaterials(self):
        self.reader.seek(self.matsOffset, NOESEEK_ABS)   
        num = self.reader.readUInt() 
        
        for i in range(num*self.matNum):
            material = ExMMaterial(self.reader)
            material.read()
            materials = [mat.name for mat in self.materials]
            if material.name in materials:
                material.name +=  str(i)
            self.materials.append(material)         
 
    def read(self):
        self.readHeader()       
        self.readBones()
        self.readMeshes()
        
        self.readAnimations()
        self.readMaterials()        
        
        
def exmModelCheckType(data):

    return 1     
    

def exmModelLoadModel(data, mdlList):
    noesis.logPopup()
    model = ExMModel(NoeBitStream(data))
    model.read()
    
    ctx = rapi.rpgCreateContext()
    
    #transMatrix = NoeMat43( ((-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)) ) 
    #rapi.rpgSetTransform(transMatrix)
    
    # load textures
    materials = []
    textures = [] 
        
    for mat in model.materials:          
        material = NoeMaterial(mat.name, "")
        material.setDiffuseColor(NoeVec4(mat.diffuse.getStorage()))
        material.setAmbientColor(NoeVec4(mat.ambient.getStorage()))
        material.setSpecularColor(NoeVec4(mat.specular.getStorage()))
        if "specular" in material.name:
            material.setDefaultBlend(0)
        materials.append(material)
        
        for tex in mat.textures:
            texture = rapi.loadExternalTex(tex.name)

            if texture is None:
                texture = NoeTexture(tex.name, 0, 0, bytearray())
                  
            if tex.type == 0:
                material.setTexture(tex.name)
            elif tex.type == 1:
                material.setNormalTexture(tex.name)
            elif tex.type == 3:
                material.setEnvTexture(tex.name)                
            elif tex.type == 4:
                material.setBumpTexture(tex.name)
            textures.append(texture)          
 
    for msh in model.staticMeshes: 
        rapi.rpgSetMaterial(model.materials[msh.matIndex].name)        
        rapi.rpgSetName(msh.name)    
        for i in range(msh.faceNum):
            face = msh.faces[i]
            rapi.immBegin(noesis.RPGEO_TRIANGLE)
            for k in range(3):              
                vIndex = face.indexes.getStorage()[k] 
                rapi.immUV2(msh.vertices[vIndex].uv.getStorage())  
                rapi.immNormal3(msh.vertices[vIndex].normal.getStorage())  
                
                if msh.vertexData:
                    indexes = [vertexWeight.index for vertexWeight in msh.vertexData[vIndex].weights]
                    weights = [vertexWeight.weight for vertexWeight in msh.vertexData[vIndex].weights]

                    rapi.immBoneIndex(indexes)
                    rapi.immBoneWeight(weights)
                else:    
                    rapi.immBoneIndex([msh.boneIndex])
                    rapi.immBoneWeight([1])                     
                rapi.immVertex3(msh.vertices[vIndex].pos.getStorage())      
        
            rapi.immEnd() 
 
    for msh in model.animatedMeshes: 
        rapi.rpgSetMaterial(model.materials[msh.matIndex].name)        
        rapi.rpgSetName(msh.name)    
        for i in range(msh.faceNum):
            face = msh.faces[i]
            rapi.immBegin(noesis.RPGEO_TRIANGLE)
            for k in range(3):              
                vIndex = face.indexes.getStorage()[k] 
                rapi.immUV2(msh.vertices[vIndex].uv.getStorage())  
                rapi.immNormal3(msh.vertices[vIndex].normal.getStorage())  
                
                if msh.vertexData:
                    indexes = [vertexWeight.index for vertexWeight in msh.vertexData[vIndex].weights]
                    weights = [vertexWeight.weight for vertexWeight in msh.vertexData[vIndex].weights]

                    rapi.immBoneIndex(indexes)
                    rapi.immBoneWeight(weights)
                else:    
                    rapi.immBoneIndex([msh.boneIndex])
                    rapi.immBoneWeight([1])                  
                rapi.immVertex3(msh.vertices[vIndex].pos.getStorage())      
        
            rapi.immEnd()
 
    for msh in model.skinnedMeshes: 
        rapi.rpgSetMaterial(model.materials[msh.matIndex].name)        
        rapi.rpgSetName(msh.name)    
        for i in range(msh.faceNum):
            face = msh.faces[i]
            rapi.immBegin(noesis.RPGEO_TRIANGLE)
            for k in range(3):              
                vIndex = face.indexes.getStorage()[k] 
                rapi.immUV2(msh.vertices[vIndex].uv.getStorage())  
                rapi.immNormal3(msh.vertices[vIndex].normal.getStorage())  
                
                if msh.vertexData:
                    indexes = [vertexWeight.index for vertexWeight in msh.vertexData[vIndex].weights]
                    weights = [vertexWeight.weight for vertexWeight in msh.vertexData[vIndex].weights]

                    rapi.immBoneIndex(indexes)
                    rapi.immBoneWeight(weights)
                else:    
                    rapi.immBoneIndex([msh.boneIndex])
                    rapi.immBoneWeight([1])                     
                rapi.immVertex3(msh.vertices[vIndex].pos.getStorage())      
            rapi.immEnd()     
    
    # show skeleton
    bones = []
    for index, bone in enumerate(model.bones):
        boneName = bone.name
        
        if bone.parentIndex >= 0:
            parentMat = model.bones[bone.parentIndex].transMatrix
            boneMat = bone.getTransMat() * parentMat
            bone.transMatrix = boneMat
            
            parentName = model.bones[bone.parentIndex].name
            bones.append(NoeBone(index, boneName, boneMat, parentName, bone.parentIndex))             
        else:         
            bone.transMatrix = bone.getTransMat()
            boneMat = bone.transMatrix
      
            bones.append(NoeBone(index, boneName, boneMat, "", -1))

    anims = []
    
    if model.animations:    
        frameToTime = 1.0 / ANIM_EVAL_FRAMERATE

        for animation in model.animations: 
            kfBones = []     
            for bone in bones:                              
                boneFramePoses = [frame.keys[bone.index] for frame in animation.frames]
                
                keyFramedBone = NoeKeyFramedBone(bone.index)
                rkeys = []
                pkeys = []
                for index, bfp in enumerate(boneFramePoses):  
                    mat = NoeQuat(bfp.orientation.getStorage()).toMat43().inverse()
                    rkeys.append(NoeKeyFramedValue(index * frameToTime, mat.toQuat() ))           
                    pkeys.append(NoeKeyFramedValue(index * frameToTime, NoeVec3(bfp.pos.getStorage())))
    
                keyFramedBone.setRotation(rkeys)          
                keyFramedBone.setTranslation(pkeys)

                kfBones.append(keyFramedBone)   
                
            anims.append(NoeKeyFramedAnim(animation.name, bones, kfBones) )              
 
    mdl = rapi.rpgConstructModelSlim() 
    mdl.setAnims(anims)  
    mdl.setBones(bones)
    
    # set materials
    if materials:    
        mdl.setModelMaterials(NoeModelMaterials(textures, materials))    
    mdlList.append(mdl)
    
    #rapi.setPreviewOption("setAngOfs", "0 0 0")
    rapi.setPreviewOption("setAnimSpeed", "20.0")
	
    return 1        