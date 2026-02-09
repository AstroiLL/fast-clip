# Fast-Clip Developer Documentation

## Архитектура

Fast-Clip состоит из трех основных компонентов:

1. **main.py** - ядро системы сборки видео
2. **convert_script.py** - конвертер между форматами MD и JSON
3. **Pydantic модели** - валидация и структура данных

## main.py

### Основные компоненты

#### Константы и конфигурация

```python
SUPPORTED_FORMATS = {"mp4", "avi", "mov", "mkv"}
FORMAT_CODECS = {
    "mp4": "libx264",
    "avi": "mpeg4",
    "mov": "libx264",
    "mkv": "libx264"
}

RESOLUTIONS = {
    "2160p": 2160,
    "1440p": 1440,
    "1080p": 1080,
    "720p": 720,
    "480p": 480
}

ORIENTATION_RATIOS = {
    "landscape": 16/9,
    "portrait": 9/16,
    "square": 1/1
}
```

#### Классы данных (Pydantic)

**TimelineItem**
```python
class TimelineItem(BaseModel):
    id: int                    # Порядковый номер (>=1)
    resource: str              # Имя файла
    time_start: str            # Время начала (MM:SS или HH:MM:SS)
    time_end: str              # Время окончания
    start_effect: Optional[str] = None      # fade_in
    start_duration: Optional[str] = None    # "3s"
    effect_during: Optional[str] = None     # grayscale, sepia
    end_effect: Optional[str] = None        # fade_out
    end_duration: Optional[str] = None      # "3s"
    description: Optional[str] = None
```

**ScriptConfig**
```python
class ScriptConfig(BaseModel):
    name: str
    resources_dir: str
    timeline: List[TimelineItem]
    result_file: str
    output_format: Optional[str] = None     # mp4, avi, mov, mkv
    resolution: Optional[str] = "1080p"     # 2160p, 1440p, 1080p, 720p, 480p
    orientation: Optional[str] = "landscape" # landscape, portrait, square
    
    # Валидация: максимум 10 клипов
    @model_validator(mode='after')
    def validate_timeline(self):
        if len(self.timeline) > 10:
            raise ValueError("Timeline cannot have more than 10 clips")
```

#### Методы валидации

**get_output_format()** → `Optional[str]`
- Проверяет формат выходного файла
- Возвращает None если формат некорректный
- Выводит предупреждение

**get_resolution()** → `Optional[int]`
- Проверяет разрешение
- Возвращает высоту в пикселях или None
- Выводит предупреждение при некорректном значении

**get_orientation()** → `Optional[str]`
- Проверяет ориентацию
- Возвращает None если не указана или некорректная
- Вызывающий код должен определить из первого клипа

#### Вспомогательные функции

**parse_time(time_str: str)** → `float`
- Конвертирует MM:SS или HH:MM:SS в секунды
- Поддерживает форматы: "00:05", "01:30:00"

**parse_duration(duration_str: Optional[str])** → `float`
- Конвертирует "3s" в 3.0
- Возвращает 0.0 если None

**detect_orientation_from_size(width: int, height: int)** → `str`
- Определяет ориентацию по размерам видео
- Логика:
  - aspect_ratio > 1.1 → "landscape"
  - aspect_ratio < 0.9 → "portrait"
  - иначе → "square"

**calculate_target_size(resolution_height: Optional[int], orientation: Optional[str])** → `Optional[Tuple[int, int]]`
- Вычисляет размеры контейнера
- Возвращает None если resolution_height или orientation is None
- Корректирует размеры до четных (требование кодеков)

#### Основная логика обработки

**fit_video_to_container(clip: VideoFileClip, container_size: Tuple[int, int])** → `VideoClip`

Алгоритм вписывания видео:

1. Получает размеры контейнера и клипа
2. Вычисляет масштаб: `min(container_width / clip_width, container_height / clip_height)`
3. Масштабирует видео пропорционально
4. Корректирует до четных размеров
5. Создает черный фон (ColorClip)
6. Центрирует видео на фоне
7. Возвращает CompositeVideoClip

**load_and_process_clip(resources_dir: Path, item: TimelineItem, target_size: Optional[Tuple[int, int]])** → `Union[VideoFileClip, VideoClip]`

Процесс обработки клипа:

1. Проверяет существование файла
2. Загружает VideoFileClip
3. Извлекает subclip (time_start → time_end)
4. Если target_size указан:
   - Вызывает fit_video_to_container()
   - Оборачивает в try/except с fallback на оригинал
5. Применяет эффекты:
   - FadeIn если start_effect == "fade_in"
   - FadeOut если end_effect == "fade_out"
6. Возвращает обработанный клип

**assemble_video(config: ScriptConfig, script_dir: Path)** → `Path`

Основной пайплайн сборки:

1. **Определение параметров:**
   - Получает resolution_height из config.get_resolution()
   - Получает orientation из config.get_orientation()
   - Если orientation is None:
     - Загружает первый клип временно
     - Определяет ориентацию через detect_orientation_from_size()
     - Выводит информацию: "Detected orientation from first clip: portrait (1080x1920)"

2. **Вычисление целевого размера:**
   - Вызывает calculate_target_size()
   - Выводит: "Target size: 1080x1920 (portrait)"

3. **Обработка клипов:**
   - Цикл по timeline
   - Для каждого элемента вызывает load_and_process_clip()
   - Собирает список обработанных клипов

4. **Конкатенация:**
   - Объединяет все клипы через concatenate_videoclips()

5. **Определение пути выхода:**
   - Использует result_file из конфигурации
   - Меняет расширение если указан output_format
   - Добавляет авто-нумерацию если файл существует (output_001.mp4)

6. **Запись файла:**
   - Определяет кодек по формату
   - Вызывает write_videofile() с codec

7. **Очистка ресурсов:**
   - Закрывает все клипы через clip.close()

#### Точка входа

**main()**

CLI интерфейс:
- Принимает один аргумент: путь к JSON-скрипту
- Загружает и парсит JSON
- Создает ScriptConfig
- Выводит информацию о проекте
- Вызывает assemble_video()
- Выводит путь к результату

## convert_script.py

### Назначение

Конвертер между форматами:
- Markdown → JSON
- JSON → Markdown

### Классы

Используют те же модели TimelineItem и ScriptConfig, но с упрощенной валидацией (без Field constraints).

### Основные функции

#### md_to_json(md_path: Path) → ScriptConfig

Парсинг Markdown-скрипта:

1. **Парсинг заголовков:**
   - Регулярные выражения для: name, resources_dir, result_file
   - Опциональные: output_format, resolution, orientation
   - Проверка обязательных полей

2. **Парсинг таблицы:**
   - Ищет строку с `| # | Resources |`
   - Пропускает разделитель `| --- | --- |`
   - Парсит каждую строку таблицы:
     - Разбивает по `|`
     - Извлекает 8+ колонок
     - Парсит time_start/time_end из колонки "Time"
     - Конвертирует эффекты: "fade in" → "fade_in"
     - Конвертирует длительность: "3 sec" → "3s"

3. **Возвращает ScriptConfig**

#### json_to_md(config: ScriptConfig) → str

Генерация Markdown:

1. **Заголовки:**
   - Всегда: name, resources_dir
   - Условно: output_format, resolution (если не 1080p), orientation (если не landscape)

2. **Таблица:**
   - Заголовок с колонками
   - Разделитель
   - Строки для каждого элемента timeline
   - Обратная конвертация: "fade_in" → "fade in", "3s" → "3 sec"

3. **Возвращает строку Markdown**

#### convert_file(input_path: Path, output_path: Optional[Path]) → Path

Универсальная функция конвертации:
- Определяет направление по расширению (.md или .json)
- Вызывает соответствующую функцию
- Записывает результат
- Возвращает путь к выходному файлу

## Процессы и потоки данных

### Поток сборки видео

```
script.json
    ↓
ScriptConfig (валидация Pydantic)
    ↓
main.assemble_video()
    ↓
[Определение ориентации] → (из файла или из первого клипа)
    ↓
[Вычисление target_size]
    ↓
[Цикл по timeline]
    ├─ load_and_process_clip()
    │   ├─ VideoFileClip (загрузка)
    │   ├─ subclip() (обрезка по времени)
    │   ├─ fit_video_to_container() (масштабирование)
    │   ├─ with_effects() (эффекты)
    │   └─ return clip
    ↓
concatenate_videoclips()
    ↓
write_videofile()
    ↓
cleanup (close clips)
    ↓
output.mp4
```

### Поток конвертации MD → JSON

```
script.md
    ↓
md_to_json()
    ├─ re.search() (парсинг заголовков)
    ├─ split('\n') (построчный разбор)
    ├─ split('|') (разбор таблицы)
    └─ parse_md_effect(), parse_md_duration() (конвертация)
    ↓
ScriptConfig
    ↓
json.dumps()
    ↓
script.json
```

## Обработка ошибок

### Graceful degradation

Все валидационные методы возвращают None при ошибках:
- `get_output_format()` → None → используется исходный формат
- `get_resolution()` → None → используется исходное разрешение
- `get_orientation()` → None → определяется из первого клипа

### Исключения

**FileNotFoundError**
- В load_and_process_clip() если видео не найдено
- Логируется и пробрасывается выше

**ValueError**
- В parse_time() при некорректном формате времени
- В model_validator при >10 клипов

**Exception**
- В fit_video_to_container() при ошибках moviepy
- Перехватывается, логируется, используется оригинальный клип

## Оптимизации

### Ресурсы

- moviepy загружает видео в память
- Каждый клип закрывается через clip.close()
- Финальное видео также закрывается

### Производительность

- Все операции последовательные
- Нет параллельной обработки клипов
- Ограничение в 10 клипов защищает от переполнения памяти

## Расширение функциональности

### Добавление нового эффекта

1. Добавить в документацию JSON_SCRIPT_FORMAT.md
2. В load_and_process_clip() добавить обработку:
```python
if item.effect_during == "new_effect":
    clip = clip.with_effects([vfx.NewEffect()])
```

### Добавление нового формата

1. Добавить в SUPPORTED_FORMATS
2. Добавить кодек в FORMAT_CODECS
3. Обновить документацию

### Добавление нового разрешения

1. Добавить в RESOLUTIONS
2. Обновить документацию

## Тестирование

### Ручное тестирование

```bash
# Тест без ориентации (автоопределение)
python main.py test_no_orientation.json

# Тест с квадратным форматом
python main.py test_square.json

# Тест с некорректными параметрами
python main.py test_invalid.json
```

### Проверка выхода

```bash
# Проверить размеры видео
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 output.mp4
```

## Зависимости

- **moviepy** (>=2.0.0) - обработка видео
- **pydantic** (>=2.0.0) - валидация данных
- **ffmpeg** - moviepy использует ffmpeg внутри

## Известные ограничения

- Максимум 10 клипов в timeline
- Нет поддержки аудио-эффектов
- Нет поддержки текстовых наложений
- Нет поддержки переходов между клипами (только эффекты на клипах)
