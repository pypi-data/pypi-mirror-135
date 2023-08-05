# -*- encoding: utf-8 -*-
'''
@File    :   arrayQueue.py
@Time    :   2022/01/13 13:19:18
@Author  :   ufy
@Contact :   antarm@outlook.com
@Version :   v1.0
@Desc    :   这里我们约定:
                left: front  指向队首元素
                right: rear 指向队尾元素（而不是队尾的下一个位置）
'''

# here put the import lib


class Array(object):
    DEFAULT_CAPCITY = 10  # 队列的默认容量

    def __init__(self):
        self._data = [None] * Array.DEFAULT_CAPCITY
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0


class Queue(Array):
    '基于python list 实现的FIFO队列'

    def __init__(self):
        super().__init__()
        self._front = 0
        self._cur = 0

    def _resize(self, cap: int = 0):
        # 思考：换用self._data + [None] * (cap - self._size)来实现，是否更优？
        # old = self._data
        # self._data = [None] * cap
        # walk = self._front
        # for k in range(self._size):
        #     self._data[k] = old[walk]
        #     walk = (1+walk) % len(old)
        # self._front = 0
        self._data += [None] * (cap - self._size)  # 代码更少，性能更优

    def first(self):
        # 获取队首元素的值
        if self.is_empty():
            raise Exception('Queue is empty')

        return self._data[self._front]

    def dequeue(self):
        # 从队首出队一个元素
        if self.is_empty():
            raise Exception('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer

    def enqueue(self, e):
        # 从队尾进入一个元素
        if self._size == len(self._data):
            self._resize(cap=2 * len(self._data))
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def __str__(self) -> str:
        pstr = '['
        for i in range(self._size):
            avail = (self._front + i) % len(self._data)
            pstr += str(self._data[avail]) + ','
        if len(pstr) > 1:
            pstr = pstr[:-1]
        pstr += '>'
        return pstr

    def __repr__(self) -> str:
        return self.__str__()

    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._cur < self._size:
            val = self._data[(self._front+self._cur)%len(self._data)]
            self._cur += 1
            return val
        else:
            self._cur = 0
            raise StopIteration


class DeQueue(Array):
    '''使用python list 实现双端队列'''

    def __init__(self):
        super().__init__()
        self._front = 0
        self._tail = 0
        self._cur = 0

    def _resize(self, cap: int = 0):
        self._data += [None] * (cap - len(self._data))

    def first(self):
        if self.is_empty():
            raise Exception('Double-ended queue is empty')
        return self._data[self._front]

    def last(self):
        if self.is_empty():
            raise Exception('Double-ended queue is empty')
        return self._data[self._tail]

    def add_first(self, e):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        avail = (self._tail - self._size) % len(self._data)
        self._data[avail] = e
        self._front = avail
        self._size += 1

    def add_last(self, e):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._tail = avail
        self._size += 1

    def del_first(self):
        if self.is_empty():
            raise Exception('Double-ended queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer

    def del_last(self):
        if self.is_empty():
            raise Exception('Double-ended queue is empty')
        answer = self._data[self._tail]
        self._data[self._tail] = None
        self._tail = (self._tail + 1) % len(self._data)
        self._size -= 1
        return answer

    def __str__(self) -> str:
        pstr = '[<'
        for i in range(self._size):
            avail = (self._front + i) % len(self._data)
            pstr += str(self._data[avail]) + ','
        if len(pstr) > 1:
            pstr = pstr[:-1]
        pstr += '>]'
        return pstr

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._cur < self._size:
            val = self._data[(self._front+self._cur)%len(self._data)]
            self._cur += 1
            return val
        else:
            self._cur = 0
            raise StopIteration
