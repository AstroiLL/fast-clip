# Fast-Clip

Инструмент для автоматической сборки видео из фрагментов по JSON-скриптам.

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/AstroiLL/fast-clip.git
cd fast-clip

# Установить зависимости
uv sync
```

## Быстрый старт

### 1. Создайте структуру проекта

```
my_project/
├── Video_01/          # Папка с исходными видео
│   ├── clip_01.mp4
│   └── clip_02.mp4
└── script.json        # Скрипт сборки
```

### 2. Создайте скрипт (JSON)

```json
{
  "name": "my_video",
  "resources_dir": "Video_01",
  "timeline": [
    {
      "id": 1,
      "resource": "clip_01.mp4",
      "time_start": "00:00",
      "time_end": "00:05",
      "start_effect": "fade_in",
      "start_duration": "3s"
    },
    {
      "id": 2,
      "resource": "clip_02.mp4",
      "time_start": "00:00",
      "time_end": "00:07",
      "end_effect": "fade_out",
      "end_duration": "3s"
    }
  ],
  "result_file": "output.mp4",
  "output_format": "mp4",
  "resolution": "1080p",
  "orientation": "landscape"
}
```

### 3. Запустите сборку

```bash
uv run python main.py script.json
```

Результат: `output.mp4`

## Использование

### Запуск сборки видео

```bash
# Базовый запуск
uv run python main.py script.json

# Пример
uv run python main.py script_video_01.json
```

### Конвертация скриптов

Конвертируйте между форматами MD и JSON:

```bash
# MD → JSON
uv run python convert_script.py script.md

# JSON → MD
uv run python convert_script.py script.json

# С указанием выходного файла
uv run python convert_script.py input.md output.json
```

### Проверка скрипта перед сборкой

Проверьте скрипт на ошибки перед запуском:

```bash
# Молчаливый режим (только код возврата)
uv run python check_script.py script.json

# Подробный режим с выводом всех проверок
uv run python check_script.py -v script.json
```

Проверка включает:
- Корректность JSON-формата
- Наличие всех обязательных полей
- Существование исходных видео
- Корректность временных меток
- Проверку эффектов и их длительностей
- Соответствие параметров допустимым значениям

**Коды возврата:**
- `0` - проверка пройдена
- `1` - есть ошибки
- `2` - неверные аргументы

## Формат скрипта (JSON)

### Обязательные поля

| Поле | Описание | Пример |
|------|----------|--------|
| `name` | Название проекта | `"my_video"` |
| `resources_dir` | Папка с исходниками | `"Video_01"` |
| `timeline` | Массив клипов | `[...]` |
| `result_file` | Имя выходного файла | `"output.mp4"` |

### Опциональные поля

| Поле | Описание | Допустимые значения | По умолчанию |
|------|----------|---------------------|--------------|
| `output_format` | Формат выходного файла | `"mp4"`, `"avi"`, `"mov"`, `"mkv"` | Исходный формат |
| `resolution` | Разрешение видео | `"2160p"`, `"1440p"`, `"1080p"`, `"720p"`, `"480p"` | `"1080p"` |
| `orientation` | Ориентация | `"landscape"`, `"portrait"`, `"square"` | Определяется из первого клипа |

### Timeline (элементы)

```json
{
  "id": 1,                      // Порядковый номер
  "resource": "video.mp4",      // Имя файла
  "time_start": "00:00",        // Начало (MM:SS)
  "time_end": "00:05",          // Конец (MM:SS)
  "start_effect": "fade_in",    // Эффект в начале
  "start_duration": "3s",       // Длительность эффекта
  "end_effect": "fade_out",     // Эффект в конце
  "end_duration": "3s",
  "description": "Описание"     // Описание (опционально)
}
```

### Эффекты

**Начальные:**
- `fade_in` - появление

**Конечные:**
- `fade_out` - исчезновение

## Формат скрипта (Markdown)

```markdown
## name: my_video
## resources_dir: Video_01
## output_format: mp4
## resolution: 1080p
## orientation: landscape

| # | Resources | Time | Start_Effect | Start_Duration | Effect_During | End_Effect | End_Duration | Description
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | clip_01.mp4 | 00:00 - 00:05 | fade in | 3 sec | | | | |
| 2 | clip_02.mp4 | 00:00 - 00:07 | | | | fade out | 3 sec | |

## result_file: output.mp4
```

## Разрешение и ориентация

### Разрешение (resolution)

Указывает базовую высоту видео:
- `2160p` - 4K (2160px)
- `1440p` - 2K (1440px)
- `1080p` - Full HD (1080px)
- `720p` - HD (720px)
- `480p` - SD (480px)

### Ориентация (orientation)

Определяет пропорции контейнера:

- **landscape** - горизонтальная (16:9)
  - 1080p → 1920x1080
- **portrait** - вертикальная (9:16)
  - 1080p → 1080x1920
- **square** - квадрат (1:1)
  - 1080p → 1080x1080

**Автоопределение:** Если не указана или некорректная, ориентация определяется из первого клипа.

### Вписывание видео

Видео масштабируется пропорционально до максимального размера в контейнере без искажений и обрезки. Пустые области заполняются черным цветом (letterboxing/pillarboxing).

**Пример:**
- Исходное: 1920x1080 (16:9)
- Контейнер: 1080x1080 (square)
- Результат: видео 1080x608 (сохраняя 16:9) вписано в квадрат с черными полосами сверху и снизу

## Обработка ошибок

При некорректных параметрах программа выводит предупреждение и использует значения по умолчанию:

- **Некорректный формат:** → используется исходный формат
- **Некорректное разрешение:** → используется исходное разрешение
- **Некорректная ориентация:** → определяется из первого клипа

## Примеры

### Пример 1: Базовая сборка

```json
{
  "name": "simple",
  "resources_dir": "Video_01",
  "timeline": [
    {"id": 1, "resource": "clip.mp4", "time_start": "00:00", "time_end": "00:10"}
  ],
  "result_file": "output.mp4"
}
```

### Пример 2: С эффектами

```json
{
  "name": "with_effects",
  "resources_dir": "Video_01",
  "timeline": [
    {
      "id": 1,
      "resource": "clip.mp4",
      "time_start": "00:00",
      "time_end": "00:10",
      "start_effect": "fade_in",
      "start_duration": "2s",
      "end_effect": "fade_out",
      "end_duration": "2s"
    }
  ],
  "result_file": "output.mp4"
}
```

### Пример 3: Квадратное видео для Instagram

```json
{
  "name": "instagram",
  "resources_dir": "Video_01",
  "timeline": [
    {"id": 1, "resource": "clip.mp4", "time_start": "00:00", "time_end": "00:15"}
  ],
  "result_file": "instagram.mp4",
  "resolution": "1080p",
  "orientation": "square"
}
```

## Ограничения

- Максимум 10 клипов в timeline
- Поддерживаемые форматы: MP4, AVI, MOV, MKV
- Временные метки: MM:SS или HH:MM:SS

## Лицензия

MIT
