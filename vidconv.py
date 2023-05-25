# /* vidconv.py
#  * Copyright (C) 2023 MikuInvidious Team
#  *
#  * This software is free software; you can redistribute it and/or
#  * modify it under the terms of the GNU General Public License as
#  * published by the Free Software Foundation; either version 3 of
#  * the License, or (at your option) any later version.
#  *
#  * This software is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  * General Public License for more details.
#  *
#  * You should have received a copy of the GNU General Public License
#  * along with this library. If not, see <http://www.gnu.org/licenses/>.
#  */

# The following algorithm is adopted from bilibili-API-collect.
# https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/other/bvid_desc.md
import unittest

table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
itable = { table[i]: i for i in range(len(table)) }

s = [11, 10, 3, 8, 4, 6]
XOR = 177451812
ADD = 8728348608

def bv2av(x):
    r = 0
    for i in range(6):
        r += itable[x[s[i]]] * 58 ** i
    return (r - ADD) ^ XOR

def av2bv(x):
    x = (x ^ XOR) + ADD
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[x // 58 ** i % 58]
    return ''. join(r)

class AvBvConversionTest(unittest.TestCase):
    def test_bv2av(self):
        self.assertEqual(av2bv(170001), 'BV17x411w7KC')
    def test_av2bv(self):
        self.assertEqual(bv2av('BV17x411w7KC'), 170001)

if __name__ == '__main__':
    unittest.main()