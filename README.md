# EasyAtlas
A Blender addon for creating texture atlases.

EasyAtlas adds a "create atlas" button to Blender's render panel. Pressing the button will loop through all meshes in the scene creating new EasyAtlas UV sets and baking each object to a single EasyAtlas texture.

If using Unity, once atlas creation is complete export scene as .fbx and check the "Swap UVs" option in the Unity mesh importer (this will use EasyAtlas's UVs rather than your originals).

In dev, use at your own risk. ;D
