# Style Guide Hub

```python

import pandas as pd

df = pd.read_excel('risultato_finale (1).xlsx')

print("Columns:", df.columns.tolist())

print("Shape:", df.shape)

print("Head:")

print(df.head(2).to_dict(orient='records'))

```

```text

Columns: ['ID', 'Nome Modello', 'Descrizione', 'Descrizione Eng', 'Colori', 'Styling / Abbinamenti', 'Consigli di Vendita', 'Consigli di Vendita Eng', 'Gestione Obiezioni', 'Gestione Obiezioni Eng']

Shape: (273, 10)

Head:

[{'ID': 1, 'Nome Modello': 'Cadino', 'Descrizione': 'Этот изысканный пуловер из категории кардной мануфактуры Luisa Spagnoli представляет собой гармоничное сочетание тепла и высокой моды. Модель прямого силуэта (Regular fit) выполнена из благородной смеси шерсти и кашемира с добавлением вискозы для исключительной мягкости. Главным стилистическим акцентом является широкий круглый вырез, дополненный нежной вставкой из несшитого кружева, которая придает образу ноту аристократичной чувственности. Длинные рукава с открытыми краями завершают утонченный дизайн этого изделия.', 'Descrizione Eng': "This exquisite pullover from Luisa Spagnoli's carded knitwear manufactory embodies a harmonious union of warmth and high fashion. Cut in a Regular fit silhouette, the piece is crafted from a noble wool and cashmere blend enriched with viscose for exceptional softness. The signature stylistic accent is a wide round neckline, finished with a delicate raw-edge lace insert that lends the look a note of aristocratic sensuality. Long sleeves with raw-edge cuffs complete this refined design.", 'Colori': 'Beige Tortora (1142 1122): URL non disponibile', 'Styling / Abbinamenti': nan, 'Consigli di Vendita': 'Акцентируйте внимание клиента на роскошном составе: наличие кашемира и шерсти обеспечивает безупречную терморегуляцию и тактильный комфорт. | Предложите модель как идеальное решение для перехода от дневного делового образа к вечернему выходу благодаря изысканной кружевной вставке. | Подчеркните современность кроя: открытые манжеты — актуальный тренд сезона, который выделяет эту модель на фоне классического трикотажа.', 'Consigli di Vendita Eng': "Draw the client's attention to the luxurious composition: the presence of cashmere and wool ensures impeccable thermoregulation and tactile comfort. | Present the piece as the perfect solution for transitioning from a daytime professional look to an evening appearance, thanks to its exquisite lace insert. | Emphasize the contemporary cut: the open cuffs are this season's leading trend, setting this piece apart from classic knitwear.", 'Gestione Obiezioni': "[Кружевная вставка кажется слишком деликатной для повседневного трикотажа.] -> Кружево интегрировано в структуру изделия с использованием высококачественного полиамида, что гарантирует сохранение формы и долговечность декора при правильном уходе. || [Боязнь, что кардная шерсть может вызывать дискомфорт на коже.] -> В состав пряжи входит 30% вискозы и 5% кашемира, что делает текстуру полотна шелковистой и приятной даже для самой чувствительной кожи. || [Модель кажется слишком свободной.] -> Посадка Regular fit разработана специально для создания элегантного, но расслабленного силуэта, который подчеркивает достоинства фигуры, не стесняя движений. || [Бежевый цвет (Tortora) может выглядеть бледно.] -> Этот сложный оттенок является классикой 'тихой роскоши'. Он идеально сочетается с контрастными аксессуарами в золотом исполнении, такими как сумки линии LS1928., || [Как ухаживать за таким комбинированным изделием?] -> Мы рекомендуем профессиональную чистку или исключительно бережную ручную стирку, чтобы сохранить объемную структуру шерсти и не повредить тонкое кружево.", 'Gestione Obiezioni Eng': "[The lace insert seems too delicate for everyday knitwear.] -> The lace is integrated into the structure of the piece using a high-quality polyamide, which guarantees the decoration retains its shape and durability with proper care. || [Concern that carded wool may feel uncomfortable against the skin.] -> The yarn blend includes 30% viscose and 5% cashmere, giving the knit a silky, pleasant texture even for the most sensitive skin. || [The model seems too loose-fitting.] -> The Regular fit is specifically designed to create an elegant yet relaxed silhouette that flatters the figure without restricting movement. || [The beige shade (Tortora) may look pale.] -> This sophisticated shade is a 'Quiet Luxury' classic. It pairs beautifully with contrasting gold-tone accessories, such as bags from the LS1928 line. || [How should this combined-fabric piece be cared for?] -> We recommend professional cleaning or exclusively gentle hand-washing, to preserve the volume of the wool structure and protect the delicate lace."}, {'ID': 2, 'Nome Modello': 'Capire', 'Descrizione': 'Этот пуловер из коллекции Luisa Spagnoli — воплощение чувственной элегантности и мягкого комфорта. Модель выполнена из роскошной смеси мохера, шерсти и полиамида, обеспечивающей воздушную легкость и нежное тепло. Главная деталь — изысканный воротник, открывающий линию плеч, что придает образу аристократичную женственность и утонченность. Прямой силуэт (Regular fit) и безупречно гладкая вязка делают это изделие универсальным дополнением к любому современному гардеробу, идеально подходящим как для дневных образов, так и для вечерних выходов.', 'Descrizione Eng': 'This pullover from the Luisa Spagnoli collection is the embodiment of sensuous elegance and gentle comfort. Crafted from a luxurious blend of mohair, wool and polyamide, it offers airy lightness paired with tender warmth. The defining detail is an exquisite collar that reveals the shoulder line, lending the silhouette an aristocratic femininity and refinement. The Regular fit silhouette and flawlessly smooth knit make this piece a versatile addition to any contemporary wardrobe, equally suited to daytime ensembles and evening occasions.', 'Colori': 'Bordeaux (2452): https://cdn.jooraccess.com/img/uploads/accounts/598756/images/tpx4YIVOQIiHt8_Igw7clQ_966025813696f430ca6aa01_65494584_02830020XX1.jpg | Grigio Melange (0829): https://cdn.jooraccess.com/img/uploads/accounts/598756/images/eb047c27-acac-4b5a-a97c-f54ad6d9fd9d.jpg | Nero (0101): https://cdn.jooraccess.com/img/uploads/accounts/598756/images/7gE-VLFDQvq9vexaNQ3bxw_2132901143696f430c387c93_50366657_02830010XX1.jpg', 'Styling / Abbinamenti': 'Total Look (Bordeaux): Capire 2452 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/tpx4YIVOQIiHt8_Igw7clQ_966025813696f430ca6aa01_65494584_02830020XX1.jpg) в сочетании с юбкой Fumaiolo 3417 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/wwFiw_oWT2q_GVyGFGdBTA_2101252950696f422e559462_75140582_02820100XX1.jpg), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/wwFiw_oWT2q_GVyGFGdBTA_2101252950696f422e559462_75140582_02820100XX1.jpg) браслетом Niassesi 2449 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/2449.png) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/2449.png) и туфлями Uragano A 0986 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/URAGANO_98600000000.jpg). | Total Look (Grigio Melange): Capire 0829 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/eb047c27-acac-4b5a-a97c-f54ad6d9fd9d.jpg) (nan) дополнен юбкой Franchezza 0863 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/franchezza%20grigio%20melange.PNG), (nan) брюками Ustica A 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/USTICA_10100000000.jpg), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/-kY3Y2KLSViF2xufxBbpgA_1050821030696f42287e3c47_60877874_02801390XX1.jpg) серьгами Neanide 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1605403396691c57d8aee920_21613301_02800170XX1.jpg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1605403396691c57d8aee920_21613301_02800170XX1.jpg) и очками Xnina A 0101 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/WhatsApp%20Image%202025-12-10%20at%2014.20.26%20(1).jpeg). | Total Look (Nero): Capire 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/7gE-VLFDQvq9vexaNQ3bxw_2132901143696f430c387c93_50366657_02830010XX1.jpg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/WhatsApp Image 2025-12-12 at 10.52.59.jpeg) со стильной юбкой Faustin 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/dGH9ZaVFQbyTxVct5sWatA_1894557478696f422c166df5_93606032_02820020XX1.jpg), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/dGH9ZaVFQbyTxVct5sWatA_1894557478696f422c166df5_93606032_02820020XX1.jpg) туфлями Udita 0101 0101 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/26a004e2-2211-4fe0-8a64-48232e44c8d0-removebg-preview.png), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/26a004e2-2211-4fe0-8a64-48232e44c8d0-removebg-preview.png) браслетом Necessario 0101 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/3.png) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/necessario 0986.png) и серьгами Nordici 0068 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/nordici.png). (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/nordici.png)', 'Consigli di Vendita': 'Делайте акцент на актуальном тренде открытых плеч: этот фасон визуально удлиняет шею и создает притягательный, но сдержанный образ. | Рекомендуйте модель клиентам, ценящим тактильные ощущения: высокое содержание мохера делает трикотаж невероятно мягким и уютным. | Предлагайте игру фактур: пуловер идеально сочетается с кожей, кружевом или плотным твидом, что подтверждается нашими подиумными образами.', 'Consigli di Vendita Eng': "Emphasize the season's key trend of the off-shoulder neckline: this silhouette visually elongates the neck, creating a captivating yet understated look. | Recommend this piece to clients who value tactile sensation: the high mohair content makes the knit remarkably soft and inviting. | Suggest a play of textures: the pullover pairs beautifully with leather, lace, or heavy tweed, as confirmed by our runway looks.", 'Gestione Obiezioni': "[Мохер может вызывать покалывание.] -> В составе изделия используется высококачественный мохер в сочетании с 35% полиамида, что придает нити шелковистость и минимизирует раздражение кожи. || [Открытые плечи — это непрактично для холодного времени года.] -> Дизайн 'collo rovesciato' (отвернутый воротник) позволяет регулировать степень открытости. К тому же, мохер обладает отличными терморегулирующими свойствами. || [Бордовый цвет кажется слишком ярким.] -> Оттенок 2452 — это глубокий, классический винный тон, который в этом сезоне признан новым нейтральным цветом, идеально сочетающимся с базовой гаммой. || [Прямой крой (Regular fit) может выглядеть мешковато.] -> Именно акцент на плечах балансирует силуэт, создавая элегантную вертикаль, а мягкая драпировка трикотажа деликатно подчеркивает фигуру. || [Как ухаживать за таким деликатным составом?] -> Мы рекомендуем профессиональную химчистку или ручную стирку в прохладной воде со специальными средствами для шерсти, чтобы сохранить пушистую структуру волокон.", 'Gestione Obiezioni Eng': "[Mohair may cause a prickling sensation.] -> The piece is made with high-quality mohair blended with 35% polyamide, which lends the yarn a silky quality and minimizes any skin irritation. || [Off-the-shoulder styling seems impractical for the cold season.] -> The 'collo rovesciato' (folded collar) design allows the degree of coverage to be adjusted. Moreover, mohair offers excellent thermoregulating properties. || [The burgundy shade seems too bold.] -> Shade 2452 is a deep, classic wine tone that this season has become the new neutral, pairing beautifully with the core wardrobe palette. || [The Regular fit cut may look shapeless.] -> It is precisely the emphasis at the shoulders that balances the silhouette, creating an elegant vertical line, while the soft drape of the knit delicately flatters the figure. || [How should such a delicate fiber blend be cared for?] -> We recommend professional dry cleaning or hand-washing in cool water with specialized wool detergents, to preserve the fibers' plush texture."}]

```

```python

import pandas as pd

import re

df = pd.read_excel('risultato_finale (1).xlsx')

# Inspect how styling text looks across records

sample_stylings = df['Styling / Abbinamenti'].dropna().head(5).tolist()

for i, s in enumerate(sample_stylings):

    print(f"--- SAMPLE {i+1} ---")

    print(s)

# Function to parse items and extract name, color code, and image URL from text like "pantaloni Olap 0214 (http://...)"

def extract_items_with_urls(text):

    if not isinstance(text, str):

        return []

    # Pattern matching Name Code (optional) and (URL) or URL

    # Let's test pattern

    # Looks like "Capire 2452 (https://...)" or "юбкой Fumaiolo 3417 (https://...)"

    pattern = r'([A-Za-zА-Яа-я0-9\s]+?)\s*\(?(https?://[^\s)]+)\)?'

    matches = re.findall(pattern, text)

    return matches

print("\nExtracted samples:")

for item in extract_items_with_urls(sample_stylings[0]):

    print(item)

```

```text

--- SAMPLE 1 ---

Total Look (Bordeaux): Capire 2452 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/tpx4YIVOQIiHt8_Igw7clQ_966025813696f430ca6aa01_65494584_02830020XX1.jpg) в сочетании с юбкой Fumaiolo 3417 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/wwFiw_oWT2q_GVyGFGdBTA_2101252950696f422e559462_75140582_02820100XX1.jpg), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/wwFiw_oWT2q_GVyGFGdBTA_2101252950696f422e559462_75140582_02820100XX1.jpg) браслетом Niassesi 2449 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/2449.png) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/2449.png) и туфлями Uragano A 0986 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/URAGANO_98600000000.jpg). | Total Look (Grigio Melange): Capire 0829 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/eb047c27-acac-4b5a-a97c-f54ad6d9fd9d.jpg) (nan) дополнен юбкой Franchezza 0863 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/franchezza%20grigio%20melange.PNG), (nan) брюками Ustica A 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/USTICA_10100000000.jpg), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/-kY3Y2KLSViF2xufxBbpgA_1050821030696f42287e3c47_60877874_02801390XX1.jpg) серьгами Neanide 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1605403396691c57d8aee920_21613301_02800170XX1.jpg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1605403396691c57d8aee920_21613301_02800170XX1.jpg) и очками Xnina A 0101 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/WhatsApp%20Image%202025-12-10%20at%2014.20.26%20(1).jpeg). | Total Look (Nero): Capire 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/7gE-VLFDQvq9vexaNQ3bxw_2132901143696f430c387c93_50366657_02830010XX1.jpg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/WhatsApp Image 2025-12-12 at 10.52.59.jpeg) со стильной юбкой Faustin 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/dGH9ZaVFQbyTxVct5sWatA_1894557478696f422c166df5_93606032_02820020XX1.jpg), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/dGH9ZaVFQbyTxVct5sWatA_1894557478696f422c166df5_93606032_02820020XX1.jpg) туфлями Udita 0101 0101 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/26a004e2-2211-4fe0-8a64-48232e44c8d0-removebg-preview.png), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/26a004e2-2211-4fe0-8a64-48232e44c8d0-removebg-preview.png) браслетом Necessario 0101 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/3.png) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/necessario 0986.png) и серьгами Nordici 0068 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/nordici.png). (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/nordici.png)

--- SAMPLE 2 ---

Total Look (Cammello): Cremina 2331 2219 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/BDt_ZIILRNmGizWnsP5YxA_412933266696f435c3f9cf4_66565473_02830290XX1.jpg), Caprese B 2331 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/q-dcDsRCTh-irYmaGwi0fg_1660235822696f430d81f0d5_01266196_02830040XX1.jpg), Fragolino 3274 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/7yuoR1bWTgyth5POk6xtow_2013389323696f422d086a32_26895525_02820060XX1.jpg), Ulisside 2240 0038 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/KXcd3RQpRempSSjJYb6_JA_362957278696f4225f41342_14448703_02801260XX1.jpg), Iago 2240 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/pPKAJyd4QEmcmVBttAaFpw_1733856224696f421e02ec19_56647549_02800630XX1.jpg), Nagorno 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/nagorno.PNG). | Total Look (Nero): Cremina 0101 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/968GUVoMR7eNk2H7UQeWPg_345108726696f435bd28378_65218503_02830280XX1.jpg), Caprese B 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/2sl41gfjQaK9ETlHxdmwRg_220518545696f430d1b6002_25349365_02830030XX1.jpg), Fabula 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1793823539691c5782a10598_51289165_02780010XX1.jpg), Ulisside 0101 0038 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/WhatsApp_Image_2025-12-04_at_09.24.39-removebg-preview (2).png), Neanide 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1605403396691c57d8aee920_21613301_02800170XX1.jpg).

--- SAMPLE 3 ---

Total Look 211 (Blu Inchiostro): Caserta 2544 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/W1aXfSOzQDSO-GRNfAbOfw_373832204696f43567b5bc8_49607223_02830060XX1.jpg) гармонично сочетается с брюками Olap 0214 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/YfLJIN9OTCCGsGAaoXfqug_610004726696f4308184709_09444034_02821440XX1.jpg), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/ynGKN9IHR7KZkKRYYDtgyg_1991141854696f42e6826470_95751980_02820640XX1.jpg) дополнен браслетом Navigero 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1112265162691c57d765cee8_66461141_02800150XX1.jpg), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1112265162691c57d765cee8_66461141_02800150XX1.jpg) колье Navali 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/811531311691c57d6aba2e4_67623166_02800140XX1.jpg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/811531311691c57d6aba2e4_67623166_02800140XX1.jpg) и туфлями Usuale A 0901 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/USUALE_90100020000.jpg). | Total Look 228 (Grigio Melange): Caserta 0856 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/bX-dAybdTxKK_QxHTqy-FQ_1848300653696f430e286d40_01104931_02830050XX2.jpg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/USUALE_90100020000.jpg) в паре с джинсами Olla 1073 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/76c4b186-5565-4440-a457-4d0c57cfa520-removebg-preview.png), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1890676542692424d4b4f858_36560463_02781390XX1.jpg) декорирован брошью Nabrezina 0068 0001 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1988193391691c57e8db2b01_98940325_02800380XX1.jpg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1988193391691c57e8db2b01_98940325_02800380XX1.jpg) и дополнен лоферами Uramaky 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/urmaky.png). (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/Uramaky nero.PNG)

--- SAMPLE 4 ---

Total Look 171 (Menta): Cassina 0506 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/Uc1CyVvMRxq35iiNrN6cig_638464507696f437093a2c8_38813856_02831000XX1.jpg) в сочетании с брюками Olivetano 0943 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/qdI5UwLCT1OH3R6NaxIWHg_1650191426696f42e87b11a6_96447037_02820670XX1.jpg), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/QXBRddRtRfyF-CI0R37DgA_392918825696f43087b6123_57329480_02821450XX1.jpg) дополненный серьгами Neanide 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1605403396691c57d8aee920_21613301_02800170XX1.jpg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1605403396691c57d8aee920_21613301_02800170XX1.jpg) и обувью Uramaky 0990 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/Uramaky nero.PNG). | Total Look 226 (Peonia): Cassina 1802 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/FvNEyO1hTF2ukTdVI6WIyA_1912334563696f43716d5de8_92507245_02831020XX1.jpg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/Uramaky nero.PNG) в паре с джинсами Olla 1073 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/76c4b186-5565-4440-a457-4d0c57cfa520-removebg-preview.png), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1890676542692424d4b4f858_36560463_02781390XX1.jpg) туфлями Urbana 0101 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/image-removebg-preview (27).png), (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/7BoHBVbqTtCtxociDR_4dQ_2049283379696f42280ae740_09477040_02801350XX1.jpg) очками Xnina A 0101 0002 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/WhatsApp Image 2025-12-10 at 14.20.26 (1).jpeg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/WhatsApp Image 2025-12-12 at 10.52.59.jpeg) и сумкой Ls1928p A 0101 0038 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/LS1928P_10100180000 (2).jpg). (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/LS1928P_10100180000 (2).jpg)

--- SAMPLE 5 ---

Total Look Vetrina 99: Cavina (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/0000_0128 (1).jpg) 0952 0428 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/0000_0128 (1).jpg) в сочетании с блузой Latteria 0994 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/j__M1_8VRfWTU6KNBj3dfw_1833518067696f42375a3cc3_36777422_02820360XX1.jpg) (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/3Mx2ef25TdugVXg2-i0IIg_1643286833696f42dfd5b5f6_19897444_02820400XX1.jpg) и брюками Opaglio 0927 (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/2134929375692424d668cd78_06695675_02781440XX1.jpg). (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/2134929375692424d668cd78_06695675_02781440XX1.jpg) Образ дополнен аксессуаром Iri 0970 0002 (Данные отсутствуют в официальных источниках). | Стилистическое решение (Luxury Casual): Сочетание текстурированного кардигана Cavina (https://cdn.jooraccess.com/img/uploads/accounts/598756/images/0000_0128 (1).jpg) с лаконичными формами коллекции Maglieria Cardata позволяет создать многослойный образ, где мерцание люрекса сбалансировано глубиной коричневых оттенков (Marrone).

Extracted samples:

(' Capire 2452', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/tpx4YIVOQIiHt8_Igw7clQ_966025813696f430ca6aa01_65494584_02830020XX1.jpg')

(' в сочетании с юбкой Fumaiolo 3417', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/wwFiw_oWT2q_GVyGFGdBTA_2101252950696f422e559462_75140582_02820100XX1.jpg')

(' ', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/wwFiw_oWT2q_GVyGFGdBTA_2101252950696f422e559462_75140582_02820100XX1.jpg')

(' браслетом Niassesi 2449 0002', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/2449.png')

(' ', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/2449.png')

(' и туфлями Uragano A 0986', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/URAGANO_98600000000.jpg')

(' Capire 0829', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/eb047c27-acac-4b5a-a97c-f54ad6d9fd9d.jpg')

(' дополнен юбкой Franchezza 0863', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/franchezza%20grigio%20melange.PNG')

(' брюками Ustica A 0101', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/USTICA_10100000000.jpg')

(' ', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/-kY3Y2KLSViF2xufxBbpgA_1050821030696f42287e3c47_60877874_02801390XX1.jpg')

(' серьгами Neanide 0002', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1605403396691c57d8aee920_21613301_02800170XX1.jpg')

(' ', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/1605403396691c57d8aee920_21613301_02800170XX1.jpg')

(' и очками Xnina A 0101 0002', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/WhatsApp%20Image%202025-12-10%20at%2014.20.26%20(1')

(' Capire 0101', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/7gE-VLFDQvq9vexaNQ3bxw_2132901143696f430c387c93_50366657_02830010XX1.jpg')

(' ', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/WhatsApp')

(' со стильной юбкой Faustin 0101', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/dGH9ZaVFQbyTxVct5sWatA_1894557478696f422c166df5_93606032_02820020XX1.jpg')

(' ', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/dGH9ZaVFQbyTxVct5sWatA_1894557478696f422c166df5_93606032_02820020XX1.jpg')

(' туфлями Udita 0101 0101 0002', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/26a004e2-2211-4fe0-8a64-48232e44c8d0-removebg-preview.png')

(' ', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/26a004e2-2211-4fe0-8a64-48232e44c8d0-removebg-preview.png')

(' браслетом Necessario 0101 0002', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/3.png')

(' ', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/necessario')

(' и серьгами Nordici 0068 0002', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/nordici.png')

(' ', 'https://cdn.jooraccess.com/img/uploads/accounts/598756/images/nordici.png')

```

Per adattare al meglio il blueprint alle caratteristiche reali del dataset contenuto nel file Excel `risultato_finale (1).xlsx` (che contiene 273 modelli con descrizioni, varianti colore, styling e relative immagini URL), ho aggiornato la specifica tecnica mantenendo l'approccio mobile-first ed elegante.

Ecco il **blueprint aggiornato e ottimizzato**, con le aggiunte specifiche per il parsing degli URL di tutti i capi citati e la struttura completa del progetto:

---

# 📋 BLUEPRINT AGGIORNATO — LUISA SPAGNOLI FW 2026/2027 TRAINING WEB APP

Crea una Web App mobile-first elegante, performante e bilingue (Inglese come lingua predefinita, con possibilità di switch rapido in Russo) per la formazione interna del personale retail di Luisa Spagnoli.

**Titolo Applicazione**:

- **EN**: `"Training Material Fall Winter 2026/2027"`

- **RU**: `"Учебные материалы Осень-Зима 2026/2027"`

---

## 1. ARCHITETTURA TECNICA & STACK

- **Framework**: React (Vite) + TypeScript

- **Stile**: Tailwind CSS (mobile-first, palette lusso: panna, oro satinato/champagne, nero grafite, bordeaux)

- **Componenti UI**: Lucide React Icons, Shadcn UI (`Select` / `Combobox`, `Card`, `Accordion`, `Tabs`, `Badge`, `Button`, `Dialog` / `Lightbox`).

- **Stato lingua**: React Context (`en` predefinito, `ru` alternativo) con persistenza in `localStorage`.

- **Data Source**: Import diretto del file `risultato_finale.json` (convertito dal dataset Excel con i 273 modelli).

---

## 2. LOGICA DI PARSING DATI & ESTRAZIONE URL (CRITICA)

### A. Pulizia del Testo e Parsing degli Outfit/Styling (`parseStylingText`)

Il campo `Styling / Abbinamenti` contiene il testo descrittivo del look interleaved con URL tra parentesi o liberi.

Crea una funzione helper `parseStyling(rawText: string)` che:

1. **Separazione Look**: Divide il testo nei vari look/vetrine usando il separatore `|`.

2. **Estrazione Capi Citati & URL**:

- Analizza ciascun outfit per individuare **tutti i modelli citati** e i rispettivi URL di immagine associate: `NomeModello CodiceColore (http://...)`.

- Struttura ciascun capo estratto come oggetto:

```typescript
interface OutfitItem {
  name: string; // es. "Fumaiolo", "Niassesi", "Uragano A"

  colorCode?: string; // es. "3417", "2449 0002"

  imageUrl: string; // URL immagine funzionante dell'articolo citato
}
```

3. **Pulizia Testo Visivo**:

- Rimuove dal testo dell'outfit qualsiasi URL grezzo (es. `[https://cdn.jooraccess.com/](https://cdn.jooraccess.com/)...`), stringhe `(nan)`, doppie parentesi vuote `()` e spazi in eccesso.

- Il testo finale mostrato nella Card Outfit deve risultare **100% pulito e scorrevole**, privo di link testuali visibili.

### B. Gestione Varianti Colore (`parseColorVariants`)

Formato nel dataset: `Nome Colore (Codice): URL | Nome Colore 2 (Codice): URL`.

- Parsing in array di oggetti: `{ name: string, code: string, imageUrl: string }`.

- Se l'URL è `"URL non disponibile"`, nullo o assente:

- Mostra una card di fallback elegante con sfondo champagne tenue, il nome del colore, il codice e un'icona tematica (es. `Palette` o `Shirt`).

- **Funzione Lightbox**: Tap/Click sulla miniatura per aprire il dettaglio immagine a schermo intero.

### C. Consigli di Vendita (3 Punti Tattici)

- Separati dal carattere `|`.

- Mostrati sia in **EN** (`Consigli di Vendita Eng`) che in **RU** (`Consigli di Vendita`) a seconda della lingua attiva.

- Visualizzati come 3 Card ben formattate con numerazione `01`, `02`, `03` e iconografia luxury (`Sparkles`, `Award`, `TrendingUp`).

### D. Gestione Obiezioni (Anti-Truncate & Layout Dinamico)

- Separati dal delimitatore `||`.

- Pattern di parsing: `[Obiezione cliente] -> Risposta sales assistant`.

- **REQUISITO LAYOUT**:

- `whitespace-normal`, `break-words`, `h-auto`, `overflow-visible`.

- Layout ad **Accordion** o **Card estendibili dinamicamente** per accogliere testi lunghi sia in Russo che in Inglese senza alcun taglio di testo.

---

## 3. STRUTTURA DELLE PAGINE E UI MOBILE-FIRST

### Header Fisso Superiore

- Brand: **LUISA SPAGNOLI** (_Cormorant Garamond_ / _Playfair Display_, maiuscolo, spaziato).

- Sottotitolo: _Training Material FW 2026/2027_.

- Switcher Lingua in alto a destra: Toggle Pill **[ EN | RU ]**.

### Barra di Selezione & Ricerca Modelli

- `Combobox` / `Select` ricercabile contenente la lista in ordine alfabetico di tutti i **273 modelli** presenti nel file (es. _Cadino, Capire, Caprese B, Caserta, Cassina, Cavina..._).

- Pulsante di Azione: **"SEARCH"** (EN) / **"ПОИСК"** (RU) con styling oro satinato `#A37D45` e testo scuro/bianco.

---

### Scheda Modello (Vista Dettaglio capo selezionato)

#### 1. Hero & Intestazione Modello

- Titolo dinamico: **ANALYSIS: [Nome Modello]** (EN) / **АНАЛИЗ: [Nome Modello]** (RU).

- Badge ID e Categoria (es. _ID #2 | Maglieria / Capispalla_).

- Immagine Hero principale del modello (estratta dalla prima variante colore valida).

#### 2. DESCRIPTION / ОПИСАНИЕ

- Testo completo della descrizione (in base alla lingua selezionata: `Descrizione Eng` o `Descrizione`).

- Tipografia moderna e leggibile (_Inter_ / _Montserrat_), interlinea comoda (`leading-relaxed`).

#### 3. COLOR VARIANTS / ВАРИАНТЫ ЦВЕТА

- Griglia a 2 colonne su mobile (3 su tablet/desktop).

- Miniatura dell'immagine variante con bordo dorato sottile + funzione tap-to-zoom (Modal Lightbox).

- Nome del colore e codice univoco (es. _Bordeaux (2452)_).

#### 4. STYLING & COMBINATIONS / СТАЙЛИНГ И СОЧЕТАНИЯ

- Per ogni Total Look / Vetrina parsed:

- **Box Testo Outfit**: Testo completamente pulito da qualsiasi URL o parentesi residua.

- **Gallery Capi Abbinati (Carousel/Grid)**: Sotto al testo dell'outfit, mostra le card visive di tutti i singoli capi citati (con immagine preview, nome del modello e codice colore). Facendo tap sulla card di un capo abbinato, l'app permette di passare direttamente alla scheda di quel modello.

#### 5. SALES ADVICE / СОВЕТЫ ПО ПРОДАЖАМ

- 3 Card numerate (`01`, `02`, `03`) con finiture in oro satinato `#A37D45`, che mettono in risalto i punti di forza del tessuto, la vestibilità e l'esperienza d'uso.

#### 6. OBJECTION HANDLING / УПРАВЛЕНИЕ ВОЗРАЖЕНИЯМИ

- Card espandibili (Accordion) o verticali complete per le 5 obiezioni tipiche:

- **Box Domanda/Obiezione**: Sfondo grigio chiaro/champagne, icona `HelpCircle`, testo in grassetto (`font-semibold text-stone-900`).

- **Box Risposta Sales Assistant**: Sfondo panna, bordo sinistro color oro (`border-l-4 border-[#A37D45]`), icona `CheckCircle2`, testo fluido ed esaustivo.

---

## 4. DESIGN SYSTEM & REGOLE CSS

- **Colori Primari**:

- Background: `#FAF8F5` (Panna/Alabastro)

- Card & Container: `#FFFFFF` con bordo `#E7E2DA` e ombra leggera `shadow-sm`

- Testo Principale: `#1C1917` (Stone 900)

- Dettagli & Accenti: `#A37D45` (Oro Satinato Luisa Spagnoli)

- Sfondo Card Obiezioni: `#F4F0EA` (Champagne tenue)

- **Tipografia**:

- Headings/Titoli: _Playfair Display_ / _Cormorant Garamond_ (Serif lusso)

- Body/Descrizioni: _Inter_ / _Montserrat_ (Sans-serif pulita per mobile)

- **Layout Spacing**: `px-4 py-6` per schermi mobile, `max-w-md` o `max-w-2xl` centrato per schermi più ampi.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/efcbc015-1560-4626-a82e-6a85a53089b9).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
