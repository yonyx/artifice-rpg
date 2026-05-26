# Artifice RPG — CLAUDE.md

## Descripción del proyecto

RPG estilo HD-2D inspirado visualmente en *Octopath Traveler*, desarrollado en **Godot 4** con GDScript.
Combina personajes en pixel art 2D (Sprite3D) sobre escenarios 3D con cámara ortográfica.

## Stack técnico

| Elemento | Tecnología |
|---|---|
| Motor | Godot 4.6 |
| Lenguaje | GDScript |
| Tipo de proyecto | 3D |
| Personajes | Sprite3D (pixel art 2D en mundo 3D) |
| Escenarios | Modelos 3D low-poly / estilizados |
| Cámara | Camera3D ortográfica |
| Física | Jolt Physics |
| Renderer | GL Compatibility |
| Arte | Aseprite (sprites), Krita (retratos), Blender (modelos 3D) |

## Estructura de carpetas del proyecto Godot

```
res://
  scenes/
    player/       # Player.tscn y variantes
    npcs/         # NPC.tscn y variantes
    enemies/      # Escenas de enemigos
    maps/         # Mapas del mundo (Pueblo_01, Bosque_01, etc.)
    battle/       # UI y lógica de combate
    ui/           # Menús, HUD, inventario, diálogo
    systems/      # Autoloads y sistemas globales

  scripts/
    player/       # Movimiento, stats, interacción
    dialogue/     # DialogueManager, caja de diálogo
    battle/       # BattleManager, lógica de turnos
    inventory/    # InventoryManager, objetos
    quests/       # QuestManager
    save/         # SaveManager

  assets/
    sprites/
      characters/ # Hojas de sprites de personajes
      enemies/    # Sprites de enemigos
      icons/      # Iconos de objetos (32x32)
    portraits/    # Retratos para diálogos (512x512)
    models/
      environment/ # Casas, árboles, rocas, puentes
      props/       # Cofres, mesas, faroles
    textures/     # Materiales y texturas
    audio/
      music/      # BGM
      sfx/        # Efectos de sonido

  data/
    items/        # JSON/Resource de objetos
    enemies/      # Datos de enemigos
    skills/       # Habilidades
    dialogues/    # Guiones de diálogos
    quests/       # Definición de misiones
```

## Estilo visual

- Personajes: pixel art, 32x48 px o 48x64 px, 4 direcciones
- Animaciones por personaje: Idle, Caminar, Atacar, Recibir daño, Morir (3–6 frames cada una)
- Retratos: 512x512 px
- Iconos: 32x32 px
- Iluminación: DirectionalLight3D principal + OmniLight3D/SpotLight3D secundarias
- Efectos: bloom, niebla, sombras suaves, depth of field (WorldEnvironment)
- Escenarios: low-poly, estilo diorama

## Sistemas principales (Autoloads / Managers)

```
GameManager.gd       # Estado global del juego
BattleManager.gd     # Combate por turnos
InventoryManager.gd  # Objetos e inventario
QuestManager.gd      # Misiones
DialogueManager.gd   # Sistema de diálogos
SaveManager.gd       # Guardado/carga (JSON o Resource)
AudioManager.gd      # Música y efectos
```

Cada sistema va separado. No mezclar lógica entre managers.

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
# Campos de cada Item (Resource o JSON)
id: String          # "potion_001"
nombre: String      # "Poción"
descripcion: String # "Restaura 50 HP."
tipo: String        # "consumible" | "equipo" | "llave"
efecto: String      # "heal_hp"
valor: int          # 50
precio: int         # 30
icono: Texture2D
```

## Plan de prototipos (orden estricto)

1. **Prototipo 1** — Movimiento y cámara: CharacterBody3D + Sprite3D caminando en escenario 3D simple
2. **Prototipo 2** — NPC e interacción: Area3D + caja de diálogo
3. **Prototipo 3** — Mapa Pueblo_01: 3 casas, 2 NPCs, 1 cofre, 1 salida, niebla y música
4. **Prototipo 4** — Combate básico: sistema de turnos 1v1 con Slime
5. **Prototipo 5** — Inventario básico: Poción, Éter, Antídoto, Llave

## Fases del proyecto

| Fase | Objetivo | Duración estimada |
|---|---|---|
| 1 | Base técnica (movimiento, cámara, NPC) | 2–4 semanas |
| 2 | Vertical slice jugable (10–15 min) | 1–2 meses |
| 3 | Arte propio y guía visual | Paralelo a Fase 2 |
| 4 | Sistemas RPG completos | TBD |
| 5 | Producción completa y lanzamiento en itch.io | TBD |

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

## Notas de importación de sprites pixel art en Godot 4

- Filtro de textura: **Nearest** (no Linear)
- Compresión: **Lossless**
- Mipmaps: desactivados
- En `Sprite3D`: activar `pixel_size` ajustado a la escala del mundo

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
