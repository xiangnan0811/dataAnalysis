import re
import jieba
import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}


def get_hot_50_songs(user_id):
    response = requests.get(f'https://music.163.com/artist?id={user_id}', headers=headers)
    song_ids = re.findall(r'<a href="/song\?id=(\d+)">(.*?)</a>', response.text, re.S)
    return song_ids


def get_song(song_id):
    response = requests.get(f'https://music.163.com/song/media/outer/url?id={song_id}.mp3', headers=headers)
    return response.content


def get_lyric(song_id):
    response = requests.get(f'http://music.163.com/api/song/lyric?os=pc&id={song_id}&lv=-1&kv=-1&tv=-1', headers=headers)
    lyric = re.sub(r'\[.*?\]', '', response.json()['lrc']['lyric'])
    return lyric


def remove_stop_words(f):
    stop_words = ['作词', '作曲', '编曲', 'Arranger', '录音', '混音', '人声', 'Vocal', '弦乐', 'Keyboard', '键盘', '编辑', '助理', 'Assistants', 'Mixing', 'Editing', 'Recording', '音乐', '制作', 'Producer', '发行', 'produced', 'and', 'distributed', '的', '你', '我', '了', '是', '在', '不', '也', '还']
    for stop_word in stop_words:
        f = f.replace(stop_word, '')
    return f


def create_word_cloud(f, filename):
    print('根据词频，开始生成词云!')
    f = remove_stop_words(f)
    cut_text = " ".join(jieba.cut(f,cut_all=False, HMM=True))
    wc = WordCloud(
        font_path="MSYH.TTC",
        max_words=100,
        width=2000,
        height=1200,
    )
    wordcloud = wc.generate(cut_text)
    # 写词云图片
    wordcloud.to_file(f"{filename}.jpg")
    # 显示词云文件
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    user_id = '5771'
    all_words = ''
    songs = get_hot_50_songs(user_id)
    for song_id, song_name in songs:
        print(song_name)
        print('-' * 100)
        lyric = get_lyric(song_id)
        all_words  = f'{all_words} {lyric}'
    create_word_cloud(all_words, user_id)

