import sys
sys.path.insert(0, r'C:\AppPython\pitonit\tools')
from edit import sub

sub(r'C:\AppPython\pitonit\src\Modules\getpath.py', '''    config['isolated'] = 1
    config['use_environment'] = 0
    config['site_import'] = 0
    config['safe_path'] = 1
''', '''    # pitonit: ignora le variabili d'ambiente e il site utente di Python,
    # ma lascia la cartella dello script in sys.path[0] (niente isolated/safe_path)
    config['use_environment'] = 0
    config['user_site_directory'] = 0
    config['site_import'] = 0
''')
print("ok")
