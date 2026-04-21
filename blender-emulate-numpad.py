import bpy

bl_info = {
    "name": "blender-emulate-numpad",
    "author": "Gemini CLI",
    "version": (1, 6),
    "blender": (2, 80, 0),
    "location": "Addon Preferences",
    "description": "Toggle Emulate Numpad / Переключает эмуляцию цифровой клавиатуры",
    "category": "Interface",
}

# Словарь переводов
translations_dict = {
    "en_US": {
        ("*", "Toggle Emulate Numpad"): "Toggle Emulate Numpad",
        ("*", "Key Configuration:"): "Hotkey Settings:",
        ("*", "Key Name"): "Key Name",
        ("*", "Examples: ACCENT_GRAVE (tilde), F1, SPACE, ONE, TAB"): "Examples: ACCENT_GRAVE (tilde), F1, SPACE, ONE, TAB",
        ("*", "Emulate Numpad: ON"): "Emulate Numpad: ON",
        ("*", "Emulate Numpad: OFF"): "Emulate Numpad: OFF",
        ("*", "Hotkey Settings"): "Hotkey Settings",
        ("*", "Toggle setting for Emulate Numpad"): "Toggle setting for Emulate Numpad",
    },
    "ru_RU": {
        ("*", "Toggle Emulate Numpad"): "Переключить Emulate Numpad",
        ("*", "Key Configuration:"): "Настройка горячей клавиши:",
        ("*", "Key Name"): "Клавиша",
        ("*", "Examples: ACCENT_GRAVE (tilde), F1, SPACE, ONE, TAB"): "Примеры: ACCENT_GRAVE (тильда), F1, SPACE, ONE, TAB",
        ("*", "Emulate Numpad: ON"): "Emulate Numpad: ВКЛ",
        ("*", "Emulate Numpad: OFF"): "Emulate Numpad: ВЫКЛ",
        ("*", "Hotkey Settings"): "Настройка хоткея",
        ("*", "Toggle setting for Emulate Numpad"): "Переключить настройку эмуляции цифровой клавиатуры",
    }
}

class WM_OT_TildeToggleNumpad(bpy.types.Operator):
    """Toggle setting for Emulate Numpad"""
    bl_idname = "wm.tilde_toggle_numpad"
    bl_label = "Toggle Emulate Numpad"

    def execute(self, context):
        prefs = context.preferences.inputs
        prefs.use_emulate_numpad = not prefs.use_emulate_numpad
        
        # Используем bpy.app.translations.pgettext для перевода сообщений
        state_msg = "Emulate Numpad: ON" if prefs.use_emulate_numpad else "Emulate Numpad: OFF"
        self.report({'INFO'}, bpy.app.translations.pgettext(state_msg))
        return {'FINISHED'}

def update_keymap(self, context):
    register_keymaps()

class TildeNumpadPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    key_type: bpy.props.StringProperty(
        name="Key Name",
        default='ACCENT_GRAVE',
        update=update_keymap
    )
    use_ctrl: bpy.props.BoolProperty(
        name="Ctrl",
        default=False,
        update=update_keymap
    )
    use_alt: bpy.props.BoolProperty(
        name="Alt",
        default=False,
        update=update_keymap
    )
    use_shift: bpy.props.BoolProperty(
        name="Shift",
        default=False,
        update=update_keymap
    )

    def draw(self, context):
        layout = self.layout
        # Тексты в интерфейсе будут переведены автоматически, если они есть в словаре
        layout.label(text=bpy.app.translations.pgettext("Key Configuration:"))
        
        box = layout.box()
        row = box.row()
        row.prop(self, "key_type", text=bpy.app.translations.pgettext("Key Name"))
        
        row = box.row(align=True)
        row.prop(self, "use_ctrl", toggle=True)
        row.prop(self, "use_alt", toggle=True)
        row.prop(self, "use_shift", toggle=True)
        
        layout.label(text=bpy.app.translations.pgettext("Examples: ACCENT_GRAVE (tilde), F1, SPACE, ONE, TAB"), icon='INFO')

addon_keymaps = []

def register_keymaps():
    unregister_keymaps()
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc:
        return

    prefs = bpy.context.preferences.addons.get(__name__)
    if not prefs:
        return
    prefs = prefs.preferences
    
    for km_name, space in [('3D View', 'VIEW_3D'), ('Window', 'EMPTY')]:
        km = kc.keymaps.new(name=km_name, space_type=space)
        kmi = km.keymap_items.new(
            WM_OT_TildeToggleNumpad.bl_idname, 
            prefs.key_type, 
            'PRESS',
            ctrl=prefs.use_ctrl,
            alt=prefs.use_alt,
            shift=prefs.use_shift
        )
        addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register():
    # Регистрация переводов
    bpy.app.translations.register(__name__, translations_dict)
    
    bpy.utils.register_class(WM_OT_TildeToggleNumpad)
    bpy.utils.register_class(TildeNumpadPreferences)
    register_keymaps()

def unregister():
    unregister_keymaps()
    bpy.utils.unregister_class(TildeNumpadPreferences)
    bpy.utils.unregister_class(WM_OT_TildeToggleNumpad)
    
    # Удаление переводов
    bpy.app.translations.unregister(__name__)

if __name__ == "__main__":
    register()
