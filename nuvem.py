import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import polars as pl
import spacy

from collections import Counter

nlp = spacy.load('pt_core_news_lg')
caminho_da_fonte = 'NotoSansJP-Regular.ttf' 

stopword = ["a","ah","acerca","adeus","agora","ainda","alem",
             "algmas","algo","algumas","alguns","ali","além",
             "ambas","ambos","ano","anos","antes","ao","aonde",
             "aos","apenas","apoio","apontar","apos","após","aquela",
             "aquelas","aquele","aqueles","aqui","aquilo","as","assim",
             "através","atrás","até","aí","baixo","bastante","bem","boa",
             "boas","bom","bons","breve","cada","caminho","catorze","cedo",
             "cento","certamente","certeza","cima","cinco","coisa","com","como",
             "comprido","conhecido","conselho","contra","contudo","corrente",
             "cuja","cujas","cujo","cujos","custa","cá","da","daquela",
             "daquelas","daquele","daqueles","dar","das","de","debaixo",
             "dela","delas","dele","deles","demais","dentro","depois",
             "desde","desligado","dessa","dessas","desse","desses","desta",
             "destas","deste","destes","deve","devem","deverá","dez","dezanove",
             "dezasseis","dezassete","dezoito","dia","diante","direita","dispoe",
             "dispoem","diversa","diversas","diversos","diz","dizem","dizer",
             "do","dois","dos","doze","duas","durante","dá","dão","dúvida","e",
             "ela","elas","ele","eles","em","embora","enquanto","entao","entre",
             "então","era","eram","essa","essas","esse","esses","esta","estado",
             "estamos","estar","estará","estas","estava","estavam","este","esteja",
             "estejam","estejamos","estes","esteve","estive","estivemos","estiver",
             "estivera","estiveram","estiverem","estivermos","estivesse","estivessem",
             "estiveste","estivestes","estivéramos","estivéssemos","estou","está",
             "estás","estávamos","estão","eu","exemplo","falta","fará","favor",
             "faz","fazeis","fazem","fazemos","fazer","fazes","fazia","faço",
             "fez","fim","final","foi","fomos","for","fora","foram",
             "forem","forma","formos","fosse","fossem","foste","fostes",
             "fui","fôramos","fôssemos","geral","grande","grandes","grupo",
             "ha","haja","hajam","hajamos","havemos","havia","hei","hoje",
             "hora","horas","houve","houvemos","houver","houvera","houveram",
             "houverei","houverem","houveremos","houveria","houveriam","houvermos",
             "houverá","houverão","houveríamos","houvesse","houvessem","houvéramos",
             "houvéssemos","há","hão","iniciar","inicio","ir","irá","isso","ista","iste","isto",
             "já","lado","lhe","lhes","ligado","local","logo","longe","lugar","lá",
             "maior","maioria","maiorias","mais","mal","mas","me","mediante","meio",
             "menor","menos","meses","mesma","mesmas","mesmo","mesmos","meu","meus",
             "mil","minha","minhas", "mim", "my", "the", "to", "that", "and", "your", "I", "ai",
             "momento","muito","muitos","máximo","mês","na","nada","nao","naquela","naquelas",
             "naquele","naqueles","nas","nem","nenhuma","nessa","nessas","nesse","nesses","nesta",
             "nestas","neste","nestes","no","noite","nome","nos","nossa","nossas","nosso","nossos","nova",
             "novas","nove","novo","novos","num","numa","numas","nunca","nuns","não","nível","nós","número",
             "o", "oh","obra","obrigada","obrigado","oitava","oitavo","oito","onde","ontem","onze","os","ou","outra",
             "outras","outro","outros","para","parece","parte","partir","paucas","pegar","pela","pelas","pelo",
             "pelos","perante","perto","pessoas","pode","podem","poder","poderá","podia","pois","ponto","pontos",
             "por","porque","porquê","portanto","posição","possivelmente","posso","possível","pouca","pouco","poucos",
             "povo","pra", "primeira","primeiras","primeiro","primeiros","pro","promeiro","propios","proprio","própria",
             "próprias","próprio","próprios","próxima","próximas","próximo","próximos","puderam","pôde","põe","põem",
             "quais","qual","qualquer","quando","quanto","quarta","quarto","quatro","que","quem","quer","quereis","querem",
             "queremas","queres","quero","questão","quieto","quinta","quinto","quinze","quáis","quê","relação","sabe","sabem",
             "saber","se","segunda","segundo","sei","seis","seja","sejam","sejamos","sem","sempre","sendo","ser","serei","seremos",
             "seria","seriam","será","serão","seríamos","sete","seu","seus","sexta","sexto","sim","sistema","sob","sobre","sois",
             "somente","somos","sou","sua","suas","são","sétima","sétimo","só","tá","tal","talvez","tambem","também","tanta","tantas",
             "tanto","tarde","te","tem","temos","tempo","tendes","tenha","tenham","tenhamos","tenho","tens","tentar","tentaram",
             "tente","tentei","ter","terceira","terceiro","terei","teremos","teria","teriam","terá","terão","teríamos","teu",
             "teus","teve","tinha","tinham","tipo","tive","tivemos","tiver","tivera","tiveram","tiverem","tivermos","tivesse",
             "tivessem","tiveste","tivestes","tivéramos","tivéssemos","toda","todas","todo","todos","trabalhar","trabalho",
             "treze","três","tu","tua","tuas","tudo","tão","tém","têm","tínhamos","uh",
             "um","uma","umas","uns","usa","usar","vai","vais","valor","veja","vem","vens","ver","verdade",
             "verdadeiro","vez","vezes","viagem","vindo","vinte","você","vocês","vos","vossa","vossas","vosso",
             "vossos","vários","vão","vêm","vós","zero","à","às","área","é","éramos","és","último", "vi", 
             "to", "i'll", "tô", "will", "iô", "2x", "is", "from", "it", "up", "be", "m", "d", "hm",
             "lo", "la", "ia", "just", "i'm", "yeah", "in", "this", "therefore", "this", "you", "vou",
             "ahn", "so", "but", "tava", "cê", "ti", "4x", "iria", "hein", "gente", "deixa", "ra",
             "us", "eu","hey","trás", "one", "pros", "deu",
             "dei", "viu", "irei", "fiz", "t", "3x", "uoh", "i'm", "i 'm", 
             "10000", "uh-uh", "essa", "que", "ohse", "1", "alguém", "quis", "4x)se", 
             "ninguém", "'s", "i'd", "bout", " 's", "i'd", 
             "i 'd", "i' d", "30000",'あそこ', 'あっ', 'あと', 'い', 'いう', 'います', 'いる', 'う', 'うち',
            'お', 'おり', 'おります', 'か', 'から', 'が', 'き', 'ここ', 'こと', 'この',
            'これ', 'さ', 'し', 'しかし', 'する', 'ず', 'せ', 'せる', 'そこ', 'その', 'それ', 
            'た', 'ため', 'だ', 'て', 'で', 'でき', 'できる', 'です', 'では', 'でも', 'と', 
            'ない', 'な', 'など', 'に', 'の', 'は', 'ます', 'ました', 'まで', 'も', 'もの', 
            'や', 'よう', 'より', 'られる', 'れ', 'れる', 'を', 'ん', '何', 
            '私', "'S", "' S", "i' m", "meu", "meus"] + list(STOPWORDS)


df = pl.read_csv('fresno_stats2.csv')
wc = WordCloud(
    width=1280,
    height=720,
    background_color='white',
    stopwords=stopword,
    font_path=caminho_da_fonte
)



for album in df.sort('data').partition_by('album'):
    palavras = nlp(''.join(album['letra'].drop_nulls()))

    contador = Counter(
        palavra.text for palavra in palavras 
        if palavra.text not in stopword and not palavra.is_punct
    )
    
    img = wc.generate_from_frequencies(contador)

    fig, ax = plt.subplots()

    ax.set_title(album['album'][0])
    ax.imshow(img)
    ax.axis('off')
    plt.show()
    # plt.savefig(result_clould.png)