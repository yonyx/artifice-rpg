extends CharacterBody3D

class_name Player

const SPEED := 4.0
const GRAVITY := 9.8

@onready var sprite: Sprite3D = $Sprite3D


func _physics_process(delta: float) -> void:
	var input_dir := Vector2(
		Input.get_axis("ui_left", "ui_right"),
		Input.get_axis("ui_up", "ui_down")
	)

	var direction := Vector3.ZERO
	if input_dir != Vector2.ZERO:
		direction = Vector3(input_dir.x, 0.0, input_dir.y).normalized()

	velocity.x = direction.x * SPEED
	velocity.z = direction.z * SPEED

	if not is_on_floor():
		velocity.y -= GRAVITY * delta

	if direction.x != 0.0:
		sprite.flip_h = direction.x < 0.0

	move_and_slide()
