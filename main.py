from client import client
from key import token


# To load new modules, copy/paste the line below, uncommented, with X filled in for the name of your file
# from modules import X

from modules import help
from modules import hail_awoobis_rep
from modules import markov
from modules import nou
from modules import ping
from modules import pingreact
from modules import stats
from modules import uptime
from modules import tag

client.run(token)
