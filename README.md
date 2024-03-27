# Описание

Форматы и плагины для просмотра файлов игр Targam. Описание форматов в шаблонах .bt для программы 010Editor.

 № | Формат файла       | Шаблон (010Editor)     |    Описание |
| :--- | :--------- | :----------- | :---------- |
| 1 | .gdp        | [GDP.bt](https://github.com/AlexKimov/targem-file-formats/blob/master/templates/010editor/GDP.bt)  |   архив игровых ресурсов Магии Войны |
| 2 | .sam        | [SAM.bt](https://github.com/AlexKimov/targem-file-formats/blob/master/templates/010editor/SAM.bt)  |   3d модели и анимация Магии Войны |
| 3 | .gsm        | [GSM.bt](https://github.com/AlexKimov/targem-file-formats/blob/master/templates/010editor/GSM.bt)  |   3d модели без анимации Магии Войны |
| 4 | .gdp        | [GDP(ExM).bt](https://github.com/AlexKimov/targem-file-formats/blob/master/templates/010editor/GDP(ExM).bt)  |   архив игровых ресурсов ExMashina |

**Инструменты**

| № | Плагин       | Программа | Описание |  
| :--- | :--------- | :----------- | :---- | 
| 1 | [unpack_gdp.bms](https://github.com/AlexKimov/targem-file-formats/blob/master/scripts/quickbms/unpack_gdp.bms) | Quickbms | Распаковка файлов ресурсов .gdp Магии Войны  |
| 2 | [unpack_gdp_exm.bms](https://github.com/AlexKimov/targem-file-formats/blob/master/scripts/quickbms/exm/unpack_gdp_exm.bms) | Quickbms | Распаковка файлов ресурсов .gdp ExMachina |
| 3 | [fmt_bms_sam.py](https://github.com/AlexKimov/targem-file-formats/blob/main/plugins/noesis/fmt_bms_sam.py) | Noesis | Просмотр моделей с анимациями .sam Магии Войны |
| 4 | [fmt_bms_mrk.py](https://github.com/AlexKimov/targem-file-formats/blob/main/plugins/noesis/fmt_bms_mrk.py) | Noesis | Просмотр изображений .mrk Магии Войны |

    Как использовать quickbms скрипты
    1. Нужен quickbms https://aluigi.altervista.org/quickbms.htm
    2. Для запуска в репозитории лежит bat файл с настройками, нужно открыть его и задать свои пути: до места, где находится quickbms, папки с игрой и места куда нужно сохранить результат.
    3. Запустить процесс через bat файл или вручную (задав свои параметры для запуска quickbms, документация на английском есть здесь https://aluigi.altervista.org/papers/quickbms.txt ). 

