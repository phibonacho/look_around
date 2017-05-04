'''Library needed'''
import random
from random import randint
from os import listdir
from os.path import isfile
import time
import max7219.led as led

'''Initialize Device'''

device = led.matrix(cascaded = 2, spi_device=0)
device.orientation(180)

'''Constant'''

PATH = 'cfg_f/'
REFRESH_CFG = 'n_cfg/s_r/refresh.cfg'
TRANSITION = 1/3
WAIT = 2

random.seed()

'''Funzione di pulizia della matrice'''
def clear_all():
	device.flush()


'''Funzione di caricamento da file'''
def load_sheet(filename):
	contents = []
	with open(filename, "r")as f:
		for line in f:
                        contents.append(line)

	return contents

'''Funzione di caricamento su Matrice'''
def load_cfg(bitm_cfg):
	for i in range(8):
		for j in range(8):
			if(((bitm_cfg[i])[j])!='2'):
				device.pixel(i, j, int((bitm_cfg[i])[j]))
	return

'''Funzione mostra sequenza'''
def perf_seq(dir_name):
	dir_path = PATH+dir_name+'/'
	cfg_list = listdir(dir_path)
	cfg_list.sort()	
	for cfile in cfg_list:
		if isfile(dir_path+cfile):
			load_cfg(load_sheet(dir_path+cfile))
			time.sleep(TRANSITION)

'''Mostra sequenza inversa'''
def perf_inv(dir_name):
	dir_path = PATH+dir_name+'/'
	cfg_list = listdir(PATH+dir_name)	
	cfg_list.sort()
	for cfile in cfg_list[::-1]:
		if isfile(dir_path+cfile):
			load_cfg(load_sheet(dir_path+cfile))
			time.sleep(TRANSITION)
	
def open_eye():
	perf_inv('s_e')
	
def close_eye():
	perf_seq('s_e')	

def blink():
	for i in range(2):
		close_eye()
		open_eye()

'''Funzione di appoggio a look_around'''
def possible_next(start, dir_list):
	result = []
	for directory in dir_list:
		if start in directory:
			result.append(directory)
	return result


def look_around(start, path):
	next_cfg = possible_next(start, listdir(path))
	dir_name = next_cfg[randint(0,len(next_cfg)-1)]
	if dir_name[0]==start:
		perf_seq(dir_name)
		return dir_name[2]
	else:
		perf_inv(dir_name)
		return dir_name[0]

'''main'''
def do_something(flag):
	start = "c"
	run = True
	open_eye()

	time.sleep(1)

	blink()

	time.sleep(1)

	while flag:
			new_start = look_around(start, PATH)
			time.sleep(1)
			start = new_start
			if start == 'c' and randint(0, 100)>=80:
				blink()
			run = flag	
	
	time.sleep(1)		
	close_eye()
	time.sleep(1)
	
def main():
	do_something(True)

if __name__=='__main__':
	main()	
