import os
import sys
import subprocess
import shutil

def find_ghostscript_executable():
    # Определяем директорию, где находится .exe или .py файл
    if getattr(sys, 'frozen', False):
        # Если программа запущена как упакованный .exe файл
        base_dir = os.path.dirname(sys.executable)
    else:
        # Если запускается как обычный Python-скрипт
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Путь к Ghostscript в папке 'gs10.04.0\bin' рядом с .exe файлом
    gs_executable = os.path.join(base_dir, 'gs10.04.0', 'bin', 'gswin32.exe')

    # Проверяем, существует ли файл gswin32.exe
    if os.path.exists(gs_executable):
        return gs_executable
    else:
        print(f"Не удалось найти Ghostscript по пути: {gs_executable}")
        sys.exit(1)

def compress_pdf(input_file, output_file):
    # Находим путь к Ghostscript
    gs_bin_path = find_ghostscript_executable()

    # Параметры для вызова Ghostscript
    args = [
        gs_bin_path,             # Путь к исполняемому файлу Ghostscript
        "-sDEVICE=pdfwrite",     # Указываем, что вывод будет в формате PDF
        "-dCompatibilityLevel=1.4",  # Совместимость с версиями PDF 1.4
        "-dPDFSETTINGS=/screen",  # Пресет для сжатия
        "-dNOPAUSE",             # Без паузы между страницами
        "-dBATCH",               # Завершение после обработки
        "-sOutputFile=" + output_file,  # Выходной файл
        input_file               # Входной файл
    ]

    try:
        # Запуск Ghostscript с помощью subprocess
        subprocess.run(args, check=True)
        print(f"Файл успешно сжат и сохранен как {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при сжатии файла: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: script.py <путь к файлу PDF>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    
    if not os.path.exists(input_pdf):
        print(f"Файл {input_pdf} не найден")
        sys.exit(1)
    
    # Временное имя для сжатого PDF файла
    temp_output_pdf = input_pdf + "_temp_compressed.pdf"

    # Сжимаем PDF с использованием локальной копии Ghostscript
    compress_pdf(input_pdf, temp_output_pdf)

    # Заменяем оригинальный файл сжатым
    try:
        shutil.move(temp_output_pdf, input_pdf)
        print(f"Оригинальный файл заменён сжатой версией: {input_pdf}")
    except Exception as e:
        print(f"Ошибка при замене файла: {str(e)}")
