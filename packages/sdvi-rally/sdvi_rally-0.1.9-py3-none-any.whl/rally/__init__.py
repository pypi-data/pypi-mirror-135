# ./server/venv/bin/pip install --upgrade -t server/app/evaluate/eval2/rally/rally/_vendored/ requests==2.22.0
#
# for each of: urllib3, chardet, idna, certifi
#   grep for 'import x' and 'from x'
#   replace 'import x' with 'from rally._vendored import x'
#   replace 'from x' with 'from rally._vendored.x'
#
# also replace 'for package in ('urllib3', 'idna', 'chardet')' with
#              'for package in ('rally._vendored.urllib3', 'rally._vendored.idna', 'rally._vendored.chardet')
# in packages.py

from . import asset
from . import exceptions
from . import files
from . import jobs
from . import notifications
from . import secret
from . import supplyChain
from . import experimental

__version__ = '0.1.9'
