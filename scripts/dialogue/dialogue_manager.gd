extends Node

signal dialogue_started
signal dialogue_ended
signal line_changed(speaker: String, text: String)

var is_active: bool = false

var _lines: Array[String] = []
var _speaker: String = ""
var _index: int = 0


func start(lines: Array[String], speaker: String) -> void:
	if is_active:
		return
	_lines = lines
	_speaker = speaker
	_index = 0
	is_active = true
	dialogue_started.emit()
	line_changed.emit(_speaker, _lines[_index])


func advance() -> void:
	if not is_active:
		return
	_index += 1
	if _index >= _lines.size():
		close()
	else:
		line_changed.emit(_speaker, _lines[_index])


func close() -> void:
	is_active = false
	_lines = []
	_index = 0
	dialogue_ended.emit()
