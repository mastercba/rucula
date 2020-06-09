# MAIN - RUCULA
# -----------------------------------------------------------------------------

from main import rucula


def start():
    from main.rucula import Rucula

    # Read version
    #     cv = ota_updater.read_current_version()
    cv = '3.9'    
    # Begin MAINcode
    irrigation = Rucula(cv)

def boot():
    start()
    

boot()
# -----------------------------------------------------------------------------