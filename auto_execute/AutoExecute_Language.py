import time


class Auto_Language:
    Language_list = ["sleep", "loop"]

    @classmethod
    def analysis_command(cls, command, source, script):
        if command.startswith("@ae "):
            try:
                content = command.split()[1:]
                if content[0] in cls.Language_list:
                    if getattr(cls, content[0])(command, source, script):
                        return True, content[0]

                    return False,

                source.reply(f"§4§l命令{command}错误")
                return False,

            except Exception as e:
                source.reply(f"§4§l脚本{script}命令{command}运行出错。错误信息:\n§e{e}")
                return False,

        return False,

    @staticmethod
    def sleep(command, source, script):
        try:
            source.reply(f"§a§l脚本{script}将在{command.split()[2]}秒后继续执行")
            time.sleep(float(command.split()[2]))
            return True

        except Exception as e:
            source.reply(f"§4§l脚本{script}命令{command.split()[2]}运行出错。错误信息:\n§e{e}")
            return False

    @staticmethod
    def loop(command, source, script):
        try:
            source.reply(f"§a§l脚本{script}将在{command.split()[2]}秒后开始下一次循环")
            time.sleep(float(command.split()[2]))
            return True

        except Exception as e:
            source.reply(f"§4§l脚本{script}命令{command.split()[2]}运行出错。错误信息:\n§e{e}")
            return False
