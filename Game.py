# Game.py
# A Streamlit dashboard for the Blank & Spy word-guessing game
# Run on your LAN with `streamlit run Game.py --server.address=0.0.0.0`

import streamlit as st
import random

st.title("🔍 Blank & Spy Game")

# Role display mapping with English and Chinese
ROLE_DISPLAY = {
    'normal': 'Civilian (平民)',
    'spy': 'Spy (间谍)',
    'blank': 'Innocent Civilian (白板)'
}

# Sidebar controls: Restart and Setup
st.sidebar.header("Controls")
if st.sidebar.button("Restart Game"):
    for key in ['num_players', 'num_blanks', 'num_spies', 'roles_list', 'current_turn', 'revealed']:
        st.session_state.pop(key, None)
    st.experimental_rerun = lambda: None
    st.experimental_rerun()

# Setup: define game parameters if not set
if 'num_players' not in st.session_state:
    st.sidebar.subheader("Game Setup")
    n = st.sidebar.number_input("Number of players", min_value=3, max_value=100, step=1)
    b = st.sidebar.number_input("Number of Innocent Civilians", min_value=1, max_value=n-1, step=1)
    s = st.sidebar.number_input("Number of Spies", min_value=1, max_value=n-b, step=1)
    if st.sidebar.button("Initialize Game"):
        st.session_state['num_players'] = int(n)
        st.session_state['num_blanks'] = int(b)
        st.session_state['num_spies'] = int(s)
        st.sidebar.success(f"Game: {n} players, {b} Innocent Civilians, {s} Spies.")
    else:
        st.write("*Configure game parameters in the sidebar and click Initialize Game.*")
        st.stop()

# Initialize roles once
if 'roles_list' not in st.session_state:
    total = st.session_state['num_players']
    blanks = st.session_state['num_blanks']
    spies = st.session_state['num_spies']
    # choose word pair
# Composite word pairs in the format ("English 中文", "English 中文")
    word_pairs = [
        ("toothbrush 牙刷", "paintbrush 画刷"),
        ("soap 肥皂", "sponge 海绵"),
        ("fork 叉子", "spoon 勺子"),
        ("laptop 笔记本电脑", "tablet 平板电脑"),
        ("saxophone 萨克斯管", "clarinet 单簧管"),
        ("key 钥匙", "lock 锁"),
        ("pen 钢笔", "pencil 铅笔"),
        ("shampoo 洗发水", "conditioner 护发素"),
        ("car 汽车", "bicycle 自行车"),
        ("camera 相机", "binoculars 双筒望远镜"),
        ("headphone 耳机", "speaker 扬声器"),
        ("umbrella 雨伞", "raincoat 雨衣"),
        ("pillow 枕头", "blanket 毯子"),
        ("shoe 鞋子", "sock 袜子"),
        ("glove 手套", "mitten 连指手套"),
        ("bottle 瓶子", "cup 杯子"),
        ("ruler 尺子", "tape measure 卷尺"),
        ("knife 刀子", "scissors 剪刀"),
        ("watch 手表", "alarm clock 闹钟"),
        ("suitcase 行李箱", "backpack 背包"),
        ("mirror 镜子", "window 窗户"),
        ("chair 椅子", "bench 长凳"),
        ("book 书", "magazine 杂志"),
        ("hat 帽子", "cap 鸭舌帽"),
        ("telescope 望远镜", "microscope 显微镜"),
        ("guitar 吉他", "violin 小提琴"),
        ("pancake 煎饼", "waffle 华夫饼"),
        ("candle 蜡烛", "lamp 灯"),
        ("clock 时钟", "calendar 日历"),
        ("map 地图", "compass 指南针"),
        ("broom 扫帚", "vacuum cleaner 吸尘器"),
        ("remote control 遥控器", "joystick 操纵杆"),
        ("jar 罐子", "bottle 瓶子"),
        ("kettle 水壶", "teapot 茶壶"),
        ("pliers 钳子", "wrench 扳手"),
        ("hammer 锤子", "screwdriver 螺丝刀"),
        ("soap dispenser 洗手液分配器", "hand sanitizer 免洗洗手液"),
        ("earmuffs 耳罩", "earplugs 耳塞"),
        ("shirt 衬衫", "jacket 夹克"),
        ("shorts 短裤", "pants 长裤"),
        ("sunglasses 太阳镜", "goggles 护目镜"),
        ("frying pan 煎锅", "saucepan 炖锅"),
        ("couch 沙发", "armchair 扶手椅"),
        ("treadmill 跑步机", "exercise bike 健身车"),
        ("pillowcase 枕套", "duvet cover 被套"),
        ("web browser 网页浏览器", "file explorer 文件管理器"),
        ("smartphone 智能手机", "smartwatch 智能手表"),
        ("toaster 烤面包机", "microwave 微波炉"),
        ("refrigerator 冰箱", "freezer 冷冻柜"),
        ("mattress 床垫", "box spring 弹簧床"),
        ("hairbrush 发刷", "comb 梳子"),
        ("notebook 笔记本", "notepad 便签本"),
        ("envelope 信封", "package 包裹"),
        ("stamp 邮票", "sticker 贴纸"),
        ("paint 油漆", "dye 染料"),
        ("fertilizer 肥料", "pesticide 农药"),
        ("shovel 铲子", "rake 耙子"),
        ("sailboat 帆船", "speedboat 快艇"),
        ("glasses 眼镜", "contacts 隐形眼镜"),
        ("cushion 坐垫", "pillow 抱枕"),
        ("marker 马克笔", "highlighter 荧光笔"),
        ("skateboard 滑板", "roller skate 轮滑鞋"),
        ("beach towel 沙滩巾", "bath towel 浴巾"),
        ("ice cream 冰淇淋", "yogurt 酸奶"),
        ("burger 汉堡", "hot dog 热狗"),
        ("coffee 咖啡", "tea 茶"),
        ("wine 葡萄酒", "beer 啤酒"),
        ("stool 凳子", "high chair 高脚椅"),
        ("desk 书桌", "table 餐桌"),
        ("floor lamp 落地灯", "desk lamp 台灯"),
        ("curtain 窗帘", "blind 百叶窗"),
        ("painting 画", "photograph 照片"),
        ("flute 长笛", "trumpet 小号"),
        ("handbag 手提包", "wallet 钱包"),
        ("ring 戒指", "bracelet 手链"),
        ("necklace 项链", "earrings 耳环"),
        ("tie 领带", "scarf 围巾"),
        ("belt 皮带", "suspenders 背带"),
        ("detergent 清洁剂", "bleach 漂白剂"),
        ("body wash 沐浴露", "shower gel 沐浴啫喱"),
        ("printer 打印机", "scanner 扫描仪"),
        ("CPU 中央处理器", "GPU 图形处理器"),
        ("keyboard 键盘", "mouse 鼠标"),
        ("monitor 显示器", "projector 投影仪"),
        ("router 路由器", "modem 调制解调器"),
        ("vault 金库", "safe 保险箱"),
        ("bookshelf 书架", "cabinet 橱柜"),
        ("sandbox 沙箱", "playground 游乐场"),
        ("cradle 摇篮", "crib 婴儿床"),
        ("incubator 孵化器", "greenhouse 温室"),
        ("spatula 锅铲", "ladle 长柄勺"),
        ("kite 风筝", "balloon 气球"),
        ("parachute 降落伞", "paraglider 滑翔伞"),
        ("life jacket 救生衣", "wetsuit 潜水服"),
        ("helmet 头盔", "cap 鸭舌帽"),
        ("sneaker 运动鞋", "boot 靴子"),
        ("sandal 凉鞋", "flip-flop 人字拖"),
        ("hammock 吊床", "swing 秋千"),
        ("username 用户名", "password 密码"),
        ("email 电子邮件", "letter 信")
    ]

    common, spy_word = random.choice(word_pairs)
    indices = list(range(total))
    blank_idx = random.sample(indices, blanks)
    remaining = [i for i in indices if i not in blank_idx]
    spy_idx = random.sample(remaining, spies)
    roles = []
    for idx in indices:
        if idx in blank_idx:
            roles.append({'role': 'blank', 'word': ''})
        elif idx in spy_idx:
            roles.append({'role': 'spy', 'word': spy_word})
        else:
            roles.append({'role': 'normal', 'word': common})
    random.shuffle(roles)
    st.session_state['roles_list'] = roles
    st.session_state['current_turn'] = 0
    st.session_state['revealed'] = False

# Gameplay controls
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Reveal"):
        st.session_state['revealed'] = True
with col2:
    if st.button("Hide & Next"):
        total_roles = len(st.session_state['roles_list'])
        st.session_state['current_turn'] = (st.session_state['current_turn'] + 1) % total_roles
        st.session_state['revealed'] = False

# Display current player index
roles = st.session_state['roles_list']
turn = st.session_state['current_turn']
info = roles[turn]
st.subheader(f"Player {turn+1} of {len(roles)}")

# Show role & word when revealed
if st.session_state['revealed']:
    display_role = ROLE_DISPLAY.get(info['role'], info['role'])
    #st.markdown(f"**Role:** {display_role}")
    word = info['word'] or "(no word)"
    st.markdown(f"### **{word}**")

st.caption("Use 'Hide & Next' to pass control to the next player.")

# Kill feature at bottom
st.divider()
st.subheader("Reveal Specific Player")
player_options = [f"Player {i+1}" for i in range(len(roles))]
selected = st.selectbox("Select Player to Reveal", player_options)
if st.button("Kill"):
    idx = player_options.index(selected)
    info_kill = st.session_state['roles_list'][idx]
    display_role_kill = ROLE_DISPLAY.get(info_kill['role'], info_kill['role'])
    st.markdown(f"**Player {idx+1} Role:** {display_role_kill}")
