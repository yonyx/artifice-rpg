extends Area3D

## Zona de salida. Cambia de escena al contacto con el jugador.
@export var next_scene: String = ""


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node3D) -> void:
	if not body is Player:
		return
	if next_scene != "":
		get_tree().change_scene_to_file(next_scene)
	else:
		DialogueManager.start(["[Salida al Bosque — Próximamente]"], "Sistema")
