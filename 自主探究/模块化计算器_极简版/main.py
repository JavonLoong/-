# import calculator: import 是导入语句(import statement)，用于引入外部模块(module)
# Python 会在当前目录下查找 calculator.py 文件，将其作为模块加载
# 加载后可通过 "模块名.函数名" 的方式调用模块中定义的函数，即点运算符(dot operator)访问成员
import calculator

# ops 是一个字典(dictionary)，Python 的内置数据结构(data structure)，存储键值对(key-value pair)
# 键(key): 字符串类型(str)的运算符符号，如 '+', '-', '*', '/'
# 值(value): 函数对象(function object)的引用(reference)，如 calculator.add
# 在 Python 中，函数是一等公民(first-class citizen)，可以像变量一样被赋值、传递和存储
# 这种设计模式叫做"策略模式(Strategy Pattern)"——用字典映射(mapping)替代冗长的 if-elif 分支
ops = {'+': calculator.add, '-': calculator.subtract, '*': calculator.multiply, '/': calculator.divide}

# __name__ 是 Python 的内置特殊变量(dunder variable / magic variable)
# 当文件被直接运行时，__name__ 的值为字符串 '__main__'
# 当文件被其他模块 import 时，__name__ 的值为模块名（如 'main'）
# 这个条件判断叫做"模块入口守卫(entry point guard)"，确保主逻辑只在直接运行时执行
if __name__ == '__main__':

    # while 是循环语句(loop statement)，条件为 True 时反复执行循环体(loop body)
    # := 是赋值表达式运算符(assignment expression operator)，俗称"海象运算符(walrus operator)"
    # 它在 Python 3.8 中引入（PEP 572），作用是在表达式(expression)内部完成赋值(assignment)
    # 这里等价于: a = input(...); while a != 'q':  但更简洁
    # input() 是内置函数(built-in function)，从标准输入(stdin)读取用户输入，返回值类型为 str
    # != 是不等比较运算符(inequality operator)
    while (a := input("数字1 (q退出): ")) != 'q':

        # 提示用户输入运算符(operator)，即要执行的运算类型
        o = input("运算符 (+-*/): ")

        # 提示用户输入第二个操作数(operand)
        b = input("数字2: ")

        # try-except 是异常处理结构(exception handling)，属于 Python 的错误处理机制
        # try 块(try block): 包裹可能抛出异常(raise exception)的代码
        # 如果 try 块中没有异常发生，except 块会被跳过
        try:
            # float() 是类型转换函数(type casting/conversion)，将字符串转为浮点数(floating-point number)
            # 如果字符串无法转换（如 "abc"），会抛出 ValueError 异常
            # ops[o]: 通过下标运算符(subscript operator) [] 从字典中取出键 o 对应的函数
            # 如果键不存在，会抛出 KeyError 异常
            # ops[o](float(a), float(b)): 调用(call)取出的函数，传入两个实参(argument)
            # f"...": f-string，格式化字符串字面量(formatted string literal)，Python 3.6 引入
            # {} 内的表达式会被求值(evaluate)后插入字符串中
            print(f"= {ops[o](float(a), float(b))}")

        # except 块(except block): 捕获(catch)指定类型的异常
        # (ValueError, KeyError): 元组(tuple)，表示同时捕获这两种异常
        #   - ValueError: 类型转换失败（输入非数字）或除数为零（calculator.divide 抛出）
        #   - KeyError: 用户输入了字典中不存在的运算符（如 '%', '^' 等）
        # as e: 将捕获到的异常对象(exception object)绑定到变量 e，可通过 str(e) 获取错误描述
        except (ValueError, KeyError) as e:
            # 输出错误提示信息，程序不会崩溃(crash)，继续下一轮循环(next iteration)
            print(f"错误: {e}")
