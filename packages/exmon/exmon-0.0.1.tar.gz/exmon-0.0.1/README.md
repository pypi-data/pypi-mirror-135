# ExMon

exmon can monitor your script and forward exceptions to specified services
- super easy
- modular

# Example

```python

from exmon import ExMon
from exmon.services import Alerta
from exmon.services import DiscordWebhook

# set up discord webhook
discord = DiscordWebhook('<URL>')

# set up alerta
alerta = Alerta(host_url='<HOST_URL>', api_key='<API_KEY>')

# start up ex mon with both services
ExMon(services=[discord, alerta])

# raise test exception
raise Exception('Totally unexpected exception')

```
