extends CanvasLayer

@onready var panel: PanelContainer = $Panel
@onready var speaker_label: Label = $Panel/Margin/VBox/SpeakerLabel
@onready var text_label: Label = $Panel/Margin/VBox/TextLabel
@onready var hint_label: Label = $Panel/Margin/VBox/HintLabel


func _ready() -> void:
	panel.hide()
	DialogueManager.dialogue_started.connect(_on_started)
	DialogueManager.dialogue_ended.connect(_on_ended)
	DialogueManager.line_changed.connect(_on_line_changed)


func _on_started() -> void:
	panel.show()


func _on_ended() -> void:
	panel.hide()


func _on_line_changed(speaker: String, text: String) -> void:
	speaker_label.text = speaker
	text_label.text = text
