# -*- coding: utf-8 -*-
import os
import re

# 去除\r\n\t字符

s = "武汉天气 ：当前温度21℃，感冒低发期，天气舒适，请注意多吃蔬菜水果，多喝水哦。{br}[10月27日]：多云，低温 15℃，高温 24℃，风力2级{br}[10月28日] ：阴，低温 13℃，高温 19℃，风力3级{br}[10月29日]：多云，低温 12℃，高温 22℃，风力1级{br}[10月30日] ：多云，低温 14℃，高温 22℃，风力2级{br}[10月31日] ：阴，低温 14℃，高温 19℃，风力2级"

print(re.sub('{br}', '\n', s))

# str = "12345"

# with open("README.md", mode='wt', encoding='utf-8') as f:
# 	# for line in f:
# 	# 	print(line, end='')
# 	f.writelines("111\n")
# 	f.write("22\n")
# 	f.write("3\n")

# f.close()


# with open("README.md", mode='wt', encoding='utf-8') as f:
# 	# for line in f:
# 	# 	print(line, end='')
# 	f.writelines("3\n")
# 	f.write("4\n")
# 	f.write("5\n")
# 	f.write(str)
# f.close()
