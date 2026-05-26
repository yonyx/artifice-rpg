extends CharacterBody3D

class_name Player

const SPEED := 4.0
const GRAVITY := 9.8

@export var tex_south: Texture2D
@export var tex_north: Texture2D
@export var tex_east: Texture2D
@export var tex_west: Texture2D

@onready var sprite: Sprite3D = $Sprite3D

var _last_dir := Vector2.DOWN


func _ready() -> void:
	add_to_group("player")
	_set_sprite(_last_dir)


func _physics_process(delta: float) -> void:
	if DialogueManager.is_active:
		velocity.x = 0.0
		velocity.z = 0.0
		if not is_on_floor():
			velocity.y -= GRAVITY * delta
		move_and_slide()
		return

	var input_dir := Vector2(
		Input.get_axis("ui_left", "ui_right") + Input.get_axis("move_left", "move_right"),
		Input.get_axis("ui_up", "ui_down") + Input.get_axis("move_up", "move_down")
	).clampf(-1.0, 1.0)

	var direction := Vector3.ZERO
	if input_dir != Vector2.ZERO:
		direction = Vector3(input_dir.x, 0.0, input_dir.y).normalized()
		_last_dir = input_dir
		_set_sprite(input_dir)

	velocity.x = direction.x * SPEED
	velocity.z = direction.z * SPEED

	if not is_on_floor():
		velocity.y -= GRAVITY * delta

	move_and_slide()


func _set_sprite(dir: Vector2) -> void:
	if abs(dir.x) >= abs(dir.y):
		if dir.x > 0:
			sprite.texture = tex_east
		else:
			sprite.texture = tex_west
	else:
		if dir.y > 0:
			sprite.texture = tex_south
		else:
			sprite.texture = tex_north
