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









