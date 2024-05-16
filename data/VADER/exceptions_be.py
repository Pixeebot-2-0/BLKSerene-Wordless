NEGATE = ['не', 'так', 'нельга', 'касяк', 'мог', 'адважны', 'зрабіў', 'робіць', "з'яўляюцца", 'магу', 'смею', 'рабіць', 'меў', 'мае', 'няма', 'можа', 'павінен', 'ні', 'трэба', 'было', 'маюць', "з'яўляецца", 'і', 'ніколі', 'адзін', 'нічога', 'нідзе', 'варта', 'шанц', 'ага', 'буду', 'э-э-э', 'былі', 'без', 'звычайна', 'хацеў', 'бы', 'будзе', 'стаў', 'рэдка', 'нягледзячы', 'на']
BOOSTER_DICT = {'абсалютна': 0.293, 'дзіўна': 0.293, 'жудасна': 0.293, 'цалкам': 0.293, 'значная': 0.293, 'значна': 0.293, 'рашуча': 0.293, 'глыбока': 0.293, 'выпіваючы': 0.293, 'велізарны': 0.293, 'велізарна': 0.293, 'асабліва': 0.293, 'выключны': 0.293, 'выключна': 0.293, 'экстрэмальны': 0.293, 'надзвычай': 0.293, 'казачна': 0.293, 'гартаць': 0.293, 'фліппін': 0.293, 'хрэн': 0.293, 'фрэкінг': 0.293, 'дзяўбаць': 0.293, 'чароўны': 0.293, 'чорт': 0.293, 'вазьмі': 0.293, 'па-чартоўску': 0.293, 'дурань': 0.293, 'траханне': 0.293, 'прывітанне': 0.293, 'высока': 0.293, 'неверагодна': 0.293, 'інтэнсіўна': 0.293, 'маёр': 0.293, 'галоўным': 0.293, 'чынам': 0.293, 'больш': 0.293, 'большасць': 0.293, 'чыста': 0.293, 'даволі': 0.293, 'сапраўды': 0.293, 'выдатна': 0.293, 'так': 0.293, 'істотна': 0.293, 'старанна': 0.293, 'усяго': 0.293, 'надзвычайна': 0.293, 'uber': 0.293, 'незвычайна': 0.293, 'вымаўляць': 0.293, 'вельмі': 0.293, 'амаль': -0.293, 'ледзьве': -0.293, 'наўрад': -0.293, 'ці': -0.293, 'проста': -0.293, 'дастаткова': -0.293, 'свайго': -0.293, 'роду': -0.293, 'накшталт': -0.293, 'менш': -0.293, 'мала': -0.293, 'маргінальны': -0.293, 'нязначна': -0.293, 'выпадковыя': -0.293, 'часам': -0.293, 'часткова': -0.293, 'дэфіцытны': -0.293, 'невялікі': -0.293, 'злёгку': -0.293, 'некалькі': -0.293, 'гатунак': -0.293}
SENTIMENT_LADEN_IDIOMS = {'парэзаць гарчыцу': 2.0, 'рука ў рот': -2.0, 'назад перадаў': -2.0, 'пускаць дым': -2.0, 'пускаючы дым': -2.0, 'верх': 1.0, 'зламаць нагу': 2.0, 'падрыхтоўка ежы на газе': 2.0, 'у чорным': 2.0, 'у чырвоным': -2.0, 'на мячы': 2.0, "пад надвор'ем": -2.0}
SPECIAL_CASES = {'дзярмо': 3.0, 'бомба': 3.0, 'дрэнная задніца': 1.5, 'задзіра': 1.5, 'аўтобусны прыпынак': 0.0, 'так, правільна': -2.0, 'пацалунак смерці': -1.5, 'памерці за': 3.0, "б'ецца сэрца": 3.5}