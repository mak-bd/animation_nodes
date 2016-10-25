import bpy
from bpy.props import *
from ... events import propertyChanged
from ... data_structures import MeshData
from ... base_types.node import AnimationNode

class MeshDataFromObjectNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_MeshDataFromObjectNode"
    bl_label = "Mesh Data from Object"
    bl_width_default = 160

    loadEdges = BoolProperty(name = "Load Edges", default = False,
        update = propertyChanged)
    loadPolygons = BoolProperty(name = "Load Polygons", default = False,
        update = propertyChanged)
    useModifiers = BoolProperty(name = "Use Modifiers", default = False,
        update = propertyChanged)
    useWorldSpace = BoolProperty(name = "Use World Space", default = False,
        update = propertyChanged)

    def create(self):
        self.newInput("Object", "Object", "object", defaultDrawType = "PROPERTY_ONLY")
        self.newInput("Scene", "Scene", "scene", hide = True)
        self.newOutput("Mesh Data", "Mesh Data", "meshData")

    def draw(self, layout):
        col = layout.column()
        subcol = col.row(align = True)
        subcol.prop(self, "loadEdges", text = "Edges", icon = "EDGESEL")
        subcol.prop(self, "loadPolygons", text = "Faces", icon ="FACESEL")
        subcol = col.column(align = True)
        subcol.prop(self, "useModifiers", icon = "MODIFIER")
        subcol.prop(self, "useWorldSpace", icon = "WORLD")

    def execute(self, object, scene):
        return self.meshDataFromObject(object, scene)

    def meshDataFromObject(self, object, scene):
        if getattr(object, "type", "") != "MESH":
            return MeshData()

        temporaryMesh = self.useModifiers and scene is not None
        if temporaryMesh: mesh = object.an.createModifiedMesh(scene)
        else: mesh = object.data

        vertices = mesh.an.getVertices()
        if self.useWorldSpace:
            vertices.transform(object.matrix_world)

        if self.loadEdges: edges = mesh.an.getEdgeIndices()
        else: edges = None
        if self.loadPolygons: polygons = mesh.an.getPolygonIndices()
        else: polygons = None

        if temporaryMesh:
            bpy.data.meshes.remove(mesh)

        return MeshData(vertices, edges, polygons)
