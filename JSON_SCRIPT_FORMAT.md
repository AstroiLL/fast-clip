# Fast-Clip JSON Script Format

## Overview

JSON-скрипт определяет последовательность и параметры видеофрагментов для сборки финального видео.

## File Structure

```json
{
  "name": "project_name",
  "resources_dir": "directory_name",
  "timeline": [...],
  "result_file": "output.mp4"
}
```

## Field Descriptions

### Root Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Название проекта/видео. Используется для логирования и идентификации. |
| `resources_dir` | string | Yes | Имя директории с исходными файлами (относительно рабочей директории). |
| `timeline` | array | Yes | Массив объектов timeline, определяющих последовательность клипов. |
| `result_file` | string | Yes | Имя выходного файла (будет создан в рабочей директории). |

### Timeline Item Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | Yes | Порядковый номер клипа (начинается с 1). Должен быть уникальным. |
| `resource` | string | Yes | Имя файла ресурса (видео или изображение). Поддерживаемые форматы: .mp4, .jpg, .png. |
| `time_start` | string | Yes | Время начала фрагмента в формате `MM:SS` или `HH:MM:SS`. Для изображений: `00:00`. |
| `time_end` | string | Yes | Время окончания фрагмента в формате `MM:SS` или `HH:MM:SS`. Для изображений: желаемая длительность. |
| `start_effect` | string \| null | No | Эффект в начале клипа. Возможные значения: `"fade_in"`, `"slide_in"`, `null`. |
| `start_duration` | string \| null | No | Длительность начального эффекта. Формат: `"Xs"` где X - число секунд. |
| `effect_during` | string \| null | No | Эффект, применяемый во время воспроизведения. Возможные значения: `"grayscale"`, `"sepia"`, `null`. |
| `end_effect` | string \| null | No | Эффект в конце клипа. Возможные значения: `"fade_out"`, `"slide_out"`, `null`. |
| `end_duration` | string \| null | No | Длительность конечного эффекта. Формат: `"Xs"` где X - число секунд. |
| `description` | string \| null | No | Описание клипа (для документации, не влияет на обработку). |

## Field Syntax

### Time Format

Временные метки используют формат:
- `MM:SS` - минуты:секунды (например, "00:05" = 5 секунд)
- `HH:MM:SS` - часы:минуты:секунды (например, "01:30:00" = 1.5 часа)

### Duration Format

Длительности эффектов:
- `"Xs"` - X секунд (например, "3s" = 3 секунды)

### Effect Names

Стандартизированные имена эффектов (snake_case):
- Начальные: `fade_in`, `slide_in`, `zoom_in`
- Конечные: `fade_out`, `slide_out`, `zoom_out`
- Во время: `grayscale`, `sepia`, `blur`, `speed_up`, `slow_down`

## Complete Example

```json
{
  "name": "cyborgs",
  "resources_dir": "Video_01",
  "timeline": [
    {
      "id": 1,
      "resource": "clip_01.mp4",
      "time_start": "00:00",
      "time_end": "00:05",
      "start_effect": "fade_in",
      "start_duration": "3s",
      "effect_during": null,
      "end_effect": null,
      "end_duration": null,
      "description": "Opening scene with fade"
    },
    {
      "id": 2,
      "resource": "clip_02.mp4",
      "time_start": "00:00",
      "time_end": "00:07",
      "start_effect": null,
      "start_duration": null,
      "effect_during": null,
      "end_effect": "fade_out",
      "end_duration": "3s",
      "description": "Main content with fade out"
    }
  ],
  "result_file": "video_res_01.mp4"
}
```

## Validation Rules

1. **id**: Должны быть последовательными (1, 2, 3...) без пропусков
2. **resource**: Файл должен существовать в `resources_dir`
3. **time_start**: Должен быть меньше `time_end`
4. **start_effect** + **start_duration**: Если указан эффект, должна быть указана длительность
5. **end_effect** + **end_duration**: Если указан эффект, должна быть указана длительность
6. **timeline**: Максимум 10 клипов для MVP версии
7. **result_file**: Должен иметь расширение .mp4

## Notes

- Для изображений поля `time_start` и `time_end` определяют длительность показа
- Изображения автоматически масштабируются до 1920x1080 (landscape)
- Если эффект не указан (null), он не применяется
- При отсутствии эффектов видео просто склеивается последовательно
