import os
import configparser


BASE_DIR = os.getcwd()
CONFIG_DIR = '/application/config.cfg'

config = configparser.ConfigParser()
config.read(BASE_DIR + CONFIG_DIR)
