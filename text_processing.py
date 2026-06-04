import math
import re
from collections import Counter

from data import CATEGORY_NAMES, TRAINING_DATA


STOP_WORDS = {
    "ai",
    "anh",
    "bạn",
    "bằng",
    "bị",
    "biết",
    "các",
    "cách",
    "cần",
    "cho",
    "có",
    "còn",
    "của",
    "đã",
    "để",
    "được",
    "giá",
    "hỏi",
    "không",
    "là",
    "lại",
    "làm",
    "mình",
    "mới",
    "một",
    "mua",
    "nào",
    "người",
    "nhiều",
    "ở",
    "thế",
    "thì",
    "tốt",
    "từ",
    "và",
    "với",
    "xin",
}

SEMANTIC_PHRASES = {
    "24 inch",
    "âm thanh",
    "bài đăng",
    "bài hát",
    "bài học",
    "bài nhạc",
    "bài thực hành",
    "bài thuyết trình",
    "bài tập",
    "bạn bè",
    "bàn phím",
    "bàn phím cơ",
    "balo laptop",
    "bán ghế",
    "bán laptop",
    "bán màn hình",
    "bán điện thoại",
    "bảo hành",
    "bắt đầu",
    "bộ phim",
    "bóng đá",
    "ca nhạc",
    "cà phê",
    "cài đặt",
    "cài đặt môi trường",
    "cách sửa",
    "chắc chắn",
    "chia sẻ",
    "chơi game",
    "chương trình",
    "chương trình ca nhạc",
    "chương trình hài",
    "chương trình python",
    "cosplay",
    "cơ bản",
    "cơ sở dữ liệu",
    "cuối tuần này",
    "cuối tuần",
    "cũ giá rẻ",
    "cấu hình ổn",
    "dễ hiểu",
    "dell cũ",
    "đăng nhập",
    "đăng ký",
    "đề cương ôn thi",
    "đề cương",
    "đề xuất",
    "địa chỉ",
    "điện thoại",
    "điện thoại cũ",
    "điện thoại không nhận sạc",
    "độ tin cậy",
    "đông vui",
    "đổi mật khẩu",
    "đội chơi",
    "đọc lúc rảnh",
    "file pdf",
    "file bài giảng",
    "game này",
    "game vui",
    "gần trường",
    "giải trí",
    "giá rẻ",
    "giá sinh viên",
    "giá thương lượng",
    "giá tốt",
    "giáo trình xử lý ngôn ngữ tự nhiên",
    "giáo trình",
    "giấy xác nhận sinh viên",
    "giờ học",
    "giờ làm",
    "hà nội",
    "hài nhẹ nhàng",
    "hình xanh windows",
    "học html css",
    "học lập trình",
    "học mỗi ngày",
    "học python",
    "học python cơ bản",
    "học tập",
    "học tiếng anh",
    "học xử lý ngôn ngữ tự nhiên",
    "khá hay",
    "khá vui",
    "kết nối wifi",
    "khóa học",
    "khóa học miễn phí",
    "khôi phục",
    "khôi phục bài viết",
    "khu vực gần trường",
    "kinh nghiệm",
    "kinh nghiệm học",
    "kinh nghiệm làm bài thuyết trình",
    "laptop cũ",
    "laptop dell cũ",
    "lập đội",
    "lập đội chơi",
    "lập trình",
    "lập trình python",
    "lập trình web",
    "lỗi không mở được file pdf",
    "lỗi màn hình xanh windows",
    "lỗi màn hình xanh",
    "lỗi đăng nhập",
    "lỗi khi chạy chương trình",
    "lời giải bài tập lập trình python",
    "lời giải",
    "mạng máy tính",
    "mạng máy tính",
    "màn hình",
    "màn hình máy tính",
    "màn hình máy tính 24 inch",
    "màn hình xanh",
    "mất kết nối wifi",
    "mật khẩu",
    "máy tính",
    "máy tính cũ",
    "máy tính bị mất kết nối wifi",
    "máy tính không nghe được âm thanh",
    "máy tính xanh windows",
    "môi trường học lập trình web",
    "môi trường lập trình",
    "môi trường lập trình web",
    "môi trường",
    "mới ra rạp",
    "mới dùng vài lần",
    "mua bàn phím cơ",
    "mua sách",
    "mua sách lập trình python",
    "mua chuột không dây",
    "mua bán",
    "nhạc sống",
    "nhận sạc",
    "nhẹ nhàng",
    "nhạc sống",
    "ngôn ngữ",
    "ngôn ngữ tự nhiên",
    "người mới",
    "người mới bắt đầu",
    "nguyên nhân",
    "nội dung",
    "nội dung khá hay",
    "ôn thi cơ sở dữ liệu",
    "ôn tập",
    "ôn tập lý thuyết",
    "ôn thi",
    "pin còn khỏe",
    "phân loại",
    "phân loại nội dung",
    "phân loại nội dung bài đăng",
    "phím cơ",
    "phim hài",
    "phim hài nhẹ nhàng",
    "phim hay",
    "phim mới",
    "phim mới ra rạp",
    "phù hợp học tập",
    "qua sử dụng",
    "quán cà phê",
    "rất vui",
    "sách lập trình",
    "sách lập trình python",
    "sau giờ học",
    "sau giờ làm",
    "sinh viên",
    "sự kiện cosplay",
    "tài khoản",
    "tài khoản không đăng nhập được",
    "tài liệu",
    "tài liệu cơ sở dữ liệu",
    "tài liệu học python",
    "tài liệu ôn thi",
    "tài liệu xử lý ngôn ngữ tự nhiên",
    "sinh viên",
    "tài khoản",
    "tài liệu",
    "tai nghe",
    "tai nghe bluetooth",
    "tai nghe còn bảo hành",
    "tai nghe còn bảo hành âm thanh tốt",
    "thanh lý",
    "thanh lý balo laptop",
    "thanh lý tai nghe",
    "thao tác",
    "thủ tục",
    "thủ tục xin giấy xác nhận sinh viên",
    "thương mại",
    "thuyết trình",
    "thú vị",
    "tiếng anh",
    "tối nay",
    "trình duyệt",
    "trình duyệt không tải được ảnh",
    "trí tuệ nhân tạo",
    "trí tuệ nhân tạo",
    "trung tâm",
    "trung tâm thương mại",
    "truyện hay",
    "tự cài đặt",
    "tự nhiên",
    "từ đặc trưng",
    "ưu tiên",
    "văn bản",
    "văn bản mẫu",
    "web bằng python",
    "windows",
    "xác nhận sinh viên",
    "xác suất",
    "xác suất từng nhóm",
    "xanh windows",
    "xem phim",
    "xem phim hài",
    "xử lý file pdf",
    "xử lý",
    "xử lý ngôn ngữ tự nhiên",
    "xử lý văn bản",
    "xóa nhầm",
    "âm nhạc miễn phí",
    "bài giảng cơ sở dữ liệu",
    "bài tập thuật toán",
    "bàn học gỗ",
    "bàn phím không dây",
    "bàn phím không gõ được tiếng việt",
    "bảo mật",
    "bộ phim kinh dị",
    "ca nhạc ở công viên",
    "chứng chỉ bảo mật",
    "combo chuột và bàn phím",
    "diễn đàn",
    "dung lượng cao",
    "dễ đọc",
    "dễ hiểu",
    "đồ án python",
    "đổi tên hiển thị",
    "giá dưới năm triệu",
    "giá hợp lý",
    "giải bóng đá sinh viên",
    "giáo trình trí tuệ nhân tạo",
    "hệ thống học tập",
    "học máy",
    "học lập trình python",
    "học online",
    "học python nâng cao",
    "không gian đẹp",
    "không gửi được email",
    "không kết nối được máy chiếu",
    "không tải được tài liệu",
    "không tải được file bài giảng",
    "liên quân",
    "loa bluetooth",
    "máy chiếu",
    "máy in",
    "máy in cũ",
    "máy in không nhận lệnh in",
    "máy tính bảng",
    "máy tính bảng cũ",
    "mật khẩu wifi",
    "mã xác nhận",
    "mở lại",
    "môn xử lý ngôn ngữ tự nhiên",
    "naive bayes",
    "ngoại hình đẹp",
    "nhạc nhẹ",
    "nhạc thư giãn",
    "nhóm học chung",
    "nhanh hết pin",
    "ổ cứng di động",
    "phân loại văn bản",
    "phim hoạt hình",
    "pin ảo",
    "pin ổn",
    "playlist nhạc thư giãn",
    "phòng trọ sinh viên",
    "sách cơ sở dữ liệu",
    "sách thuật toán",
    "sắp xếp",
    "sự kiện âm nhạc",
    "tài liệu học python nâng cao",
    "tài liệu ôn thi lập trình hướng đối tượng",
    "tài khoản diễn đàn bị khóa",
    "tập huấn luyện",
    "thuật toán",
    "thuật toán sắp xếp",
    "thuật toán sắp xếp và tìm kiếm",
    "thứ bảy",
    "tiếng việt",
    "tìm kiếm",
    "trà sữa",
    "truyện tranh",
    "truyện tranh hài",
    "tuần này",
    "từ đâu",
    "văn phòng",
    "webcam học online",
    "đã qua sử dụng",
}

ATOMIC_TERMS = {
    "ảnh",
    "android",
    "bán",
    "bàn",
    "bóng",
    "bluetooth",
    "chill",
    "combo",
    "css",
    "cũ",
    "dell",
    "email",
    "game",
    "ghế",
    "học",
    "html",
    "laptop",
    "lỗi",
    "máy",
    "pdf",
    "phim",
    "pin",
    "python",
    "mini",
    "online",
    "webcam",
    "sách",
    "sạc",
    "sửa",
    "tìm",
    "web",
    "wifi",
    "windows",
}

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_phrase_dictionary(phrases):
    phrase_words = set()
    max_length = 1

    for phrase in phrases:
        words = tuple(normalize_text(phrase).split())
        if len(words) > 1:
            phrase_words.add(words)
            max_length = max(max_length, len(words))

    return phrase_words, max_length


PHRASE_DICTIONARY, MAX_PHRASE_LENGTH = build_phrase_dictionary(SEMANTIC_PHRASES)


def maximum_matching_segment(words):
    segmented = []
    index = 0

    while index < len(words):
        max_length = min(MAX_PHRASE_LENGTH, len(words) - index)
        matched = None

        for length in range(max_length, 1, -1):
            candidate = tuple(words[index : index + length])
            if candidate in PHRASE_DICTIONARY:
                matched = candidate
                break

        if matched is None:
            segmented.append(words[index])
            index += 1
        else:
            segmented.append(" ".join(matched))
            index += len(matched)

    return segmented


def split_words(text, remove_stop_words=False):
    words = maximum_matching_segment(normalize_text(text).split())
    if remove_stop_words:
        words = [word for word in words if word not in STOP_WORDS]
    return words


def expand_feature_terms(words):
    expanded = []
    seen = set()

    def add_term(term):
        if term and term not in seen and term not in STOP_WORDS:
            seen.add(term)
            expanded.append(term)

    for word in words:
        add_term(word)
        parts = word.split()

        for part in parts:
            if part in ATOMIC_TERMS:
                add_term(part)

        for start in range(len(parts)):
            for end in range(start + 2, len(parts) + 1):
                sub_phrase = " ".join(parts[start:end])
                if sub_phrase != word and tuple(parts[start:end]) in PHRASE_DICTIONARY:
                    add_term(sub_phrase)

    return expanded


def count_words(text):
    return len(split_words(text))


def count_word_frequency(text, remove_stop_words=False):
    return Counter(split_words(text, remove_stop_words=remove_stop_words))


def analyze_text(text):
    frequency = count_word_frequency(text)
    sorted_frequency = sorted(
        frequency.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return {
        "original": text,
        "normalized": normalize_text(text),
        "character_count": len(text),
        "word_count": count_words(text),
        "unique_word_count": len(frequency),
        "frequency": sorted_frequency,
    }


def build_model(training_data):
    category_document_count = Counter()
    category_word_count = Counter()
    category_word_frequency = {}
    vocabulary = set()

    for category, text in training_data:
        category_document_count[category] += 1
        words = expand_feature_terms(split_words(text, remove_stop_words=True))
        vocabulary.update(words)
        if category not in category_word_frequency:
            category_word_frequency[category] = Counter()
        category_word_frequency[category].update(words)
        category_word_count[category] += len(words)

    return {
        "document_count": len(training_data),
        "category_document_count": category_document_count,
        "category_word_count": category_word_count,
        "category_word_frequency": category_word_frequency,
        "vocabulary": vocabulary,
    }


MODEL = build_model(TRAINING_DATA)


def get_training_summary():
    category_summary = []
    for category in sorted(CATEGORY_NAMES):
        document_count = MODEL["category_document_count"][category]
        word_count = MODEL["category_word_count"][category]
        category_summary.append(
            {
                "category": category,
                "name": CATEGORY_NAMES[category],
                "document_count": document_count,
                "word_count": word_count,
            }
        )

    return {
        "document_count": MODEL["document_count"],
        "category_count": len(CATEGORY_NAMES),
        "vocabulary_size": len(MODEL["vocabulary"]),
        "categories": category_summary,
    }


def extract_feature_words(limit=30):
    all_words = Counter()
    for frequency in MODEL["category_word_frequency"].values():
        all_words.update(frequency)
    return sorted(all_words.items(), key=lambda item: (-item[1], item[0]))[:limit]


def extract_category_feature_words(limit=8):
    result = []
    for category in sorted(CATEGORY_NAMES):
        frequency = MODEL["category_word_frequency"][category]
        words = sorted(frequency.items(), key=lambda item: (-item[1], item[0]))[:limit]
        result.append(
            {
                "category": category,
                "name": CATEGORY_NAMES[category],
                "words": words,
            }
        )
    return result


def classify_text(text, model=None):
    model = model or MODEL
    segmented_words = split_words(text)
    filtered_words = split_words(text, remove_stop_words=True)
    words = expand_feature_terms(filtered_words)
    vocabulary_size = max(len(model["vocabulary"]), 1)
    scores = []

    for category in sorted(CATEGORY_NAMES):
        prior = model["category_document_count"][category] / model["document_count"]
        score = math.log(prior)
        total_words = model["category_word_count"][category]
        word_frequency = model["category_word_frequency"][category]

        for word in words:
            word_count = word_frequency.get(word, 0)
            probability = (word_count + 1) / (total_words + vocabulary_size)
            score += math.log(probability)

        scores.append((category, score))

    max_score = max(score for _, score in scores)
    exp_scores = [(category, math.exp(score - max_score)) for category, score in scores]
    total_exp = sum(score for _, score in exp_scores)
    probabilities = [
        {
            "category": category,
            "name": CATEGORY_NAMES[category],
            "probability": score / total_exp,
        }
        for category, score in exp_scores
    ]
    probabilities.sort(key=lambda item: item["probability"], reverse=True)

    best = probabilities[0]
    best_frequency = model["category_word_frequency"][best["category"]]
    matched_words = sorted(set(words) & model["vocabulary"])
    evidence_words = sorted(
        [
            {
                "word": word,
                "count": best_frequency[word],
            }
            for word in matched_words
            if best_frequency.get(word, 0) > 0
        ],
        key=lambda item: (-item["count"], item["word"]),
    )[:10]

    return {
        "category": best["category"],
        "name": best["name"],
        "probability": best["probability"],
        "probabilities": probabilities,
        "segmented_words": segmented_words,
        "filtered_words": filtered_words,
        "words": words,
        "matched_words": matched_words,
        "evidence_words": evidence_words,
    }


def evaluate_training_data():
    categories = sorted(CATEGORY_NAMES)
    confusion = {
        actual: {predicted: 0 for predicted in categories}
        for actual in categories
    }
    results = []
    correct = 0

    for index, (actual_category, text) in enumerate(TRAINING_DATA):
        fold_training_data = TRAINING_DATA[:index] + TRAINING_DATA[index + 1 :]
        fold_model = build_model(fold_training_data)
        prediction = classify_text(text, model=fold_model)
        predicted_category = prediction["category"]
        is_correct = predicted_category == actual_category

        if is_correct:
            correct += 1
        confusion[actual_category][predicted_category] += 1
        results.append(
            {
                "index": index + 1,
                "text": text,
                "actual_category": actual_category,
                "actual_name": CATEGORY_NAMES[actual_category],
                "predicted_category": predicted_category,
                "predicted_name": CATEGORY_NAMES[predicted_category],
                "probability": prediction["probability"],
                "is_correct": is_correct,
            }
        )

    total = len(TRAINING_DATA)
    category_scores = []
    for category in categories:
        true_positive = confusion[category][category]
        predicted_total = sum(confusion[actual][category] for actual in categories)
        actual_total = sum(confusion[category].values())
        precision = true_positive / predicted_total if predicted_total else 0
        recall = true_positive / actual_total if actual_total else 0
        category_scores.append(
            {
                "category": category,
                "name": CATEGORY_NAMES[category],
                "precision": precision,
                "recall": recall,
                "correct": true_positive,
                "total": actual_total,
            }
        )

    return {
        "method": "Leave-one-out",
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "accuracy": correct / total if total else 0,
        "categories": [
            {"category": category, "name": CATEGORY_NAMES[category]}
            for category in categories
        ],
        "confusion": confusion,
        "category_scores": category_scores,
        "results": results,
    }
