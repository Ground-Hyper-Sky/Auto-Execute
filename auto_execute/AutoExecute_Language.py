import time
import datetime
from dateutil.relativedelta import relativedelta


class Auto_Language:
    Language_list = ["sleep", "loop", "tell"]

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

    # @ae sleep <time>
    @staticmethod
    def sleep(command, source, script):
        try:
            source.reply(f"§a§l脚本{script}将在{command.split()[2]}秒后继续执行")
            time.sleep(float(command.split()[2]))
            return True

        except Exception as e:
            source.reply(f"§4§l脚本{script}命令{command.split()[2]}运行出错。错误信息:\n§e{e}")
            return False

    # @ae loop <time>
    @staticmethod
    def loop(command, source, script):
        try:
            source.reply(f"§a§l脚本{script}将在{command.split()[2]}秒后开始下一次循环")
            time.sleep(float(command.split()[2]))
            return True

        except Exception as e:
            source.reply(f"§4§l脚本{script}命令{command.split()[2]}运行出错。错误信息:\n§e{e}")
            return False

    # @ae tell <obj> <con>
    @staticmethod
    def tell(command, source, script):

        pass

    # @ae timed %Y-%m-%d %H:%M:%S
    @staticmethod
    def timed(command, source, script):
        i = command.split(maxsplit=2)[-1]

        if not (len(i.split()) == 2 and len(i.split()[0].split(sep="-")) == 3 and len(
                i.split()[1].split(sep=":")) == 3):
            return

        d = i.split()[0].split(sep="-")
        t = i.split()[1].split(sep=":")

        def get_date_obj(date, _time):
            try:
                return datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S")

            except ValueError:
                pass

            if date[0] == "YY":
                if date[1] == "mm":
                    if date[2] == "dd":
                        if datetime.datetime.now() < datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]),
                                                                                     second=int(_time[2]), microsecond=0):
                            return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                                   microsecond=0)

                        return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                               microsecond=0) + datetime.timedelta(days=1)

                    if int(date[2]) > datetime.datetime.now().day:
                        return datetime.datetime.now().replace(day=int(date[2]), hour=int(_time[0]), minute=int(_time[1]),
                                                               second=int(_time[2]), microsecond=0) + relativedelta(month=1)

                    if int(date[2]) == datetime.datetime.now().day:
                        if datetime.datetime.now() < datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]),
                                                                                     second=int(_time[2]), microsecond=0):
                            return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                                   microsecond=0)

                        return datetime.datetime.now().replace(day=int(date[2]), hour=int(_time[0]), minute=int(_time[1]),
                                                               second=int(_time[2]), microsecond=0) + relativedelta(month=1)

                    return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                           microsecond=0)

                if date[2] != "dd":
                    if datetime.datetime.now() < datetime.datetime.now().replace(month=int(date[1]), day=int(date[2]),
                                                                                 hour=int(_time[0]), minute=int(_time[1]),
                                                                                 second=int(_time[2]), microsecond=0):
                        return datetime.datetime.now().replace(month=int(date[1]), day=int(date[2]), hour=int(_time[0]),
                                                               minute=int(_time[1]), second=int(_time[2]), microsecond=0)

                    return datetime.datetime.now().replace(month=int(date[1]), day=int(date[2]), hour=int(_time[0]),
                                                           minute=int(_time[1]),
                                                           second=int(_time[2]), microsecond=0) + relativedelta(year=1)

                if int(date[1]) > datetime.datetime.now().month:
                    return datetime.datetime.now().replace(month=int(date[1]), day=1, hour=int(_time[0]), minute=int(_time[1]),
                                                           second=int(_time[2]), microsecond=0) + relativedelta(year=1)

                if int(date[1]) == datetime.datetime.now().month:
                    if datetime.datetime.now() < datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]),
                                                                                 second=int(_time[2]), microsecond=0):
                        return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                               microsecond=0)

                    return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                           microsecond=0) + datetime.timedelta(days=1)

                return datetime.datetime.now().replace(month=int(date[1]), day=1, hour=int(_time[0]), minute=int(_time[1]),
                                                       second=int(_time[2]), microsecond=0)

            elif date[1] == "mm":

                if date[2] == "dd":
                    if int(date[0]) > datetime.datetime.now().year:
                        return datetime.datetime.now().replace(year=int(date[0]), month=1, day=1, hour=int(_time[0]),
                                                               minute=int(_time[1]), second=int(_time[2]), microsecond=0)

                    if int(date[0]) == datetime.datetime.now().year:
                        if datetime.datetime.now() < datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]),
                                                                                     second=int(_time[2]), microsecond=0):
                            return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                                   microsecond=0)

                        return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                               microsecond=0) + datetime.timedelta(days=1)
                    return

                if int(date[0]) > datetime.datetime.now().year:
                    return datetime.datetime.now().replace(year=int(date[0]), month=1, day=1, hour=int(_time[0]),
                                                           minute=int(_time[1]), second=int(_time[2]), microsecond=0)

                if int(date[0]) == datetime.datetime.now().year:
                    if int(date[2]) > datetime.datetime.now().day:
                        return datetime.datetime.now().replace(day=int(date[2]), hour=int(_time[0]),
                                                               minute=int(_time[1]), second=int(_time[2]), microsecond=0)

                    if int(date[2]) == datetime.datetime.now().day:
                        if datetime.datetime.now() < datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]),
                                                                                     second=int(_time[2]), microsecond=0):
                            return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                                   microsecond=0)

                        return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                               microsecond=0) + relativedelta(month=1)

                    return datetime.datetime.now().replace(hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]),
                                                           microsecond=0) + relativedelta(month=1)

                return

            elif date[2] == "dd":
                if int(date[0]) > datetime.datetime.now().year:
                    return datetime.datetime.now().replace(year=int(date[0]), month=int(date[1]), day=1, hour=int(_time[0]),
                                                           minute=int(_time[1]), second=int(_time[2]),
                                                           microsecond=0)

                if int(date[0]) == datetime.datetime.now().year:
                    if int(date[1]) > datetime.datetime.now().month:
                        return datetime.datetime.now().replace(month=int(date[1]), day=1, hour=int(_time[0]),
                                                               minute=int(_time[1]), second=int(_time[2]),
                                                               microsecond=0)

                    if int(date[1]) == datetime.datetime.now().month:
                        if datetime.datetime.now() < datetime.datetime.now().replace(hour=int(_time[0]),
                                                                                     minute=int(_time[1]), second=int(_time[2]),
                                                                                     microsecond=0):
                            return datetime.datetime.now().replace(hour=int(_time[0]),
                                                                   minute=int(_time[1]), second=int(_time[2]),
                                                                   microsecond=0)

                        return datetime.datetime.now().replace(hour=int(_time[0]),
                                                               minute=int(_time[1]), second=int(_time[2]),
                                                               microsecond=0) + datetime.timedelta(days=1)

                    return

                return

            return

        if get_date_obj(d,t):
            pass


    @staticmethod
    def copy(command, source, script):
        pass
