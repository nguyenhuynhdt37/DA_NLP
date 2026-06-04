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
    "hỏi",
    "không",
    "là",
    "lại",
    "làm",
    "mình",
    "mới",
    "một",
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

# Tu dien chi nen gom cac don vi co nghia, tranh gom ca menh de/cau dai.
SEMANTIC_PHRASES = {
    "24 inch",
    "âm thanh",
    "bài đăng",
    "bài hát",
    "bài học",
    "bài giảng",
    "bài nhạc",
    "bài thực hành",
    "bài thuyết trình",
    "bài tập",
    "bạn bè",
    "bàn phím",
    "bàn phím cơ",
    "balo laptop",
    "bảo hành",
    "bắt đầu",
    "bộ phim",
    "bóng đá",
    "bị khóa",
    "ca nhạc",
    "cà phê",
    "cài đặt",
    "cách sửa",
    "chắc chắn",
    "chia sẻ",
    "chơi game",
    "chương trình",
    "chương trình hài",
    "cosplay",
    "cơ bản",
    "cơ sở dữ liệu",
    "cuối tuần",
    "cũ giá rẻ",
    "cấu hình ổn",
    "dễ hiểu",
    "dell cũ",
    "đăng nhập",
    "đăng ký",
    "đề cương",
    "đề xuất",
    "địa chỉ",
    "điện thoại",
    "điện thoại cũ",
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
    "giáo trình",
    "giấy xác nhận",
    "giấy xác nhận sinh viên",
    "gõ được",
    "gửi được",
    "giờ học",
    "giờ làm",
    "hà nội",
    "hài nhẹ nhàng",
    "học mỗi ngày",
    "học python",
    "học tập",
    "học tiếng anh",
    "khá hay",
    "khá vui",
    "kết nối wifi",
    "khóa học",
    "khôi phục",
    "khôi phục bài viết",
    "khu vực gần trường",
    "kinh nghiệm",
    "laptop cũ",
    "lập đội",
    "lập đội chơi",
    "lập trình",
    "lập trình python",
    "lập trình web",
    "lệnh in",
    "lỗi màn hình xanh",
    "lỗi đăng nhập",
    "lỗi khi chạy",
    "lời giải",
    "mạng máy tính",
    "màn hình",
    "màn hình máy tính",
    "màn hình xanh",
    "mất kết nối wifi",
    "mật khẩu",
    "máy tính",
    "máy tính cũ",
    "môi trường lập trình",
    "môi trường",
    "miễn phí",
    "mới ra rạp",
    "mới dùng vài lần",
    "mua bán",
    "nhận sạc",
    "nhận lệnh in",
    "nhẹ nhàng",
    "nhạc sống",
    "ngôn ngữ",
    "ngôn ngữ tự nhiên",
    "người mới",
    "nguyên nhân",
    "nội dung",
    "ôn tập",
    "ôn tập lý thuyết",
    "ôn thi",
    "pin còn khỏe",
    "phân loại",
    "phân loại nội dung",
    "phím cơ",
    "phim hài",
    "phim hay",
    "phim mới",
    "qua sử dụng",
    "quán cà phê",
    "rất vui",
    "sách lập trình",
    "sau giờ học",
    "sau giờ làm",
    "sinh viên",
    "sự kiện cosplay",
    "tài khoản",
    "tài liệu",
    "tai nghe",
    "tai nghe bluetooth",
    "thanh lý",
    "thanh lý tai nghe",
    "thao tác",
    "thủ tục",
    "thương mại",
    "thuyết trình",
    "thú vị",
    "tiếng anh",
    "tối nay",
    "trình duyệt",
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
    "windows",
    "xác nhận sinh viên",
    "xác suất",
    "xanh windows",
    "xem phim",
    "xem phim hài",
    "xử lý",
    "xử lý ngôn ngữ tự nhiên",
    "xử lý văn bản",
    "xóa nhầm",
    "âm nhạc miễn phí",
    "bài tập thuật toán",
    "bàn học gỗ",
    "bàn phím không dây",
    "bảo mật",
    "bộ phim kinh dị",
    "chứng chỉ bảo mật",
    "chứng chỉ",
    "diễn đàn",
    "diễn đàn bị khóa",
    "dung lượng cao",
    "dưới năm triệu",
    "dễ đọc",
    "dễ hiểu",
    "đồ án python",
    "đổi tên hiển thị",
    "giá dưới năm triệu",
    "giá hợp lý",
    "giải bóng đá sinh viên",
    "hệ thống học tập",
    "hệ thống",
    "học máy",
    "học online",
    "hướng đối tượng",
    "không gian đẹp",
    "không gửi được email",
    "không dây",
    "kinh dị",
    "liên quân",
    "loa bluetooth",
    "máy chiếu",
    "máy in",
    "máy in cũ",
    "máy tính bảng",
    "mật khẩu wifi",
    "mã xác nhận",
    "mất kết nối",
    "mở lại",
    "mở được",
    "naive bayes",
    "ngoại hình đẹp",
    "nhạc nhẹ",
    "nhạc thư giãn",
    "nhóm học chung",
    "nâng cao",
    "nhanh hết pin",
    "ổ cứng di động",
    "phân loại văn bản",
    "phim hoạt hình",
    "pin ảo",
    "pin ổn",
    "phòng trọ sinh viên",
    "phòng trọ",
    "sách thuật toán",
    "sắp xếp",
    "sự kiện âm nhạc",
    "sự kiện",
    "âm nhạc",
    "tập huấn luyện",
    "thuật toán",
    "thuật toán sắp xếp",
    "thứ bảy",
    "tiếng việt",
    "tìm kiếm",
    "tải được",
    "trà sữa",
    "truyện tranh",
    "truyện tranh hài",
    "tuần này",
    "từ đâu",
    "văn phòng",
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

PROTECTED_PHRASES = {
    "24 inch",
    "cơ sở dữ liệu",
    "giải bóng đá sinh viên",
    "giấy xác nhận sinh viên",
    "mạng máy tính",
    "màn hình máy tính",
    "ngôn ngữ tự nhiên",
    "ổ cứng di động",
    "trí tuệ nhân tạo",
    "trung tâm thương mại",
    "xử lý ngôn ngữ tự nhiên",
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


def is_semantic_unit(words):
    term = " ".join(words)
    return (
        term in STOP_WORDS
        or term in ATOMIC_TERMS
        or tuple(words) in PHRASE_DICTIONARY
    )


def split_into_smaller_units(words):
    phrase = " ".join(words)
    if len(words) <= 2 or phrase in PROTECTED_PHRASES:
        return None

    result = []
    index = 0

    while index < len(words):
        matched = None
        max_length = min(len(words) - index, len(words) - 1)

        for length in range(max_length, 0, -1):
            candidate = words[index : index + length]
            candidate_text = " ".join(candidate)
            if candidate_text == phrase:
                continue
            if is_semantic_unit(candidate):
                matched = candidate_text
                break

        if matched is None:
            return None

        result.append(matched)
        index += len(matched.split())

    return result if len(result) > 1 else None


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
            smaller_units = split_into_smaller_units(list(matched))
            if smaller_units is None:
                segmented.append(" ".join(matched))
            else:
                segmented.extend(smaller_units)
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
        score = prior
        total_words = model["category_word_count"][category]
        word_frequency = model["category_word_frequency"][category]

        for word in words:
            word_count = word_frequency.get(word, 0)
            probability = (word_count + 1) / (total_words + vocabulary_size)
            score *= probability

        scores.append((category, score))

    total_score = sum(score for _, score in scores)
    probabilities = [
        {
            "category": category,
            "name": CATEGORY_NAMES[category],
            "probability": score / total_score if total_score else 0,
        }
        for category, score in scores
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
