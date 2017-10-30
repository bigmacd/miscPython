import pip
import os

print(os.getcwd())

directory = 'c:/Users/cooleyma/git/miscPython'
package = 'psycopg2'

arguments = [
    '--python-version',
    '2',
    '--only-binary=:all:', 
    '--no-deps', 
    '--platform',
    'manylinux1_x86_64', 
    '--implementation', 
    'cp',
    '--abi', 'cp27mu', 
    '--dest', 
    directory, 
package]

def download():
    pip.main(['download'] + arguments)

download()