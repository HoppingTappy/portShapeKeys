import bpy
import bmesh

bl_info = {
	"name": "port shape keys",
	"author": "tappy",
	"version": (1, 0),
	"blender": (2, 91, 2),
	"location": "Object Data > Shape Keys Specials",
	"description": "シェイプキーを他のオブジェクトから移植します",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object",
}

translationDict = {
	"en_US": {
		("*", "Port Shape Keys From Selected Objects"):"Port Shape Keys From Selected Objects",
	},
	"ja_JP": {
		("*", "Port Shape Keys From Selected Objects"):"選択中のオブジェクトからシェイプキーを移植",
	}
}

class PortShapeKeys(bpy.types.Operator):

	bl_idname = "object.port_shape_keys"
	bl_label = bpy.app.translations.pgettext("Port Shape Keys From Selected Objects")
	bl_description = "シェイプキーを他のオブジェクトから移植します"
	bl_options = {'REGISTER', 'UNDO'}


	@classmethod
	def poll(cls, context):
		obj = context.active_object
		if not obj:
			return False

		if len(context.selected_objects)<2:
			return False

		for obj in context.selected_objects:
			if not obj.type in {'MESH'}:
				return False

		return True

	def execute(self, context):

		aObj = context.active_object

		if not aObj.data.shape_keys:
			aObjBasisShape = aObj.shape_key_add('Basis')
			aObjBasisShape.interpolation = 'KEY_LINEAR'
		else:
			aObjBasisShape = aObj.data.shape_keys.key_blocks[0]

		for obj in context.selected_objects:
			if obj != aObj:
				if len(obj.data.vertices) == len(aObj.data.vertices):
					if obj.data.shape_keys:
						basisShape = obj.data.shape_keys.key_blocks[0]

						basisDiffFlag = False
						for t,s in zip(aObjBasisShape.data,basisShape.data):
							if t.co!=s.co:
								basisDiffFlag = True
								break
						if basisDiffFlag:
							newBasisShape = aObj.shape_key_add()
							newBasisShape.name = basisShape.name


						for shape in obj.data.shape_keys.key_blocks:
							if basisShape != shape:
								newShape = aObj.shape_key_add()
								newShape.name = shape.name
								newShape.interpolation = shape.interpolation
								newShape.slider_min = shape.slider_min
								newShape.slider_max = shape.slider_max

								for i,vert in enumerate(shape.data):
									newShape.data[i].co = vert.co
#								if basisDiffFlag:
#									newShape.relative_key = newBasisShape

		return {'FINISHED'}

def addMenu(self, context):
	self.layout.separator()
	self.layout.operator(PortShapeKeys.bl_idname,text=bpy.app.translations.pgettext("Port Shape Keys From Selected Objects"))

classes = [
	PortShapeKeys,
]

def register():
	bpy.app.translations.register(__name__, translationDict)
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.MESH_MT_shape_key_context_menu.append(addMenu)


def unregister():
	bpy.app.translations.unregister(__name__)
	bpy.types.MESH_MT_shape_key_context_menu.remove(addMenu)
	for c in classes:
		bpy.utils.unregister_class(c)


if __name__ == "__main__":
	register()
