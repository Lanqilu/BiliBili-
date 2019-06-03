import time

def date():
    """
    获取现在时间格式为-年-月-日
    """
    date = time.strftime("%Y-%m-%d", time.localtime())
    return date


def print_info(j):
    """
    打印进程
    """
    r = j/52
    list1 = []
    for i in range(1, 101):
        list1.append(i)
    if r in list1:
        print("{}%".format(r))
    elif r == 100:
        print("成功完成")


if __name__ == "__main__":
    list1 = []
    for i in range(1,101):
        list1.append(i)
    print(list1)