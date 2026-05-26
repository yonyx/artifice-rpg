extends Node3D

@export var items: Array[String] = ["Poción"]
@export var opened: bool = false

var _player_nearby: bool = false


func _ready() -> void:
	$InteractionArea.body_entered.connect(_on_body_entered)
	$InteractionArea.body_exited.connect(_on_body_exited)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("interact") and _player_nearby and not opened:
		opened = true
		$Lid.rotation_degrees.x = -80
		var contenido := ", ".join(items)
		DialogueManager.start(["Encontraste: " + contenido + "!"], "Cofre")


func _on_body_entered(body: Node3D) -> void:
	if body is Player:
		_player_nearby = true


func _on_body_exited(body: Node3D) -> void:
	if body is Player:
		_player_nearby = false
