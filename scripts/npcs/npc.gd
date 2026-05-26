extends Node3D

class_name NPC

@export var speaker_name: String = "Aldeano"
@export var dialogue_lines: Array[String] = [
	"Hola, viajero.",
	"Bienvenido a este lugar.",
	"Que tengas un buen viaje."
]

var _player_nearby: bool = false


func _ready() -> void:
	$InteractionArea.body_entered.connect(_on_body_entered)
	$InteractionArea.body_exited.connect(_on_body_exited)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("interact"):
		if _player_nearby:
			if DialogueManager.is_active:
				DialogueManager.advance()
			else:
				DialogueManager.start(dialogue_lines, speaker_name)


func _on_body_entered(body: Node3D) -> void:
	if body is Player:
		_player_nearby = true


func _on_body_exited(body: Node3D) -> void:
	if body is Player:
		_player_nearby = false
