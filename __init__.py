# DDSAnimation - Moves settings and controls from other areas to the 3D Viewport for beggining animators.
# Copyright (C) 2020 Dwayne Savage
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import bpy
from bpy.types import Panel, AddonPreferences
from bpy.props import StringProperty

#Adds motion path panel to the User Input panel
class MyPath(bpy.types.Panel):
    bl_idname = "DDS_PT_mypath"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_label = "Motion Paths"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self, context):
        try:
            return (context.active_object.data)
        except (AttributeError, KeyError, TypeError):
            return False
        
    def draw(self, context):
        mpath = context.object.motion_path
        bs = context.active_pose_bone
        if bs:
            bones = context.active_pose_bone.motion_path
            mps = context.object.pose.animation_visualization.motion_path
        else:
            bones=False
            mps = context.object.animation_visualization.motion_path
        col = self.layout.column(align=True)
        col.prop(mps, "type", expand=True)
        col.prop(mps, "range", text="Calculation Range")
        col.label(text="Display Range:")
        sub = col.column(align=True)
        if mps.type == 'CURRENT_FRAME':
            sub.prop(mps, "frame_before", text="Before")
            sub.prop(mps, "frame_after", text="After")
        elif mps.type == 'RANGE':
            sub.prop(mps, "frame_start", text="Start")
            sub.prop(mps, "frame_end", text="End")
        sub.prop(mps, "frame_step", text="Step")
        if hasattr(mps, "bake_in_camera_space"):
            sub.prop(mps, "bake_in_camera_space", text="Bake to Active Camera")
        if bs:
            col.label(text="Cache for Bone:")
        else:
            col.label(text="Cache:")
        if bones:
            sub = col.column(align=True)
            sub.enabled = False
            sub.prop(bones, "frame_start", text="From")
            sub.prop(bones, "frame_end", text="To")
            sub = col.row(align=True)
            sub.operator("pose.paths_update", text="Update Paths", icon='BONE_DATA')
            sub.operator("pose.paths_clear", text="", icon='X').only_selected = True
            sub = col.row(align=True)
            sub.operator("object.paths_update_visible", text="Update All Paths", icon='WORLD')
            sub.operator("pose.paths_clear", text="", icon='X').only_selected = False
        elif mpath:
            sub = col.column(align=True)
            sub.enabled = False
            sub.prop(mpath, "frame_start", text="From")
            sub.prop(mpath, "frame_end", text="To")
            sub = col.row(align=True)
            sub.operator("object.paths_update", text="Update Paths", icon='OBJECT_DATA')
            sub.operator("object.paths_clear", text="", icon='X').only_selected = True
            sub = col.row(align=True)
            sub.operator("object.paths_update_visible", text="Update All Paths", icon='WORLD')
            sub.operator("object.paths_clear", text="", icon='X').only_selected = False
        else:
            sub = col.column(align=True)
            sub.label(text="Nothing to show yet...", icon='ERROR')
            if bs:
                sub.operator("pose.paths_calculate", text="Calculate...", icon='BONE_DATA')
                sub = col.row(align=True)
                sub.operator("object.paths_update_visible", text="Update All Paths", icon='WORLD')
                sub.operator("object.paths_clear", text="", icon='X').only_selected = False
            else:
                sub.operator("object.paths_calculate", text="Calculate...", icon='OBJECT_DATA')
                sub = col.row(align=True)
                sub.operator("object.paths_update_visible", text="Update All Paths", icon='WORLD')
                sub.operator("object.paths_clear", text="", icon='X').only_selected = False
        col.label(text="Show:")
        col.prop(mps, "show_frame_numbers", text="Frame Numbers")
        col.prop(mps, "show_keyframe_highlight", text="Keyframes")
        sub = col.column()
        sub.enabled = mps.show_keyframe_highlight
        if bs:
            sub.prop(mps, "show_keyframe_action_all", text="+ Non-Grouped Keyframes")
        sub.prop(mps, "show_keyframe_numbers", text="Keyframe Numbers")
        if bones:
            col.prop(bones, "lines", text="Lines")
            col.prop(bones, "line_thickness", text="Thickness")
            split = col.split(factor=0.6)
            split.prop(bones, "use_custom_color", text="Color")
            sub = split.column()
            sub.enabled = bones.use_custom_color
            sub.prop(bones, "color", text="")
            if hasattr(bones, "color_post"):
                sub.prop(bones, "color_post", text="")
        elif mpath:
            col.prop(mpath, "lines", text="Lines")
            col.prop(mpath, "line_thickness", text="Thickness")
            split = col.split(factor=0.6)
            split.prop(mpath, "use_custom_color", text="Color")
            sub = split.column()
            sub.enabled = mpath.use_custom_color
            sub.prop(mpath, "color", text="")
            if hasattr(mpath, "color_post"):
                sub.prop(mpath, "color_post", text="")
            
class MyPath2(bpy.types.Panel):
    bl_idname = "DDS_PT_mypath2"
    bl_space_type = "GRAPH_EDITOR"
    bl_region_type = "UI"
    bl_category = "View"
    bl_label = "Motion Paths"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self, context):
        try:
            return (context.active_object.data)
        except (AttributeError, KeyError, TypeError):
            return False
        
    def draw(self, context):
        mpath = context.object.motion_path
        bs = context.active_pose_bone
        if bs:
            bones = context.active_pose_bone.motion_path
            mps = context.object.pose.animation_visualization.motion_path
        else:
            bones=False
            mps = context.object.animation_visualization.motion_path
        col = self.layout.column(align=True)
        col.prop(mps, "type", expand=True)
        col.prop(mps, "range", text="Calculation Range")
        col.label(text="Display Range:")
        sub = col.column(align=True)
        if mps.type == 'CURRENT_FRAME':
            sub.prop(mps, "frame_before", text="Before")
            sub.prop(mps, "frame_after", text="After")
        elif mps.type == 'RANGE':
            sub.prop(mps, "frame_start", text="Start")
            sub.prop(mps, "frame_end", text="End")
        sub.prop(mps, "frame_step", text="Step")
        if hasattr(mps, "bake_in_camera_space"):
            sub.prop(mps, "bake_in_camera_space", text="Bake to Active Camera")
        if bs:
            col.label(text="Cache for Bone:")
        else:
            col.label(text="Cache:")
        if bones:
            sub = col.column(align=True)
            sub.enabled = False
            sub.prop(bones, "frame_start", text="From")
            sub.prop(bones, "frame_end", text="To")
            sub = col.row(align=True)
            sub.operator("pose.paths_update", text="Update Paths", icon='BONE_DATA')
            sub.operator("pose.paths_clear", text="", icon='X').only_selected = True
            sub = col.row(align=True)
            sub.operator("object.paths_update_visible", text="Update All Paths", icon='WORLD')
            sub.operator("pose.paths_clear", text="", icon='X').only_selected = False
        elif mpath:
            sub = col.column(align=True)
            sub.enabled = False
            sub.prop(mpath, "frame_start", text="From")
            sub.prop(mpath, "frame_end", text="To")
            sub = col.row(align=True)
            sub.operator("object.paths_update", text="Update Paths", icon='OBJECT_DATA')
            sub.operator("object.paths_clear", text="", icon='X').only_selected = True
            sub = col.row(align=True)
            sub.operator("object.paths_update_visible", text="Update All Paths", icon='WORLD')
            sub.operator("object.paths_clear", text="", icon='X').only_selected = False
        else:
            sub = col.column(align=True)
            sub.label(text="Nothing to show yet...", icon='ERROR')
            if bs:
                sub.operator("pose.paths_calculate", text="Calculate...", icon='BONE_DATA')
                sub = col.row(align=True)
                sub.operator("object.paths_update_visible", text="Update All Paths", icon='WORLD')
                sub.operator("object.paths_clear", text="", icon='X').only_selected = False
            else:
                sub.operator("object.paths_calculate", text="Calculate...", icon='OBJECT_DATA')
                sub = col.row(align=True)
                sub.operator("object.paths_update_visible", text="Update All Paths", icon='WORLD')
                sub.operator("object.paths_clear", text="", icon='X').only_selected = False
        col.label(text="Show:")
        col.prop(mps, "show_frame_numbers", text="Frame Numbers")
        col.prop(mps, "show_keyframe_highlight", text="Keyframes")
        sub = col.column()
        sub.enabled = mps.show_keyframe_highlight
        if bs:
            sub.prop(mps, "show_keyframe_action_all", text="+ Non-Grouped Keyframes")
        sub.prop(mps, "show_keyframe_numbers", text="Keyframe Numbers")
        if bones:
            col.prop(bones, "lines", text="Lines")
            col.prop(bones, "line_thickness", text="Thickness")
            split = col.split(factor=0.6)
            split.prop(bones, "use_custom_color", text="Color")
            sub = split.column()
            sub.enabled = bones.use_custom_color
            sub.prop(bones, "color", text="")
            if hasattr(bones, "color_post"):
                sub.prop(bones, "color_post", text="")
        elif mpath:
            col.prop(mpath, "lines", text="Lines")
            col.prop(mpath, "line_thickness", text="Thickness")
            split = col.split(factor=0.6)
            split.prop(mpath, "use_custom_color", text="Color")
            sub = split.column()
            sub.enabled = mpath.use_custom_color
            sub.prop(mpath, "color", text="")
            if hasattr(mpath, "color_post"):
                sub.prop(mpath, "color_post", text="")

#sets up the animation panel
class DDSAnime:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_label = "Animation Tools"

#populates animation panel with main buttons and options    
class DDSTools(DDSAnime, Panel):

    @classmethod
    def poll(self, context):
        try:
            return (True)
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        scene = context.scene
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.operator("screen.frame_jump", text="", icon='REW').end = False
        row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False
        if not context.screen.is_animation_playing:
            if scene.sync_mode == 'AUDIO_SYNC' and context.user_preferences.system.audio_device == 'JACK':
                sub = row.row(align=True)
                #sub.scale_x = 2.0
                sub.operator("screen.animation_play", text="", icon='PLAY')
            else:
                row.operator("screen.animation_play", text="", icon='PLAY_REVERSE').reverse = True
                row.operator("screen.animation_play", text="", icon='PLAY')
        else:
            sub = row.row(align=True)
            sub.scale_x = 1.4
            sub.operator("screen.animation_play", text="", icon='PAUSE')
        row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
        row.operator("screen.frame_jump", text="", icon='FF').end = True
        col.prop(context.tool_settings, 'keyframe_type', text='')
        if hasattr(context.preferences.edit, "key_insert_channels"):
            row = col.row(align=False)
            row.alignment = "CENTER"
            row.label(text="Key Channels")
            row = col.row(align=False)
            sub = row.box()
            sub.prop(context.preferences.edit, "key_insert_channels", expand=True)
        row = col.row(align=True)
        row.prop(context.tool_settings, "use_keyframe_insert_auto", text="", toggle=True)
        if context.tool_settings.use_keyframe_insert_auto:
            row.prop(context.tool_settings, "use_keyframe_insert_keyingset", text="", toggle=True)
            if context.screen.is_animation_playing and not context.user_preferenes.edit.use_keyframe_insert_available:
                subsub = row.row(align=True)
                subsub.prop(toolsettings, "use_record_with_nla", toggle=True)
        row.prop(scene, "use_preview_range", text="")
        row = col.row(align=True)
        row.prop_search(scene.keying_sets_all, "active", scene, "keying_sets_all", text="")
        row.operator("anim.keyframe_insert", text="", icon='KEY_HLT')
        row.operator("anim.keyframe_delete", text="", icon='KEY_DEHLT')
        col.prop(scene, "frame_current", text="Current")
        if context.scene.use_preview_range == True:
            col.prop(scene, "frame_preview_start", text="Start")
            col.prop(scene, "frame_preview_end", text="End")
        else:
            col.prop(scene, "frame_start", text="Start")
            col.prop(scene, "frame_end", text="End")
        box = self.layout.box()
        col = box.column(align=True)
        col.label(text="Animation Preference")
        col.prop(context.preferences.edit, "use_mouse_depth_cursor", toggle=True)
        col.prop(context.preferences.edit, "use_visual_keying", toggle=True, text="Visual Keying")
        col.prop(context.preferences.edit, "use_keyframe_insert_needed", toggle=True, text="Only insert needed")
        col.prop(context.preferences.edit, "use_keyframe_insert_available", toggle=True, text="Only insert Available")
        col.prop(context.preferences.edit, "keyframe_new_interpolation_type", text="")
        col.prop(context.preferences.edit, "keyframe_new_handle_type", text="")
        col.prop(context.preferences.inputs.walk_navigation, "view_height")

#Adds Simplify subpanel to Anime Tools        
class DDSSimple(DDSAnime, Panel):
    bl_label = "Simplify"
    bl_parent_id = "DDSTools"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        self.layout.prop(context.scene.render, "use_simplify", text="")
        
    def draw(self, context):
        rd = context.scene.render
        cscene = context.scene.cycles
        eg = context.engine
        layout = self.layout
        col = layout.column(align=True)
        col.active = rd.use_simplify
        col.label(text="View Port")
        row = col.row(align=True)
        row.prop(rd, "simplify_subdivision", text="")
        row.prop(rd, "simplify_child_particles", text="")
        if hasattr(rd, "simplify_volumes"):
            row = col.row(align=True)
            row.prop(rd, "simplify_volumes", text="Volume Resolution")
        else:
            row = col.row(align=True)
            row.prop(rd, "use_simplify_smoke_highres", text="High-Res Smoke")
        
        if eg in 'BLENDER_EEVEE_NEXT':
            row = col.row(align=True)
            row.prop(rd, "simplify_shadows", text="Shadow Resolution")
              
        if eg == "CYCLES":
            row = col.row(align=True)
            row.label(text="Texture Limit")
            row = col.row(align=True)
            row.prop(cscene, "texture_limit", text="")
            row = col.row(align=True)
            row.prop(cscene, "ao_bounces", text="AO Bounces")
        
        if hasattr(rd, "use_simplify_normals"):
            row = col.row(align=True)
            row.prop(rd, "use_simplify_normals", text="Normals")
        col.label(text="Render")
        row = col.row(align=True)
        row.prop(rd, "simplify_subdivision_render", text="")
        row.prop(rd, "simplify_child_particles_render", text="")
        if eg == "CYCLES":
            row = col.row(align=True)
            row.label(text="Texture Limit")
            row = col.row(align=True)
            row.prop(cscene, "texture_limit_render", text="")
            row = col.row(align=True)
            row.prop(cscene, "ao_bounces_render", text="AO Bounces")
        if eg == "CYCLES":
            box = layout.box()
            col.label(text="Culling")
            col = box.column(align=True)
            col.active = rd.use_simplify
            col.prop(cscene, "use_camera_cull")
            row = col.row()
            row.active = cscene.use_camera_cull
            row.prop(cscene, "camera_cull_margin", text="Cam Margin")
            col.prop(cscene, "use_distance_cull")
            row = col.row()
            row.active = cscene.use_distance_cull
            row.prop(cscene, "distance_cull_margin", text="Dist Margin")
        if eg in 'BLENDER_EEVEE_NEXT':
            row = col.row(align=True)
            row.prop(rd, "simplify_shadows_render", text="Shadow Resolution")
            
        col = layout.column()
        col.active = rd.use_simplify
        col.prop(rd, "simplify_gpencil", text="Grease Pencil")
        box = layout.box()
        if rd.use_simplify and rd.simplify_gpencil:
            box.active = True
        else:
            box.active = False
        col = box.column(align=True)
        col.prop(rd, "simplify_gpencil_onplay", text="Playback Only") 
        col.prop(rd, "simplify_gpencil_view_fill", text="Fill")
        col.prop(rd, "simplify_gpencil_modifier", text="Modifiers") 
        col.prop(rd, "simplify_gpencil_shader_fx", text="ShaderFX") 
        col.prop(rd, "simplify_gpencil_tint", text="Layers Tinting") 
        col.prop(rd, "simplify_gpencil_antialiasing", text="Antialiasing")

panels = (
    DDSTools,
    DDSSimple,
    MyPath,
    MyPath2,
        )
        
def update_panel(self, context):
    message = "Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        for panel in panels:
            panel.bl_category = context.preferences.addons[__name__].preferences.category
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass

class DDSNamePrefs(AddonPreferences):
    bl_idname = __name__

    category: StringProperty(
            name="Tab Category",
            description="Choose a name for the category of the panel",
            default="Item",
            update=update_panel
            )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text="Tab Category:")
        col.prop(self, "category", text="")        


classes = (
    DDSTools,
    DDSSimple,
    MyPath,
    MyPath2,
    DDSNamePrefs,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    update_panel(None, bpy.context)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__": 
    register()    
