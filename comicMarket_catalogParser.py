import sys, csv, re

# Check if a file path is provided as a command-line argument
if len(sys.argv) < 3:
    print("Usage: python comicMarket_catalogParser.py <inputfile_path> <outputfile_path>")
    sys.exit(1)

inputfile_path = sys.argv[1]
outputfile_path = sys.argv[2]

block_names = ["Ａ", "Ｂ", "Ｃ", "Ｄ", "Ｅ", "Ｆ", "Ｇ", "Ｈ", "Ｉ", "Ｊ","Ｋ", "Ｌ", "Ｍ", "Ｎ", "Ｏ","Ｐ", "Ｑ", "Ｒ", "Ｓ", "Ｔ","Ｕ", "Ｖ", "Ｗ", "Ｘ", "Ｙ","Ｚ",
               "ア", "イ", "ウ", "エ", "オ", "カ", "キ", "ク", "ケ", "コ", "サ", "シ", "ス", "セ", "ソ", "タ", "チ", "ツ", "テ", "ト","ナ", "ニ", "ヌ", "ネ", "ノ","ハ", "パ", "ヒ", "ピ", "フ", "ピ", "ヘ", "ぺ", "ホ", "ポ", "マ", "ミ", "ム", "メ", "モ","ヤ", "ユ", "ヨ","ラ", "リ", "ル", "レ", "ロ","ワ", "ヲ", "ン",
               "ａ", "ｂ", "ｃ", "ｄ", "ｅ", "ｆ", "ｇ", "ｈ", "ｉ", "ｊ","ｋ", "ｌ", "ｍ", "ｎ", "ｏ","ｐ", "ｑ", "ｒ", "ｓ", "ｔ","ｕ", "ｖ", "ｗ", "ｘ", "ｙ","ｚ",
               "あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ", "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と","な", "に", "ぬ", "ね", "の","は", "ひ", "ふ", "へ", "ほ","ま", "み", "む", "め", "も","や", "ゆ", "よ","ら", "り", "る", "れ", "ろ","わ", "を", "ん",]

catalog_keys = ['タイプ', 'シリアル番号', 'お気に入り色', 'カタログページ', 'ページ内位置', '曜日', '地区', 'ブロック', 'スペース', 'ジャンル', 'サークル名', 'さーくる名', '代表者', '著作物', 'url', 'mail', '概要', 'メモ']
select_keys = ['サークル名', '優先度', '曜日','地区', 'ブロック', 'スペース', '机', 'インデックス', 'スペース名','メモ', '金額', '代表者']
priority_label = ['優先', '中', '低', 'その他', 'その他', 'その他', 'その他', '未定', '対象外',]



with open(inputfile_path, newline='', encoding="utf-8_sig") as fi, open(outputfile_path, 'w', newline='', encoding="utf-8_sig") as fo:
    reader = csv.reader(fi)
    writer = csv.writer(fo)
    next(reader)  # Skip the first row
    writer.writerow(select_keys) # Write the header row
    for row in reader:
        # Skip the row if the first column is "UnKnown"
        if row[0] == 'UnKnown':
            continue
        record = dict(zip(catalog_keys, row))

        # Add a/b column (e.g. "a" or "b")
        record.update(机='a' if int(record['スペース']) % 2 == 0 else 'b')
        # Add space_name column (e.g. "東Ａ-01a")
        record.update(スペース名= record['地区'] + record['ブロック'] + '-' + record['スペース'] + record['机'])
        # Add index column (e.g. 0, 1, 2, ...)
        record.update(インデックス=block_names.index(record['ブロック']))
        # Replace backslash with yen sign
        record['メモ'] = record['メモ'].replace('\\', '￥')
        # Add price column
        prices = re.findall(r'￥(\d+)', record['メモ'])
        total_price = sum(int(price) for price in prices)
        record.update(金額=total_price)
        # Add priority column
        record.update(優先度=priority_label[int(record['お気に入り色'])-1])
        
        selected_values = [record[key] for key in select_keys]
        writer.writerow(selected_values)
    
    fo.close()
    fi.close()

        
        