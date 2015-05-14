bl_info = {
	"name": "EasyAtlas",
	"description": "Easy texture atlas baking from scene",
	"author": "kode80",
	"version": (1, 0),
	"blender": (2, 65, 0),
	"location": "Properties > Render > EasyAtlas",
	"warning": "", # used for warning icon and text in addons panel
	"wiki_url": "http://kode80.com/",
	"category": "Render"
	}

import bpy
import bmesh
import math

#------------ OPERATOR ------------

class Bounds:
	minX = 0.0
	minY = 0.0
	maxX = 0.0
	maxY = 0.0

	def midX( self):
		return self.minX + (self.maxX - self.minX) * 0.5

	def midY( self):
		return self.minY + (self.maxY - self.minY) * 0.5

	def width( self):
		return self.maxX - self.minX

	def height( self):
		return self.maxY - self.minY

class EasyAtlas_Settings(bpy.types.PropertyGroup):
	width = bpy.props.IntProperty( name="Atlas Width", description="Atlas texture width in pixels", default=1024, min=64)
	height = bpy.props.IntProperty( name="Atlas Height", description="Atlas texture height in pixels", default=1024, min=64)

class EasyAtlas_CreateAtlas(bpy.types.Operator):
	"""Create atlas from scene"""
	bl_idname = "kode80.easyatlas_create_atlas"
	bl_label = "Create Atlas"
	bl_options = {'REGISTER', 'UNDO'}
	
	def CalcBoundsOfObject( self, obj):
		bounds = Bounds()

		mesh = obj.data
		uv_layer = mesh.uv_layers.active.data

		for poly in mesh.polygons:
			for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
				uv = uv_layer[loop_index].uv

				if uv.x < bounds.minX:
					bounds.minX = uv.x
				if uv.x > bounds.maxX:
					bounds.maxX = uv.x

				if uv.y < bounds.minY:
					bounds.minY = uv.y
				if uv.y > bounds.maxY:
					bounds.maxY = uv.y
				
		return bounds

	def execute(self, context):
		settings = bpy.context.scene.EasyAtlas_Settings
		
		atlasImage = None
		for image in bpy.data.images:
			if image.name == "EasyAtlas":
				atlasImage = image

		if atlasImage == None:
			atlasImage = bpy.data.images.new( "EasyAtlas", settings.width, settings.height, alpha=True)

		context.scene.render.use_bake_clear = True
		context.scene.render.bake_type = 'FULL'

		meshObjects = []
		for obj in context.scene.objects:
			if obj.type == "MESH":
				meshObjects.append( obj)

		gridSize = math.ceil( math.sqrt( len(meshObjects)))
		cellSize = 1.0 / gridSize
		end = 0.5 - (cellSize * 0.5)
		start = -end
		x = start
		y = start

		margin = context.scene.render.bake_margin
		cellMargin = margin * 2.0 / settings.width


		for obj in meshObjects:
			bpy.ops.object.mode_set(mode="OBJECT")
			bpy.ops.object.select_all(action="DESELECT")
			obj.select = True
			bpy.context.scene.objects.active = obj


			bounds = self.CalcBoundsOfObject( obj)
			offsetX = 0.5 - bounds.midX()
			offsetY = 0.5 - bounds.midY()


			oldLayer = obj.data.uv_textures.active
			uvLayer = obj.data.uv_textures.new( "EasyAtlas")
			obj.data.uv_textures.active = uvLayer

			for p in uvLayer.data:
				p.image = atlasImage

			bpy.ops.object.mode_set(mode="EDIT")
			bpy.ops.mesh.select_all(action='SELECT')
			bpy.ops.uv.select_all(action='SELECT')

			oldAreaType = context.area.type
			context.area.type = 'IMAGE_EDITOR'
			bpy.ops.transform.translate(value=( x + offsetX, y + offsetY, 0.0))
			bpy.ops.transform.resize(value=( cellSize - cellMargin, cellSize - cellMargin, 0.0))
			
			bpy.ops.object.bake_image()

			bpy.ops.object.mode_set(mode="OBJECT")
			obj.data.uv_textures.active = oldLayer
			context.area.type = oldAreaType

			x += cellSize
			if x > end:
				x = start
				y += cellSize

			context.scene.render.use_bake_clear = False

		return {'FINISHED'}

#------------ PANEL ------------

class EasyAtlasPanel(bpy.types.Panel):
	bl_label = "EasyAtlas"
	bl_idname = "kode80.easyatlas_panel"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"

	def draw(self, context):
		settings = bpy.context.scene.EasyAtlas_Settings
		layout = self.layout

		layout.prop( settings, "width")
		layout.prop( settings, "height")
		layout.operator( "kode80.easyatlas_create_atlas", "Create Atlas")


def register():
	bpy.utils.register_class(EasyAtlas_Settings)
	bpy.types.Scene.EasyAtlas_Settings = bpy.props.PointerProperty(type=EasyAtlas_Settings)

	bpy.utils.register_class(EasyAtlas_CreateAtlas)
	bpy.utils.register_class(EasyAtlasPanel)

def unregister():
	bpy.utils.unregister_class(EasyAtlasPanel)
	bpy.utils.unregister_class(EasyAtlas_CreateAtlas)

	bpy.utils.unregister_class(EasyAtlas_Settings)

if __name__ == "__main__":
	register()