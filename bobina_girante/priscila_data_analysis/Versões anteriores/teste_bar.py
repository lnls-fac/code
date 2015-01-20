import os
def directory(path,extension):
  list_dir = []
  list_dir = os.listdir(path)
  count = 0
  for file in list_dir:
    if file.endswith(extension): # eg: '.txt'
      count += 1
  return count,list_dir

path1="C:\\Users\\priscila.sanchez\\Desktop\\TESTES-BOBINA\\BQF03 - Curva Excitacao\\Fonte 130A\\Ligacao_Defocalizador\\01_Sequencia"
ext='.dat'
files_info=directory(path1, ext)
n_file=files_info[1]
	
