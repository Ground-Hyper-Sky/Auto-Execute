# Auto-Execute
---------
一个以脚本为基本单位存储各类指令多模式执行的MCDR插件

模式(服务器启动时执行,手动执行,循环执行,间隔执行)

需要 `v2.6.0` 以上的 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged)

部分代码参考了 Fallen-Breath 的 [QuickBackupM](https://github.com/TISUnion/QuickBackupM).

##  命令基本说明

`!!ae` 显示帮助信息

`!!ae create <脚本id>` 创建一个脚本用于存储指令

`!!ae add <脚本id> <指令>` 往脚本里添加一条指令,脚本里的的指令具有顺序

`!!ae insert <脚本id> <行> <指令>` 在脚本指定行插入一条指令,可以理解为插队,指令的行数可以使用!!ae look <脚本id>查看

`!!ae del <脚本id> <指令>` 删除脚本里的一条指令,如出现重复指令，则删除更靠前的指令

`!!ae re <脚本id> <行范围>` 删除脚本指定行数的指令,行范围可以是单独的数字,也可以是一个区间,例如1-3表示1到3行

`!!ae remove <脚本id>` 删除一个脚本

`!!ae list` 查看所有存在且格式无误的脚本

`!!ae auto_list` 查看所有服务器启动后自启的脚本

`!!ae look <脚本id>` 查看脚本详情

`!!ae run <脚本id>` 通过指令运行脚本

`!!ae auto <脚本id>` 打开或者关闭某个脚本自启

`!!ae des <脚本id> <简介>` 修改脚本的简介

`!!ae set <脚本id> <权限等级>` 修改脚本的独立权限，权限等级应为一个整数

`!!ae reload` 重载插件，这会使正在运行的脚本终止运行

除了以上MCDR指令，ae还有着专用于脚本的指令

`@ae sleep <时间>` 使脚本暂停一段时间，单位为秒，可以为小数，例如@ae sleep 60使得脚本运行于此时间隔60秒后继续执行剩余指令

`@ae loop <时间>` 置于脚本末尾，用法和sleep类似，区别在于暂停结束后不会执行剩余指令，而是循环当前脚本。

##  配置文件说明

如果你不太熟悉json文件格式，建议您使用指令完成操作，而不是修改配置文件

### auto_execute

路径：`config/AutoExecute.json`

#### minimum_permission_level

使用各指令的最低权限要求

如果一个脚本的权限高于对脚本进行操作的指令（如add,insert,del,re,remove,set,run,auto,des）的权限，那么对该脚本进行操作需要的权限以其独立权限为准。

#### auto_execute_list

一个用于存放服务器启动后自启脚本的列表

例如[主世界伪和平,地狱伪和平,末地伪和平]

列表内脚本启动具有顺序性，但启动完上个





