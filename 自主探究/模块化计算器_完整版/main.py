"""
主程序模块 (main.py)
导入 calculator 模块，提供交互式循环计算功能。
"""

import calculator


def main():
    """主函数：循环接收用户输入并执行计算，直到用户选择退出。"""

    # 运算符与函数的映射
    operations = {
        '+': calculator.add,
        '-': calculator.subtract,
        '*': calculator.multiply,
        '/': calculator.divide,
    }

    print("=" * 40)
    print("       欢迎使用模块化计算器")
    print("=" * 40)
    print("支持的运算：+  -  *  /")
    print("输入 q 退出程序\n")

    while True:
        # 获取第一个数字
        num1_input = input("请输入第一个数字（或输入 q 退出）：")
        if num1_input.strip().lower() == 'q':
            print("感谢使用，再见！")
            break

        # 获取运算符
        operator = input("请输入运算符（+, -, *, /）：").strip()

        # 获取第二个数字
        num2_input = input("请输入第二个数字：")

        try:
            num1 = float(num1_input)
            num2 = float(num2_input)
        except ValueError:
            print("❌ 输入有误：请输入有效的数字！\n")
            continue

        if operator not in operations:
            print(f"❌ 不支持的运算符：'{operator}'，请使用 +, -, *, /\n")
            continue

        try:
            result = operations[operator](num1, num2)
            print(f"✅ 计算结果：{num1} {operator} {num2} = {result}\n")
        except ValueError as e:
            print(f"❌ 计算错误：{e}\n")


if __name__ == '__main__':
    main()
