# converters/unit_converter.py
import math  # <-- ДОБАВЛЕНО!

UNITS = {
    'length': {
        'м': 1, 'см': 0.01, 'мм': 0.001, 'км': 1000,
        'дюйм': 0.0254, 'фут': 0.3048, 'миля': 1609.34, 'нм': 1e-9, 'мкм': 1e-6
    },
    'mass': {
        'кг': 1, 'г': 0.001, 'мг': 1e-6, 'т': 1000,
        'фунт': 0.453592, 'унция': 0.0283495, 'центнер': 100
    },
    'temperature': {
        'C': 'celsius', 'F': 'fahrenheit', 'K': 'kelvin'
    },
    'volume': {
        'л': 0.001, 'мл': 1e-6, 'м³': 1,
        'галлон': 0.00378541, 'пинта': 0.000473176, 'баррель': 0.158987
    },
    'speed': {
        'м/с': 1, 'км/ч': 1/3.6, 'узел': 0.514444, 'миля/ч': 0.44704
    },
    'pressure': {
        'Па': 1, 'кПа': 1000, 'МПа': 1e6, 'бар': 1e5, 'атм': 101325, 'мм рт. ст.': 133.322
    },
    'energy': {
        'Дж': 1, 'кДж': 1000, 'МДж': 1e6, 'ккал': 4184, 'эВ': 1.602e-19
    },
    'power': {
        'Вт': 1, 'кВт': 1000, 'МВт': 1e6, 'л.с.': 735.5
    },
    'information': {
        'бит': 1, 'байт': 8, 'КБ': 8*1024, 'МБ': 8*1024**2, 'ГБ': 8*1024**3,
        'ТБ': 8*1024**4, 'ПБ': 8*1024**5
    },
    'frequency': {
        'Гц': 1, 'кГц': 1000, 'МГц': 1e6, 'ГГц': 1e9
    },
    'force': {
        'Н': 1, 'кН': 1000, 'МН': 1e6, 'кгс': 9.80665
    },
    'electric_current': {
        'А': 1, 'мА': 0.001, 'кА': 1000
    },
    'voltage': {
        'В': 1, 'мВ': 0.001, 'кВ': 1000
    },
    'resistance': {
        'Ом': 1, 'кОм': 1000, 'МОм': 1e6
    },
    'capacitance': {
        'Ф': 1, 'мкФ': 1e-6, 'нФ': 1e-9, 'пФ': 1e-12
    },
    'inductance': {
        'Гн': 1, 'мГн': 0.001, 'мкГн': 1e-6
    },
    'magnetic_field': {
        'Тл': 1, 'мТл': 0.001, 'мкТл': 1e-6
    },
    'luminous_flux': {
        'лм': 1, 'клм': 1000
    },
    'illuminance': {
        'лк': 1, 'клк': 1000
    },
    'angle': {
        'рад': 1,
        'град': math.pi / 180,
        'мин': math.pi / (180 * 60),
        'сек': math.pi / (180 * 3600)
    }
}

def convert_unit(category, value, from_unit, to_unit):
    value = float(value)
    if category not in UNITS:
        raise ValueError("Неизвестная категория")

    units = UNITS[category]
    if from_unit not in units or to_unit not in units:
        raise ValueError("Неизвестная единица")

    if category == 'temperature':
        if from_unit == 'C':
            k = value + 273.15
        elif from_unit == 'F':
            k = (value - 32) * 5/9 + 273.15
        elif from_unit == 'K':
            k = value
        else:
            raise ValueError("Неподдерживаемая шкала")

        if to_unit == 'C':
            return k - 273.15
        elif to_unit == 'F':
            return (k - 273.15) * 9/5 + 32
        elif to_unit == 'K':
            return k
        else:
            raise ValueError("Неподдерживаемая шкала")
    else:
        return value * units[from_unit] / units[to_unit]