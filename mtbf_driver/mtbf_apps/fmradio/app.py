# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base
from gaiatest.apps.fmradio.app import FmRadio
import time

class MTBF_FmRadio(FmRadio, Base):
    name = 'FM Radio'

    def launch(self):
        Base.launch(self) 
