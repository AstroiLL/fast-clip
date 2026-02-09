# Video Effects Guide

Руководство по использованию видео-эффектов MoviePy в Fast-Clip

## Быстрый справочник

| Эффект | Категория | Описание | Сложность |
|--------|-----------|----------|-----------|
| **CrossFadeIn** | Переход | Плавное появление клипа | ⭐⭐ |
| **CrossFadeOut** | Переход | Плавное исчезновение клипа | ⭐⭐ |
| **BlackAndWhite** | Цвет | Чёрно-белое изображение | ⭐ |
| **InvertColors** | Цвет | Инверсия цветов (негатив) | ⭐ |
| **GammaCorrection** | Цвет | Коррекция гаммы | ⭐⭐ |
| **LumContrast** | Цвет | Яркость и контраст | ⭐⭐ |
| **MultiplyColor** | Цвет | Умножение цветов | ⭐⭐ |
| **Resize** | Геометрия | Изменение размера | ⭐⭐ |
| **Rotate** | Геометрия | Поворот клипа | ⭐⭐⭐ |
| **Crop** | Геометрия | Обрезка кадра | ⭐⭐ |
| **MirrorX** | Геометрия | Отражение по горизонтали | ⭐ |
| **MirrorY** | Геометрия | Отражение по вертикали | ⭐ |
| **MultiplySpeed** | Время | Изменение скорости | ⭐⭐ |
| **Freeze** | Время | Заморозка кадра | ⭐⭐ |
| **Loop** | Время | Цикличное повторение | ⭐ |
| **Painting** | Визуальные | Эффект живописи | ⭐⭐⭐ |
| **HeadBlur** | Визуальные | Размытие области | ⭐⭐⭐ |
| **Blink** | Визуальные | Мигание | ⭐ |
| **Scroll** | Движение | Прокрутка изображения | ⭐⭐⭐ |
| **SlideIn** | Движение | Выезд с края экрана | ⭐⭐⭐ |
| **SlideOut** | Движение | Выезд за пределы экрана | ⭐⭐⭐ |
| **Margin** | Композитинг | Добавление полей | ⭐ |

## Общий синтаксис применения эффектов

```python
from moviepy import VideoFileClip, vfx

# Загрузка клипа
clip = VideoFileClip("video.mp4")

# Применение одного эффекта
clip = clip.with_effects([vfx.EffectName(parameters)])

# Применение нескольких эффектов
clip = clip.with_effects([
    vfx.EffectName1(params1),
    vfx.EffectName2(params2),
])

# Экспорт результата
clip.write_videofile("output.mp4")
```

---

## Переходы (Transitions)

### CrossFadeIn

**Описание:** Плавное появление клипа из прозрачности (или другого клипа). Клип постепенно становится видимым.

**Параметры:**
- `duration` (float): Длительность перехода в секундах

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip1 = VideoFileClip("intro.mp4")
clip2 = VideoFileClip("main.mp4")

# Применяем CrossFadeIn ко второму клипу
clip2 = clip2.with_effects([vfx.CrossFadeIn(1.0)])

# Составляем композицию с перекрытием для эффекта
final = CompositeVideoClip([
    clip1,
    clip2.with_start(clip1.duration - 1.0)  # Перекрытие на 1 секунду
])
```

**Особенности:**
- Требует CompositeVideoClip для работы
- Клип должен иметь ту же размерность, что и вся композиция

---

### CrossFadeOut

**Описание:** Плавное исчезновение клипа в прозрачность.

**Параметры:**
- `duration` (float): Длительность перехода в секундах

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

# Применяем CrossFadeOut в конце
clip = clip.with_effects([vfx.CrossFadeOut(1.5)])

# Клип будет плавно исчезать последние 1.5 секунды
```

**Особенности:**
- Работает как с CompositeVideoClip, так и с отдельными клипами

---

## Цветовые эффекты (Color Effects)

### BlackAndWhite

**Описание:** Преобразует видео в чёрно-белое (оттенки серого).

**Параметры:**
- `RGB` (list или str): Веса каналов [R, G, B] или "CRT_phosphor" для стандартных весов
- `preserve_luminosity` (bool): Сохранять сумму весов = 1

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

# Простое чёрно-белое
clip_bw = clip.with_effects([vfx.BlackAndWhite()])

# С весами каналов (красный канал преобладает)
clip_bw_custom = clip.with_effects([
    vfx.BlackAndWhite(RGB=[2, 1, 1], preserve_luminosity=True)
])

# Стандартные веса для CRT мониторов
clip_bw_crt = clip.with_effects([
    vfx.BlackAndWhite(RGB="CRT_phosphor")
])
```

**Особенности:**
- "CRT_phosphor" использует веса [0.2125, 0.7154, 0.0721]
- Можно создать эффект "красного фильтра" или "синего фильтра"

---

### InvertColors

**Описание:** Инвертирует все цвета (негатив). Чёрный становится белым, зелёный — фиолетовым и т.д.

**Параметры:**
- Нет параметров

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

# Применяем инверсию цветов
clip_negative = clip.with_effects([vfx.InvertColors()])
```

**Особенности:**
- Для масок инвертирует значения (1-v вместо 255-v)
- Быстрый и лёгкий эффект

---

### GammaCorrection

**Описание:** Коррекция гаммы изображения. Полезно для исправления слишком тёмных или светлых видео.

**Параметры:**
- `gamma` (float): Значение гаммы
  - gamma < 1.0: Изображение становится светлее
  - gamma = 1.0: Без изменений
  - gamma > 1.0: Изображение становится темнее

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

# Осветление (gamma < 1)
clip_bright = clip.with_effects([vfx.GammaCorrection(gamma=0.5)])

# Затемнение (gamma > 1)
clip_dark = clip.with_effects([vfx.GammaCorrection(gamma=2.0)])

# Нормализация недоэкспонированного видео
clip_normalized = clip.with_effects([vfx.GammaCorrection(gamma=0.7)])
```

**Особенности:**
- Нелинейное изменение яркости
- Полезно для коррекции экспозиции

---

### LumContrast

**Описание:** Коррекция яркости (luminosity) и контраста изображения.

**Параметры:**
- `lum` (float): Смещение яркости (0 — без изменений)
- `contrast` (float): Коэффициент контраста (0 — без изменений)
- `contrast_threshold` (float): Точка отсчёта для контраста (по умолчанию 127)

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

# Увеличение яркости
clip_bright = clip.with_effects([vfx.LumContrast(lum=30)])

# Увеличение контраста
clip_contrast = clip.with_effects([vfx.LumContrast(contrast=0.3)])

# Комбинация: ярче и контрастнее
clip_enhanced = clip.with_effects([
    vfx.LumContrast(lum=20, contrast=0.4)
])

# Снижение контраста
clip_flat = clip.with_effects([vfx.LumContrast(contrast=-0.2)])
```

**Особенности:**
- Линейное изменение яркости (в отличие от GammaCorrection)
- Значения lum обычно в диапазоне -100 до 100
- Значения contrast обычно в диапазоне -1.0 до 1.0

---

### MultiplyColor

**Описание:** Умножает все цвета на заданный коэффициент. Увеличивает или уменьшает общую яркость.

**Параметры:**
- `factor` (float): Коэффициент умножения
  - factor > 1.0: Увеличение яркости
  - factor = 1.0: Без изменений
  - factor < 1.0: Уменьшение яркости

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

# Увеличение яркости в 1.5 раза
clip_brighter = clip.with_effects([vfx.MultiplyColor(factor=1.5)])

# Затемнение до 60%
clip_darker = clip.with_effects([vfx.MultiplyColor(factor=0.6)])

// Драматичное высветление
clip_dramatic = clip.with_effects([vfx.MultiplyColor(factor=2.0)])
```

**Особенности:**
- Значения ограничиваются 255 (не происходит переполнения)
- Простое линейное изменение яркости

---

## Геометрические трансформации

### Resize

**Описание:** Изменяет размеры видеоклипа.

**Параметры:**
- `newsize` (tuple, float, или function): Новый размер
  - tuple (width, height): Конкретные размеры в пикселях
  - float: Масштабный коэффициент (0.5 = 50%)
  - function: Функция lambda t: scale(t) для динамического изменения
- `width` (int): Только ширина (высота вычисляется автоматически)

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

# До конкретных размеров
clip_resized = clip.with_effects([vfx.Resize((1920, 1080))])

# Только ширина (высота пропорциональна)
clip_width = clip.with_effects([vfx.Resize(width=800)])

// Масштабирование (60% от оригинала)
clip_scaled = clip.with_effects([vfx.Resize(0.6)])

// Динамическое изменение размера (эффект "пульсации")
clip_dynamic = clip.with_effects([
    vfx.Resize(lambda t: 1 + 0.1 * t)  # Постепенное увеличение
])
```

**Особенности:**
- Использует PIL для ресайза
- При указании только width сохраняет пропорции
- Можно использовать для создания эффекта зума

---

### Rotate

**Описание:** Поворачивает клип на заданный угол.

**Параметры:**
- `angle` (float): Угол поворота
- `unit` (str): Единицы измерения угла — "deg" (градусы) или "rad" (радианы)
- `resample` (str): Фильтр ресемплинга — "nearest", "bilinear", "bicubic"
- `expand` (bool): Расширить изображение, чтобы вместить весь повёрнутый клип
- `center` (tuple): Центр вращения (x, y)
- `translate` (tuple): Смещение после поворота (x, y)
- `bg_color` (tuple): Цвет фона для расширенных областей

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Простой поворот на 45 градусов
clip_rotated = clip.with_effects([vfx.Rotate(angle=45)])

// Поворот с расширением
clip_expanded = clip.with_effects([
    vfx.Rotate(angle=30, expand=True, bg_color=(0, 0, 0))
])

// Вращение вокруг центра
clip_centered = clip.with_effects([
    vfx.Rotate(angle=90, center=(clip.w/2, clip.h/2))
])

// Поворот в радианах
clip_rad = clip.with_effects([vfx.Rotate(angle=3.14159, unit="rad")])
```

**Особенности:**
- При углах 90, 180, 270 градусов использует оптимизированные транспозиции
- Может создавать чёрные поля при rotate не кратном 90°
- Bicubic даёт лучшее качество, но медленнее

---

### Crop

**Описание:** Обрезает клип до заданного прямоугольника.

**Параметры:**
- `x1` (int): Левая координата
- `y1` (int): Верхняя координата
- `x2` (int): Правая координата
- `y2` (int): Нижняя координата
- `width` (int): Ширина области (альтернатива x2)
- `height` (int): Высота области (альтернатива y2)
- `x_center` (int): X-координата центра области
- `y_center` (int): Y-координата центра области

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Обрезка по координатам
clip_cropped = clip.with_effects([vfx.Crop(x1=100, y1=50, x2=500, y2=400)])

// Обрезка с указанием ширины и высоты
clip_sized = clip.with_effects([vfx.Crop(x1=100, y1=50, width=400, height=350)])

// Центрированная обрезка
clip_center = clip.with_effects([
    vfx.Crop(x_center=clip.w/2, y_center=clip.h/2, width=300, height=200)
])

// Удаление чёрных полос сверху
clip_no_bars = clip.with_effects([vfx.Crop(y1=50)])
```

**Особенности:**
- Можно комбинировать параметры (например, x_center + width + y1)
- Если не указаны x1/x2, используются края клипа
- Полезно для удаления чёрных полос letterbox

---

### MirrorX

**Описание:** Отражает клип по горизонтали (зеркальное отражение слева направо).

**Параметры:**
- `apply_to` (str или list): Применять ли к маске (по умолчанию "mask")

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Зеркальное отражение
clip_mirrored = clip.with_effects([vfx.MirrorX()])
```

**Особенности:**
- Быстрый эффект, изменяет только порядок пикселей
- Полезно для исправления "зеркальных" видео

---

### MirrorY

**Описание:** Отражает клип по вертикали (переворачивает вверх ногами).

**Параметры:**
- `apply_to` (str или list): Применять ли к маске (по умолчанию "mask")

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Переворот вверх ногами
clip_flipped = clip.with_effects([vfx.MirrorY()])
```

**Особенности:**
- Быстрый эффект
- Полезно для исправления перевернутых видео

---

## Временные эффекты (Time Effects)

### MultiplySpeed

**Описание:** Изменяет скорость воспроизведения клипа.

**Параметры:**
- `factor` (float): Коэффициент скорости
  - factor > 1.0: Ускорение
  - factor = 1.0: Нормальная скорость
  - factor < 1.0: Замедление

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Ускорение в 2 раза (timelapse)
clip_fast = clip.with_effects([vfx.MultiplySpeed(factor=2.0)])

// Замедление в 2 раза (slow motion)
clip_slow = clip.with_effects([vfx.MultiplySpeed(factor=0.5)])

// Экстремальное ускорение
clip_hyper = clip.with_effects([vfx.MultiplySpeed(factor=10.0)])
```

**Особенности:**
- Изменяет длительность клипа
- При замедлении пропускаются кадры (не интерполируются)

---

### Freeze

**Описание:** Замораживает кадр на заданное время.

**Параметры:**
- `t` (float или str): Время заморозки в секундах или "end" для конца клипа
- `freeze_duration` (float): Длительность заморозки
- `total_duration` (float): Общая длительность (альтернатива freeze_duration)
- `padding_end` (float): Отступ от конца (когда t="end")
- `update_start_end` (bool): Обновлять ли свойства start/end

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Заморозка на 3 секунды в начале
clip_freeze_start = clip.with_effects([
    vfx.Freeze(t=0, freeze_duration=3)
])

// Заморозка кадра на 5 секунде на 2 секунды
clip_freeze_mid = clip.with_effects([
    vfx.Freeze(t=5, freeze_duration=2)
])

// Заморозка последнего кадра на 3 секунды
clip_freeze_end = clip.with_effects([
    vfx.Freeze(t="end", freeze_duration=3)
])
```

**Особенности:**
- Создаёт статичный кадр указанной длительности
- Полезно для акцента на важный момент

---

### Loop

**Описание:** Циклически повторяет клип.

**Параметры:**
- `n` (int): Количество повторений (None = бесконечно, но не используется для записи)

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("short_clip.mp4")

// Повторить 3 раза
clip_looped = clip.with_effects([vfx.Loop(n=3)])
```

**Особенности:**
- Используется для создания GIF или фоновых анимаций
- n=None создаёт бесконечный цикл (не записывается в файл)

---

## Визуальные эффекты

### Painting

**Описание:** Преобразует видео в стиль живописи/рисунка.

**Параметры:**
- `saturation` (float): Коэффициент насыщенности (по умолчанию 1.8)
- `black` (float): Уровень чёрного (по умолчанию 0.006)

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Эффект живописи
clip_painting = clip.with_effects([vfx.Painting()])

// С усиленной насыщенностью
clip_art = clip.with_effects([
    vfx.Painting(saturation=2.5, black=0.01)
])
```

**Особенности:**
- Использует PIL для обработки
- Создаёт эффект масляной живописи
- Настройка saturation влияет на выраженность эффекта

---

### HeadBlur

**Описание:** Размывает движущуюся область в кадре (например, лицо для анонимизации).

**Параметры:**
- `fx` (callable): Функция x(t) — X-координата центра размытия
- `fy` (callable): Функция y(t) — Y-координата центра размытия
- `radius` (float): Радиус размытия
- `intensity` (float): Интенсивность размытия (по умолчанию 2*radius/3)

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Размытие движущейся области (например, лицо)
// Предположим, лицо движется слева направо
clip_blurred = clip.with_effects([
    vfx.HeadBlur(
        fx=lambda t: 100 + 50 * t,  # X координата
        fy=lambda t: 200,           # Y координата
        radius=50,
        intensity=30
    )
])
```

**Особенности:**
- Требует отслеживания позиции объекта
- Использует GaussianBlur
- Полезно для цензуры или акцента

---

### Blink

**Описание:** Создаёт эффект мигания клипа.

**Параметры:**
- `d` (float): Длительность одного цикла мигания
- `ns` (int): Количество миганий (по умолчанию 1)

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Мигание каждые 0.5 секунды
clip_blink = clip.with_effects([vfx.Blink(d=0.5)])

// Три мигания
clip_blink_3 = clip.with_effects([vfx.Blink(d=0.3, ns=3)])
```

**Особенности:**
- Простой эффект для привлечения внимания
- Можно комбинировать с другими эффектами

---

## Эффекты движения (Motion Effects)

### Scroll

**Описание:** Прокручивает изображение по горизонтали или вертикали.

**Параметры:**
- `w` (int): Ширина финального клипа
- `h` (int): Высота финального клипа
- `x_speed` (float): Скорость прокрутки по X
- `y_speed` (float): Скорость прокрутки по Y
- `x_start` (int): Начальная позиция X
- `y_start` (int): Начальная позиция Y
- `apply_to` (str): Применять ли к маске

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Горизонтальная прокрутка (как бегущая строка)
clip_scroll_h = clip.with_effects([
    vfx.Scroll(x_speed=100, w=clip.w, h=clip.h)
])

// Вертикальная прокрутка (как титры)
clip_scroll_v = clip.with_effects([
    vfx.Scroll(y_speed=50, w=clip.w, h=clip.h)
])

// Диагональная прокрутка
clip_scroll_diag = clip.with_effects([
    vfx.Scroll(x_speed=30, y_speed=30, w=clip.w, h=clip.h)
])
```

**Особенности:**
- Полезно для создания бегущих строк
- Можно использовать для эффекта "бесконечной" прокрутки

---

### SlideIn

**Описание:** Клип выезжает с одной из сторон экрана.

**Параметры:**
- `duration` (float): Длительность анимации выезда
- `side` (str): Сторона — "left", "right", "top", "bottom"

**Пример использования:**
```python
from moviepy import VideoFileClip, CompositeVideoClip, vfx

clip = VideoFileClip("video.mp4")

// Выезд слева за 1 секунду
clip_slide_left = clip.with_effects([vfx.SlideIn(1.0, "left")])

// Выезд справа
clip_slide_right = clip.with_effects([vfx.SlideIn(1.0, "right")])

// Выезд сверху
clip_slide_top = clip.with_effects([vfx.SlideIn(1.0, "top")])

// Использование в композиции
final = CompositeVideoClip([clip_slide_left.with_effects([vfx.SlideIn(1.0, "left")])])
```

**Особенности:**
- Требует CompositeVideoClip
- Клип должен иметь ту же размерность, что и композиция
- Полезно для создания слайд-шоу

---

### SlideOut

**Описание:** Клип выезжает за пределы экрана.

**Параметры:**
- `duration` (float): Длительность анимации
- `side` (str): Сторона выезда — "left", "right", "top", "bottom"

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Выезд вправо
clip_out = clip.with_effects([vfx.SlideOut(1.0, "right")])
```

**Особенности:**
- Обратный эффект SlideIn
- Полезно для завершения сцен

---

## Композитинг

### Margin

**Описание:** Добавляет поля/рамку вокруг клипа.

**Параметры:**
- `margin_size` (int): Размер полей (или tuple для разных сторон)
- `color` (tuple): Цвет полей (R, G, B)
- `opacity` (float): Прозрачность полей (0-1)

**Пример использования:**
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Белая рамка 20 пикселей
clip_margin = clip.with_effects([
    vfx.Margin(margin_size=20, color=(255, 255, 255))
])

// Разные поля
clip_mixed = clip.with_effects([
    vfx.Margin(margin_size=(10, 20, 30, 40), color=(0, 0, 0))
])

// Прозрачные поля
clip_transparent = clip.with_effects([
    vfx.Margin(margin_size=50, color=(255, 0, 0), opacity=0.5)
])
```

**Особенности:**
- Полезно для создания "полароидного" эффекта
- Можно использовать для выравнивания клипов разных размеров

---

## Комбинирование эффектов

### Пример 1: Эффект "Ken Burns"
```python
from moviepy import ImageClip, vfx

// Плавное приближение и панорамирование
clip = ImageClip("photo.jpg").with_duration(10)
clip = clip.with_effects([
    vfx.Resize(lambda t: 1 + 0.1 * t),  // Постепенное увеличение
    vfx.Crop(  // Панорамирование
        x_center=lambda t: clip.w/2 + 50 * t,
        y_center=clip.h/2,
        width=1920,
        height=1080
    )
])
```

### Пример 2: Виньетка
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Затемнение краёв + цветокоррекция
clip = clip.with_effects([
    vfx.MultiplyColor(factor=0.9),
    vfx.LumContrast(lum=-10, contrast=0.1),
    vfx.FadeIn(0.5),
    vfx.FadeOut(0.5)
])
```

### Пример 3: Слайд-шоу с переходами
```python
from moviepy import ImageClip, CompositeVideoClip, concatenate_videoclips, vfx

clips = []
for i, img_path in enumerate(["img1.jpg", "img2.jpg", "img3.jpg"]):
    clip = ImageClip(img_path).with_duration(3)
    clip = clip.with_effects([
        vfx.SlideIn(0.5, "left"),
        vfx.SlideOut(0.5, "right")
    ])
    clip = clip.with_start(i * 2.5)  // Перекрытие для переходов
    clips.append(clip)

final = CompositeVideoClip(clips)
final = final.with_effects([vfx.CrossFadeIn(0.5)])
```

### Пример 4: Цветовая коррекция
```python
from moviepy import VideoFileClip, vfx

clip = VideoFileClip("video.mp4")

// Профессиональная цветокоррекция
clip = clip.with_effects([
    vfx.GammaCorrection(gamma=0.9),  // Осветление теней
    vfx.LumContrast(contrast=0.15),   // Увеличение контраста
    vfx.MultiplyColor(factor=1.1),    // Небольшое повышение яркости
    vfx.BlackAndWhite(RGB=[1.2, 1.0, 0.8])  // Тёплые тона
])
```

---

## Ограничения и производительность

### Производительность эффектов

| Эффект | Скорость | Нагрузка на CPU | Примечание |
|--------|----------|-----------------|------------|
| MirrorX/Y | ⭐⭐⭐⭐⭐ | Низкая | Только перестановка пикселей |
| InvertColors | ⭐⭐⭐⭐⭐ | Низкая | Простая математическая операция |
| MultiplyColor | ⭐⭐⭐⭐⭐ | Низкая | Умножение массива |
| Resize | ⭐⭐⭐⭐ | Средняя | PIL интерполяция |
| Crop | ⭐⭐⭐⭐ | Низкая | Обрезка массива |
| Rotate | ⭐⭐⭐ | Средняя | PIL rotate |
| HeadBlur | ⭐⭐ | Высокая | Gaussian blur |
| Painting | ⭐⭐ | Высокая | Множество PIL операций |

### Рекомендации по производительности

1. **Избегайте цепочек из множества эффектов** — каждый эффект обрабатывает кадр отдельно
2. **Используйте Resize один раз** — многократное изменение размера ухудшает качество
3. **Предварительно обработайте изображения** — если эффект применяется к статичному изображению
4. **Используйте подходящий resample** — "bicubic" для качества, "nearest" для скорости

### Частые ошибки

**Ошибка 1:** Применение SlideIn к обычному клипу без CompositeVideoClip
```python
// ❌ Неправильно
clip = clip.with_effects([vfx.SlideIn(1.0, "left")])
clip.write_videofile("out.mp4")

// ✅ Правильно
clip = clip.with_effects([vfx.SlideIn(1.0, "left")])
final = CompositeVideoClip([clip])
final.write_videofile("out.mp4")
```

**Ошибка 2:** Неправильный порядок эффектов
```python
// ❌ Resize после Crop может вернуть чёрные полосы
clip = clip.with_effects([vfx.Crop(...), vfx.Resize((1920, 1080))])

// ✅ Сначала Resize, потом Crop
clip = clip.with_effects([vfx.Resize((1920, 1080)), vfx.Crop(...)])
```

**Ошибка 3:** Забытый duration для ImageClip
```python
// ❌ Нет длительности
img = ImageClip("image.jpg")
img = img.with_effects([vfx.FadeIn(1.0)])

// ✅ С длительностью
img = ImageClip("image.jpg").with_duration(5)
img = img.with_effects([vfx.FadeIn(1.0)])
```

---

## Полезные ссылки

- [Официальная документация MoviePy](https://zulko.github.io/moviepy/)
- [Репозиторий на GitHub](https://github.com/Zulko/moviepy)
- [Cookbook с примерами](https://zulko.github.io/moviepy/user_guide/cookbook.html)

---

*Документация создана на основе MoviePy v2.x*
*Последнее обновление: 2024*
