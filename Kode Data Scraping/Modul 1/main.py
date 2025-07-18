import os
release = os.getcwd()
print(release)

def create_directory(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

create_directory("Scraping")

def create_new_file(path):
    f = open(path,'w')
    f.write("")
    f.close()

create_new_file("scraping/test.txt")

def write_to_file(path,data):
    with open(path,'a')as file:
        file.write(data + '\n')

write_to_file("Scraping/test.txt","ini adalah data yang akan digunakan untuk menampung big data")

def clear_file(path):
    f = open(path, 'w')
    f.close()

clear_file("Scraping/test.txt")

def does_file_exist(path):
    return os.path.isfile(path)

print(does_file_exist("Scraping/test.txt"))

def read_data(path):
    with open(path,'rt')as file:    
        for line in file:
            print(line.replace("\n",""))
            
read_data("Scraping/test.txt")