from typing import TYPE_CHECKING, Optional, Dict, Any

import logging

from datetime import datetime

from weconnect.util import robustTimeParse, toBool

from weconnect.addressable import AddressableObject, AddressableAttribute

if TYPE_CHECKING:
    from weconnect.elements.generic_status import GenericStatus

LOG: logging.Logger = logging.getLogger("weconnect")


class Error(AddressableObject):
    def __init__(
        self,
        localAddress: str,
        parent: Optional['GenericStatus'],
        fromDict: Dict[str, Any] = None,
    ) -> None:
        super().__init__(localAddress=localAddress, parent=parent)
        self.code: AddressableAttribute[int] = AddressableAttribute(localAddress='code', parent=self, value=None, valueType=int)
        self.message: AddressableAttribute[str] = AddressableAttribute(localAddress='message', parent=self, value=None, valueType=str)
        self.group: AddressableAttribute[int] = AddressableAttribute(localAddress='group', parent=self, value=None, valueType=int)
        self.info: AddressableAttribute[str] = AddressableAttribute(localAddress='info', parent=self, value=None, valueType=str)
        self.timestamp: AddressableAttribute[str] = AddressableAttribute(localAddress='timestamp', parent=self, value=None, valueType=datetime)
        self.retry: AddressableAttribute[bool] = AddressableAttribute(localAddress='retry', parent=self, value=None, valueType=bool)

        if fromDict is not None:
            self.update(fromDict)

    def reset(self) -> None:
        self.code.setValueWithCarTime(None, lastUpdateFromCar=None, fromServer=True)
        self.code.enabled = False
        self.message.setValueWithCarTime(None, lastUpdateFromCar=None, fromServer=True)
        self.message.enabled = False
        self.group.setValueWithCarTime(None, lastUpdateFromCar=None, fromServer=True)
        self.group.enabled = False
        self.info.setValueWithCarTime(None, lastUpdateFromCar=None, fromServer=True)
        self.info.enabled = False
        self.retry.setValueWithCarTime(None, lastUpdateFromCar=None, fromServer=True)
        self.retry.enabled = False
        self.enabled = False

    def update(self, fromDict: Dict[str, Any]) -> None:
        LOG.debug('Update Status Error from dict')

        if 'code' in fromDict:
            self.code.setValueWithCarTime(int(fromDict['code']), lastUpdateFromCar=None, fromServer=True)
        else:
            self.code.enabled = False

        if 'message' in fromDict:
            self.message.setValueWithCarTime(fromDict['message'], lastUpdateFromCar=None, fromServer=True)
        else:
            self.message.enabled = False

        if 'group' in fromDict:
            self.group.setValueWithCarTime(int(fromDict['group']), lastUpdateFromCar=None, fromServer=True)
        else:
            self.code.enabled = False

        if 'info' in fromDict:
            self.info.setValueWithCarTime(fromDict['info'], lastUpdateFromCar=None, fromServer=True)
        else:
            self.info.enabled = False

        if 'errorTimeStamp' in fromDict:
            carCapturedTimestamp: Optional[datetime] = robustTimeParse(fromDict['errorTimeStamp'])
            self.timestamp.setValueWithCarTime(carCapturedTimestamp, lastUpdateFromCar=None, fromServer=True)
            if self.timestamp.value is None:
                self.timestamp.enabled = False
        else:
            self.timestamp.enabled = False

        if 'retry' in fromDict:
            self.retry.setValueWithCarTime(toBool(fromDict['retry']), lastUpdateFromCar=None, fromServer=True)
        else:
            self.retry.enabled = False

        if not self.code.enabled and not self.message.enabled and not self.code.enabled and not self.info.enabled \
                and not self.retry.enabled:
            self.enabled = False
        else:
            self.enabled = True

        for key, value in {key: value for key, value in fromDict.items()
                           if key not in ['code', 'message', 'group', 'info', 'errorTimeStamp', 'retry']}.items():
            LOG.warning('%s: Unknown attribute %s with value %s', self.getGlobalAddress(), key, value)

    def __str__(self) -> str:
        return f'Error {self.code.value}: {self.message.value} \n\tinfo: {self.info.value} \n\ttimestamp: {self.timestamp.value}'
