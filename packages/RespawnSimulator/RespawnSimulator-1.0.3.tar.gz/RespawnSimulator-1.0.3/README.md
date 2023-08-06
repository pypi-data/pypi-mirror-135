# Respawn Simulator

*Developed by N0P3*

*have fun : )*

## 1.0.3

- `GodChoose()`函数现在是Events的一个方法，`Events.god_choose(character,density=100)`并增加了density参数用于控制事件密度
- Events类现在增加了`get() set()`方法，便于从指定事件取值和修改指定事件
- 现在Events和Events可以直接合并 `events3=events1+events2` 这将会使events2的空事件被忽略

## 简述

重生模拟器框架，可以用来写各种由属性主导的随机事件游戏。

- 如果属性是智力，幸福，财富等可以写常规的重生游戏
- 如果属性是氧气，辐射，温度等可以写类生命线游戏《Lifeline》
- 如果属性是人口，气象，人均生存资料消费，人均享受资料消费等可以写模拟市长
- 如果属性是高度，土壤养分含量，土壤含水量等可以写重生之我是一棵树（？）、
- 还可以创建多个角色，每个玩家设置初始属性，看谁活到最后。《幸运方块》
- 或者创建多个角色共用一套属性：送星际快递坠毁在火星，四人小分队共用氧气，食物等，随机事件导致某些角色死亡影响后续事件
- ......
- 计算工作交给框架，创造你的故事吧。

## 开始使用

### 待更新...

## DEMO

```python
# main.py
import msvcrt

from RespawnSimulator import event, character, property

from test_events import main_events # 从test_events.py中载入main_events (你也可以从表格或是数据库中读入)

ppts = {
    "health": property.Property("健康", 50, 0, 120),
    "face": property.Property("魅力", 10, 0, 100),
    "happiness": property.Property("幸福", 50, 0, 100),
    "_line_pc": property.Property("拥有电脑", 0, 0, 2), # 下划线开头是隐藏属性 此处_line_pc充当一个开关
    "_age": property.Property("年龄", 0, 0, 100), 
    "_die": property.Property("死亡", 0, 0, 1)
}


player = character.Character("Redshirt", ppts)

goon = True
while goon:
    print(player.get("_age"), "岁")
    eid = main_events.god_choose(player) # 上帝掷骰子
    if eid == 0:# 如果发生空事件就增加1岁跳过循环
        player.change("_age", 1)
        continue

    print(main_events.get(eid, "name")) # 显示事件名
    print(main_events.get(eid, "description")) # 显示事件描述
    
    main_events.happen(eid,player) # 让事件发生
    player.show() # 显示角色属性
    player.change("_age", 1) # 年龄+1
    if player.get("_die") > 0 or player.get("health") <= 0 or player.get("_age") >= 100:
        goon = False
    msvcrt.getch()
print(player.Name, " 人生结束") # 可以在这里写人生总结
```

```python
# test_events.py
from RespawnSimulator import event

main_events = event.Events("主线", "没有事件发生", "平安度过一岁..")
main_events.append("自然老死", "活得够久了",
                   {
                       "_age": (70, 101),
                       "health": (50, 101)
                   },
                   {
                       "_die": 1
                   }, 100
                   )
main_events.append("病死", "非常不幸",
                   {
                       "_age": (70, 101),
                       "health": (0, 50)
                   },
                   {
                       "_die": 1
                   }, 100
                   )
main_events.append("死神来了", "无处可逃",
                   {
                       "_age": (51, 52)
                   },
                   {
                       "_die": 1
                   }, 100
                   )
main_events.append("爸妈给你买了电脑", "好耶",
                   {
                       "_age": (20, 30),
                       "happiness": (30, 101)
                   },
                   {
                       "health": -10,
                       "_line_pc": 1
                   })
main_events.append("夺得扫雷中国冠军", "NB",
                   {
                       "_age": (20, 30),
                       "_line_pc": (1, 10),
                   },
                   {
                       "happiness": 10,
                       "_line_pc": 1
                   })
main_events.append("夺得扫雷世界冠军", "NB666",
                   {
                       "_age": (20, 50),
                       "_line_pc": (2, 10),
                   },
                   {
                       "happiness": 10
                   })
```

