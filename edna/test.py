# -*- coding:utf-8 -*-

from edna import SimpleEDNA
from pprint import pprint

edna = SimpleEDNA()
ss = edna.getServiceList('SSERVER')
pprint(ss)

ps = edna.getPointList(ss[0][0])
pprint(ps[:10])