'''
Author: config 57167701+YconfigY@users.noreply.github.com
Date: 2023-04-16 21:09:50
LastEditors: config 57167701+YconfigY@users.noreply.github.com
LastEditTime: 2023-06-11 21:36:59
FilePath: \DropTrack\lib\train\dataset\__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from .lasot import Lasot
from .got10k import Got10k
from .tracking_net import TrackingNet
from .imagenetvid import ImagenetVID
from .coco import MSCOCO
from .coco_seq import MSCOCOSeq
from .got10k_lmdb import Got10k_lmdb
from .lasot_lmdb import Lasot_lmdb
from .imagenetvid_lmdb import ImagenetVID_lmdb
from .coco_seq_lmdb import MSCOCOSeq_lmdb
from .tracking_net_lmdb import TrackingNet_lmdb
from .lmd_tship import LMD_TShip
