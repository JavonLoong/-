# def add(a, b): 定义名为 add 的函数，形参(parameter) a 和 b 分别为两个操作数(operand)
# return a + b: 返回两个操作数的算术和，"+" 是加法运算符(arithmetic operator)
def add(a, b): return a + b

# def subtract(a, b): 定义减法函数，形参 a 是被减数(minuend)，b 是减数(subtrahend)
# return a - b: 返回差(difference)，"-" 是减法运算符
def subtract(a, b): return a - b

# def multiply(a, b): 定义乘法函数，形参 a 是被乘数(multiplicand)，b 是乘数(multiplier)
# return a * b: 返回积(product)，"*" 是乘法运算符
def multiply(a, b): return a * b

# def divide(a, b): 定义除法函数，形参 a 是被除数(dividend)，b 是除数(divisor)
def divide(a, b):
    # if b == 0: 条件判断语句(conditional statement)，"==" 是比较运算符(comparison operator)
    # 检查除数是否为零，防止触发 ZeroDivisionError（除零错误）
    # raise ValueError(...): raise 是抛出异常的关键字(keyword)
    # ValueError 是 Python 内置异常类(built-in exception class)，表示"值不合法"
    # 抛出异常后，程序的控制流(control flow)会跳转到最近的 except 块中
    if b == 0: raise ValueError("除数不能为零")
    # return a / b: "/" 是真除法运算符(true division operator)，返回商(quotient)，结果为浮点数(float)
    # 注意区分 "/" (真除法，返回 float) 和 "//" (整除/地板除法，返回 int)
    return a / b
