extends Camera3D

## Camara que sigue al jugador suavemente manteniendo un offset fijo.

const OFFSET := Vector3(0, 8, 8)
const SPEED  := 8.0

var _target: Node3D


func _ready() -> void:
	var players := get_tree().get_nodes_in_group("player")
	if players.size() > 0:
		_target = players[0]
		global_position = _target.global_position + OFFSET


func _process(delta: float) -> void:
	if not _target:
		return
	var goal := _target.global_position + OFFSET
	global_position = global_position.lerp(goal, SPEED * delta)
