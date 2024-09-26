import os
import sys
import subprocess
import shutil

def find_ghostscript_executable():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    gs_executable = os.path.join(base_dir, 'gs10.04.0', 'bin', 'gswin32.exe')

    if os.path.exists(gs_executable):
        return gs_executable
    else:
        print(f"Не удалось найти Ghostscript по пути: {gs_executable}")
        sys.exit(1)

def compress_pdf(input_file, output_file):
    gs_bin_path = find_ghostscript_executable()

    args = [
        gs_bin_path,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/screen",
        "-dNOPAUSE",
        "-dBATCH",
        "-sOutputFile=" + output_file,
        input_file
    ]

    try:
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
    
    temp_output_pdf = input_pdf + "_temp_compressed.pdf"

    compress_pdf(input_pdf, temp_output_pdf)

    try:
        shutil.move(temp_output_pdf, input_pdf)
        print(f"Оригинальный файл заменён сжатой версией: {input_pdf}")
    except Exception as e:
        print(f"Ошибка при замене файла: {str(e)}")
