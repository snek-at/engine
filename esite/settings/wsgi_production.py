from django.core.wsgi import get_wsgi_application

from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
