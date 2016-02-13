# -*- coding: utf-8 -*-

# Code by Yinzo:        https://github.com/Yinzo
# Origin repository:    https://github.com/Yinzo/SmartQQBot

import cPickle
import random
from collections import namedtuple
from QQLogin import *
from Configs import *
from Msg import *
from plugin import shuishiwodi, shuishiwodiStartStatus
from plugin.weather import Weather
from plugin.Turing import Turing

logging.basicConfig(
    filename='smartqq.log',
    level=logging.DEBUG,
    format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
)


# logging.basicConfig(level=logging.DEBUG)


class Group:
    def __init__(self, operator, ip):
        assert isinstance(operator, QQ), "Pm's operator is not a QQ"
        self.__operator = operator
        if isinstance(ip, (int, long, str)):
            # 使用uin初始化
            self.guin = ip
            self.gid = ""
        elif isinstance(ip, GroupMsg):
            self.guin = ip.from_uin
            self.gid = ip.group_code
        self.msg_id = int(random.uniform(20000, 50000))
        self.group_code = 0
        self.member_list = []
        self.msg_list = []
        self.follow_list = []
        self.tucao_dict = {}
        self.global_config = DefaultConfigs()
        self.private_config = GroupConfig(self)
        self.update_config()
        self.process_order = [
            "game",
            "weather",
            'ask',
            "follow",
            "repeat",
            "callout",
            "command_0arg",
            "command_1arg",
            "tucao",
        ]

        self.dictionary = {'制空':{
                #制空信息
                '1-1':'无制空', '1-2':'无制空', '1-3':'无制空', '1-4':'60确保', '1-5':'无制空，除非掉沟~', '1-6':'下路需要400才能确保Orz',
                '2-1':'84确保', '2-2':'162确保', '2-3':'111确保', '2-4':'246确保', '2-5':'上路无制空，下路306确保',
                '3-1':'boss点84确保，沟里面216确保', '3-2':'boss点无制空，沟里234确保', '3-3':'237确保', '3-4':'246确保', '3-5':'上路762确保，下路G点斩杀阶段有69确保',
                '4-1':'144确保', '4-2':'225确保', '4-3':'228确保', '4-4':'312确保', '4-5':'250可保空优~',
                '5-1':'312确保', '5-2':'291确保', '5-3':'230确保，除非掉沟', '5-4':'348确保', '5-5':'出门420制空，全程空优'
            },
                '攻略':{
                '5-5':'武大B隼鹰翔鹤骑脸~出门420制空','E1':'1BBV2cl3dd 出门选上路 多带反潜~','E2':'带路配置：霞 大淀 足柄 朝霜或者清霜 （带路船有四艘 少一艘都不行） 另外秋月级一艘和CAV，航巡带三式弹 中间分歧选择上路，如果没有带路的话就秋月3bb2cv莽一波，或者下路四战：霞旗舰 bbv 2cav 1cv 1秋月级对空ci，建议带道中支援',
                'E3':'先清运输条然后打血条，水上补给部队阵容：僵尸丸cav4dd + cl2ca秋月+另外两个dd。装备上僵尸丸双大发+指挥塔，航巡配二连，一队dd全部带桶。之后用普通水打就好 不ban雷巡~'
            },
                '配置':{
                '5-5':'武大B隼鹰翔鹤骑脸~出门420制空','E1':'1BBV2cl3dd 出门选上路 多带反潜~','E2':'带路配置：霞 大淀 足柄 朝霜或者清霜 带路船有四艘 少一艘都不行 另外秋月级一艘和CAV，航巡带三式弹，dd可以带一个火箭弹 中间分歧选择上路，如果没有带路的话就秋月3bb2cv莽一波，或者下路四战：霞旗舰 bbv 2cav 1cv 1秋月级对空ci，建议带道中支援',
                'E3':'先清运输条然后打血条，水上补给部队阵容：僵尸丸cav4dd + cl2ca秋月+另外两个dd。装备上僵尸丸双大发+指挥塔，航巡配二连，一队dd全部带桶。二队是作战装备。之后用普通水打就好 不ban雷巡~'
            },
                '奖励':{'E1':'奖励一批战斗粮食 伊良湖 女神 和衣阿华主炮','E2':'初月还有勋章等等','E3':'新的海外舰面条国ca zara 还有如果你是甲鱼就有甲章咯'
            },
                '掉落':{
                '齐柏林':'在E3 L点 就是下路门神那里',
                '欧根':'E3的两个boss都有掉落'
            },
                 '任务':{
                #任务信息
                'E3':'1CL5DD跑活动远征',
                '新年任务':'第一个任务1-3配置1cl5dd 第二任务2-3s胜3次 任意配置（ss队）第三任务4-2要求4bb2dd（带路）或者4bb2cv（战罗盘）第四任务 6-2要求2cv 推荐：3ca1clt2cv或者2ca2clt2cv（制空270） 撒 祝各位提督大人武运 啊！沟1-3沟到死吧！诶嘿！'
            },
                '远征':{
                '东京急行怎么开':'先跑掉80小时的26号远征（敌母港空袭作战），然后跑一下mo作战和水上机作战就可以开东急系远征了。这也和Z1的任务线有关哦~'
            },
                '建造':{
            },
                '大建':{
            },
                '开发':{
            },
                '改修':{
            },
                '配装':{
            },
                '改二':{
                '晓':'70级改二','北上':'50级改二'
            },
                '练级':{

            }
        }


        self.__game_handler = None
        logging.info(str(self.gid) + "群已激活, 当前执行顺序： " + str(self.process_order))
        self.tucao_load()

    def update_config(self):
        self.private_config.update()
        use_private_config = bool(self.private_config.conf.getint("group", "use_private_config"))
        if use_private_config:
            self.config = self.private_config
        else:
            self.config = self.global_config
        self.config.update()

    def handle(self, msg):
        self.update_config()
        if self.group_code <= 0:
            self.group_code = msg.group_code
        logging.info("msg handling.")
        # 仅关注消息内容进行处理 Only do the operation of handle the msg content
        for func in self.process_order:
            try:
                if bool(self.config.conf.getint("group", func)):
                    logging.info("evaling " + func)
                    if eval("self." + func)(msg):
                        logging.info("msg handle finished.")
                        self.msg_list.append(msg)
                        return func
            except ConfigParser.NoOptionError as er:
                logging.warning(str(er) + "没有找到" + func + "功能的对应设置，请检查共有配置文件是否正确设置功能参数")
        self.msg_list.append(msg)

    def get_member_list(self):
        if not self.member_list:
            result = self.__operator.get_group_info_ext2(self.group_code)
            if not result or not result["minfo"]:
                return self.member_list
            MemberInfo = namedtuple('MemberInfo', 'nick province gender uin country city')
            member_lst = map(lambda x: MemberInfo(**x), result["minfo"])
            d = {}
            if result["cards"]:
                for item in result["cards"]:
                    d[item["muin"]] = item["card"]
            if d:
                for member in member_lst:
                    key = str(member.uin)
                    if key in d:
                        member.nick = d[key]
            self.member_list = member_lst
        return self.member_list

    # 发送群消息
    def reply(self, reply_content):
        self.msg_id += 1
        return self.__operator.send_qun_msg(self.guin, reply_content, self.msg_id)

    # 发送临时消息给群成员
    def reply_sess(self, tuin, reply_content, service_type=0):
        self.msg_id += 1
        self.__operator.send_sess_msg2_fromGroup(self.guin, tuin, reply_content, self.msg_id, service_type)

    def command_0arg(self, msg):
        # webqq接受的消息会以空格结尾
        match = re.match(r'^(?:!|！)([^\s\{\}]+)\s*$', msg.content)
        if match:
            command = str(match.group(1))
            logging.info("command format detected, command: " + command)

            if command == "吐槽列表":
                self.show_tucao_list()
                return True

        return False

    def command_1arg(self, msg):
        match = re.match(r'^(?:!|！)([^\s\{\}]+)(?:\s?)\{([^\s\{\}]+)\}\s*$', msg.content)
        if match:
            command = str(match.group(1))
            arg1 = str(match.group(2))
            logging.info("command format detected, command:{0}, arg1:{1}".format(command, arg1))
            if command == "删除关键字" and unicode(arg1) in self.tucao_dict:
                self.tucao_dict.pop(unicode(arg1))
                self.reply("已删除关键字:{0}".format(arg1))
                self.tucao_save()
                return True

        return False

    def show_tucao_list(self):
        result = ""
        for key in self.tucao_dict:
            result += "关键字：{0}      回复：{1}\n".format(key, " / ".join(self.tucao_dict[key]))
        logging.info("Replying the list of tucao")
        self.reply(result)
    '''
    def callout(self, msg):
        if "智障机器人" in msg.content:
            logging.info(str(self.gid) + " calling me out, trying to reply....")
            self.reply("干嘛（‘·д·）")
            return True
        return False
    '''
    def callout(self, msg):
        #TODO: Revise the callout function from dict search based to weight based
        #Using some numerical method to determine the right answer
        #TODO: user specific answer, determined by id of group member
        #TODO: specific nickname: 'taiju' 'zhanshen' 'shaoye'...
      #  logging.info(str(QQ.get_friend_info(msg.send_uin)))

        if "呼叫翔鹤" in msg.content:
         #   logging.info(str(self.tid) + " calling me out, trying to reply....")
            self.reply("干嘛（‘·д·）")
            return True
        if "打倒" in msg.content and "群主" in msg.content:
            self.reply("N酱就由我来守护！")
            return True
        if "打倒" in msg.content and "奶子" in msg.content:
            self.reply("N酱就由我来守护！")
            return True
        if "翔鹤，" in msg.content:
           # logging.info(str(self.tid) + " entering inquiry mode")
            for w in self.dictionary.keys():
                if w in msg.content:
                    logging.debug("type = " + str(type(self.dictionary[w])))
                    if not str(type(self.dictionary[w])) == "<type 'dict'>":
                        self.reply(str(self.dictionary[w]))
                        return True
                    else:
                        for w2 in self.dictionary[w].keys():
                            if w2 in msg.content:
                                if not str(type(self.dictionary[w][w2])) == "<type 'dict'>":
                                    self.reply(str(self.dictionary[w][w2]))


        return False
    def repeat(self, msg):
        if len(self.msg_list) > 0 and self.msg_list[-1].content == msg.content:
            if str(msg.content).strip() not in ("", " ", "[图片]", "[表情]"):
                logging.info(str(self.gid) + " repeating, trying to reply " + str(msg.content))
                self.reply(msg.content)
                return True
        return False

    def tucao(self, msg):
        match = re.match(r'^(?:!|！)(learn|delete)(?:\s?){(.+)}(?:\s?){(.+)}', msg.content)
        if match:
            logging.info("tucao command detected.")
            command = str(match.group(1)).decode('utf8')
            key = str(match.group(2)).decode('utf8')
            value = str(match.group(3)).decode('utf8')
            if command == 'learn':
                if key in self.tucao_dict and value not in self.tucao_dict[key]:
                    self.tucao_dict[key].append(value)
                else:
                    self.tucao_dict[key] = [value]
                self.reply("学习成功！快对我说" + str(key) + "试试吧！")
                self.tucao_save()
                return True

            elif command == 'delete':
                if key in self.tucao_dict and self.tucao_dict[key].count(value):
                    self.tucao_dict[key].remove(value)
                    self.reply("呜呜呜我再也不说" + str(value) + "了")
                    self.tucao_save()
                    return True
        else:
            for key in self.tucao_dict.keys():
                if str(key) in msg.content and self.tucao_dict[key]:
                    logging.info("tucao pattern detected, replying...")
                    self.reply(random.choice(self.tucao_dict[key]))
                    return True
        return False

    def tucao_save(self):
        try:
            tucao_file_path = str(self.global_config.conf.get('global', 'tucao_path')) + str(self.gid) + ".tucao"
            with open(tucao_file_path, "w+") as tucao_file:
                cPickle.dump(self.tucao_dict, tucao_file)
            logging.info("tucao saved. Now tucao list:  {0}".format(str(self.tucao_dict)))
        except Exception:
            logging.error("Fail to save tucao.")
            raise IOError("Fail to save tucao.")

    def tucao_load(self):
        # try:
        tucao_file_path = str(self.global_config.conf.get('global', 'tucao_path'))
        tucao_file_name = tucao_file_path + str(self.gid) + ".tucao"
        if not os.path.isdir(tucao_file_path):
            os.makedirs(tucao_file_path)
        if not os.path.exists(tucao_file_name):
            with open(tucao_file_name, "w") as tmp:
                tmp.close()
        with open(tucao_file_name, "r") as tucao_file:
            try:
                self.tucao_dict = cPickle.load(tucao_file)
                logging.info("tucao loaded. Now tucao list:  {0}".format(str(self.tucao_dict)))
            except EOFError:
                logging.info("tucao file is empty.")
                # except Exception as er:
                #     logging.error("Fail to load tucao:  ", er)
                #     raise IOError("Fail to load tucao:  ", er)

    def follow(self, msg):
        match = re.match(r'^(?:!|！)(follow|unfollow) (\d+|me)', msg.content)
        if match:
            logging.info("following...")
            command = str(match.group(1))
            target = str(match.group(2))
            if target == 'me':
                target = str(self.__operator.uin_to_account(msg.send_uin))

            if command == 'follow' and target not in self.follow_list:
                self.follow_list.append(target)
                self.reply("我开始关注" + target + "啦")
                return True
            elif command == 'unfollow' and target in self.follow_list:
                self.follow_list.remove(target)
                self.reply("我不关注" + target + "了")
                return True
        else:
            if str(self.__operator.uin_to_account(msg.send_uin)) in self.follow_list:
                self.reply(msg.content)
                return True
        return False

    def weather(self, msg):
        match = re.match(ur'^(weather|天气) (\w+|[\u4e00-\u9fa5]+)', msg.content)
        if match:
            logging.info("查询天气...")
            print msg.content
            command = match.group(1)
            city = match.group(2)
            logging.info(msg.content)
            print city
            if command == 'weather' or command == u'天气':
                query = Weather()
                info = query.getWeatherOfCity(city)
                logging.info(str(info))
                self.reply(str(info))
                return True
        return False

    def ask(self, msg):
        match = re.match(ur'^(ask|问) (\w+|[\u4e00-\u9fa5]+)', msg.content)
        if match:
            # logging.info("问答测试...")
            print msg.content
            command = match.group(1)
            info = match.group(2)
            # logging.info("info:")
            logging.info(msg.content)
            # print info
            if command == 'ask' or command == u'问':
                # self.reply("我开始查询" + city + "的天气啦")
                query = Turing()
                info = query.getReply(info)
                logging.info(str(info))
                self.reply(str(info))
                return True
        return False

    def game(self, msg):
        match = re.match(ur'^(?:!|！)(game)\s*(\w+|[\u4e00-\u9fa5]+)?', msg.content)
        if match:
            command = str(match.group(1))
            args1 = match.group(2)
            if not args1:
                self.reply('玩游戏：!game 开始谁是卧底5人局\n结束游戏：!game end')
                return True
            if args1 == 'end':
                if self.__game_handler and self.__game_handler.statusHandle:
                    self.__game_handler.statusHandle = None
                self.__game_handler = None
                self.reply('游戏结束')
                return True
            if args1 and u'谁是卧底' in args1:
                self.__game_handler = shuishiwodi(shuishiwodiStartStatus(), self)
                self.__game_handler.run(msg)
                return True
            return True
        # 没有处理程序时退出
        if not self.__game_handler:
            return False
        # 谁是卧底的处理程序
        if isinstance(self.__game_handler, shuishiwodi):
            if self.__game_handler.status not in ['StartStatus', 'EndStatus']:
                self.__game_handler.run(msg)
                return True  # 游戏期间屏蔽其他处理过程
        return False