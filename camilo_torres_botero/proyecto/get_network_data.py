from pymongo import MongoClient
from nltk.corpus import stopwords

client = MongoClient('localhost', 27017)
db = client.caobanutresa_repeat_nouns_emojis_adjectives

vocab = db.tweets_words.distinct('word')

users = list(db.tweets_users.find({},{'text_emojis_nouns':1, 'id':1, 'emojis':1, '_id': 0}))
# remove_words = ['chimb', 'mierda', 'puta', 'malparid', 'gonorrea', 'joder', 'cacorr', 'pirob', 'piru']
# remain_words = ['computa', 'computador', 'computadora', 'diputado']
remove_words = []
with open('remove_words.txt', encoding="utf8") as f:
    for line in f:
        remove_word = line.replace('\n', '')
        remove_words.append(remove_word)
print("remove_words:", remove_words)
print("len(remove_words):", len(remove_words))
print()

remove_chars = []
with open('remove_chars.txt', encoding="utf8") as f:
    for line in f:
        remove_char = line.replace('\n', '')
        remove_chars.append(remove_char)
print("remove_chars:", remove_chars)
print("len(remove_chars):", len(remove_chars))
print()

total_words = len(vocab)
print('total palabras vocabulario:', total_words)
print('total usuarios:', len(users))

word_count = 1
word_count_percent = 0
edges = []
# for word in vocab:
#     new_word_count_percent = int(round((word_count / total_words) * 100))
#     if new_word_count_percent > word_count_percent:
#         print(new_word_count_percent, "%")
#         word_count_percent = new_word_count_percent
#     word_count += 1
#     word_lower = word.lower()
#     for user in users:
#         if 'text_emojis_nouns' in user:
#             text_emojis_nouns_lower = list(map(lambda x:x.lower(),user['text_emojis_nouns']))
#             if word_lower in text_emojis_nouns_lower:
#                 edges.add((user['id'],word_lower))

count = 0
for user in users:
    if 'text_emojis_nouns' in user:
        ramain_emojis = []
        if 'emojis' in user:
            ramain_emojis = user['emojis']
        text_emojis_nouns_lower = list(map(lambda x:x.lower(),user['text_emojis_nouns']))
        for word in text_emojis_nouns_lower:
            word_lower = word.lower()
            add_word_flag = True
            if (word_lower in stopwords.words('spanish')) or (word_lower in stopwords.words('english')) or (word_lower in stopwords.words('portuguese')) or (len(word_lower) < 3 and word_lower not in ramain_emojis):
                # print(word_lower)
                add_word_flag = False
                count += 1
            if word_lower in remove_words:
                # print("word_lower:", word_lower)
                add_word_flag = False
                count += 1
            for remove_char in remove_chars:
                if remove_char in word_lower:
                    # print(word_lower)
                    add_word_flag = False
                    count +=1
            if word_lower.startswith("@"):
                add_word_flag = False
                count += 1
            if add_word_flag:
                edges.append((user['id'],word_lower))
print("count:", count)
print(len(edges))

edges_file = open('edges_file_total_network_weights_undirected_4.txt', 'w')

print('source\ttarget\ttype', file=edges_file)

for k, v in sorted(edges, key=lambda x: x[1]):
    print(k+'\t'+v+'\tUndirected', file=edges_file)
print(len(edges))