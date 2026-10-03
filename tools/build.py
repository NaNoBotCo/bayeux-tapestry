#!/usr/bin/env python3
"""build.py — writes docs/index.html (English) and docs/th/index.html (Thai), sitemap.xml, robots.txt
and llms.txt. Both languages are written by hand here. The strip comes from tools/strip.json
(fetch_strip.py + align_strip.py); the coast from docs/land.js (map_data.py).

Run:  python3 tools/build.py
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "..", "docs")
BASE = "https://nanobotco.github.io/bayeux-tapestry/"
E = html.escape
CSS = open(os.path.join(HERE, "site.css")).read()
GOOGLE_ESCAPE = '<script>if(/[.]translate[.]goog$/.test(location.hostname))location.replace("https://"+location.hostname.slice(0,-15).replace(/--/g,"~").replace(/-/g,".").replace(/~/g,"-")+location.pathname+location.search.replace(/([?&])_x_tr_[^&]*/g,"$1").replace(/[?&]+$/,"").replace(/[?]&+/,"?")+location.hash)</script>'

STRIP = json.load(open(os.path.join(HERE, "strip.json")))
W = STRIP[-1]["x"] + STRIP[-1]["w"]
# The nine linen pieces, in metres (Bayeux museum press kit 2024; French Wikipedia).
PANELS = [13.70, 13.90, 8.19, 7.725, 5.52, 7.125, 7.19, 2.8, 2.43]
LEN = round(sum(PANELS), 3)
# Halley's Comet perihelia since 1066, as decimal years (Yeomans & Kiang 1981; JPL).
PERIHELIA = [1066.22, 1145.30, 1222.74, 1301.82, 1378.86, 1456.44, 1531.65, 1607.82, 1682.71, 1759.20, 1835.88, 1910.30, 1986.11, 2061.57]


def scene_starts():
    """Scene N begins where the photograph centred on scene N-1 ends (checked against the
    backing-cloth numbers). Scenes 28 and 31 share a photograph with 27 and 30: put halfway."""
    start = {}
    for i, t in enumerate(STRIP):
        a = 40 if i == 0 else STRIP[i - 1]["x"] + STRIP[i - 1]["w"]
        start[t["scenes"][0]] = a
        if len(t["scenes"]) > 1:
            start[t["scenes"][1]] = round((a + t["x"] + t["w"]) / 2)
    return start


# Scene number, Latin on the cloth (letters the needle left out restored, after en.wikipedia
# "Bayeux Tapestry tituli"), plain English, plain Thai.
SCENES = [
    (1, "EDWARD REX", "King Edward the Confessor on his throne. The name EDWARD was stitched in by later restorers.", "พระเจ้าเอ็ดเวิร์ดผู้สารภาพประทับบนบัลลังก์ คำว่า EDWARD ช่างซ่อมรุ่นหลังปักเติม"),
    (2, "UBI HAROLD DUX ANGLORUM ET SUI MILITES EQUITANT AD BOSHAM", "Harold, an English earl, rides with his men to Bosham, a hawk on his wrist and hounds running ahead.", "ฮาโรลด์ ขุนนางอังกฤษ ขี่ม้ากับคนของเขาไปบอแชม เหยี่ยวเกาะข้อมือ หมาล่าเนื้อวิ่งนำหน้า"),
    (3, "ECCLESIA", "They stop to pray at Bosham church.", "แวะสวดที่โบสถ์บอแชม"),
    (4, "HIC HAROLD MARE NAVIGAVIT", "A feast upstairs, then Harold wades out to his ship and sails.", "กินเลี้ยงกันบนชั้นบน แล้วฮาโรลด์ลุยน้ำขึ้นเรือ ออกทะเล"),
    (5, "ET VELIS VENTO PLENIS VENIT IN TERRA WIDONIS COMITIS", "Sails full of wind, he comes to the land of Count Guy of Ponthieu.", "ใบเรือเต็มลม เขามาขึ้นฝั่งในแดนของเคานต์กีแห่งปงตีเยอ"),
    (6, "HAROLD", "Harold steps ashore.", "ฮาโรลด์ก้าวขึ้นฝั่ง"),
    (7, "HIC APPREHENDIT WIDO HAROLDUM", "Guy seizes Harold.", "กีจับตัวฮาโรลด์"),
    (8, "ET DUXIT EUM AD BELREM ET IBI EUM TENUIT", "And takes him to Beaurain and holds him there.", "พาไปโบแร็ง แล้วกักตัวไว้ที่นั่น"),
    (9, "UBI HAROLD ET WIDO PARABOLANT", "Harold and Guy talk.", "ฮาโรลด์กับกีเจรจากัน"),
    (10, "UBI NUNTII WILLELMI DUCIS VENERUNT AD WIDONEM · TUROLD", "Duke William's messengers reach Guy. The small man holding the horses has his name stitched beside him: Turold.", "ทูตของดยุกวิลเลียมมาถึงกี ชายตัวเล็กที่จูงม้ามีชื่อปักไว้ข้างตัว ตูโรลด์"),
    (11, "NUNTII WILLELMI", "William's messengers ride hard.", "ทูตของวิลเลียมควบม้าเร่งมา"),
    (12, "HIC VENIT NUNTIUS AD WILGELMUM DUCEM", "A messenger comes to Duke William.", "ผู้ส่งข่าวมาเฝ้าดยุกวิลเลียม"),
    (13, "HIC WIDO ADDUXIT HAROLDUM AD WILGELMUM NORMANNORUM DUCEM", "Guy hands Harold over to William, Duke of the Normans.", "กีพาฮาโรลด์มาส่งให้วิลเลียม ดยุกแห่งนอร์มัน"),
    (14, "HIC DUX WILGELMUS CUM HAROLDO VENIT AD PALATIUM SUUM", "William brings Harold to his palace.", "วิลเลียมพาฮาโรลด์มาที่วังของตน"),
    (15, "UBI UNUS CLERICUS ET ÆLFGYVA", "A priest and a woman named Ælfgyva. The sentence has no verb, and nobody knows what this scene is about.", "นักบวชกับหญิงชื่อแอลฟ์กีวา ประโยคนี้ไม่มีคำกริยา และไม่มีใครรู้ว่าฉากนี้เล่าเรื่องอะไร"),
    (16, "HIC WILLELMUS DUX ET EXERCITUS EIUS VENERUNT AD MONTEM MICHAELIS", "William and his army reach Mont-Saint-Michel.", "วิลเลียมกับกองทัพมาถึงมงแซ็งมีแชล"),
    (17, "ET HIC TRANSIERUNT FLUMEN COSNONIS · HIC HAROLD DUX TRAHEBAT EOS DE ARENA", "They cross the River Couesnon, and Harold pulls men out of the quicksand.", "ข้ามแม่น้ำกูเอนง ฮาโรลด์ดึงทหารขึ้นจากทรายดูด"),
    (18, "ET VENERUNT AD DOL ET CONAN FUGA VERTIT · REDNES", "They reach Dol. Duke Conan of Brittany escapes down a rope. Then Rennes.", "มาถึงเมืองดอล ดยุกโกนองแห่งเบรอตาญโหนเชือกหนีลงจากกำแพง ถัดไปคือเมืองแรน"),
    (19, "HIC MILITES WILLELMI DUCIS PUGNANT CONTRA DINANTES", "William's knights attack Dinan and set it alight.", "อัศวินของวิลเลียมตีเมืองดีน็อง จุดไฟเผา"),
    (20, "ET CUNAN CLAVES PORREXIT", "Conan hands over the keys of the town on the tip of a lance.", "โกนองยื่นกุญแจเมืองให้ที่ปลายหอก"),
    (21, "HIC WILLELMUS DEDIT ARMA HAROLDO", "William gives Harold arms: he makes him his knight.", "วิลเลียมมอบอาวุธให้ฮาโรลด์ คือรับเป็นอัศวินของตน"),
    (22, "HIE WILLELMUS VENIT BAGIAS", "William comes to Bayeux. HIE is a slip of the needle for HIC, 'here'.", "วิลเลียมมาที่บาเยอ คำว่า HIE เข็มพลาด ที่ถูกคือ HIC แปลว่า ตรงนี้"),
    (23, "UBI HAROLD SACRAMENTUM FECIT WILLELMO DUCI", "Harold swears an oath to William, his hands on two boxes of saints' relics.", "ฮาโรลด์สาบานต่อวิลเลียม มือแตะหีบอัฐินักบุญสองใบ"),
    (24, "HIC HAROLD DUX REVERSUS EST AD ANGLICAM TERRAM", "Harold sails home to England.", "ฮาโรลด์ล่องเรือกลับอังกฤษ"),
    (25, "ET VENIT AD EDWARDUM REGEM", "And comes before King Edward, head bowed.", "แล้วเข้าเฝ้าพระเจ้าเอ็ดเวิร์ด ก้มศีรษะ"),
    (26, "HIC PORTATUR CORPUS EADWARDI REGIS AD ECCLESIAM SANCTI PETRI APOSTOLI", "King Edward's body is carried to the church of St Peter, Westminster Abbey. A man fixes the weathercock on the roof.", "พระศพพระเจ้าเอ็ดเวิร์ดถูกหามไปโบสถ์นักบุญเปโตร คือเวสต์มินสเตอร์แอบบีย์ มีคนกำลังติดไก่บอกลมบนหลังคา"),
    (27, "HIC EADWARDUS REX IN LECTO ALLOQUITUR FIDELES", "Edward, in bed, speaks to his faithful men. The story runs backwards here: the funeral came first.", "พระเจ้าเอ็ดเวิร์ดบนพระแท่น ตรัสกับข้าราชบริพาร ตรงนี้เรื่องเล่าย้อนกลับ งานพระศพมาก่อน"),
    (28, "ET HIC DEFUNCTUS EST", "And here he dies: 5 January 1066.", "และสวรรคตตรงนี้ 5 มกราคม 1066"),
    (29, "HIC DEDERUNT HAROLDO CORONAM REGIS", "They give Harold the king's crown.", "ถวายมงกุฎกษัตริย์แก่ฮาโรลด์"),
    (30, "HIC RESIDET HAROLD REX ANGLORUM", "Here sits Harold, King of the English.", "ฮาโรลด์ประทับเป็นกษัตริย์ของชาวอังกฤษ"),
    (31, "STIGANT ARCHIEPISCOPUS", "Archbishop Stigand.", "อาร์ชบิชอปสติแกนด์"),
    (32, "ISTI MIRANT STELLAM", "These men marvel at the star: Halley's Comet, spring 1066.", "คนเหล่านี้แหงนดูดาวด้วยความทึ่ง คือดาวหางแฮลลีย์ ฤดูใบไม้ผลิปี 1066"),
    (33, "HAROLD", "Harold hears the news. In the border below him, ghostly ships.", "ฮาโรลด์ฟังข่าว ที่ขอบล่างใต้ตัวเขามีเรือเงาๆ ลอยมา"),
    (34, "HIC NAVIS ANGLICA VENIT IN TERRAM WILLELMI DUCIS", "An English ship comes to William's land.", "เรืออังกฤษมาถึงแดนของวิลเลียม"),
    (35, "HIC WILLELMUS DUX IUSSIT NAVES AEDIFICARE", "William orders ships built. Trees come down, planks are shaped.", "วิลเลียมสั่งต่อเรือ โค่นต้นไม้ ถากไม้กระดาน"),
    (36, "HIC TRAHUNT NAVES AD MARE", "They drag the ships to the sea.", "ลากเรือลงทะเล"),
    (37, "ISTI PORTANT ARMAS AD NAVES ET HIC TRAHUNT CARRUM CUM VINO ET ARMIS", "Men carry mail shirts, swords and helmets to the ships, and pull a cart of wine and weapons.", "ขนเสื้อเกราะ ดาบ หมวกเหล็ก ขึ้นเรือ และลากเกวียนบรรทุกเหล้าองุ่นกับอาวุธ"),
    (38, "HIC WILLELMUS DUX IN MAGNO NAVIGIO MARE TRANSIVIT ET VENIT AD PEVENESAE", "William crosses the sea in a great ship and lands at Pevensey. The horses come in the boats too.", "วิลเลียมข้ามทะเลด้วยเรือใหญ่ ขึ้นฝั่งที่เพเวนซี ม้าก็นั่งเรือมาด้วย"),
    (39, "HIC EXEUNT CABALLI DE NAVIBUS", "The horses step off the ships.", "ม้าลงจากเรือ"),
    (40, "ET HIC MILITES FESTINAVERUNT HESTINGA UT CIBUM RAPERENTUR", "Knights hurry to Hastings to seize food.", "อัศวินรีบไปเฮสติงส์ ไปยึดเสบียง"),
    (41, "HIC EST WADARD", "This is Wadard, one of Bishop Odo's men.", "นี่คือวาดาร์ด คนของบิชอปโอโด"),
    (42, "HIC COQUITUR CARO ET HIC MINISTRAVERUNT MINISTRI", "Meat is cooked, and servants serve it.", "ปรุงเนื้อ คนรับใช้ยกมาเสิร์ฟ"),
    (43, "HIC FECERUNT PRANDIUM · ET HIC EPISCOPUS CIBUM ET POTUM BENEDICIT", "They feast, and the bishop blesses the food and drink.", "กินมื้อใหญ่ บิชอปอวยพรอาหารและเครื่องดื่ม"),
    (44, "ODO EPISCOPUS · WILLELMUS · ROTBERT", "Bishop Odo, William, Robert: the duke between his two half-brothers.", "บิชอปโอโด วิลเลียม โรแบร์ ดยุกนั่งกลางระหว่างน้องชายต่างพ่อสองคน"),
    (45, "ISTE IUSSIT UT FODERETUR CASTELLUM AT HESTENGA CEASTRA", "He orders a castle mound dug at Hastings camp. CEASTRA is an English word, one clue the makers were English.", "สั่งขุดเนินป้อมที่ค่ายเฮสติงส์ คำว่า CEASTRA เป็นคำอังกฤษ เป็นเบาะแสหนึ่งว่าคนปักเป็นคนอังกฤษ"),
    (46, "HIC NUNTIATUM EST WILLELMO DE HAROLDO", "William gets news of Harold.", "วิลเลียมได้ข่าวเรื่องฮาโรลด์"),
    (47, "HIC DOMUS INCENDITUR", "A house is set on fire. A woman leads a child out.", "บ้านถูกเผา ผู้หญิงจูงเด็กออกมา"),
    (48, "HIC MILITES EXIERUNT DE HESTENGA ET VENERUNT AD PROELIUM CONTRA HAROLDUM REGEM", "The knights leave Hastings and ride to battle against King Harold.", "อัศวินออกจากเฮสติงส์ ไปรบกับพระเจ้าฮาโรลด์"),
    (49, "HIC WILLELMUS DUX INTERROGAT VITALEM SI VIDISSET HAROLDI EXERCITUM", "William asks Vital if he has seen Harold's army.", "วิลเลียมถามวีตาลว่าเห็นกองทัพของฮาโรลด์หรือยัง"),
    (50, "ISTE NUNTIAT HAROLDUM REGEM DE EXERCITU WILLELMI DUCIS", "A scout tells King Harold about William's army.", "คนสอดแนมรายงานพระเจ้าฮาโรลด์เรื่องกองทัพของวิลเลียม"),
    (51, "HIC WILLELMUS DUX ALLOQUITUR SUIS MILITIBUS UT PREPARARENT SE VIRILITER ET SAPIENTER AD PROELIUM CONTRA ANGLORUM EXERCITUM", "William tells his knights to get ready, bravely and wisely, for battle with the English army. 14 October 1066.", "วิลเลียมสั่งอัศวินให้เตรียมรบอย่างกล้าหาญและรอบคอบ สู้กับกองทัพอังกฤษ 14 ตุลาคม 1066"),
    (52, "HIC CECIDERUNT LEWINE ET GYRÐ FRATRES HAROLDI REGIS", "Leofwine and Gyrth, King Harold's brothers, fall.", "เลโอฟไวน์กับเกิร์ธ น้องชายของพระเจ้าฮาโรลด์ ล้มตาย"),
    (53, "HIC CECIDERUNT SIMUL ANGLI ET FRANCI IN PROELIO", "English and French fall together in the battle. Horses tumble at a ditch.", "ทั้งอังกฤษและฝรั่งเศสล้มตายด้วยกันกลางสนามรบ ม้าคะมำที่คูน้ำ"),
    (54, "HIC ODO EPISCOPUS BACULUM TENENS CONFORTAT PUEROS", "Bishop Odo, holding a club, rallies the young men.", "บิชอปโอโดถือกระบอง ปลุกใจพวกหนุ่มๆ"),
    (55, "HIC EST WILLELMUS DUX", "Here is Duke William. He lifts his helmet to show his men he is alive.", "นี่คือดยุกวิลเลียม เขาเปิดหมวกให้ทหารเห็นหน้าว่ายังไม่ตาย"),
    (56, "EUSTATIUS · HIC FRANCI PUGNANT ET CECIDERUNT QUI ERANT CUM HAROLDO", "Eustace of Boulogne. The French fight on and Harold's men fall. In the lower border, looters strip the dead.", "ยูสตาสแห่งบูโลญ ฝ่ายฝรั่งเศสรุกต่อ คนของฮาโรลด์ล้มตาย ขอบล่างมีคนปลดเกราะจากศพ"),
    (57, "HIC HAROLD REX INTERFECTUS EST", "King Harold is killed. Is he the man with the arrow by his eye, or the man cut down by a rider? Historians still argue; perhaps both.", "พระเจ้าฮาโรลด์ถูกสังหาร คือชายที่มีลูกธนูข้างตา หรือชายที่ถูกคนบนหลังม้าฟัน นักประวัติศาสตร์ยังเถียงกันอยู่ อาจเป็นทั้งคู่"),
    (58, "ET FUGA VERTERUNT ANGLI", "And the English turn and run. These words were stitched in shortly before 1814; the first ending is lost.", "และชาวอังกฤษแตกหนี คำนี้ปักเติมก่อนปี 1814 ไม่นาน ตอนจบเดิมหายไปแล้ว"),
]

# Places on the map: lon, lat, English, Thai, label side.
PLACES = {
    "canterbury": (1.080, 51.280, "Canterbury", "แคนเทอร์เบอรี", "r"),
    "bayeux": (-0.703, 49.276, "Bayeux", "บาเยอ", "l"),
    "paris": (2.338, 48.861, "Paris · Louvre", "ปารีส · ลูฟวร์", "r"),
    "sourches": (0.072, 48.128, "Château de Sourches", "ปราสาทซูร์ช", "r"),
    "london": (-0.127, 51.519, "London · British Museum", "ลอนดอน · บริติชมิวเซียม", "l"),
}

# Where it has been. date, place, text.
TIMELINE = {
    "en": [
        ("c. 1070s", "canterbury", "Made in England, most likely at Canterbury, probably for Bishop Odo of Bayeux, William's half-brother. The place comes from the style and the spelling; nobody wrote it down."),
        ("14 Jul 1077?", "bayeux", "Bayeux Cathedral is consecrated. The tapestry may have hung there for the first time that day. No record says so."),
        ("1476", "bayeux", "First written record. The cathedral's inventory lists a very long, narrow hanging, embroidered with the conquest, hung around the nave for the Feast of Relics and the week after. The rest of the year it lay in a chest."),
        ("1562", "bayeux", "Huguenots sack the cathedral. The clergy had already hidden the tapestry."),
        ("1728–1730", "bayeux", "Bernard de Montfaucon tracks it down. Antoine Benoît draws it in the cathedral, and Paris sees it in print for the first time."),
        ("1792", "bayeux", "The Revolution. Soldiers leaving Bayeux want it as a cover for a wagon. A local lawyer, Léonard Lambert-Leforestier, stops them and keeps it safe."),
        ("1794", "bayeux", "Nearly cut into strips to trim a float for a town festival. The district arts commission takes it into the nation's care."),
        ("Dec 1803 – Feb 1804", "paris", "Napoleon has it shown in the Apollo Gallery of the Louvre, then called the Musée Napoléon, while he plans to invade England."),
        ("1804", "bayeux", "Back to Bayeux. (One source says 1805.)"),
        ("1812–1842", "bayeux", "Kept in the town hall, wound on two rollers. A keeper cranked it past visitors scene by scene, which wore out the start."),
        ("1816–1818", "bayeux", "Charles Stothard draws every scene for the Society of Antiquaries of London. A small piece of it leaves with him."),
        ("1842", "bayeux", "First permanent display, under glass, in the town's public library."),
        ("1870–1871", "bayeux", "Hidden during the Franco-Prussian War."),
        ("1872", "bayeux", "Stothard's piece comes back from the South Kensington Museum in London. That autumn Edward Dossetter photographs the whole length on more than 180 glass plates."),
        ("Apr 1913", "bayeux", "Its own museum opens, in the Hôtel du Doyen, the old deanery beside the cathedral."),
        ("Sep 1939", "bayeux", "Rolled up and put in a concrete shelter under the deanery."),
        ("Jun 1941", "bayeux", "Researchers from the SS Ahnenerbe study and copy it. Karl Schlabow cuts small samples of the linen. Germany gave two of them back to Bayeux on 14 January 2026."),
        ("Aug 1941 – Jun 1944", "sourches", "Stored at the Château de Sourches in the Sarthe, with the treasures of France's national museums."),
        ("26 Jun 1944", "paris", "Three weeks after D-Day, the Germans send it to the Louvre."),
        ("Aug 1944", "paris", "Himmler orders it moved somewhere safe. SS men come for it on 21 or 22 August, find the Louvre in Resistance hands, and leave without it."),
        ("10 Nov – 15 Dec 1944", "paris", "Shown at the Louvre after the Liberation, hung on a 70-metre rail."),
        ("Mar 1945", "bayeux", "Home to Bayeux. Back on show at the deanery that October; a new display opens on 6 June 1948."),
        ("1953, 1966", "bayeux", "London asks to borrow it, for the coronation and then for the 900th anniversary of Hastings. Both requests fail; it stays in Bayeux."),
        ("Mar 1983", "bayeux", "Moves to the Centre Guillaume-le-Conquérant, a former seminary on rue de Nesmond, into a horseshoe-shaped gallery."),
        ("2018–2021", "bayeux", "President Macron offers Britain a loan. A survey counts 24,204 stains, 9,646 holes and 30 tears, and the plan waits."),
        ("Sep 2025", "bayeux", "The museum closes for rebuilding. On 19 September the tapestry comes down for the first time since 1983: 7 hours 15 minutes, more than 90 people."),
        ("9–10 Jul 2026", "london", "To London by lorry through the Channel Tunnel, folded on a padded screen inside a crate on springs, with a police escort from Folkestone. About 11 hours; it arrives at 2:50 a.m."),
        ("10 Sep 2026 – 11 Jul 2027", "london", "On show at the British Museum, Room 30, lying flat under glass. France reported two broken threads after the trip."),
        ("Oct 2027", "bayeux", "Due back in Bayeux, in a new museum in the old seminary, for William's thousandth birthday."),
    ],
    "th": [
        ("ราวทศวรรษ 1070", "canterbury", "ทำในอังกฤษ น่าจะที่แคนเทอร์เบอรี สั่งทำโดยบิชอปโอโดแห่งบาเยอ น้องชายต่างพ่อของวิลเลียม ที่ว่าแคนเทอร์เบอรีดูจากลายและการสะกดคำ ไม่มีใครจดไว้"),
        ("14 ก.ค. 1077?", "bayeux", "อาสนวิหารบาเยอเข้าพิธีเสก ผ้าผืนนี้อาจแขวนที่นั่นเป็นครั้งแรกในวันนั้น แต่ไม่มีบันทึก"),
        ("1476", "bayeux", "บันทึกฉบับแรก บัญชีทรัพย์สินของอาสนวิหารเขียนถึงผ้าแขวนยาวมากแต่แคบ ปักเรื่องการพิชิต แขวนรอบโถงกลางในวันฉลองอัฐินักบุญและอีกเจ็ดวันหลังจากนั้น ที่เหลือของปีเก็บไว้ในหีบ"),
        ("1562", "bayeux", "พวกอูเกอโนต์บุกปล้นอาสนวิหาร นักบวชซ่อนผ้าไว้ก่อนแล้ว"),
        ("1728–1730", "bayeux", "แบร์นาร์ เดอ มงโฟกง ตามหาจนเจอ อองตวน เบอนัว วาดลายในอาสนวิหาร ชาวปารีสได้เห็นในหนังสือเป็นครั้งแรก"),
        ("1792", "bayeux", "ช่วงปฏิวัติ ทหารที่ออกจากบาเยอจะเอาไปคลุมเกวียน ทนายความในเมือง เลโอนาร์ ล็องแบร์-เลอฟอเรสติเย ห้ามไว้และเก็บรักษา"),
        ("1794", "bayeux", "เกือบถูกตัดเป็นแถบไปประดับรถแห่ในงานเทศกาลของเมือง คณะกรรมการศิลปะประจำเขตรับไว้เป็นสมบัติของชาติ"),
        ("ธ.ค. 1803 – ก.พ. 1804", "paris", "นโปเลียนสั่งให้นำไปแสดงที่ห้องอะพอลโลในลูฟวร์ สมัยนั้นชื่อพิพิธภัณฑ์นโปเลียน ขณะวางแผนบุกอังกฤษ"),
        ("1804", "bayeux", "กลับบาเยอ (มีแหล่งหนึ่งว่า 1805)"),
        ("1812–1842", "bayeux", "เก็บไว้ที่ศาลาว่าการเมือง ม้วนอยู่บนลูกกลิ้งสองอัน คนเฝ้าหมุนให้ผู้มาเยือนดูทีละฉาก ช่วงต้นผ้าจึงสึก"),
        ("1816–1818", "bayeux", "ชาลส์ สต็อตทาร์ด วาดทุกฉากให้สมาคมนักโบราณคดีแห่งลอนดอน ผ้าชิ้นเล็กชิ้นหนึ่งติดตัวเขาไปด้วย"),
        ("1842", "bayeux", "จัดแสดงถาวรครั้งแรก ในตู้กระจก ที่ห้องสมุดประชาชนของเมือง"),
        ("1870–1871", "bayeux", "ซ่อนไว้ระหว่างสงครามฝรั่งเศส-ปรัสเซีย"),
        ("1872", "bayeux", "ผ้าชิ้นของสต็อตทาร์ดกลับมาจากพิพิธภัณฑ์เซาท์เคนซิงตันในลอนดอน ฤดูใบไม้ร่วงปีนั้น เอ็ดเวิร์ด ดอสเซตเตอร์ ถ่ายภาพตลอดความยาวลงแผ่นกระจกกว่า 180 แผ่น"),
        ("เม.ย. 1913", "bayeux", "มีพิพิธภัณฑ์ของตัวเอง ที่โอแตลดูดัวยอง บ้านเจ้าคณะเก่าข้างอาสนวิหาร"),
        ("ก.ย. 1939", "bayeux", "ม้วนเก็บในหลุมหลบภัยคอนกรีตใต้บ้านเจ้าคณะ"),
        ("มิ.ย. 1941", "bayeux", "นักวิจัยจากหน่วยอาเนนแอร์เบของเอสเอสมาศึกษาและคัดลอก คาร์ล ชลาโบว ตัดตัวอย่างผ้าลินินชิ้นเล็กไป เยอรมนีคืนสองชิ้นให้บาเยอเมื่อ 14 มกราคม 2026"),
        ("ส.ค. 1941 – มิ.ย. 1944", "sourches", "เก็บที่ปราสาทซูร์ชในจังหวัดซาร์ต รวมกับสมบัติของพิพิธภัณฑ์แห่งชาติฝรั่งเศส"),
        ("26 มิ.ย. 1944", "paris", "สามสัปดาห์หลังวันดีเดย์ เยอรมันส่งไปลูฟวร์"),
        ("ส.ค. 1944", "paris", "ฮิมม์เลอร์สั่งให้ย้ายไปที่ปลอดภัย ทหารเอสเอสมาเอาวันที่ 21 หรือ 22 สิงหาคม เจอว่าลูฟวร์อยู่ในมือฝ่ายต่อต้านแล้ว จึงกลับไปมือเปล่า"),
        ("10 พ.ย. – 15 ธ.ค. 1944", "paris", "จัดแสดงที่ลูฟวร์หลังปลดปล่อยปารีส แขวนบนราวยาว 70 เมตร"),
        ("มี.ค. 1945", "bayeux", "กลับบ้านที่บาเยอ ตุลาคมปีนั้นกลับมาจัดแสดงที่บ้านเจ้าคณะ การจัดแสดงชุดใหม่เปิด 6 มิถุนายน 1948"),
        ("1953, 1966", "bayeux", "ลอนดอนขอยืม ครั้งแรกเพื่องานบรมราชาภิเษก ครั้งที่สองเพื่อครบ 900 ปียุทธการที่เฮสติงส์ ไม่สำเร็จทั้งสองครั้ง ผ้ายังอยู่บาเยอ"),
        ("มี.ค. 1983", "bayeux", "ย้ายไปศูนย์กีโยม-เลอ-กงเกแร็ง อดีตโรงเรียนนักบวชบนถนนเดอเนสมง ในห้องจัดแสดงรูปเกือกม้า"),
        ("2018–2021", "bayeux", "ประธานาธิบดีมาครงเสนอให้อังกฤษยืม การสำรวจนับได้รอยเปื้อน 24,204 จุด รู 9,646 รู รอยขาด 30 แห่ง แผนจึงต้องรอ"),
        ("ก.ย. 2025", "bayeux", "พิพิธภัณฑ์ปิดเพื่อสร้างใหม่ วันที่ 19 กันยายน ปลดผ้าลงครั้งแรกตั้งแต่ปี 1983 ใช้เวลา 7 ชั่วโมง 15 นาที คนกว่า 90 คน"),
        ("9–10 ก.ค. 2026", "london", "ไปลอนดอนด้วยรถบรรทุกผ่านอุโมงค์ใต้ช่องแคบ พับบนฉากบุนวมในลังที่ตั้งบนสปริง ตำรวจคุ้มกันตั้งแต่โฟล์กสโตน ราว 11 ชั่วโมง ถึงตีสองห้าสิบ"),
        ("10 ก.ย. 2026 – 11 ก.ค. 2027", "london", "จัดแสดงที่บริติชมิวเซียม ห้อง 30 วางราบใต้กระจก ฝรั่งเศสรายงานว่าด้ายขาดสองเส้นหลังการเดินทาง"),
        ("ต.ค. 2027", "bayeux", "มีกำหนดกลับบาเยอ เข้าพิพิธภัณฑ์ใหม่ในอาคารโรงเรียนนักบวชเดิม ทันวันเกิดครบพันปีของวิลเลียม"),
    ],
}

# People who went to see it. name, Thai name, role, where/when, what, source.
VISITORS_NOW = [
    ("King Charles III", "พระเจ้าชาลส์ที่ 3", "King of the United Kingdom", "พระมหากษัตริย์สหราชอาณาจักร", "British Museum, 2 Sep 2026", "บริติชมิวเซียม 2 ก.ย. 2026",
     "Walked the whole length with the curators and showed President Macron his favourite scene, the Norman cart of wine. In his speech he joked it might have been called the Canterbury Embroidery.",
     "เดินดูตลอดความยาวกับภัณฑารักษ์ ชี้ฉากโปรดให้ประธานาธิบดีมาครงดู คือเกวียนเหล้าองุ่นของชาวนอร์มัน ในสุนทรพจน์ทรงพูดเล่นว่าอาจเรียกว่าผ้าปักแคนเทอร์เบอรีก็ได้",
     "https://www.theartnewspaper.com/2026/09/03/we-are-united-king-charles-iii-and-president-macron-attend-private-preview-of-londons-bayeux-tapestry-exhibition"),
    ("Queen Camilla", "สมเด็จพระราชินีคามิลลา", "Queen", "สมเด็จพระราชินี", "British Museum, 2 Sep 2026", "บริติชมิวเซียม 2 ก.ย. 2026",
     "On the same private tour.", "ร่วมชมรอบส่วนตัวรอบเดียวกัน",
     "https://www.everydayexceptional.royal.uk/news-and-activity/2026-09-03/the-king-and-queen-joined-by-the-president-of-france-and-mrs-macron"),
    ("Emmanuel Macron", "เอมานุแอล มาครง", "President of France", "ประธานาธิบดีฝรั่งเศส", "British Museum, 2 Sep 2026", "บริติชมิวเซียม 2 ก.ย. 2026",
     "Opened the exhibition. He noted Britain first asked in 1931, so a loan agreed in eight years was quick by comparison.",
     "เปิดนิทรรศการ เล่าว่าอังกฤษขอยืมครั้งแรกปี 1931 เทียบกันแล้ว ตกลงได้ในแปดปีถือว่าเร็ว",
     "https://www.franceinfo.fr/culture/emmanuel-macron-inaugure-l-exposition-de-la-tapisserie-de-bayeux-installee-a-londres-pour-un-an_8174294.html"),
    ("Brigitte Macron", "บรีฌิต มาครง", "Wife of the French president", "ภริยาประธานาธิบดีฝรั่งเศส", "British Museum, 2 Sep 2026", "บริติชมิวเซียม 2 ก.ย. 2026",
     "On the tour.", "ร่วมชม", "https://www.everydayexceptional.royal.uk/news-and-activity/2026-09-03/the-king-and-queen-joined-by-the-president-of-france-and-mrs-macron"),
    ("Andy Burnham", "แอนดี เบิร์นแฮม", "Prime Minister of the United Kingdom", "นายกรัฐมนตรีสหราชอาณาจักร", "British Museum, 2 Sep 2026", "บริติชมิวเซียม 2 ก.ย. 2026",
     "Thanked Macron for a 70-metre reminder of Britain's biggest defeat.", "ขอบคุณมาครงสำหรับเครื่องเตือนใจยาว 70 เมตร ถึงความพ่ายแพ้ครั้งใหญ่ที่สุดของอังกฤษ",
     "https://www.gov.uk/government/news/story-of-the-bayeux-tapestry-to-be-brought-to-communities-across-the-country-as-prime-minister-joins-the-king-and-queen-and-president-macron-at-exhibi"),
    ("Marie-France van Heel", "มารี-ฟรองซ์ ฟาน เฮล", "Wife of the prime minister", "ภริยานายกรัฐมนตรี", "British Museum, 2 Sep 2026", "บริติชมิวเซียม 2 ก.ย. 2026",
     "On the tour.", "ร่วมชม", "https://www.everydayexceptional.royal.uk/news-and-activity/2026-09-03/the-king-and-queen-joined-by-the-president-of-france-and-mrs-macron"),
    ("George Osborne · Nicholas Cullinan", "จอร์จ ออสบอร์น · นิโคลัส คัลลิแนน", "British Museum chair and director", "ประธานและผู้อำนวยการบริติชมิวเซียม", "British Museum, 2 Sep 2026", "บริติชมิวเซียม 2 ก.ย. 2026",
     "Led the tour.", "นำชม", "https://www.everydayexceptional.royal.uk/news-and-activity/2026-09-03/the-king-and-queen-joined-by-the-president-of-france-and-mrs-macron"),
    ("Catherine Pégard", "กาตรีน เปการ์", "French culture minister", "รัฐมนตรีวัฒนธรรมฝรั่งเศส", "British Museum, 17 Jul 2026", "บริติชมิวเซียม 17 ก.ค. 2026",
     "Watched it unrolled after the crossing and said it had arrived in excellent condition.", "ดูการคลี่ผ้าหลังข้ามช่องแคบ บอกว่ามาถึงในสภาพดีมาก",
     "https://kuwaittimes.com/article/46674/world/europe/british-museum-shows-bayeux-tapestry-unfurled-after-titanic-efforts/"),
]
VISITORS_THEN = [
    ("Antoine Benoît", "อองตวน เบอนัว", "Draughtsman", "ช่างวาด", "Bayeux Cathedral, c. 1729", "อาสนวิหารบาเยอ ราว 1729",
     "Drew it for Montfaucon's book, the first full picture of it in print.", "วาดให้หนังสือของมงโฟกง เป็นภาพเต็มผืนชุดแรกที่ได้ตีพิมพ์", "https://en.wikipedia.org/wiki/Bayeux_Tapestry"),
    ("Léonard Lambert-Leforestier", "เลโอนาร์ ล็องแบร์-เลอฟอเรสติเย", "Bayeux lawyer", "ทนายความชาวบาเยอ", "Bayeux, 1792", "บาเยอ 1792",
     "Stopped soldiers using it as a wagon cover.", "ห้ามทหารเอาไปคลุมเกวียน", "https://www.bayeuxmuseum.com/en/the-bayeux-tapestry/over-the-centuries/from-the-cathedral-to-the-louvre/"),
    ("Napoleon Bonaparte · Vivant Denon", "นโปเลียน โบนาปาร์ต · วีว็อง เดอนง", "First Consul · director of the Louvre", "กงสุลที่หนึ่ง · ผู้อำนวยการลูฟวร์", "Louvre, 1803–1804", "ลูฟวร์ 1803–1804",
     "Denon put it on show and wrote that the First Consul looked at it with great interest.", "เดอนงจัดแสดง และเขียนว่ากงสุลที่หนึ่งดูด้วยความสนใจยิ่ง", "https://www.bayeuxmuseum.com/en/the-bayeux-tapestry/over-the-centuries/from-the-cathedral-to-the-louvre/"),
    ("Charles and Anna Eliza Stothard", "ชาลส์ และแอนนา อีไลซา สต็อตทาร์ด", "Draughtsman · writer", "ช่างวาด · นักเขียน", "Bayeux, 1816–1818", "บาเยอ 1816–1818",
     "He drew every scene for the Society of Antiquaries. Years later she was accused of taking a piece, and cleared in The Times.", "เขาวาดทุกฉากให้สมาคมนักโบราณคดี หลายปีต่อมาเธอถูกกล่าวหาว่าเอาผ้าไปชิ้นหนึ่ง แล้วหนังสือพิมพ์ The Times ลงว่าเธอพ้นข้อกล่าวหา", "https://en.wikipedia.org/wiki/Anna_Eliza_Bray"),
    ("Thomas Frognall Dibdin", "ทอมัส ฟร็อกนอล ดิบดิน", "Book collector, writer", "นักสะสมหนังสือ นักเขียน", "Bayeux town hall, 1818", "ศาลาว่าการบาเยอ 1818",
     "Watched the keeper unroll it, and wrote of the worn first scenes and faded colours.", "ดูคนเฝ้าคลี่ม้วน แล้วเขียนถึงฉากต้นที่สึกและสีที่ซีด", "https://www.gutenberg.org/cache/epub/11898/pg11898.html"),
    ("Edward Dossetter", "เอ็ดเวิร์ด ดอสเซตเตอร์", "Photographer", "ช่างภาพ", "Bayeux, 1872", "บาเยอ 1872",
     "Photographed it end to end for London's Science and Art Department.", "ถ่ายภาพตลอดผืนให้กรมวิทยาศาสตร์และศิลปะของลอนดอน", "https://www.vam.ac.uk/blog/caring-for-our-collections/photographing-bayeux"),
    ("Elizabeth and Thomas Wardle", "เอลิซาเบธ และทอมัส วอร์เดิล", "Embroiderer · silk dyer", "ช่างปัก · ช่างย้อมไหม", "Bayeux, 1885", "บาเยอ 1885",
     "After seeing it, she and about 35 members of the Leek Embroidery Society and others stitched a full-size copy, finished in 1886 and now in Reading.", "หลังได้เห็น เธอกับสมาชิกสมาคมช่างปักเมืองลีกราว 35 คนและคนอื่นๆ ปักฉบับเท่าของจริงขึ้นมา เสร็จปี 1886 ตอนนี้อยู่ที่เมืองเรดดิง", "https://en.wikipedia.org/wiki/Elizabeth_Wardle"),
    ("Herbert Jankuhn · Karl Schlabow · Herbert Jeschke", "แฮร์แบร์ท ยังคูน · คาร์ล ชลาโบว · แฮร์แบร์ท เยชเคอ", "SS Ahnenerbe researchers", "นักวิจัยหน่วยอาเนนแอร์เบของเอสเอส", "Bayeux, June 1941", "บาเยอ มิ.ย. 1941",
     "Studied, measured and copied it. Schlabow took samples of the linen.", "ศึกษา วัด และคัดลอก ชลาโบวตัดตัวอย่างผ้าลินินไป", "https://www.tcd.ie/news_events/articles/2025/why-the-nazis-stole-a-fragment-of-the-bayeux-tapestry/"),
    ("Jacques Jaujard", "ฌัก โฌฌาร์", "Director of France's national museums", "ผู้อำนวยการพิพิธภัณฑ์แห่งชาติฝรั่งเศส", "Louvre, 1944", "ลูฟวร์ 1944",
     "Photographed looking it over in wartime.", "มีภาพถ่ายขณะตรวจดูผ้าในช่วงสงคราม", "https://www.mmwf.org/post/the-bayeux-tapestry-journey"),
]

PHOTOS = [
    ("museum.jpg", "https://commons.wikimedia.org/wiki/File:Bayeux_Tapestry_Museum_2025-03-26.jpg", "Andy Li", "CC0", "https://creativecommons.org/publicdomain/zero/1.0/",
     {"en": "The Centre Guillaume-le-Conquérant in Bayeux, its home from 1983 to 2025, in March 2025.", "th": "ศูนย์กีโยม-เลอ-กงเกแร็งที่บาเยอ บ้านของผ้าผืนนี้ระหว่างปี 1983 ถึง 2025 ภาพเดือนมีนาคม 2025"}),
    ("gallery.jpg", "https://commons.wikimedia.org/wiki/File:Bayeux_Centre_Guillaume_le_Conqu%C3%A9rant_Tapisserie_de_Bayeux_1.jpg", "Zairon", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/",
     {"en": "Scene 38 in the dim gallery at Bayeux: the fleet lands at Pevensey.", "th": "ฉากที่ 38 ในห้องจัดแสดงแสงสลัวที่บาเยอ กองเรือขึ้นฝั่งที่เพเวนซี"}),
    ("reading.jpg", "https://commons.wikimedia.org/wiki/File:Bayeux_Tapestry_replica_in_Reading_Museum.jpg", "Hotlorp", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/",
     {"en": "The Leek women's full-size copy, finished in 1886, in Reading Museum. Each stitcher's name runs under the section she made.", "th": "ฉบับปักเท่าของจริงของผู้หญิงเมืองลีก เสร็จปี 1886 ที่พิพิธภัณฑ์เมืองเรดดิง ช่างปักแต่ละคนปักชื่อตัวเองไว้ใต้ช่วงที่ตนทำ"}),
    ("stothard.jpg", "https://commons.wikimedia.org/wiki/File:Stothard_Bayeux_33_34_Plate_8.jpg", "Charles Alfred Stothard", "Public domain", None,
     {"en": "Stothard's drawing of the English ship and the shipbuilding, engraved for the Society of Antiquaries, 1819–1823.", "th": "ภาพวาดของสต็อตทาร์ด เรืออังกฤษกับการต่อเรือ แกะพิมพ์ให้สมาคมนักโบราณคดี 1819–1823"}),
]

COUNTS = [
    ("58", "scenes", "ฉาก"),
    ("623–626", "people (two counts)", "คน (นับสองครั้งได้ไม่เท่ากัน)"),
    ("202", "horses and mules", "ม้าและล่อ"),
    ("55", "dogs", "หมา"),
    ("41", "ships and boats", "เรือ"),
    ("37", "buildings", "อาคาร"),
    ("49", "trees", "ต้นไม้"),
    ("9", "pieces of linen", "ผืนลินิน"),
    ("10", "colours of wool", "สีไหมพรม"),
    ("2,226", "letters and signs in the captions", "ตัวอักษรและเครื่องหมายในคำบรรยาย"),
]

UI = {
    "en": {
        "title": "The Bayeux Tapestry, Unrolled",
        "other_title": "พรมผนังบาเยอ คลี่ทั้งผืน",
        "kicker": "พรมผนังบาเยอ · 1066 · 68.58 m",
        "lede": "Wool stitched on linen, nearly seventy metres long, telling how William of Normandy took England in 1066. All of it, end to end, and everywhere it has been since.",
        "cardline": "Every scene, and everywhere it has been",
        "nav": [("reel-sec", "Strip"), ("story", "Story"), ("stitches", "Stitches"), ("comet-sec", "Comet"), ("size", "Size"), ("travels", "Travels"), ("visitors", "Visitors"), ("pictures", "Pictures"), ("sources", "Sources")],
        "play": "Play", "pause": "Pause", "tour": "Play the journey",
        "hero_note": "Drag the strip. 2017 photographs by the Université de Caen and CNRS, public domain, laid end to end.",
        "reel_h": "Every scene",
        "reel_kick": "Drag, slide, or tap a scene",
        "reel_p": "The numbers on the strip's top edge were written on the backing cloth around 1800. The Latin is what the needle says; the line under it, what it means.",
        "scene": "Scene", "along": "Metres along", "prev": "‹ Back", "next": "Next ›",
        "screen": "On your screen the strip is {h} cm tall; at that size the whole thing would run {m} m.",
        "story_h": "The story",
        "story_kick": "1064–1066",
        "story_p": [
            "Four people carry it. Edward the Confessor, King of England, old and without a son. Harold Godwinson, the most powerful earl in England. William, Duke of Normandy, across the Channel. And Odo, William's half-brother, Bishop of Bayeux, who most likely paid for the tapestry.",
            "Harold sails to France, is captured, and is handed to William. He fights beside William in Brittany and swears an oath on holy relics. Back home, Edward dies, and Harold takes the crown. A comet appears. William builds a fleet, crosses the sea, and on 14 October 1066 beats Harold's army near Hastings. Harold dies on the field.",
            "The tapestry tells it from the Norman side: Harold broke his oath. But English hands stitched it, and they left Harold brave, rescuing soldiers from quicksand. The end is missing. It probably finished with William crowned in Westminster Abbey on Christmas Day 1066.",
        ],
        "st_h": "Not a tapestry",
        "st_kick": "Wool on linen",
        "st_p": [
            "A tapestry is woven: the picture is built into the cloth on a loom. This one is embroidered: the cloth came first, nine pieces of plain linen sewn into one long band, and the picture was stitched on top in wool. The French call it a tapisserie, and English has followed.",
            "Most of it uses one method, now often called Bayeux stitch. The stitcher lays long threads across a shape, side by side. Then she lays a few threads the other way, over the top, and ties those down with tiny stitches. Almost all the wool stays on the front; very little goes to waste on the back. Outlines and letters are in stem stitch: short stitches, each overlapping the last.",
            "Press the steps to stitch a Norman kite shield.",
        ],
        "stages": ["1 · Lay threads across", "2 · Lay threads over them", "3 · Tie them down", "4 · Outline in stem stitch"],
        "st_b": ["Lay", "Cross", "Tie", "Outline"],
        "st_now": "Step", "st_len": "Wool on the front", "st_tie": "Tie stitches", "kh": "shield heights",
        "st_note": "Ten colours of natural-dyed wool, mostly reds, yellows, greens and blues. A 2022 scan measured 215 shades among them, from fading and repairs.",
        "co_h": "The star",
        "co_kick": "ISTI MIRANT STELLAM",
        "co_p": [
            "In spring 1066, a few months after Harold was crowned, a long-tailed star hung in the sky. Scene 32 shows men pointing up at it. People across Europe read it as a sign.",
            "We call it Halley's Comet. It swings out past Neptune and back about every 76 years, the gap changing a little each time as the planets pull on it. Since 1066 it has come back twelve times. The last was 1986; the next, 2061.",
            "The drawing solves Kepler's equation for the comet and puts the Earth on its circle. Distances from the Sun are squeezed by a square root so both fit.",
        ],
        "co_year": "Year", "co_earth": "From Earth", "co_sun": "From the Sun", "co_ret": "Returns since 1066", "co_next": "Next close to the Sun",
        "co_note": "Orbit shape from today's elements (JPL), so positions in 1066 are approximate; this drawing puts the comet about 0.14 AU from Earth in early May 1066. 1 AU is the Earth–Sun distance, about 150 million km.",
        "earth": "Earth", "jupiter": "Jupiter", "saturn": "Saturn", "uranus": "Uranus", "neptune": "Neptune",
        "size_h": "How long",
        "size_kick": "68.58 m × 50 cm",
        "size_p": "The nine linen pieces add up to 68.58 m; other measurements give 68.38. The embroidered band is about 50 cm tall. Here it is against a football pitch, and against Chiang Mai's red songthaews parked nose to tail.",
        "pitch": "Football pitch, 105 m", "tap_len": "The tapestry, 68.58 m; ticks are the seams between the nine linen pieces", "songthaew": "About {n} red songthaews, 5.3 m each",
        "counts_h": "Counted",
        "tr_h": "Where it has been",
        "tr_kick": "950 years, five places",
        "tr_p": "Almost all its life it has stayed in one small Norman town. Before 2026 it had never left France. Tap a row to see it on the map.",
        "channel": "La Manche · English Channel",
        "vi_h": "Who came to see it",
        "vi_kick": "Named in the record",
        "vi_now": "2026, British Museum",
        "vi_then": "Before",
        "vi_p": "These are people a source names as seeing the tapestry itself. Being in Bayeux is not enough: on 14 June 1944 de Gaulle spoke in the town while the tapestry sat at Sourches, about 140 km away.",
        "src": "Source",
        "ph_h": "Pictures",
        "src_h": "Sources",
        "sources": [
            ("Bayeux Museum: from the cathedral to the Louvre", "https://www.bayeuxmuseum.com/en/the-bayeux-tapestry/over-the-centuries/from-the-cathedral-to-the-louvre/"),
            ("Bayeux Museum: during the Second World War", "https://www.bayeuxmuseum.com/en/the-bayeux-tapestry/over-the-centuries/during-the-second-world-war/"),
            ("Bayeux Museum: a new museum by 2027", "https://www.bayeuxmuseum.com/en/the-bayeux-tapestry/over-the-centuries/a-new-museum-by-2027/"),
            ("Bayeux Museum press kit, 2024", "https://bayeuxmuseum.com/wp-content/uploads/2024/08/2024_PressKit-Bayeux-Tapestry.pdf"),
            ("Wikipedia: Bayeux Tapestry", "https://en.wikipedia.org/wiki/Bayeux_Tapestry"),
            ("Wikipédia: Tapisserie de Bayeux", "https://fr.wikipedia.org/wiki/Tapisserie_de_Bayeux"),
            ("Wikipedia: Bayeux Tapestry tituli (the Latin captions)", "https://en.wikipedia.org/wiki/Bayeux_Tapestry_tituli"),
            ("V&A: photographing Bayeux, 1872", "https://www.vam.ac.uk/blog/caring-for-our-collections/photographing-bayeux"),
            ("V&A: the Stothard fragment", "https://www.vam.ac.uk/blog/caring-for-our-collections/stitch-time-va-and-bayeux-tapestry-2"),
            ("The Art Newspaper: how Britain tried to borrow it, 2018", "https://www.theartnewspaper.com/2018/02/28/how-britain-triedand-failedto-borrow-the-bayeux-tapestry-twice-before"),
            ("Museums Association: loan on hold, 2021", "https://www.museumsassociation.org/museums-journal/news/2021/04/bayeux-tapestry-loan-on-hold-due-to-poor-condition/"),
            ("France 24: it leaves the museum, 19 Sep 2025", "https://www.france24.com/en/live-news/20250919-bayeux-tapestry-leaves-museum-for-first-time-since-1983-before-uk-loan"),
            ("French Ministry of Culture: a historic loan", "https://www.culture.gouv.fr/dossiers/tapisserie-de-bayeux-un-pret-historique"),
            ("The Art Newspaper: arrival in London, 10 Jul 2026", "https://www.theartnewspaper.com/2026/07/10/bayeux-tapestry-arrives-at-the-british-museum-after-secret-english-channel-crossing"),
            ("Naharnet: two broken threads, Sep 2026", "https://naharnet.com/stories/en/322282-two-broken-threads-on-bayeux-tapestry-but-no-major-alteration-french-minister-says"),
            ("The Local: Germany returns fragments, Jan 2026", "https://www.thelocal.fr/20260116/germany-returns-to-france-fragments-of-the-bayeux-tapestry-taken-in-1941"),
            ("Trinity College Dublin: why the Nazis took a fragment", "https://www.tcd.ie/news_events/articles/2025/why-the-nazis-stole-a-fragment-of-the-bayeux-tapestry/"),
            ("GOV.UK: the Prime Minister at the exhibition, 2 Sep 2026", "https://www.gov.uk/government/news/story-of-the-bayeux-tapestry-to-be-brought-to-communities-across-the-country-as-prime-minister-joins-the-king-and-queen-and-president-macron-at-exhibi"),
            ("The Art Newspaper: the private preview, 3 Sep 2026", "https://www.theartnewspaper.com/2026/09/03/we-are-united-king-charles-iii-and-president-macron-attend-private-preview-of-londons-bayeux-tapestry-exhibition"),
            ("Atlas Obscura: the Reading copy", "https://www.atlasobscura.com/places/reading-museum-bayeux-tapestry"),
            ("Wikipedia: Elizabeth Wardle", "https://en.wikipedia.org/wiki/Elizabeth_Wardle"),
            ("Wikimedia Commons: the 2017 scene photographs", "https://commons.wikimedia.org/wiki/Category:Bayeux_Tapestry_scenes"),
            ("JPL Small-Body Database: 1P/Halley", "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=1P"),
            ("Natural Earth (coastline)", "https://www.naturalearthdata.com/"),
        ],
        "foot": "Text CC BY 4.0, NaNoBotCo · code MIT · pictures keep their own licences",
        "lang_this": "EN", "lang_other": ("th/", "ไทย", "th"),
        "desc": "The Bayeux Tapestry end to end: all 58 scenes with their Latin, the stitches, Halley's Comet, where it has been from Canterbury to the British Museum, and who came to see it.",
        "mot": "",
    },
    "th": {
        "title": "พรมผนังบาเยอ คลี่ทั้งผืน",
        "other_title": "The Bayeux Tapestry, Unrolled",
        "kicker": "Bayeux Tapestry · ค.ศ. 1066 · 68.58 เมตร",
        "lede": "ไหมพรมปักบนผ้าลินิน ยาวเกือบเจ็ดสิบเมตร เล่าว่าวิลเลียมแห่งนอร์มังดียึดอังกฤษได้อย่างไรในปี 1066 ที่นี่มีครบทั้งผืน ต่อกันตั้งแต่ต้นจนจบ และทุกที่ที่ผ้าผืนนี้เคยไปอยู่",
        "cardline": "ครบทุกฉาก และทุกที่ที่เคยไป",
        "nav": [("reel-sec", "ทั้งผืน"), ("story", "เรื่อง"), ("stitches", "ฝีเข็ม"), ("comet-sec", "ดาวหาง"), ("size", "ขนาด"), ("travels", "เส้นทาง"), ("visitors", "ผู้มาชม"), ("pictures", "ภาพ"), ("sources", "แหล่งข้อมูล")],
        "play": "เล่น", "pause": "หยุด", "tour": "เล่นเส้นทาง",
        "hero_note": "ลากแถบผ้าได้ ภาพถ่ายปี 2017 ของมหาวิทยาลัยก็องและ CNRS เป็นสาธารณสมบัติ นำมาต่อกันทั้งผืน",
        "reel_h": "ทุกฉาก",
        "reel_kick": "ลาก เลื่อน หรือแตะชื่อฉาก",
        "reel_p": "ตัวเลขที่ขอบบนเขียนไว้บนผ้ารองหลังราวปี 1800 ภาษาละตินคือคำที่ปักไว้บนผ้า บรรทัดใต้คือความหมาย",
        "scene": "ฉาก", "along": "ระยะจากต้นผืน", "prev": "‹ ก่อนหน้า", "next": "ถัดไป ›",
        "screen": "บนจอของคุณ แถบผ้าสูง {h} ซม. ถ้าขนาดนี้ทั้งผืนจะยาว {m} เมตร",
        "story_h": "เรื่องที่เล่า",
        "story_kick": "1064–1066",
        "story_p": [
            "ตัวละครหลักมีสี่คน พระเจ้าเอ็ดเวิร์ดผู้สารภาพ กษัตริย์อังกฤษ ชราและไม่มีโอรส ฮาโรลด์ กอดวินสัน ขุนนางที่มีอำนาจที่สุดในอังกฤษ วิลเลียม ดยุกแห่งนอร์มังดี อยู่อีกฝั่งของช่องแคบ และโอโด น้องชายต่างพ่อของวิลเลียม บิชอปแห่งบาเยอ ผู้น่าจะเป็นคนจ่ายเงินทำผ้าผืนนี้",
            "ฮาโรลด์ล่องเรือไปฝรั่งเศส ถูกจับ แล้วถูกส่งตัวให้วิลเลียม เขาออกรบเคียงข้างวิลเลียมที่เบรอตาญ และสาบานบนหีบอัฐินักบุญ กลับถึงบ้าน พระเจ้าเอ็ดเวิร์ดสวรรคต ฮาโรลด์ขึ้นครองราชย์ ดาวหางปรากฏ วิลเลียมต่อกองเรือ ข้ามทะเล และวันที่ 14 ตุลาคม 1066 ชนะกองทัพฮาโรลด์ใกล้เมืองเฮสติงส์ ฮาโรลด์ตายในสนามรบ",
            "ผ้าเล่าจากฝั่งนอร์มัน ว่าฮาโรลด์ผิดคำสาบาน แต่คนปักเป็นคนอังกฤษ และยังปักให้ฮาโรลด์กล้าหาญ ช่วยทหารขึ้นจากทรายดูด ตอนจบหายไป น่าจะจบที่วิลเลียมขึ้นครองราชย์ในเวสต์มินสเตอร์แอบบีย์ วันคริสต์มาส 1066",
        ],
        "st_h": "ไม่ใช่พรมทอ",
        "st_kick": "ไหมพรมบนลินิน",
        "st_p": [
            "พรมผนังแบบทอ ภาพเกิดจากการทอบนกี่ไปพร้อมกับผ้า ผืนนี้ไม่ใช่ ผืนนี้เป็นผ้าปัก ผ้ามาก่อน คือลินินเรียบเก้าผืนเย็บต่อเป็นแถบยาว แล้วจึงปักภาพลงไปด้วยไหมพรม ชาวฝรั่งเศสเรียกว่า tapisserie ภาษาอังกฤษก็เรียกตาม ภาษาไทยจึงเรียกพรมผนัง",
            "ส่วนใหญ่ใช้วิธีเดียว ปัจจุบันมักเรียกว่าฝีเข็มบาเยอ ช่างปักวางด้ายยาวพาดข้ามรูปเรียงกัน แล้ววางด้ายอีกไม่กี่เส้นพาดทับในทิศตรงข้าม ตรึงด้วยฝีเข็มเล็กๆ ไหมพรมเกือบทั้งหมดอยู่ด้านหน้า ด้านหลังแทบไม่เปลือง เส้นขอบและตัวอักษรปักแบบด้นถอยหลังเหลื่อม คือฝีสั้นๆ ซ้อนเหลื่อมฝีก่อนหน้า",
            "กดทีละขั้น เพื่อปักโล่ทรงว่าวของอัศวินนอร์มัน",
        ],
        "stages": ["1 · วางด้ายพาดขวาง", "2 · วางด้ายทับอีกทิศ", "3 · ตรึงด้วยฝีเล็ก", "4 · ปักเส้นขอบ"],
        "st_b": ["วาง", "ทับ", "ตรึง", "ขอบ"],
        "st_now": "ขั้น", "st_len": "ไหมพรมด้านหน้า", "st_tie": "ฝีตรึง", "kh": "เท่าความสูงโล่",
        "st_note": "ไหมพรมย้อมสีธรรมชาติสิบสี ส่วนใหญ่แดง เหลือง เขียว น้ำเงิน การสแกนปี 2022 วัดได้ 215 เฉด เพราะสีซีดและรอยซ่อม",
        "co_h": "ดาว",
        "co_kick": "ISTI MIRANT STELLAM",
        "co_p": [
            "ฤดูใบไม้ผลิปี 1066 ไม่กี่เดือนหลังฮาโรลด์ขึ้นครองราชย์ มีดาวหางหางยาวค้างอยู่บนฟ้า ฉากที่ 32 คนชี้ขึ้นไปดู ผู้คนทั่วยุโรปถือว่าเป็นลาง",
            "ปัจจุบันเรียกว่าดาวหางแฮลลีย์ วงโคจรเหวี่ยงออกไปไกลกว่าดาวเนปจูนแล้ววนกลับมาราวทุก 76 ปี ช่วงห่างเปลี่ยนไปเล็กน้อยทุกรอบเพราะแรงดึงของดาวเคราะห์ ตั้งแต่ปี 1066 กลับมาแล้วสิบสองครั้ง ครั้งล่าสุดปี 1986 ครั้งหน้าปี 2061",
            "ภาพนี้แก้สมการเคปเลอร์หาตำแหน่งดาวหาง และวางโลกบนวงโคจรของมัน ระยะจากดวงอาทิตย์ถูกย่อด้วยรากที่สอง เพื่อให้ใส่ได้ทั้งหมด",
        ],
        "co_year": "ปี ค.ศ.", "co_earth": "ห่างจากโลก", "co_sun": "ห่างจากดวงอาทิตย์", "co_ret": "กลับมาตั้งแต่ 1066", "co_next": "เข้าใกล้ดวงอาทิตย์ครั้งหน้า",
        "co_note": "รูปวงโคจรใช้ค่าปัจจุบันจาก JPL ตำแหน่งในปี 1066 จึงเป็นค่าประมาณ ภาพนี้วางดาวหางห่างโลกราว 0.14 AU ต้นเดือนพฤษภาคม 1066 โดย 1 AU คือระยะโลกถึงดวงอาทิตย์ ราว 150 ล้านกิโลเมตร",
        "earth": "โลก", "jupiter": "พฤหัสบดี", "saturn": "เสาร์", "uranus": "ยูเรนัส", "neptune": "เนปจูน",
        "size_h": "ยาวแค่ไหน",
        "size_kick": "68.58 ม. × 50 ซม.",
        "size_p": "ลินินเก้าผืนรวมกันยาว 68.58 เมตร บางแหล่งวัดได้ 68.38 แถบที่ปักสูงราว 50 ซม. เทียบกับสนามฟุตบอล และกับรถแดงเชียงใหม่จอดต่อท้ายกัน",
        "pitch": "สนามฟุตบอล 105 ม.", "tap_len": "พรมผนัง 68.58 ม. ขีดคือรอยต่อลินินทั้งเก้าผืน", "songthaew": "รถแดงคันละ 5.3 ม. ราว {n} คัน",
        "counts_h": "นับได้",
        "tr_h": "เคยไปอยู่ที่ไหน",
        "tr_kick": "950 ปี ห้าที่",
        "tr_p": "เกือบตลอดอายุ ผ้าผืนนี้อยู่ในเมืองเล็กๆ เมืองเดียวในนอร์มังดี ก่อนปี 2026 ไม่เคยออกนอกฝรั่งเศสเลย แตะแต่ละแถวเพื่อดูบนแผนที่",
        "channel": "ช่องแคบอังกฤษ",
        "vi_h": "ใครมาดูบ้าง",
        "vi_kick": "มีชื่อในบันทึก",
        "vi_now": "2026 บริติชมิวเซียม",
        "vi_then": "ก่อนหน้านั้น",
        "vi_p": "ข้างล่างนี้คือคนที่มีแหล่งข้อมูลระบุว่าได้เห็นผ้าผืนนี้ด้วยตา ไปถึงบาเยอยังไม่พอ วันที่ 14 มิถุนายน 1944 เดอโกลกล่าวสุนทรพจน์ในเมืองนี้ ขณะที่ผ้าอยู่ที่ซูร์ช ห่างไปราว 140 กม.",
        "src": "แหล่ง",
        "ph_h": "ภาพ",
        "src_h": "แหล่งข้อมูล",
        "foot": "เนื้อหา CC BY 4.0 NaNoBotCo · โค้ด MIT · ภาพถ่ายใช้สัญญาอนุญาตของแต่ละภาพ",
        "lang_this": "ไทย", "lang_other": ("../", "EN", "en"),
        "desc": "พรมผนังบาเยอทั้งผืน ครบ 58 ฉากพร้อมคำละติน ฝีเข็ม ดาวหางแฮลลีย์ เส้นทางจากแคนเทอร์เบอรีถึงบริติชมิวเซียม และใครมาดูบ้าง",
        "mot": "",
    },
}
UI["th"]["sources"] = UI["en"]["sources"]


def paras(ps):
    return "".join(f"<p>{E(p)}</p>" for p in ps)


def page(lang):
    u = UI[lang]
    th = lang == "th"
    root = "" if lang == "en" else "../"
    url = BASE if lang == "en" else BASE + "th/"
    starts = scene_starts()
    scenes = [{"n": n, "s": starts[n], "la": la, "t": (t_th if th else t_en)} for n, la, t_en, t_th in SCENES]
    places = {k: [v[0], v[1], v[3] if th else v[2], v[4]] for k, v in PLACES.items()}
    js = {
        "lang": lang, "root": root, "W": W, "len": LEN, "x0": 40, "x1": W - 30, "panels": PANELS,
        "strip": [{"f": t["file"], "x": t["x"], "w": t["w"]} for t in STRIP],
        "scenes": scenes, "heroStart": starts[38] - 120,
        "places": places, "mapbox": [-2.5, 47.6, 3.4, 52.0],
        "timeline": [{"d": d, "p": p, "t": t} for d, p, t in TIMELINE[lang]],
        "perihelia": PERIHELIA,
        "ui": {k: u[k] for k in ("play", "pause", "tour", "scene", "screen", "pitch", "tap_len", "songthaew", "channel", "stages", "kh", "earth", "jupiter", "saturn", "uranus", "neptune")},
    }
    nav = "".join(f'<a href="#{a}">{E(b)}</a>' for a, b in u["nav"])
    ol = u["lang_other"]
    head = f'''<!doctype html><html lang="{lang}" translate="no" class="notranslate"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate">
{GOOGLE_ESCAPE}
<title>{E(u["title"])} · {E(u["other_title"])}</title>
<meta name="description" content="{E(u["desc"])}">
<meta name="theme-color" content="#1f1d1b">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{BASE}"><link rel="alternate" hreflang="th" href="{BASE}th/"><link rel="alternate" hreflang="x-default" href="{BASE}">
<meta property="og:type" content="website"><meta property="og:site_name" content="The Bayeux Tapestry, Unrolled · พรมผนังบาเยอ คลี่ทั้งผืน">
<meta property="og:title" content="{E(u["title"])}"><meta property="og:description" content="{E(u["desc"])}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}card.jpg"><meta property="og:image:secure_url" content="{BASE}card.jpg"><meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="William's fleet crossing the Channel on the Bayeux Tapestry, with the title">
<meta property="og:locale" content="{"th_TH" if th else "en_US"}"><meta property="og:locale:alternate" content="{"en_US" if th else "th_TH"}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}card.jpg">
<link rel="icon" href="{root}icon.svg" type="image/svg+xml">
<link rel="alternate" type="text/plain" href="{BASE}llms.txt" title="llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Noto+Sans+Thai:wght@400;600;700&family=Noto+Serif+Thai:wght@600;700&display=swap" rel="stylesheet">
<script>if(/[?&]card/.test(location.search))document.documentElement.classList.add("card")</script>
<style>{CSS}</style>
</head><body>
<header class="top"><div class="in"><a class="brand" href="#top"><img src="{root}icon.svg" alt="" width="28" height="28"><span>{E(u["title"])}</span></a>
<nav aria-label="Sections">{nav}</nav>
<span class="lang"><b>{E(u["lang_this"])}</b> | <a href="{ol[0]}" hreflang="{ol[2]}">{E(ol[1])}</a></span></div></header>
'''
    hero = f'''<section id="top" class="hero"><div class="hero-t"><p class="kick">{E(u["kicker"])}</p><h1>{E(u["title"])}</h1><p class="lede">{E(u["lede"])}</p><p class="cardline">{E(u["cardline"])}<br><span>nanobotco.github.io/bayeux-tapestry</span></p></div>
<div id="hreel" class="reel hreel" role="img" aria-label="{E(u["lede"])}"></div>
<div class="tbar"><button id="hplay" class="pill hot" type="button">{E(u["pause"])}</button><p class="note">{E(u["hero_note"])}</p></div></section>
'''
    lis = "".join(f'<li data-k="{i}"><b>{s["n"]}</b><span class="la">{E(s["la"])}</span><span>{E(s["t"])}</span></li>' for i, s in enumerate(scenes))
    reel = f'''<section id="reel-sec" class="sec dark"><div class="in"><p class="kick">{E(u["reel_kick"])}</p><h2>{E(u["reel_h"])}</h2><p>{E(u["reel_p"])}</p></div>
<div id="reel" class="reel big" role="img" aria-label="{E(u["reel_h"])}"></div>
<div class="in"><input id="rpos" type="range" min="0" value="0" aria-label="{E(u["along"])}">
<div class="cap"><div class="capn"><b id="rscene">–</b><span><span id="rm">0 m</span> · {E(u["along"])}</span></div>
<div class="capt"><p id="rlatin" class="latin" lang="la"></p><p id="rsay" class="say" aria-live="polite"></p></div>
<div class="btns"><button id="rprev" class="pill" type="button">{E(u["prev"])}</button><button id="rnext" class="pill hot" type="button">{E(u["next"])}</button></div></div>
<p id="onscreen" class="note"></p>
<ol class="scenes">{lis}</ol></div></section>
'''
    story = f'''<section id="story" class="sec"><div class="in"><p class="kick">{E(u["story_kick"])}</p><h2>{E(u["story_h"])}</h2><div class="cols">{paras(u["story_p"])}</div></div></section>
'''
    btns = "".join(f'<button class="pill" type="button" data-st="{i + 1}" aria-pressed="{"true" if i == 3 else "false"}">{E(b)}</button>' for i, b in enumerate(u["st_b"]))
    stitches = f'''<section id="stitches" class="sec linen"><div class="in two"><div><canvas id="stitch" class="cv paper" role="img" aria-label="{E(u["st_h"])}"></canvas>
<div class="btns">{btns}</div>
<div class="readout"><div><span>{E(u["st_now"])}</span><b id="kst">–</b></div><div><span>{E(u["st_len"])}</span><b id="klen">–</b></div><div><span>{E(u["st_tie"])}</span><b id="ktie">–</b></div></div></div>
<div><p class="kick">{E(u["st_kick"])}</p><h2>{E(u["st_h"])}</h2>{paras(u["st_p"])}<div class="wools" aria-hidden="true"><i style="background:#a8442a"></i><i style="background:#c46a3c"></i><i style="background:#c99a3b"></i><i style="background:#ddc27a"></i><i style="background:#6f7f4f"></i><i style="background:#9aa36a"></i><i style="background:#2f4f53"></i><i style="background:#3e5c7a"></i><i style="background:#7e93a4"></i><i style="background:#2a2420"></i></div><p class="note">{E(u["st_note"])}</p></div></div></section>
'''
    comet = f'''<section id="comet-sec" class="sec night"><div class="in two"><div><canvas id="comet" class="cv" role="img" aria-label="{E(u["co_h"])}"></canvas>
<div class="btns"><button id="cplay" class="pill hot" type="button">{E(u["play"])}</button><button class="pill" type="button" data-yr="1066.35">1066</button><button class="pill" type="button" data-yr="1910.3">1910</button><button class="pill" type="button" data-yr="1986.1">1986</button><button class="pill" type="button" data-yr="2026.76">2026</button><button class="pill" type="button" data-yr="2061.57">2061</button></div>
<input id="cslide" type="range" aria-label="{E(u["co_year"])}"></div>
<div><p class="kick">{E(u["co_kick"])}</p><h2>{E(u["co_h"])}</h2>{paras(u["co_p"])}
<div class="readout"><div><span>{E(u["co_year"])}</span><b id="cyear">1066</b></div><div><span>{E(u["co_earth"])}</span><b id="cdist">–</b></div><div><span>{E(u["co_sun"])}</span><b id="csun">–</b></div><div><span>{E(u["co_ret"])}</span><b id="cret">0</b></div><div><span>{E(u["co_next"])}</span><b id="cnext">–</b></div></div>
<p class="note">{E(u["co_note"])}</p></div></div></section>
'''
    counts = "".join(f'<div><b>{E(n)}</b><span>{E(b if th else a)}</span></div>' for n, a, b in COUNTS)
    size = f'''<section id="size" class="sec"><div class="in"><p class="kick">{E(u["size_kick"])}</p><h2>{E(u["size_h"])}</h2><p>{E(u["size_p"])}</p>
<canvas id="long" class="cv paper" role="img" aria-label="{E(u["size_h"])}"></canvas>
<h3>{E(u["counts_h"])}</h3><div class="counts">{counts}</div></div></section>
'''
    tl = "".join(f'<li data-i="{i}"><b>{E(d)}</b><span class="pl">{E(PLACES[p][3] if th else PLACES[p][2])}</span><span>{E(t)}</span></li>' for i, (d, p, t) in enumerate(TIMELINE[lang]))
    travels = f'''<section id="travels" class="sec linen"><div class="in"><p class="kick">{E(u["tr_kick"])}</p><h2>{E(u["tr_h"])}</h2><p>{E(u["tr_p"])}</p>
<div class="mapwrap"><div class="mapcol"><canvas id="map" class="cv" role="img" aria-label="{E(u["tr_h"])}"></canvas>
<div class="btns"><button id="mtour" class="pill hot" type="button">{E(u["tour"])}</button><b id="mnow" class="mnow" aria-live="polite"></b></div></div>
<ol class="tl">{tl}</ol></div></div></section>
'''

    def vcards(rows):
        out = []
        for en, thn, role, role_th, where, where_th, what, what_th, src in rows:
            name, other = (thn, en) if th else (en, thn)
            out.append(f'<article><h3>{E(name)}</h3><p class="th">{E(other)}</p><p class="role">{E(role_th if th else role)} · {E(where_th if th else where)}</p><p>{E(what_th if th else what)}</p><a class="vs" href="{src}">{E(u["src"])}</a></article>')
        return "".join(out)
    visitors = f'''<section id="visitors" class="sec dark"><div class="in"><p class="kick">{E(u["vi_kick"])}</p><h2>{E(u["vi_h"])}</h2><p>{E(u["vi_p"])}</p>
<h3 class="vh">{E(u["vi_now"])}</h3><div class="vis">{vcards(VISITORS_NOW)}</div>
<h3 class="vh">{E(u["vi_then"])}</h3><div class="vis">{vcards(VISITORS_THEN)}</div></div></section>
'''
    figs = []
    for f, page_, who, lic, licu, cap in PHOTOS:
        licl = f'<a href="{licu}">{E(lic)}</a>' if licu else E(lic)
        figs.append(f'<figure><img loading="lazy" src="{root}img/{f}" width="1400" alt="{E(cap[lang])}"><figcaption>{E(cap[lang])} <a href="{page_}">{E(who)}</a> · {licl}</figcaption></figure>')
    ph = f'''<section id="pictures" class="sec"><div class="in"><h2>{E(u["ph_h"])}</h2><div class="ph">{"".join(figs)}</div></div></section>
'''
    src = "".join(f'<li><a href="{h}">{E(t)}</a></li>' for t, h in u["sources"])
    so = f'''<section id="sources" class="sec"><div class="in"><h2>{E(u["src_h"])}</h2><ul class="src">{src}</ul></div></section>
'''
    tail = f'''<footer class="bot"><div class="in">{E(u["foot"])} · <a href="https://github.com/NaNoBotCo/bayeux-tapestry">GitHub</a> · <a href="https://motdang.net/">motdang.net</a> · <a href="https://hongdam.net/">hongdam.net</a></div></footer>
<script>window.D={json.dumps(js, ensure_ascii=False, separators=(",", ":"))};</script>
<script src="{root}land.js"></script><script>window.D.land=window.LAND;</script>
<script src="{root}app.js"></script><script src="{root}top.js"></script>
</body></html>
'''
    return head + "<main>" + hero + reel + story + stitches + comet + size + travels + visitors + ph + so + "</main>" + tail


def main():
    os.makedirs(os.path.join(DOCS, "th"), exist_ok=True)
    for lang, path in (("en", "index.html"), ("th", "th/index.html")):
        with open(os.path.join(DOCS, path), "w") as f:
            f.write(page(lang))
    with open(os.path.join(DOCS, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f'<url><loc>{BASE}</loc></url>\n<url><loc>{BASE}th/</loc></url>\n</urlset>\n')
    with open(os.path.join(DOCS, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
    u = UI["en"]
    lines = ["# The Bayeux Tapestry, Unrolled · พรมผนังบาเยอ คลี่ทั้งผืน", "", u["desc"], "", f"English: {BASE}", f"Thai: {BASE}th/", "",
             f"Length: {LEN} m (sum of the nine linen pieces: {', '.join(str(p) for p in PANELS)} m). Height about 50 cm.", "", "## The 58 scenes", ""]
    lines += [f"- Scene {n}: {la} — {t}" for n, la, t, _ in SCENES]
    lines += ["", "## Where it has been", ""]
    lines += [f"- {d} · {PLACES[p][2]}: {t}" for d, p, t in TIMELINE["en"]]
    lines += ["", "## Who came to see it", ""]
    lines += [f"- {r[0]} ({r[2]}), {r[4]}: {r[6]} Source: {r[8]}" for r in VISITORS_NOW + VISITORS_THEN]
    lines += ["", "## Counted", ""] + [f"- {n} {a}" for n, a, _ in COUNTS]
    lines += ["", "## Sources", ""] + [f"- {t}: {h}" for t, h in u["sources"]]
    lines += ["", "## Licence", "", "Text CC BY 4.0, NaNoBotCo. Code MIT. The 2017 scene photographs (Université de Caen Normandie, CNRS, ENSICAEN) are public domain; other pictures keep their own licences, listed on the page.", ""]
    with open(os.path.join(DOCS, "llms.txt"), "w") as f:
        f.write("\n".join(lines))
    print("built en + th")


if __name__ == "__main__":
    main()
