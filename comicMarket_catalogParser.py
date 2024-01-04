import sys, csv, re, argparse

BLOCK_NAMES = ["Ａ", "Ｂ", "Ｃ", "Ｄ", "Ｅ", "Ｆ", "Ｇ", "Ｈ", "Ｉ", "Ｊ","Ｋ", "Ｌ", "Ｍ", "Ｎ", "Ｏ","Ｐ", "Ｑ", "Ｒ", "Ｓ", "Ｔ","Ｕ", "Ｖ", "Ｗ", "Ｘ", "Ｙ","Ｚ",
               "ア", "イ", "ウ", "エ", "オ", "カ", "キ", "ク", "ケ", "コ", "サ", "シ", "ス", "セ", "ソ", "タ", "チ", "ツ", "テ", "ト","ナ", "ニ", "ヌ", "ネ", "ノ","ハ", "パ", "ヒ", "ピ", "フ", "ピ", "ヘ", "ぺ", "ホ", "ポ", "マ", "ミ", "ム", "メ", "モ","ヤ", "ユ", "ヨ","ラ", "リ", "ル", "レ", "ロ","ワ", "ヲ", "ン",
               "ａ", "ｂ", "ｃ", "ｄ", "ｅ", "ｆ", "ｇ", "ｈ", "ｉ", "ｊ","ｋ", "ｌ", "ｍ", "ｎ", "ｏ","ｐ", "ｑ", "ｒ", "ｓ", "ｔ","ｕ", "ｖ", "ｗ", "ｘ", "ｙ","ｚ",
               "あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ", "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と","な", "に", "ぬ", "ね", "の","は", "ひ", "ふ", "へ", "ほ","ま", "み", "む", "め", "も","や", "ゆ", "よ","ら", "り", "る", "れ", "ろ","わ", "を", "ん",]

CATALOG_KEYS = ['タイプ', 'シリアル番号', 'お気に入り色', 'カタログページ', 'ページ内位置', '曜日', '地区', 'ブロック', 'スペース', 'ジャンル', 'サークル名', 'さーくる名', '代表者', '著作物', 'url', 'mail', '概要', 'メモ']
SELECT_KEYS = ['サークル名', '登録者', '優先度', '曜日','地区', 'ブロック', 'スペース', '机', 'インデックス', 'スペース名','メモ', '金額', '代表者', 'シリアル番号', '重複回数']
PRIORITY_LABEL = ['優先', '中', '低', 'その他', 'その他', 'その他', 'その他', '未定', '対象外',]


def process_record(record):
    # Add a/b column (e.g. "a" or "b")
    record.update(机='a' if int(record['スペース']) % 2 == 0 else 'b')
    # Add space_name column (e.g. "東Ａ-01a")
    record.update(スペース名= record['地区'] + record['ブロック'] + '-' + record['スペース'] + record['机'])
    # Add index column (e.g. 0, 1, 2, ...)
    record.update(インデックス=BLOCK_NAMES.index(record['ブロック']))
    # Replace backslash with yen sign
    record['メモ'] = record['メモ'].replace('\\', '￥')
    # Add price column
    prices = re.findall(r'￥(\d+)', record['メモ'])
    total_price = sum(int(price) for price in prices)
    record.update(金額=total_price)
    # Add priority column
    record.update(優先度=PRIORITY_LABEL[int(record['お気に入り色'])-1])

    # Edit 地区 column
    if record['インデックス'] in range(0,38):
        record.update(地区="東123")
    elif record['インデックス'] in range(38, 77):
        record.update(地区="東456")
    elif record['インデックス'] in range(77, 103):
        record.update(地区="東7")
    elif record['インデックス'] in range(103, 120):
        record.update(地区="西2")
    elif record['インデックス'] in range(120, 148):
        record.update(地区="西1")
    
def check_duplicate(record, records):
    # Add duplicate column
    duplicates = []
    for other_record in records:
        if record['シリアル番号'] == other_record['シリアル番号']:
            duplicates.append(other_record)
    for duplicate in duplicates:
        duplicate.update(重複回数=len(duplicates)+1)
    record.update(重複回数=len(duplicates)+1)

def open_file(path,records,name):
    with open(path, newline='', encoding="utf-8_sig") as fi:
        reader = csv.reader(fi)
        next(reader)  # Skip the first row
        for row in reader:
            # Skip the row if the first column is "UnKnown"
            if row[0] == 'UnKnown':
                continue
            record = dict(zip(CATALOG_KEYS, row))
            record.update(登録者=name)
            process_record(record)
            check_duplicate(record, records)
            records.append(record)
            
        fi.close()

def main():
    parser = argparse.ArgumentParser(description='Process Comic Market catalog file.')
    parser.add_argument('-i', '--input', type=str, nargs='*', required=True, help='input file path')
    parser.add_argument('-n','--name', type=str, nargs='*', default=range(1,10), help='user name')
    parser.add_argument('-o','--output', type=str, default='output.csv', help='output file path')
    args = parser.parse_args()

    records = []
    for path, name in zip(args.input, args.name):
        open_file(path=path, records=records, name=name)

    

    with open(args.output, 'w', newline='', encoding="utf-8_sig") as fo:
        writer = csv.writer(fo)
        writer.writerow(SELECT_KEYS)
        for record in records:
            writer.writerow([record[key] for key in SELECT_KEYS])
        fo.close()

if __name__ == "__main__":
    main()
        