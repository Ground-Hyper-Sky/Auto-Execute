import json
import os
import codecs

from mcdreforged.api.all import *
from auto_execute.AutoExecute_Language import Auto_Language as Al
from auto_execute.Edit_file import Edit_Read as Ed
from auto_execute.config import Default_script_config as Ds
from auto_execute.config import Default_total_config as Dt
from auto_execute.config import Path_config as Pc
from auto_execute.json_message import Message

Prefix = '!!ae'
script_path = f"{Pc.script_path}" + "/{0}.json"
total_config_path = Pc.config_path
script_content = Ds.get_default().serialize()
running_tasks = {}

help_msg = '''
------ {1} {2} ------
一个便携化的§a批量执行指令§c的MCDR§a插件
§3作者：FRUITS_CANDY
§d【格式说明】
#sc=!!ae,st=点击运行指令#§7{0} §a§l[▷] §e显示帮助信息
#sc=!!ae make,st=点击运行指令#§7{0} make §b<脚本名> §a§l[▷] §e创建一个脚本用于存储指令
#sc=!!ae add,st=点击运行指令#§7{0} add §b<脚本名> <指令> §a§l[▷] §e往脚本里添加一条指令,脚本里的的指令具有顺序
#sc=!!ae insert,st=点击运行指令#§7{0} insert §b<脚本名> <行> <指令> §a§l[▷] §e在指定行插入一条指令,可以理解为插队
#sc=!!ae del,st=点击运行指令#§7{0} del §b<脚本名> <指令> §a§l[▷] §e删除一条指令,出现重复指令,删除更靠前的指令
#sc=!!ae re,st=点击运行指令#§7{0} re §b<脚本名> <行> §a§l[▷] §e删除指定行数的指令,支持批量删除,例如1-3
#sc=!!ae remove,st=点击运行指令#§7{0} remove §b<脚本名> §a§l[▷] §e删除某个脚本
#sc=!!ae list,st=点击运行指令#§7{0} list §a§l[▷] §e查看所有存在的脚本
#sc=!!ae auto_list,st=点击运行指令#§7{0} auto_list §a§l[▷] §e查看自动启动的脚本
#sc=!!ae run_list,st=点击运行指令#§7{0} run_list §a§l[▷] §e查看正在运行的脚本
#sc=!!ae look,st=点击运行指令#§7{0} look §b<脚本名> §a§l[▷] §e查看某个脚本里的内容,及指令行数
#sc=!!ae run,st=点击运行指令#§7{0} run §b<脚本名> §a§l[▷] §e手动执行某个脚本
#sc=!!ae auto,st=点击运行指令#§7{0} auto §b<脚本名> §a§l[▷] §e打开或者关闭某个脚本自动执行
#sc=!!ae kill,st=点击运行指令#§7{0} kill §b<脚本名> §a§l[▷] §e终止某个脚本运行
#sc=!!ae des,st=点击运行指令#§7{0} des §b<脚本名> §a§l[▷] §e修改某个脚本的简介
#sc=!!ae set,st=点击运行指令#§7{0} set §b<脚本名> <权限> §a§l[▷] §e修改某个脚本的权限
#sc=!!ae reload,st=点击运行指令#§7{0} reload §a§l[▷] §e重载插件
'''.format(Prefix, "Auto execute", "1.1.0")


def create_script(source: CommandSource, dic: dict):
    check_file(dic["script"], source)


def remove_script(source: CommandSource, dic: dict):
    script = script_path.format(dic['script'])

    if not os.path.exists(script):
        source.reply(f"§4§l脚本{dic['script']}不存在")
    else:
        data = Ed.get_json_object(script)

        if source.get_permission_level() < data["single_permission"]:
            source.reply(
                f"§4§l你没有编辑脚本{dic['script']}的权限,需要权限{data['single_permission']},你为{source.get_permission_level()}")
        else:
            os.remove(script)
            source.reply(f"§a§l成功删除脚本{dic['script']}!!")


def add_command(source: CommandSource, dic: dict):
    script = script_path.format(dic['script'])

    if not os.path.exists(script):
        source.reply(f"§4§l脚本{dic['script']}不存在")
        return

    try:
        with codecs.open(script, 'r+', encoding='utf-8-sig') as file:
            data = json.load(file)

            if source.get_permission_level() < data["single_permission"]:
                source.reply(
                    f"§4§l你没有编辑脚本{dic['script']}的权限,需要权限{data['single_permission']},你为{source.get_permission_level()}")
                return

            if Ed.edit_json_file(script, "command", dic["command"].replace("&", "§"), mode="+"):
                source.reply("§a§l成功添加命令!!")

    except Exception as e:
        source.reply(f"§4§l添加命令时出错,请检查脚本{dic['script']}格式是否正确,错误信息:\n§e{e}")


def insert_command(source: CommandSource, dic: dict):
    script = script_path.format(dic['script'])

    if not os.path.exists(script):
        source.reply(f"§4§l脚本{dic['script']}不存在")
        return

    try:
        with codecs.open(script, 'r+', encoding='utf-8-sig') as fp:
            con = json.load(fp)

            if source.get_permission_level() < con["single_permission"]:
                source.reply(
                    f"§4§l你没有编辑脚本{dic['script']}的权限,需要权限{con['single_permission']},你为{source.get_permission_level()}")
                return

            if not con["command"] and dic["index"] == 1:
                con["command"].append(dic["command"].replace("&", "§"))
            elif 1 <= dic["index"] <= len(con["command"]):
                con["command"].insert(dic["index"] - 1, dic["command"].replace("&", "§"))
            else:
                source.reply("§4§l输入超出范围")
                return

            fp.seek(0)
            fp.truncate()
            json.dump(con, fp, indent=4, ensure_ascii=False)
            source.reply("§a§l成功添加命令!!")
    except Exception as e:
        source.reply(f"§4§l添加命令时出错,请检查脚本{dic['script']}格式是否正确,错误信息:\n§e{e}")


def delete_command(source: CommandSource, dic: dict):
    script = script_path.format(dic['script'])

    if not os.path.exists(script):
        source.reply(f"§4§l脚本{dic['script']}不存在")
        return

    try:
        with codecs.open(script, 'r+', encoding='utf-8-sig') as fp:
            new_file = json.load(fp)

            if source.get_permission_level() < new_file["single_permission"]:
                source.reply(
                    f"§4§l你没有编辑脚本{dic['script']}的权限,需要权限{new_file['single_permission']},你为{source.get_permission_level()}")
                return

            if not new_file["command"]:
                source.reply("§4§l该脚本里不存在任何命令!!")
            elif dic["command"] not in new_file["command"]:
                source.reply("§4§l该脚本里不存在该命令!!")
            elif source.get_permission_level() < new_file["single_permission"]:
                source.reply(
                    f"§4§l你没有编辑脚本{dic['script']}的权限,需要权限{new_file['single_permission']},你为{source.get_permission_level()}")
            else:
                new_file["command"].remove(dic["command"].replace("&", "§"))
                fp.seek(0)
                fp.truncate()
                json.dump(new_file, fp, indent=4, ensure_ascii=False)
                source.reply("§a§l成功删除命令!!")

    except Exception as e:
        source.reply(f"§4§l删除命令时出错,请检查脚本{dic['script']}格式是否正确,错误信息:\n§e{e}")


def del_index(source: CommandSource, dic: dict):
    script = script_path.format(dic['script'])

    if not os.path.exists(script):
        source.reply(f"§4§l脚本{dic['script']}不存在")
        return

    try:
        with codecs.open(script, 'r+', encoding='utf-8-sig') as fp:
            con = json.load(fp)

            if source.get_permission_level() < con["single_permission"]:
                source.reply(
                    f"§4§l你没有编辑脚本{dic['script']}的权限,需要权限{con['single_permission']},你为{source.get_permission_level()}")
                return

            if dic["value"].isdigit():
                index = int(dic["value"]) - 1
                if index < 0 or index > len(con["command"]):
                    source.reply("§4§l输入超出范围")
                    return
                con["command"].pop(index)
            elif "-" in dic["value"]:
                start, end = dic["value"].split('-', maxsplit=1)
                start = int(start) - 1
                end = int(end) - 1
                if not (0 <= start < len(con["command"]) and 0 <= end < len(con["command"])):
                    source.reply("§4§l输入超出范围")
                    return
                del con["command"][start: end + 1]
            else:
                source.reply("§4§l命令输入错误")
                return

            fp.seek(0)
            fp.truncate()
            json.dump(con, fp, indent=4, ensure_ascii=False)
            source.reply("§a§l成功删除命令!!")

    except IndexError:
        source.reply("§4§l脚本内无指令")

    except Exception as e:
        source.reply(f"§4§l删除命令时出错,请检查脚本{dic['script']}格式是否正确,错误信息:\n§e{e}")


def show_list(source: CommandSource):
    file_list = [json_file.replace('.json', '') for json_file in os.listdir(Pc.script_path) if
                 json_file.endswith(".json")]

    if not file_list:
        source.reply('§4§l目前没有存在的脚本')
        return

    msg_list = ["§d【脚本列表】"]

    for script in file_list:
        try:
            with codecs.open(script_path.format(script), 'r', encoding="utf-8-sig") as fp:
                con = json.load(fp)
                if con:
                    msg = f"- {script} #sc=!!ae run {script},st=运行脚本#§a§l[▷] #sc=!!ae remove {script},st=删除脚本#§c§l[×] " \
                          f"#sc=!!ae look {script},st=查看脚本内容#§b§l[c] #sc=!!ae auto {script},st=添加脚本到自动启动列表#§d§l[o] " \
                          f"##注释: {con['description'] if con['description'].strip() else '§7空'} "

                    msg_list.append(msg)

        except Exception:
            continue

    if len(msg_list) > 1:
        msg = "\n".join(msg_list)
        res = Message.get_json_str(msg)
        source.reply(res)

    else:
        source.reply('§4§l目前没有存在的脚本')


def show_content(source: CommandSource, dic: dict):
    script = script_path.format(dic['script'])
    if not os.path.exists(script):
        source.reply(f"§4§l脚本{dic['script']}不存在")
        return

    try:
        with codecs.open(script, 'r', encoding='utf-8-sig') as fp, codecs.open(total_config_path, 'r',
                                                                               encoding="utf-8-sig") as p:
            con = json.load(fp)
            t = json.load(p)

        msg_list = ["§d【脚本详情】", f"脚本名称: {dic['script']}",
                    f"{'脚本自启: 是' if dic['script'] in t['auto_execute_list'] else '脚本自启: 否'}"]

        for i in con:
            if i == "description":
                msg_list.append(f"脚本简介: {con[i]}" if con[i].strip() else "脚本简介: §7空")

            elif i == "single_permission":
                msg_list.append(f"脚本独立权限: {con[i]}")

            elif i == "command":
                if not con[i]:
                    msg_list.append("脚本命令: §7空")

                else:
                    msg_list.append("脚本命令: ")
                    for index, cmd in enumerate(con[i]):
                        msg_list.append(f"- §e{index + 1} §r[#cc={cmd},st=复制内容到剪切板#§a{cmd}##§r]")

        msg = "\n".join(msg_list)
        res = Message.get_json_str(msg)
        source.reply(res)

    except Exception as e:
        source.reply(f"§4§l读取脚本失败,请检查脚本{dic['script']}格式是否正确,错误信息:\n§e{e}")


def show_auto_list(source: CommandSource):
    if not os.path.exists(total_config_path):
        check_file()
        source.reply("§4§l配置文件不存在,已重新生成!!")
        return

    try:
        with codecs.open(total_config_path, 'r', encoding='utf-8-sig') as fp:
            al = json.load(fp)

        file_list = [json_file for json_file in al["auto_execute_list"] if
                     os.path.exists(script_path.format(json_file))]

    except Exception as e:
        source.reply(f"§4§l配置文件格式错误!!,错误信息:\n§e{e}")
        return

    if not file_list:
        source.reply("§4§l自动启动列表里不存在脚本")
        return

    msg_list = ["§d【自动启动列表】"]

    for script in file_list:
        try:
            with codecs.open(script_path.format(script), 'r', encoding="utf-8-sig") as fp:
                con = json.load(fp)
                if con:
                    desc = con['description'].strip() if con['description'].strip() else '§7空'
                    msg = f"- {script} #sc=!!ae run {script},st=运行脚本#§a§l[▷] #sc=!!ae remove {script},st=删除脚本#§c§l[×] " \
                          f"#sc=!!ae look {script},st=查看脚本内容#§b§l[c] #sc=!!ae auto on {script},st=添加脚本到自动启动列表#§d§l[o] " \
                          f"##注释: {desc}"

                    msg_list.append(msg)

        except Exception:
            continue

    if len(msg_list) > 1:
        msg = "\n".join(msg_list)
        res = Message.get_json_str(msg)
        source.reply(res)

    else:
        source.reply('§4§l请检查自启列表里脚本格式是否正确')


def switch_mode(source: CommandSource, dic: dict):
    script = dic.get("script")
    if not os.path.exists(total_config_path):
        check_file()
        source.reply("§4§l配置文件不存在,已重新生成!!")
        return

    if not os.path.exists(script_path.format(script)):
        source.reply(f"§4§l脚本{dic['script']}不存在")
        return

    try:
        with codecs.open(total_config_path, 'r+', encoding='utf-8-sig') as fp:
            con = json.load(fp)

            if script in con["auto_execute_list"]:
                con["auto_execute_list"].remove(script)
                fp.seek(0)
                fp.truncate()
                json.dump(con, fp, indent=4, ensure_ascii=False)
                source.reply(f"§a§l脚本{script}已被成功从自动启动列表里删除")

            else:
                con["auto_execute_list"].append(script)
                fp.seek(0)
                fp.truncate()
                json.dump(con, fp, indent=4, ensure_ascii=False)
                source.reply(f"§a§l脚本{script}已被成功添加到自动启动列表里")

    except Exception as e:
        source.reply(f"§4§l配置文件格式错误!!,错误信息:\n§e{e}")


def print_help_msg(source: CommandSource):
    source.reply(Message.get_json_str(help_msg))


def kill_loop_script(source: CommandSource, dic: dict):
    script = dic.get("script")
    if script in running_tasks:
        running_tasks[script].end = True
        running_tasks.pop(script)
        source.reply(f"§a§l已卸载脚本{script}")
    else:
        source.reply(f"§a§l脚本{script}未运行")


def set_des_value(source: CommandSource, dic: dict):
    script = script_path.format(dic["script"])
    if not os.path.exists(script):
        source.reply(f"§4§l脚本{dic['script']}不存在")
        return

    try:
        with codecs.open(script, 'r+', encoding='utf-8-sig') as file:
            data = json.load(file)
            if source.get_permission_level() >= data["single_permission"]:
                data["description"] = dic["value"].replace("&", "§")
                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=4, ensure_ascii=False)
                source.reply(f"§a§l成功修改脚本{dic['script']}的简介!!")
            else:
                source.reply(
                    f"§4§l你没有编辑脚本{dic['script']}的权限,需要权限{data['single_permission']},你为{source.get_permission_level()}")

    except Exception as e:
        source.reply(f"§4§l读取脚本{dic['script']}失败,请检查脚本格式是否正确,错误信息:\n§e{e}")


def set_script_permission(source: CommandSource, dic: dict):
    script = script_path.format(dic["script"])
    if not os.path.exists(script):
        source.reply(f"§4§l脚本{dic['script']}不存在")
        return

    try:
        with codecs.open(script, 'r+', encoding='utf-8-sig') as file:
            data = json.load(file)
            if source.get_permission_level() >= data["single_permission"]:
                data["single_permission"] = dic["per"]
                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=4, ensure_ascii=False)
                source.reply(f"§a§l成功修改脚本{dic['script']}的权限!!")
            else:
                source.reply(
                    f"§4§l你没有编辑脚本{dic['script']}的权限,需要权限{data['single_permission']},你为{source.get_permission_level()}")

    except Exception as e:
        source.reply(f"§4§l读取脚本{dic['script']}失败,请检查脚本格式是否正确,错误信息:\n§e{e}")


def check_file(script=None, source=None):
    if not script:
        if not os.path.exists(total_config_path):
            Ed.new_json_file(total_config_path, Dt.get_default().serialize())

        if not os.path.exists(Pc.script_path):
            os.mkdir(Pc.script_path)

        if os.path.exists(total_config_path) and os.path.exists(Pc.script_path):
            return
    else:
        if not os.path.exists(total_config_path):
            Ed.new_json_file(total_config_path, Dt.get_default().serialize())
            check_file()
        elif not os.path.exists(Pc.script_path):
            os.mkdir(Pc.script_path)
            check_file()

    if not os.path.exists(script_path.format(script)):
        Ed.new_json_file(script_path.format(script), script_content)
        source.reply('§a§l成功创建脚本')
        return

    else:
        source.reply(f"§4§l脚本{script}已存在,请更换名称！")


class Script:

    def __init__(self, source, script, data):
        self.source = source
        self.script = script
        self.data = data
        self.end = False

    def run_script(self):
        self.source.reply(f"§a§l脚本{self.script}运行成功")

        for command in self.data["command"]:
            if self.end:
                return
            '''运行@ae 指令'''
            res = Al.analysis_command(command, self.source, self.script)

            if res[0]:
                if res[1] == "loop" and not self.end:
                    thread_execute(self.source, script=self.script)
                    return
                continue
            # 执行mc指令
            if command.startswith("/"):
                self.source.get_server().execute(command)
                continue
            # 执行MCDR指令
            self.source.get_server().execute_command(command, self.source)

        try:
            running_tasks.pop(self.script)
            self.source.reply(f"§a§l脚本{self.script}运行完毕!!")
        except KeyError:
            return


def thread_execute(source: CommandSource = CommandSource, dic: dict = dict, script=None):
    if not script:
        _script = "§a" + dic["script"]
        if dic["script"] in running_tasks:
            source.reply(f"§4§l脚本{dic['script']}正在运行,请勿重复运行!!")
            return
    else:
        _script = "§a" + script

    @new_thread
    def execute_command(_script, source):
        path = script_path.format(_script)
        if not os.path.exists(path):
            source.reply(f"§4§l脚本{_script}不存在")
            return

        try:
            with codecs.open(path, 'r', encoding='utf-8-sig') as file:
                data = json.load(file)
                if not data["command"]:
                    source.reply(f"§4§l脚本{_script}里不存在指令")
                    return

                if source.get_permission_level() < data["single_permission"]:
                    source.reply(
                        f"§4§l你没有编辑脚本{_script}的权限,需要权限{data['single_permission']},你为{source.get_permission_level()}")
                    return

                running_tasks[_script] = Script(source, _script, data)
                running_tasks[_script].run_script()

        except Exception as e:
            source.reply(f"§4§l读取脚本{_script}失败,请检查脚本格式是否正确,错误信息:\n§e{e}")

    execute_command(_script.strip("§a"), source).name = _script


def reload_plugin(source: CommandSource):
    source.get_server().reload_plugin("auto_execute")
    source.reply("§a§l插件已重载")


def show_tasks(source: CommandSource):
    if not running_tasks:
        source.reply("§4§l没有脚本正在运行")
        return

    msg_list = ["§d【自动启动列表】"]

    for i in running_tasks:
        msg_list.append(f"- {i} #sc=!!ae kill {i},st=终止该脚本运行#§4§l[p]")

    msg = "\n".join(msg_list)
    res = Message.get_json_str(msg)
    source.reply(res)


def on_load(server: PluginServerInterface, old):
    server.register_help_message('!!ae', '查看与执行脚本有关的指令')
    check_file()

    with codecs.open(total_config_path, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)

    level_dict = data["minimum_permission_level"]

    builder = SimpleCommandBuilder()
    require = Requirements()

    builder.command('!!ae', print_help_msg)
    builder.command('!!ae make <script>', create_script)
    builder.command('!!ae remove <script>', remove_script)
    builder.command('!!ae add <script> <command>', add_command)
    builder.command('!!ae del <script> <command>', delete_command)
    builder.command('!!ae list', show_list)
    builder.command('!!ae look <script>', show_content)
    builder.command('!!ae auto_list', show_auto_list)
    builder.command('!!ae auto <script>', switch_mode)
    builder.command('!!ae run <script>', thread_execute)
    builder.command('!!ae kill <script>', kill_loop_script)
    builder.command('!!ae des <script> <value>', set_des_value)
    builder.command('!!ae set <script> <per>', set_script_permission)
    builder.command('!!ae insert <script> <index> <command>', insert_command)
    builder.command('!!ae re <script> <value>', del_index)
    builder.command('!!ae reload', reload_plugin)
    builder.command('!!ae run_list', show_tasks)

    builder.arg('script', Text)
    builder.arg('command', GreedyText)
    builder.arg('per', Integer)
    builder.arg('index', Integer)
    builder.arg('value', Text)

    command_literals = ["make", "remove", "add", "del", "list", "look", "auto_list", "auto", "run", "kill",
                        "des", "set", "insert", "re", "reload", "run_list"]

    for literal in command_literals:
        permissions = level_dict.get(literal, [])
        builder.literal(literal).requires(require.has_permission(permissions),failure_message_getter=lambda err: "权限不足")

    builder.register(server)


def on_server_startup(server: ServerInterface):
    with codecs.open(total_config_path, 'r', encoding='utf-8-sig') as data:
        _config = json.load(data)

    if not _config["turn_off_auto_execute"]:
        if _config["auto_execute_list"]:
            source = server.get_plugin_command_source()
            for i in _config["auto_execute_list"]:
                if i not in running_tasks:
                    thread_execute(source=source, script=i)


def on_unload(server: PluginServerInterface):
    if running_tasks:
        for obj in running_tasks.values():
            obj.end = True
        running_tasks.clear()

    else:
        running_tasks.clear()
