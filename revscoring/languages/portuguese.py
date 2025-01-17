import sys

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import Language, LanguageUtility

STEMMER = SnowballStemmer("portuguese")
STOPWORDS = set(stopwords.words("portuguese"))
BADWORDS = set([
    "abracao", "abraco", "acho", "achu", "agradeço", "ahu", "ahuahua",
        "ahuauha", "ahuhu", "ahuuha", "aki", "anal", "analfabeto", "anus",
        "ânus", "anuus", "apagou", "aproveitador", "arombado", "arregada",
        "arreganhar", "arrombadu", "arrombar", "arrotaam", "arroto", "asho",
        "ashu", "asneira", "asno", "ass", "assassino", "asshole", "assinado",
        "auh", "auhahua", "auhauha", "auhuaha", "axo", "axu",
    "babaca", "babadora", "babaka", "bacana", "badalhoca", "baitola",
        "baitolinha", "bakana", "bambi", "banbi", "bastardo", "batata",
        "batota", "batoteiro", "beijao", "beijinho", "beijo", "beijoca",
        "beijoo", "beiju", "beijuu", "bejo", "bejoo", "beju", "belo", "best",
        "besteira", "besteirol", "bicha", "bisexual", "bissexual", "bitch",
        "bixa", "bla", "blabla", "blablaa", "blala", "bobao", "bobo", "boboo",
        "boceta", "bocetaa", "bocetinha", "bodega", "boh", "boilao", "boiola",
        "boiolitico", "boketao", "bokete", "bonitao", "bonitinho", "bonito",
        "bonitona", "boqete", "boquetao", "boquete", "boquetoes", "boquette",
        "bordalhoca", "bordeis", "bordéis", "bordel", "boreis", "borel",
        "borra", "borrice", "borroi", "boset", "bosetinha", "bosset", "bosta",
        "bostaesse", "bostalhao", "boto", "boxta", "brasucas", "brasukas",
        "bravo", "brazuca", "brazukas", "broche", "brochista", "broxa",
        "broxista", "bua", "buceta", "bucetinha", "budega", "buh", "bullshit",
        "bum", "bumbum", "bumbun", "bumdao", "bumdinha", "bumm", "bummm",
        "bunbum", "bunbun", "bunda", "bundao", "bundinha", "burrai", "burrice",
        "burro", "burroi", "buseta", "busetinha", "busset", "bussetinha",
        "bxurupita", "bye",
    "cabrao", "cabrita", "cabritinha", "cabro", "cabroes", "cabrona", "cachla",
        "cachopo", "cachora", "cachorao", "cachorra", "cachorrao", "caco",
        "cagada", "cagadela", "cagadoo", "cagalhao", "cagalho", "cagalhoto",
        "caganei", "caganeira", "caganita", "cagao", "cagda", "cageiro",
        "caglhao", "caipira", "caka", "cambada", "camisinha", "camizinha",
        "canbada", "cansada", "canzana", "cao", "cara", "cara", "carago",
        "carah", "carahlo", "carahu", "caraio", "caraiu", "caralhao",
        "caralhinho", "caralho", "caralhu", "caralhus", "caramba", "cau",
        "caxda", "caxora", "caxorra", "ccao", "ccau", "cchao",
        "centricsandraemeirelles", "chana", "chaneta", "chanuda", "chao",
        "chapado", "charmoso", "chat", "chatao", "chau", "chavasca", "chereca",
        "chiao", "chiau", "chichi", "chingao", "chingar", "chixi", "chocho",
        "chochota", "chucho", "chuchu", "chuck", "chula", "chuleco", "chupa",
        "chupador", "chupatante", "chupau", "chupeta", "chupinha", "chupor",
        "chupu", "churanha", "chuxu", "ciao", "ciau", "cigano", "clamídia",
        "clites", "clitoris", "coca", "cock", "cocô", "cocsar", "coisa",
        "coiso", "coiza", "coka", "colha", "colhao", "colhoes", "come", "comi",
        "comigo", "cona", "coninha", "contigo", "corinthiano", "corinthians",
        "corinthias", "corintiana", "corintians", "corintias", "corno",
        "cornudo", "cornuto", "cosou", "cossou", "cousa", "couza", "covarde",
        "crapula", "creo", "cretino", "creu", "cromo", "croquete", "cu", "cucu",
        "cueca", "cuecao", "cuecinha", "cueko", "cuequinha", "culhao", "culho",
        "culhoes", "curte", "cusao", "cusinho", "cuzao", "cuzinho",
    "daki", "dakii", "debi", "debil", "decho", "dedicatoria", "defecar",
        "defekei", "defeque", "deicho", "deixe", "deixe", "descarada",
        "descordo", "dexe", "dfdf", "digo", "discarado", "discaradoo",
        "discordo", "dla", "dle", "doidao", "doidinho", "doido", "doidoo",
        "donload", "dorminhoco", "dotado", "download", "downloads", "droga",
        "duvido", "duvidosa", "duvidozo",
    "eamaral", "emo", "emos", "encornados", "enfiar", "enrabar", "escroto",
        "estúpido",
    "faggot", "fajuto", "fdp", "fede", "fedorento", "fee", "feiao", "feida",
        "feio", "feioo", "feorenta", "ferrar", "feses", "fezes", "fiofo",
        "fnord", "foda", "fodao", "fodau", "fodax", "fodedor", "foderlhe",
        "fodete", "fodex", "fodidor", "fodilhao", "fodilhoes", "fodite",
        "fodoes", "fodote", "fofinho", "fofo", "fofoqueira", "fofusco",
        "french", "frenchie", "frenchs", "frutinha", "fudador", "fudao",
        "fudedor", "fuder", "fuderte", "fudete", "fudidor", "fudilhao",
        "fudilhe",
    "gai", "gaijo", "gais", "gaita", "gajo", "gaju", "gajus", "galera",
        "galinha", "gatinha", "gay", "gays", "gemer", "gey", "geys", "gigalo",
        "gigolo", "gonorréia", "gordinho", "gordo", "gordona", "gorducho",
        "gordurento", "gorduxo", "gosa", "gostaria", "gostaria", "gostosao",
        "gostoso", "gostosoo", "gostoza", "gozar", "gratis", "gratiz",
        "gratuito", "grelinho", "grelo", "gringo", "grr", "grrr", "guei",
        "guey", "gueys",
    "hein", "herpes", "hey", "hipocrisia", "hipocrita", "hiv", "hmm", "hmmm",
        "homo", "homo", "homosexual", "horiveis", "horivel", "hororosa",
        "horriveis", "horrivel", "horroroso", "horrorozo", "hua", "huaahu",
        "huaauh", "huahua", "huauha", "humm", "hummm",
    "idiota", "ignorancia", "ignorantona", "ignore", "imbecil", "imbecils",
        "imbecis", "imundo", "incompetente", "inconpetente", "incopetente",
        "ipocritas", "iritante", "irritante", "irritavel",
    "japa", "jeca", "jumento",
    "kabrao", "kabrita", "kabroes", "kaca", "kachorra", "kachorrao", "kaga",
        "kaganeira", "kaganitas", "kaka", "kambada", "kanbada", "kara",
        "karago", "karah", "karahlo", "karaio", "karaiu", "karalh", "karalhao",
        "karalhinho", "karalhu", "karalhus", "karamba", "kick", "klitoris",
        "koca", "koiso", "koizo", "koko", "kolhao", "kolho", "kolhoos",
        "komigo", "kona", "koninha", "kontigo", "korno", "kornudo", "kosar",
        "kossar", "krapula", "kromo", "kuekinha", "kulho", "kulhoes", "kurtia",
        "kuzinho",
    "laalou", "laalu", "ladra", "ladrao", "ladroes", "lala", "lambe",
        "lambeme", "lambeoo", "lambero", "lambeua", "lambeume", "lambusar",
        "lambuzar", "lamento", "lanbe", "leali", "lealii", "lealui", "legal",
        "leiam", "leiao", "lela", "lerdo", "lesbia", "lesbica", "lésbica",
        "lialis", "lila", "linda", "lindaa", "llol", "lloll", "llooll",
        "lloolll", "lloollool", "loala", "lol", "lolilar", "lolll", "lollll",
        "lollo", "lollol", "lolol", "lololl", "loloo", "lolool", "lool",
        "looll", "loolll", "loolol", "louco", "loucura", "louko", "loukura",
        "luala", "lualoa", "lualua", "lyrics",
    "maconha", "maconheiro", "magnifico", "maluco", "malucu", "maluk",
        "malukeiros", "maluku", "maluqueira", "maluquer", "maminha",
        "maravilhosa", "maravilhoza", "maricá", "mariconi", "mariko", "mariqo",
        "mariquinha", "masturbar", "maxturbador", "meeeerda", "meeerda",
        "meerda", "meerdinha", "meerrda", "meirda", "mentecapto", "mentekapto",
        "mentira", "mentiroso", "merda", "merdda", "merdicas", "merdinha",
        "merdoso", "merrda", "meter", "meu", "meus", "mieeerrdinha", "mierda",
        "mierdda", "miierda", "mija", "mijador", "mijao", "mijinhas", "mim",
        "minha", "mirdi", "mmerda", "mmierda", "morcao", "morcoes", "morcos",
        "motherfucker", "motherfucking", "muthafucker", "muthafucking",
     "nadegas", "naum", "negam", "negao", "negram", "negrao", "neguin",
         "neguinho", "nerd", "nigga", "nocu", "nocuu", "nogento", "nogo",
         "nojento", "nojo", "noku", "noob", "noobs", "nooob", "nooobs", "nucu",
         "nugo", "nujento", "nujo", "nuku", "nukuu",
     "obrigado", "odeio", "ofercida", "oferecida", "oie", "oii", "ola", "olaaa",
        "olea", "oleae", "oleee", "omg", "ooo", "orgasmo", "orivei", "orivel",
        "ororosa", "orrivel", "orroroso", "orroroza", "otaria", "otario",
        "ouie",
    "palerma", "panaca", "panao", "panasca", "pandula", "paneleirices",
        "paneleirinho", "paneleiro", "paneleros", "panilas", "papa", "papai",
        "parasita", "pario", "pariu", "pariu", "parvo", "pau", "pde", "pede",
        "pederasta", "pedofilia", "peido", "peituda", "pelada", "peladinho",
        "pelado", "peludinho", "peludo", "penetrar", "penheta", "penheteiro",
        "penis", "pênis", "peniss", "penisss", "peofilia", "perfidiosamente",
        "perverso", "pervertido", "pessimo", "pevertido", "pila", "pilantra",
        "pilinha", "pilita", "piloca", "pilona", "pimp", "pintinho", "pinto",
        "pipi", "piranhada", "pirilao", "pirilau", "piroca", "pirocinha",
        "pirocudo", "piroka", "pirokinha", "pirola", "piroqinha", "piroqu",
        "piroquinha", "pirralhada", "pirroca", "pirrocudo", "pirrolo", "piru",
        "pissa", "pizi", "pobre", "podre", "podridao", "poha", "ponheta",
        "ponheteiro", "poop", "poota", "porco", "porcoria", "pornchanchada",
        "porno", "pornocanchada", "pornochancada", "pornochanchada",
        "pornochanxada", "pornochaxada", "porra", "porreiro", "porrinho",
        "potao", "poteiro", "potinha", "potista", "poto", "potoo", "potoria",
        "potto", "pouta", "poutaaa", "poutinha", "pputa", "pputinha", "pputta",
        "pputtariaa", "ppuuttaa", "preto", "prevertido", "procheneta",
        "prostitui", "prostituta", "proxeneta", "prustituta", "pts", "ptz",
        "pum", "pumm", "pummm", "punheta", "punheteiro", "puota", "purcaria",
        "puta", "putaaa", "putainha", "putana", "putao", "putare", "putariaa",
        "putariaaa", "putax", "putedo", "puteiro", "putinha", "putinhaa",
        "putinhaaa", "putista", "putoaa", "putois", "putomacho", "putona",
        "putonaa", "putonaaa", "putoona", "putoria", "putox", "putridos",
        "puts", "puttaa", "putteiro", "putto", "putz", "puuta", "puutaa",
        "puutaaa", "puuteiros", "puutona", "puutta", "puuttaa", "puuttaaa",
    "queca", "quecu", "quek", "queq", "queque",
    "rabo", "rameira", "ranha", "rebentadas", "recomendamos", "recomendo",
        "rego", "retardado", "ridiculo", "rola", "ronaldo", "ronaldon", "rosca",
        "rsrs", "ruim",
    "sacana", "sacanagem", "sacanajem", "sacanice", "saco", "safadao", "safado",
        "safadona", "safadoo", "salebot", "sandraemeirelles", "sarna", "secsso",
         "sei", "semvergonha", "sexo", "shit", "sigano", "siiim", "siim",
         "simpatica", "slt", "soco", "somos", "sovaco", "star", "stou",
         "stupid", "suck", "suja", "supimpa", "supinpa", "surra", "suruba",
         "suvaco", "suvacu",
    "tao", "taradao", "tarado", "taradoo", "tau", "tcao", "tcau", "tchao",
        "tchau", "teama", "teamoo", "tesao", "teste", "testiculos", "tesuda",
        "teta", "tetuda", "teu", "teus", "tezao", "tezudo", "thao", "thau",
        "thiao", "thiau", "tiao", "tiau", "tomano", "tomarno", "transa",
        "transadinha", "tranza", "traseiro", "traveco", "trepar", "treta",
        "trocha", "troha", "troucha", "trouxa", "trouxao", "troxa", "troxao",
        "trupe", "tua", "tuas",
    "uah", "uahauh", "uahuah", "ugly", "uha", "uhahua", "uhauah", "uhauha",
        "uie",
    "vadia", "vadiagem", "vadio", "vagabundagem", "vagabundo", "vagal",
        "vagina", "vaginal", "vaitomano", "vaitomarno", "veadagem", "veadao",
        "veadinho", "veado", "veadu", "veadus", "vergonha", "vergonhozo",
        "viadagem", "viadagems", "viadagen", "viadagens", "viadajem",
        "viadajems", "viadajen", "viadao", "viadinho", "viadinhu", "viado",
        "viadonho", "viadu", "viadunho", "viadus", "vibrador", "vibrator",
        "violador", "violou", "virgem", "virgen", "virgindade", "virjem",
        "viva", "viva", "voce", "voce", "vomito", "vos", "vtnc",
    "woo", "wtf",
    "xaboita", "xana", "xaneta", "xapado", "xata", "xatao", "xavasca",
        "xereca", "xeroca", "xichi", "xingar", "xingoes", "xixi", "xoroca",
        "xoxo", "xoxota", "xoxotinha", "xoxu", "xuchu", "xulo", "xupador",
        "xuper", "xupeta", "xupu", "xuranha", "xuxo", "xuxu", "xuxuta", "xxx",
    "yeah", "yes",
    "zipi", "zizi", "zoando", "zoar", "zoeira", "zuando", "zuar", "zueira"
])
STEMMED_BADWORDS = set(STEMMER.stem(w) for w in BADWORDS)
try:
    DICTIONARY = enchant.Dict("pt")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'pt'.  " +
                      "Consider installing 'myspell-pt'.")

def stem_word_process():
    def stem_word(word):
        return STEMMER.stem(word.lower())
    return stem_word
stem_word = LanguageUtility("stem_word", stem_word_process, depends_on=[])

def is_badword_process(stem_word):
    def is_badword(word):
        return stem_word(word) in STEMMED_BADWORDS
    return is_badword
is_badword = LanguageUtility("is_badword", is_badword_process,
                             depends_on=[stem_word])


def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)
    return is_misspelled
is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process,
                                depends_on=[])

def is_stopword_process():
    def is_stopword(word):
        return word.lower() in STOPWORDS
    return is_stopword
is_stopword = LanguageUtility("is_stopword", is_stopword_process, depends_on=[])

sys.modules[__name__] = Language(
    __name__,
    [stem_word, is_badword, is_misspelled, is_stopword]
)
"""
Implements :class:`~revscoring.languages.language.Language` for Portuguese.
Comes complete with all language utilities.
"""
