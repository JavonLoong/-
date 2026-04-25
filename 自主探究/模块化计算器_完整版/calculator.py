"""
计算模块 (calculator.py)
提供基础四则运算函数：加、减、乘、除。
"""


def add(a, b):
    """返回 a 与 b 的和"""
    return a + b


def subtract(a, b):
    """返回 a 与 b 的差"""
    return a - b


def multiply(a, b):
    """返回 a 与 b 的乘积"""
    return a * b


def divide(a, b):
    """
    返回 a 与 b 的商。
    当 b 为 0 时，抛出 ValueError 异常，避免程序崩溃。
    """
    if b == 0:
        raise ValueError("除数不能为零！")
    return a / b
