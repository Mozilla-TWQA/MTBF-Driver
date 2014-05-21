# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.phone.app import Phone
import time

class MTBF_Phone(Base):
    def __init__(self, marionette):
        Base.__init__(self, marionette)
