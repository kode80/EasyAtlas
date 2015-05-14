# EasyAtlas
A Blender addon for creating texture atlases.

EasyAtlas adds a "create atlas" button to Blender's render panel. Pressing the button will loop through all meshes in the scene creating new EasyAtlas UV sets and baking each object to a single EasyAtlas texture. EasyAtlas uses Blender's bake settings and appends the bake type to the EasyAtlas texture name allowing you to quickly output atlases of multiple textures. For example; setting bake to vertex colors, hitting "create atlas", setting bake to ambient occlusion and hitting "create atlas" will result in two textures "EasyAtlas_VERTEX_COLORS" and "EasyAtlas_AO".

If using Unity, once atlas creation is complete export scene as .fbx and check the "Swap UVs" option in the Unity mesh importer (this will use EasyAtlas's UVs rather than your originals).

EasyAtlas only touches it's own data (EasyAtlas UV set/texture) so shouldn't cause any harm to your .blend, I'm currently using it in my own projects without problem, that said it is in development so the usual disclaimers of backing up and using at your own risk apply. ;D
