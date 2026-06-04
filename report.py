from data import CATEGORY_NAMES, SAMPLE_POSTS, TRAINING_DATA
from text_processing import (
    analyze_text,
    classify_text,
    evaluate_training_data,
    expand_feature_terms,
    extract_category_feature_words,
    extract_feature_words,
    get_training_summary,
    normalize_text,
    split_words,
)


def print_line(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_overview():
    summary = get_training_summary()

    print_line("1. THONG KE TAP DU LIEU")
    print(f"So van ban mau: {len(SAMPLE_POSTS)}")
    print(f"So van ban huan luyen: {summary['document_count']}")
    print(f"So nhan/nhom: {summary['category_count']}")
    print(f"So tu/cum trong tu vung dac trung: {summary['vocabulary_size']}")

    print("\nPhan bo du lieu theo nhan:")
    for item in summary["categories"]:
        print(f"- {item['name']}: {item['document_count']} van ban")


def print_basic_text_analysis():
    print_line("2. DEM SO TU VA TAN SUAT TU TRONG VAN BAN MAU")
    for index, text in enumerate(SAMPLE_POSTS, start=1):
        analysis = analyze_text(text)
        frequency_text = ", ".join(
            f"{word}: {count}" for word, count in analysis["frequency"]
        )
        print(f"\nVan ban {index}: {text}")
        print(f"- Chuan hoa: {analysis['normalized']}")
        print(f"- So tu/cum: {analysis['word_count']}")
        print(f"- Tan suat: {frequency_text}")


def print_training_data():
    print_line("3. TAP DU LIEU MAU CO NHAN")
    for index, (category, text) in enumerate(TRAINING_DATA, start=1):
        print(f"{index:02d}. [{CATEGORY_NAMES[category]}] {text}")


def print_feature_words():
    print_line("4. DANH SACH TU/CUM DAC TRUNG")
    for index, (word, count) in enumerate(extract_feature_words(limit=40), start=1):
        print(f"{index:02d}. {word}: {count}")


def print_category_feature_words():
    print_line("5. TU/CUM DAC TRUNG THEO TUNG NHAN")
    for category in extract_category_feature_words(limit=12):
        words = ", ".join(f"{word}: {count}" for word, count in category["words"])
        print(f"- {category['name']}: {words}")


def print_model_evaluation():
    evaluation = evaluate_training_data()

    print_line("6. DANH GIA MO HINH BANG LEAVE-ONE-OUT")
    print(f"Phuong phap: {evaluation['method']}")
    print(f"So mau kiem thu: {evaluation['total']}")
    print(f"So du doan dung: {evaluation['correct']}")
    print(f"So du doan sai: {evaluation['incorrect']}")
    print(f"Do chinh xac: {evaluation['accuracy'] * 100:.2f}%")

    print("\nPrecision/Recall theo nhan:")
    for item in evaluation["category_scores"]:
        print(
            f"- {item['name']}: "
            f"precision {item['precision'] * 100:.2f}%, "
            f"recall {item['recall'] * 100:.2f}% "
            f"({item['correct']}/{item['total']})"
        )

    categories = evaluation["categories"]
    print("\nMa tran nham lan:")
    header = "Thuc te \\ Du doan".ljust(22)
    header += "".join(item["name"].rjust(14) for item in categories)
    print(header)
    for actual in categories:
        row = actual["name"].ljust(22)
        for predicted in categories:
            value = evaluation["confusion"][actual["category"]][predicted["category"]]
            row += str(value).rjust(14)
        print(row)

    wrong_results = [item for item in evaluation["results"] if not item["is_correct"]]
    if wrong_results:
        print("\nCac mau du doan sai:")
        for item in wrong_results:
            print(
                f"- #{item['index']} [{item['actual_name']}] -> "
                f"{item['predicted_name']} ({item['probability'] * 100:.2f}%): "
                f"{item['text']}"
            )
    else:
        print("\nKhong co mau nao bi du doan sai trong phep kiem thu nay.")


def print_segmentation_debug():
    print_line("7. DEBUG TACH TU/CUM THEO TU DIEN NGU NGHIA")
    all_texts = [(f"Van ban mau {index}", text) for index, text in enumerate(SAMPLE_POSTS, 1)]
    all_texts.extend(
        (f"Huan luyen {index} - {CATEGORY_NAMES[category]}", text)
        for index, (category, text) in enumerate(TRAINING_DATA, 1)
    )

    for label, text in all_texts:
        words = split_words(text)
        feature_words = split_words(text, remove_stop_words=True)
        expanded_words = expand_feature_terms(feature_words)
        print(f"\n{label}: {text}")
        print(f"- Chuan hoa: {normalize_text(text)}")
        print(f"- Tach tu/cum: {' / '.join(words)}")
        print(f"- Sau khi bo stop words: {' / '.join(feature_words)}")
        print(f"- Dac trung tinh xac suat: {' / '.join(expanded_words)}")


def print_classification_demo():
    print_line("8. DEMO PHAN LOAI VAN BAN MOI")
    demo_posts = [
        "Mình cần tài liệu học Python và bài tập thực hành.",
        "Bán tai nghe còn bảo hành, giá sinh viên.",
        "Không đăng nhập được tài khoản thì sửa như thế nào?",
        "Cuối tuần có phim hay hoặc game nào vui không?",
    ]

    for text in demo_posts:
        result = classify_text(text)
        print(f"\nVan ban: {text}")
        print(f"- Nhan du doan: {result['name']}")
        print(f"- Do tin cay: {result['probability'] * 100:.2f}%")
        print("- Xac suat tung nhom:")
        for item in result["probabilities"]:
            print(f"  + {item['name']}: {item['probability'] * 100:.2f}%")
        matched_words = ", ".join(result["matched_words"]) or "Khong co"
        print(f"- Tu/cum trung voi tap dac trung: {matched_words}")


def main():
    print_overview()
    print_basic_text_analysis()
    print_training_data()
    print_feature_words()
    print_category_feature_words()
    print_model_evaluation()
    print_segmentation_debug()
    print_classification_demo()


if __name__ == "__main__":
    main()
