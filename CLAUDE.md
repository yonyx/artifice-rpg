# Artifice RPG — CLAUDE.md

## Descripción del proyecto

RPG estilo HD-2D inspirado visualmente en *Octopath Traveler*, desarrollado en **Godot 4** con GDScript.
Combina personajes en pixel art 2D (Sprite3D) sobre escenarios 3D con cámara ortográfica.

**Argumento principal:** El protagonista se embarca en la búsqueda del Artífice — una figura misteriosa que
apareció hace 50 años para detener una guerra entre razas y desapareció. Algo ocurrirá al inicio de la
aventura que lo empujará a este viaje.

## Stack técnico

| Elemento | Tecnología |
|---|---|
| Motor | Godot 4.6 |
| Lenguaje | GDScript |
| Tipo de proyecto | 3D |
| Personajes | Sprite3D (pixel art 2D en mundo 3D) |
| Escenarios | Modelos 3D low-poly / estilizados |
| Cámara | Camera3D ortográfica con follow script |
| Física | Jolt Physics |
| Renderer | GL Compatibility |
| Arte | Aseprite (sprites), Krita (retratos), Blender (modelos 3D) |

## Estado actual del proyecto (2026-05-26)

### ✅ Prototipo 1 — Movimiento y cámara (COMPLETADO)
- `scenes/player/player.tscn` — CharacterBody3D + Sprite3D billboard + CollisionShape3D
- `scripts/player/player.gd` — Movimiento WASD + flechas, 4 direcciones, bloqueo en diálogo
- `scripts/player/camera_follow.gd` — Cámara ortográfica que sigue al jugador con look_at
- Sprites placeholder generados con Python (32x48 px): player_south/north/east/west.png
- Teclas: WASD + flechas = mover

### ✅ Prototipo 2 — NPC e interacción (COMPLETADO)
- `scenes/npcs/npc.tscn` — Node3D + Sprite3D + Area3D de interacción (radio 1.8u)
- `scripts/npcs/npc.gd` — Detecta jugador, abre diálogo con E
- `scripts/dialogue/dialogue_manager.gd` — Autoload singleton, gestiona líneas y señales
- `scripts/dialogue/dialogue_box.gd` — UI conectada al DialogueManager
- `scenes/ui/dialogue_box.tscn` — Panel inferior con nombre del hablante y texto
- Tecla E = interactuar / avanzar diálogo

### ✅ Prototipo 3 — Mapa Pueblo_01 (COMPLETADO)
- `scenes/maps/pueblo_01.tscn` — Mapa completo con luz, objetos y personajes
- `scenes/objects/house.tscn` — Casa reutilizable (paredes beige + techo rojo + colisión)
- `scenes/objects/tree.tscn` — Árbol reutilizable (tronco + copa esférica + colisión)
- `scenes/objects/chest.tscn` — Cofre interactuable con animación de tapa
- `scripts/objects/chest.gd` — Abre cofre con E, muestra contenido en diálogo
- `scripts/objects/exit_zone.gd` — Zona de salida con cambio de escena o mensaje
- WorldEnvironment configurado desde el editor (GL Compatibility requiere configuración manual)
- Escena principal: `res://scenes/maps/pueblo_01.tscn`

### 🔲 Prototipo 4 — Combate básico (PENDIENTE)
- Sistema de turnos 1v1 con Slime (HP:20, ATK:4, DEF:1, EXP:5)
- Opciones: Atacar | Habilidad | Objeto | Huir
- Stats: HP, MP, Ataque, Defensa, Velocidad, Experiencia, Nivel

### 🔲 Prototipo 5 — Inventario básico (PENDIENTE)
- Objetos: Poción, Éter, Antídoto, Llave

## Estructura de carpetas del proyecto Godot

```
res://
  scenes/
    player/       # Player.tscn
    npcs/         # NPC.tscn
    enemies/      # Escenas de enemigos
    maps/         # pueblo_01.tscn, main.tscn (test)
    battle/       # UI y lógica de combate
    ui/           # dialogue_box.tscn, menús, HUD
    objects/      # house.tscn, tree.tscn, chest.tscn
    systems/      # Autoloads y sistemas globales

  scripts/
    player/       # player.gd, camera_follow.gd
    dialogue/     # dialogue_manager.gd, dialogue_box.gd
    npcs/         # npc.gd
    objects/      # chest.gd, exit_zone.gd
    battle/       # BattleManager (pendiente)
    inventory/    # InventoryManager (pendiente)
    quests/       # QuestManager (pendiente)
    save/         # SaveManager (pendiente)

  assets/
    sprites/
      characters/ # player_south/north/east/west.png, npc_aldeano.png
      enemies/    # sprites de enemigos
      icons/      # iconos de objetos (32x32)
    portraits/    # retratos para diálogos (512x512)
    models/
      environment/ # modelos 3D (pendiente Blender)
      props/
    textures/
    audio/
      music/
      sfx/

  data/
    items/
    enemies/
    skills/
    dialogues/
    quests/

  tools/          # scripts Python para generar assets
    gen_placeholder_sprite.py
    gen_npc_sprite.py
```

## Sistemas implementados

### DialogueManager (Autoload)
```gdscript
DialogueManager.start(lines: Array[String], speaker: String)
DialogueManager.advance()
DialogueManager.close()
# Señales: dialogue_started, dialogue_ended, line_changed(speaker, text)
# Variable: is_active: bool
```

### Player
- Grupo: `"player"` (usado por camera_follow para encontrarlo)
- Se detiene automáticamente cuando `DialogueManager.is_active == true`
- Exports: `tex_south`, `tex_north`, `tex_east`, `tex_west` (Texture2D)

### NPC
- Exports: `speaker_name: String`, `dialogue_lines: Array[String]`
- Interacción por Area3D (radio 1.8u, detección de CharacterBody3D)

### Chest
- Exports: `items: Array[String]`, `opened: bool`
- Al abrir: anima tapa (-80° en X) + muestra diálogo con contenido

### CameraFollow
- Offset fijo: `Vector3(0, 8, 8)`
- Usa `look_at()` para siempre apuntar al jugador
- Busca al jugador por grupo `"player"` en `_process`

## Controles
```
WASD / Flechas  →  Mover jugador
E               →  Interactuar / Avanzar diálogo
```

## Input Actions registradas en project.godot
```
move_left   → A
move_right  → D
move_up     → W
move_down   → S
interact    → E
```

## Autoloads registrados
```
DialogueManager  →  res://scripts/dialogue/dialogue_manager.gd
```

## Notas críticas de GL Compatibility

- **WorldEnvironment**: configurar SIEMPRE desde el editor de Godot, no desde el tscn.
  Las propiedades de `Environment` no se serializan igual en GL Compatibility.
  Configurar: Ambient Light > Source = Color, Energy = 1.0
- **Sprites pixel art**: filtro Nearest, sin mipmaps, preset "2D" en importación
- **Sprite3D**: billboard = Enabled, pixel_size = 0.01

## Historia — Primer Acto

**Cinemática de apertura:**
- Guerra entre razas del reino (motivo revelado después)
- Rey humano vs Rey monstruo, ambos heridos
- Aparece el Artífice — dice "basta" — fundido a blanco
- Protagonista despierta: era un sueño/visión de hace 50 años

**Primera escena jugable:**
- El jugador elige el nombre del protagonista
- Entorno: granja de 2 pisos (3 habitaciones, sala, comedor, cocina)
- Exterior: cosechas, árboles, rejas de madera

**Razas del mundo:** Humanos, Elfos, Monstruos, Personas Bestia

## Estadísticas del jugador/enemigos

```
HP, MP, Ataque, Defensa, Velocidad, Experiencia, Nivel
```

## Opciones de combate (por turno)

```
Atacar | Habilidad | Objeto | Huir
```

## Primer enemigo de prueba

```
Nombre: Slime | HP: 20 | Ataque: 4 | Defensa: 1 | EXP: 5
```

## Esquema de datos de objetos

```gdscript
id: String          # "potion_001"
nombre: String      # "Poción"
descripcion: String # "Restaura 50 HP."
tipo: String        # "consumible" | "equipo" | "llave"
efecto: String      # "heal_hp"
valor: int          # 50
precio: int         # 30
icono: Texture2D
```

## Fases del proyecto

| Fase | Objetivo | Estado |
|---|---|---|
| 1 | Base técnica (movimiento, cámara, NPC) | ✅ Completada |
| 2 | Vertical slice jugable (10–15 min) | 🔄 En progreso |
| 3 | Arte propio y guía visual | 🔲 Pendiente |
| 4 | Sistemas RPG completos | 🔲 Pendiente |
| 5 | Producción completa y lanzamiento en itch.io | 🔲 Pendiente |

## Convenciones de código GDScript

- Nombres de archivos: `snake_case.gd`, `PascalCase.tscn`
- Clases: `class_name PascalCase`
- Variables: `snake_case`
- Constantes: `UPPER_SNAKE_CASE`
- Señales: `snake_case` (sin prefijo `on_`)
- Un nodo raíz por escena, sin lógica de otros sistemas en scripts de jugador
- Usar `@export` para datos configurables en el Inspector
- Usar `Resource` para datos de objetos, enemigos y habilidades cuando sea posible
- Preferir señales sobre referencias directas entre nodos hermanos

## Herramientas del equipo

```
Godot 4.6       Motor principal
Aseprite        Sprites y animaciones pixel art
Krita           Retratos y concept art
Blender         Modelos 3D de escenarios y props
Material Maker  Texturas procedurales
Audacity        Edición de audio
Figma           Diseño de UI
GitHub          Control de versiones
```
