#!/usr/bin/env python3
"""Restructure VOCAB to add easy/medium/hard levels."""

import re

with open('/home/duong/viet-fun/index.html', 'r') as f:
    content = f.read()

# Parse existing entries per category
match = re.search(r'const VOCAB = \{(.*?)\};', content, re.DOTALL)
vocab_start = match.start()
vocab_end = match.end()

lines = match.group(0).split('\n')
cat_entries = {}
current_cat = None
bracket_depth = 0
current_text = []

for line in lines:
    m = re.match(r'  (\w+): \[', line)
    if m:
        current_cat = m.group(1)
        bracket_depth = 1
        current_text = [line]
    elif current_cat is not None:
        current_text.append(line)
        for c in line:
            if c == '[': bracket_depth += 1
            if c == ']': bracket_depth -= 1
        if bracket_depth <= 0:
            text = '\n'.join(current_text)
            cat_entries[current_cat] = re.findall(r'\{[^}]*\}', text)
            current_cat = None

print("Existing categories:", list(cat_entries.keys()))
for cat, entries in cat_entries.items():
    print(f"  {cat}: {len(entries)} entries")

# New medium words per category
MEDIUM_WORDS = {
    'animals': [
        '{ en:"Squirrel",  vi:"con sóc",   emoji:"🐿️" }',
        '{ en:"Turtle",    vi:"con rùa",   emoji:"🐢" }',
        '{ en:"Butterfly", vi:"con bướm",  emoji:"🦋" }',
        '{ en:"Elephant",  vi:"con voi",   emoji:"🐘" }',
        '{ en:"Monkey",    vi:"con khỉ",   emoji:"🐒" }',
        '{ en:"Shark",     vi:"con cá mập",emoji:"🦈" }',
        '{ en:"Dragon",    vi:"con rồng",  emoji:"🐉" }',
        '{ en:"Crab",      vi:"con cua",   emoji:"🦀" }',
    ],
    'family': [
        '{ en:"Cousin",          vi:"anh em họ",   emoji:"👥" }',
        '{ en:"Nephew",          vi:"cháu trai",    emoji:"👦" }',
        '{ en:"Niece",           vi:"cháu gái",     emoji:"👧" }',
        '{ en:"Father-in-law",   vi:"bố vợ",        emoji:"👴" }',
        '{ en:"Mother-in-law",   vi:"mẹ vợ",        emoji:"👵" }',
        '{ en:"Husband",         vi:"chồng",        emoji:"👨" }',
        '{ en:"Wife",            vi:"vợ",           emoji:"👩" }',
        '{ en:"Son",             vi:"con trai",     emoji:"👦" }',
    ],
    'food': [
        '{ en:"Spring roll", vi:"chả giò",    emoji:"🌯" }',
        '{ en:"Noodles",     vi:"mì",         emoji:"🍝" }',
        '{ en:"Candy",       vi:"kẹo",        emoji:"🍬" }',
        '{ en:"Ice cream",   vi:"kem",        emoji:"🍦" }',
        '{ en:"Cake",        vi:"bánh ngọt",  emoji:"🎂" }',
        '{ en:"Tea",         vi:"trà",        emoji:"🍵" }',
        '{ en:"Coffee",      vi:"cà phê",     emoji:"☕" }',
        '{ en:"Coconut",     vi:"dừa",        emoji:"🥥" }',
    ],
    'numbers': [
        '{ en:"Zero (0)",        vi:"không",    emoji:"0️⃣" }',
        '{ en:"Ten (10)",        vi:"mười",     emoji:"🔟" }',
        '{ en:"Twenty (20)",     vi:"hai mươi", emoji:"2️⃣0️⃣" }',
        '{ en:"One hundred",     vi:"một trăm", emoji:"💯" }',
        '{ en:"First",           vi:"thứ nhất", emoji:"🥇" }',
        '{ en:"Second",          vi:"thứ hai",  emoji:"🥈" }',
        '{ en:"Pair",            vi:"đôi",      emoji:"👫" }',
        '{ en:"Half",            vi:"một nửa",  emoji:"½" }',
    ],
    'colors': [
        '{ en:"Brown",    vi:"màu nâu",  emoji:"🟤" }',
        '{ en:"Gray",     vi:"màu xám",  emoji:"⬜" }',
        '{ en:"Gold",     vi:"màu vàng kim", emoji:"🥇" }',
        '{ en:"Silver",   vi:"màu bạc",  emoji:"🥈" }',
        '{ en:"Dark",     vi:"màu tối",  emoji:"🌑" }',
        '{ en:"Light",    vi:"màu sáng", emoji:"☀️" }',
        '{ en:"Rainbow",  vi:"cầu vồng", emoji:"🌈" }',
        '{ en:"Beige",    vi:"màu be",   emoji:"🟫" }',
    ],
    'everyday': [
        '{ en:"Cup",        vi:"cốc",       emoji:"🥤" }',
        '{ en:"Plate",      vi:"đĩa",       emoji:"🍽️" }',
        '{ en:"Spoon",      vi:"thìa",      emoji:"🥄" }',
        '{ en:"Fork",       vi:"dĩa",       emoji:"🍴" }',
        '{ en:"Knife",      vi:"dao",       emoji:"🔪" }',
        '{ en:"Chair",      vi:"ghế",       emoji:"🪑" }',
        '{ en:"Table",      vi:"bàn",       emoji:"🪑" }',
        '{ en:"Clock",      vi:"đồng hồ",   emoji:"⏰" }',
    ],
    'body': [
        '{ en:"Cheek",        vi:"má",         emoji:"🫠" }',
        '{ en:"Elbow",        vi:"khuỷu tay",  emoji:"💪" }',
        '{ en:"Knee",         vi:"đầu gối",    emoji:"🦵" }',
        '{ en:"Shoulder",     vi:"vai",        emoji:"🤷" }',
        '{ en:"Neck",         vi:"cổ",         emoji:"🧣" }',
        '{ en:"Wrist",        vi:"cổ tay",     emoji:"⌚" }',
        '{ en:"Ankle",        vi:"mắt cá chân",emoji:"🦶" }',
        '{ en:"Forehead",     vi:"trán",       emoji:"🤔" }',
    ],
    'actions': [
        '{ en:"Sing",        vi:"hát",        emoji:"🎤" }',
        '{ en:"Dance",       vi:"nhảy múa",   emoji:"💃" }',
        '{ en:"Cook",        vi:"nấu ăn",     emoji:"🍳" }',
        '{ en:"Clean",       vi:"lau dọn",    emoji:"🧹" }',
        '{ en:"Throw",       vi:"ném",        emoji:"🤾" }',
        '{ en:"Catch",       vi:"bắt",        emoji:"🧤" }',
        '{ en:"Push",        vi:"đẩy",        emoji:"🏋️" }',
        '{ en:"Pull",        vi:"kéo",        emoji:"🚂" }',
    ],
    'places': [
        '{ en:"Airport",      vi:"sân bay",     emoji:"✈️" }',
        '{ en:"Museum",       vi:"bảo tàng",   emoji:"🏛️" }',
        '{ en:"Gym",          vi:"phòng tập",  emoji:"🏋️" }',
        '{ en:"Church",       vi:"nhà thờ",    emoji:"⛪" }',
        '{ en:"Market",       vi:"chợ",        emoji:"🏪" }',
        '{ en:"Parking lot",  vi:"bãi đỗ xe",  emoji:"🅿️" }',
        '{ en:"Factory",      vi:"nhà máy",    emoji:"🏭" }',
        '{ en:"Bridge",       vi:"cây cầu",    emoji:"🌉" }',
    ],
    'school': [
        '{ en:"Desk",         vi:"bàn học",    emoji:"🪑" }',
        '{ en:"Chalkboard",   vi:"bảng đen",   emoji:"🖥️" }',
        '{ en:"Ruler",        vi:"thước kẻ",   emoji:"📏" }',
        '{ en:"Notebook",     vi:"vở",         emoji:"📓" }',
        '{ en:"Eraser",       vi:"cục tẩy",    emoji:"🧽" }',
        '{ en:"Glue",         vi:"keo",        emoji:"🫙" }',
        '{ en:"Pencil sharpener",vi:"gọt bút chì",emoji:"✏️" }',
        '{ en:"Calculator",   vi:"máy tính",   emoji:"🔢" }',
    ],
    'nature': [
        '{ en:"River",        vi:"con sông",   emoji:"🏞️" }',
        '{ en:"Mountain",     vi:"núi",        emoji:"⛰️" }',
        '{ en:"Lake",         vi:"cái hồ",     emoji:"🏞️" }',
        '{ en:"Forest",       vi:"rừng",       emoji:"🌲" }',
        '{ en:"Ocean",        vi:"đại dương",  emoji:"🌊" }',
        '{ en:"Volcano",      vi:"núi lửa",    emoji:"🌋" }',
        '{ en:"Desert",       vi:"sa mạc",     emoji:"🏜️" }',
        '{ en:"Island",       vi:"hòn đảo",    emoji:"🏝️" }',
    ],
    'feelings': [
        '{ en:"Nervous",     vi:"lo lắng",    emoji:"😰" }',
        '{ en:"Bored",       vi:"chán",       emoji:"😑" }',
        '{ en:"Surprised",   vi:"ngạc nhiên", emoji:"😲" }',
        '{ en:"Proud",       vi:"tự hào",     emoji:"😌" }',
        '{ en:"Lonely",      vi:"cô đơn",     emoji:"😔" }',
        '{ en:"Calm",        vi:"bình tĩnh",  emoji:"😌" }',
        '{ en:"Confused",    vi:"bối rối",    emoji:"😕" }',
        '{ en:"Shy",         vi:"ngại ngùng", emoji:"☺️" }',
    ],
}

# Hard sentences per category
HARD_SENTENCES = {
    'animals': [
        '{ en:"The cat is sleeping on the sofa",   vi:"Con mèo đang ngủ trên ghế sô pha",   emoji:"🐱" }',
        '{ en:"I feed the fish every morning",     vi:"Tôi cho cá ăn mỗi sáng",             emoji:"🐟" }',
        '{ en:"The bird is singing in the tree",   vi:"Con chim đang hót trên cây",        emoji:"🐦" }',
        '{ en:"My dog likes to play outside",      vi:"Chó của tôi thích chơi ngoài sân",   emoji:"🐕" }',
        '{ en:"The rabbit hops very fast",         vi:"Con thỏ nhảy rất nhanh",              emoji:"🐰" }',
    ],
    'family': [
        '{ en:"My dad cooks dinner for us",        vi:"Bố tôi nấu bữa tối cho chúng tôi",   emoji:"👨" }',
        '{ en:"Grandma tells me bedtime stories",  vi:"Bà kể chuyện trước khi ngủ cho tôi", emoji:"👵" }',
        '{ en:"My mom drives me to school",        vi:"Mẹ chở tôi đến trường",              emoji:"👩" }',
        '{ en:"I love my little brother very much",vi:"Tôi yêu em trai lắm",                emoji:"🧒" }',
        '{ en:"We visit grandpa every weekend",    vi:"Chúng tôi thăm ông mỗi cuối tuần",   emoji:"👴" }',
    ],
    'food': [
        '{ en:"I like to eat pho for breakfast",   vi:"Tôi thích ăn phở vào bữa sáng",      emoji:"🍜" }',
        '{ en:"Mom makes delicious spring rolls",  vi:"Mẹ làm chả giò rất ngon",            emoji:"🌯" }',
        '{ en:"I drink milk before going to bed",  vi:"Tôi uống sữa trước khi đi ngủ",      emoji:"🥛" }',
        '{ en:"The bread is fresh from the oven",  vi:"Bánh mì mới ra lò còn nóng",         emoji:"🥖" }',
        '{ en:"I want to eat ice cream after lunch",vi:"Tôi muốn ăn kem sau bữa trưa",      emoji:"🍦" }',
    ],
    'numbers': [
        '{ en:"I have ten fingers on my hands",    vi:"Tôi có mười ngón tay",               emoji:"🔟" }',
        '{ en:"There are seven days in a week",    vi:"Có bảy ngày trong một tuần",         emoji:"📅" }',
        '{ en:"I count to one hundred at school",  vi:"Tôi đếm đến một trăm ở trường",      emoji:"💯" }',
        '{ en:"Two plus two equals four",          vi:"Hai cộng hai bằng bốn",              emoji:"➕" }',
        '{ en:"I am the first in line",            vi:"Tôi đứng đầu hàng",                  emoji:"🥇" }',
    ],
    'colors': [
        '{ en:"The sky is blue today",             vi:"Bầu trời hôm nay màu xanh",          emoji:"🔵" }',
        '{ en:"My favorite color is green",        vi:"Màu yêu thích của tôi là màu xanh lá",emoji:"🟢" }',
        '{ en:"The rainbow has seven colors",      vi:"Cầu vồng có bảy màu",                emoji:"🌈" }',
        '{ en:"Apples are red and bananas are yellow",vi:"Táo màu đỏ và chuối màu vàng",    emoji:"🍎" }',
        '{ en:"I paint with many colors in art class",vi:"Tôi vẽ bằng nhiều màu trong lớp mỹ thuật",emoji:"🎨" }',
    ],
    'everyday': [
        '{ en:"Please pass me the cup of water",   vi:"Làm ơn đưa cho tôi cốc nước",        emoji:"🥤" }',
        '{ en:"I set the table for dinner",        vi:"Tôi dọn bàn cho bữa tối",            emoji:"🍽️" }',
        '{ en:"The clock on the wall is ticking",  vi:"Đồng hồ trên tường đang chạy",       emoji:"⏰" }',
        '{ en:"I brush my teeth every morning",    vi:"Tôi đánh răng mỗi sáng",             emoji:"🪥" }',
        '{ en:"We sit on chairs around the table", vi:"Chúng tôi ngồi ghế quanh bàn",       emoji:"🪑" }',
    ],
    'body': [
        '{ en:"I can touch my toes with my hands", vi:"Tôi có thể sờ ngón chân bằng tay",   emoji:"🤸" }',
        '{ en:"Close your eyes and go to sleep",   vi:"Nhắm mắt lại và đi ngủ",             emoji:"😴" }',
        '{ en:"I use my mouth to speak Vietnamese",vi:"Tôi dùng miệng để nói tiếng Việt",   emoji:"👄" }',
        '{ en:"My arms are strong from climbing",  vi:"Tay tôi khỏe vì leo trèo",           emoji:"💪" }',
        '{ en:"I wear a hat on my head",           vi:"Tôi đội mũ trên đầu",                emoji:"🧢" }',
    ],
    'actions': [
        '{ en:"I sing a song in Vietnamese class", vi:"Tôi hát một bài trong lớp tiếng Việt",emoji:"🎤" }',
        '{ en:"We dance together at the party",    vi:"Chúng tôi nhảy múa cùng nhau ở bữa tiệc",emoji:"💃" }',
        '{ en:"I help mom cook dinner every day",  vi:"Tôi giúp mẹ nấu bữa tối mỗi ngày",   emoji:"🍳" }',
        '{ en:"Please clean your room after playing",vi:"Làm ơn dọn phòng sau khi chơi",    emoji:"🧹" }',
        '{ en:"I can throw the ball very far",     vi:"Tôi có thể ném bóng rất xa",         emoji:"🤾" }',
    ],
    'places': [
        '{ en:"We fly from the airport to Hanoi",  vi:"Chúng tôi bay từ sân bay đến Hà Nội", emoji:"✈️" }',
        '{ en:"The museum has many old artifacts", vi:"Bảo tàng có nhiều đồ cổ",             emoji:"🏛️" }',
        '{ en:"I borrow books from the library",   vi:"Tôi mượn sách ở thư viện",            emoji:"📚" }',
        '{ en:"We buy vegetables at the market",   vi:"Chúng tôi mua rau ở chợ",            emoji:"🏪" }',
        '{ en:"Dad parks the car in the parking lot",vi:"Bố đỗ xe ở bãi đỗ xe",              emoji:"🅿️" }',
    ],
    'school': [
        '{ en:"I sit at my desk in the classroom", vi:"Tôi ngồi ở bàn học trong lớp",        emoji:"🪑" }',
        '{ en:"The teacher writes on the chalkboard",vi:"Cô giáo viết trên bảng đen",       emoji:"🖥️" }',
        '{ en:"I put my books in my backpack",     vi:"Tôi bỏ sách vào ba lô",              emoji:"🎒" }',
        '{ en:"We use a ruler to draw straight lines",vi:"Chúng tôi dùng thước kẻ để vẽ đường thẳng",emoji:"📏" }',
        '{ en:"I write spelling words in my notebook",vi:"Tôi viết từ chính tả vào vở",     emoji:"📓" }',
    ],
    'nature': [
        '{ en:"We swim in the river on hot days",  vi:"Chúng tôi bơi ở sông vào ngày nóng", emoji:"🏞️" }',
        '{ en:"The mountain is covered with snow", vi:"Núi phủ đầy tuyết trắng",             emoji:"⛰️" }',
        '{ en:"Fish live in the lake and the ocean",vi:"Cá sống ở hồ và đại dương",          emoji:"🌊" }',
        '{ en:"We walk through the forest to find mushrooms",vi:"Chúng tôi đi qua rừng để tìm nấm",emoji:"🌲" }',
        '{ en:"The volcano erupted many years ago", vi:"Núi lửa phun trào nhiều năm trước", emoji:"🌋" }',
    ],
    'feelings': [
        '{ en:"I feel happy when I play with friends",vi:"Tôi cảm thấy vui khi chơi với bạn",emoji:"😊" }',
        '{ en:"I am scared of the dark at night",   vi:"Tôi sợ bóng tối vào ban đêm",       emoji:"😨" }',
        '{ en:"Mom is proud when I do good work",   vi:"Mẹ tự hào khi tôi làm tốt",         emoji:"😌" }',
        '{ en:"I feel lonely when no one is home",  vi:"Tôi thấy cô đơn khi không có ai ở nhà",emoji:"😔" }',
        '{ en:"The magic trick made me surprised",  vi:"Màn ảo thuật làm tôi ngạc nhiên",   emoji:"😲" }',
    ],
}

# Build structured VOCAB
def entries_to_str(entries, indent=4):
    pad = ' ' * indent
    return '[' + '\n' + ',\n'.join(f'{pad}{e}' for e in entries) + '\n' + ' ' * (indent-2) + ']'

new_vocab_parts = []
cats_order = ['animals','family','food','numbers','colors','everyday','body','actions','places','school','nature','feelings']
for cat in cats_order:
    easy = cat_entries[cat]
    medium = MEDIUM_WORDS[cat]
    hard = HARD_SENTENCES[cat]
    
    block = f'  {cat}: {{\n'
    block += f'    easy:   {entries_to_str(easy, 4)},\n'
    block += f'    medium: {entries_to_str(medium, 4)},\n'
    block += f'    hard:   {entries_to_str(hard, 4)},\n'
    block += f'  }},'
    new_vocab_parts.append(block)

new_vocab = 'const VOCAB = {\n' + '\n\n'.join(new_vocab_parts) + '\n};\n'

new_content = content[:vocab_start] + new_vocab + content[vocab_end+2:]

# Also update CAT_LABELS to no longer be needed as flat list (keep same)
# Update localStorage key references
new_content = new_content.replace("JSON.parse(localStorage.getItem('viet_mo_2')", "JSON.parse(localStorage.getItem('viet_mo')")
new_content = new_content.replace("localStorage.setItem('viet_mo_2'", "localStorage.setItem('viet_mo'")

with open('/home/duong/viet-fun/index.html', 'w') as f:
    f.write(new_content)

print("Done! VOCAB now has easy/medium/hard per category")
import os
print(f"File size: {os.path.getsize('/home/duong/viet-fun/index.html')} bytes")
