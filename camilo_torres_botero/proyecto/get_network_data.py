from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.caobanutresa_100000_nouns_emojis_adjectives

vocab = db.tweets_words.distinct('word')

users = list(db.tweets_users.find({},{'text_emojis_nouns':1, 'id':1,'_id': 0}))

total_words = len(vocab)
print('total palabras vocabulario:', total_words)
print('total usuarios:', len(users))

word_count = 1
word_count_percent = 0
edges = set()
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

for user in users:
    if 'text_emojis_nouns' in user:
        text_emojis_nouns_lower = list(map(lambda x:x.lower(),user['text_emojis_nouns']))
        for word in text_emojis_nouns_lower:
            word_lower = word.lower()
            edges.add((user['id'],word_lower))

edges_file = open('edges_file_caobanutresa_100000_nouns_emojis_adjectives.txt', 'w')

print('source\ttarget', file=edges_file)

for k, v in sorted(edges, key=lambda x: x[1]):
    print(k+'\t'+v, file=edges_file)
print(len(edges))