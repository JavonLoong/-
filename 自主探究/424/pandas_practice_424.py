import pandas as pd


def main() -> None:
    # 1. 创建一个最简单的 DataFrame
    df = pd.DataFrame(
        [[88, 92, "A"], [75, 81, "B"], [90, 85, "A"]],
        index=["张三", "李四", "王五"],
        columns=["数学", "英语", "班级"],
    )

    print("原始 DataFrame：")
    print(df)
    print()

    # 2. 看行名和列名
    print("df.columns 返回的不是 list，而是 Index 对象：")
    print(df.columns)
    print("转成 list 后：", list(df.columns))
    print()

    print("df.index 返回的也是 Index 对象：")
    print(df.index)
    print("转成 list 后：", list(df.index))
    print()

    # 3. 看 DataFrame 的基本信息
    print("df.shape =", df.shape, "=> (行数, 列数)")
    print("df.size =", df.size, "=> 总元素个数")
    print()

    # 4. 用 loc 按“名字/标签”取数据
    print("df.loc['李四']：按行名取一整行")
    print(df.loc["李四"])
    print()

    print("df.loc[:, ['数学', '英语']]：按列名取两列")
    print(df.loc[:, ["数学", "英语"]])
    print()

    # 5. 用 iloc 按“位置”取数据
    print("df.iloc[1]：取第 2 行")
    print(df.iloc[1])
    print()

    print("df.iloc[1, 0]：取第 2 行第 1 列的值")
    print(df.iloc[1, 0])
    print()

    # 6. 添加新列
    df["总分"] = df["数学"] + df["英语"]
    print("添加新列 df['总分'] 后：")
    print(df)


if __name__ == "__main__":
    main()
