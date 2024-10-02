import os
import sys
import subprocess
import shutil
import winshell  # либа для ярлыков

def create_shortcut():
    exe_path = sys.executable
    sendto_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'SendTo')
    shortcut_path = os.path.join(sendto_dir, 'Зашакалить ПДФ.lnk')
    
    with winshell.shortcut(shortcut_path) as link:
        link.path = exe_path
        link.description = "Compress PDF Files"
    
    print(f"Ярлык создан и добавлен в папку SendTo: {shortcut_path}")

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

def compress_pdf(input_files):
    gs_bin_path = find_ghostscript_executable()

    for input_file in input_files:
        output_file = input_file + "_compressed.pdf"
        args = [
            gs_bin_path,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/ebook",
            "-dColorImageDownsampleType=/Bicubic",
            "-dColorImageResolution=120",
            "-dGrayImageDownsampleType=/Bicubic",
            "-dGrayImageResolution=120",
            "-dMonoImageDownsampleType=/Bicubic",
            "-dMonoImageResolution=120",
            "-dRemoveUnusedObjects=true",
            "-dRemoveUnusedResources=true",
            "-dEmbedAllFonts=true",
            "-dSubsetFonts=false",
            "-dDoThumbnails=false",
            "-dNOPAUSE",
            "-dBATCH",
            "-sOutputFile=" + output_file,
            input_file
        ]

        try:
            subprocess.run(args, check=True)
            print(f"Файл {input_file} успешно сжат и сохранен как {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при сжатии файла {input_file}: {str(e)}")

if __name__ == "__main__":
    # Создаем ярылк если нет пдф
    if len(sys.argv) == 1:
        create_shortcut()
    else:
        input_files = sys.argv[1:]  # список входных файлов
        for file in input_files:
            if not os.path.exists(file):
                print(f"Файл {file} не найден")
                sys.exit(1)
        
        compress_pdf(input_files)
        
        # Опционально используем 
        for input_file in input_files:
            temp_output_pdf = input_file + "_compressed.pdf"
            try:
                shutil.move(temp_output_pdf, input_file)
                print(f"Оригинальный файл {input_file} заменён сжатой версией")
            except Exception as e:
                print(f"Ошибка при замене файла {input_file}: {str(e)}")
