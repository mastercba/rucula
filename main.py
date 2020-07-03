# MAIN - RUCULA
# -----------------------------------------------------------------------------

from main import rucula
from main.ota_updater import OTAUpdater


def download_and_install_update_if_available():
    ota_updater = OTAUpdater('https://github.com/mastercba/almacigo')
    ota_updater.download_and_install_update_if_available('TORRIMORA', 'santino989')

def start():
    from main import ota_updater   
    from main.rucula import Rucula

#     ota_updater = OTAUpdater('https://github.com/mastercba/almacigo')
#     ota_updater.using_network('TORRIMORA', 'santino989')
#     ota_updater.check_for_update_to_install_during_next_reboot()

    # Read version
#     cv = ota_updater.read_current_version()
    cv = '3.9'
    # Begin MAINcode
    irrigation = Rucula(cv)

def boot():
#     download_and_install_update_if_available()
    start()
    

boot()
# -----------------------------------------------------------------------------
