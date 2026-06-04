import re
from collections import Counter
from typing import Any

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

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_phrase_dictionary(phrases: set[str]) -> tuple[set[tuple[str, ...]], int]:
    phrase_words: set[tuple[str, ...]] = set()
    max_length = 1

    for phrase in phrases:
        words = tuple(normalize_text(phrase).split())
        if len(words) > 1:
            phrase_words.add(words)
            max_length = max(max_length, len(words))

    return phrase_words, max_length


PHRASE_DICTIONARY, MAX_PHRASE_LENGTH = build_phrase_dictionary(SEMANTIC_PHRASES)


def get_categories() -> list[str]:
    return sorted(CATEGORY_NAMES)


def sort_word_counts(
    word_counts: Counter[str],
    limit: int | None = None,
) -> list[tuple[str, int]]:
    sorted_items = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_items[:limit] if limit else sorted_items


def find_longest_phrase(words: list[str], start_index: int) -> tuple[str, ...] | None:
    remaining = len(words) - start_index
    max_length = min(MAX_PHRASE_LENGTH, remaining)

    for length in range(max_length, 1, -1):
        candidate = tuple(words[start_index : start_index + length])
        if candidate in PHRASE_DICTIONARY:
            return candidate

    return None


def maximum_matching_segment(words: list[str]) -> list[str]:
    segmented: list[str] = []
    index = 0

    while index < len(words):
        phrase = find_longest_phrase(words, index)
        if phrase is None:
            segmented.append(words[index])
            index += 1
            continue

        segmented.append(" ".join(phrase))
        index += len(phrase)

    return segmented


def split_words(text: str, remove_stop_words: bool = False) -> list[str]:
    words = maximum_matching_segment(normalize_text(text).split())
    if remove_stop_words:
        words = [word for word in words if word not in STOP_WORDS]
    return words


def expand_feature_terms(words: list[str]) -> list[str]:
    expanded: list[str] = []
    seen: set[str] = set()

    def add_term(term: str) -> None:
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


def extract_model_words(text: str) -> list[str]:
    words = split_words(text, remove_stop_words=True)
    return expand_feature_terms(words)


def count_words(text: str) -> int:
    return len(split_words(text))


def count_word_frequency(text: str, remove_stop_words: bool = False) -> Counter[str]:
    return Counter(split_words(text, remove_stop_words=remove_stop_words))


def analyze_text(text: str) -> dict[str, Any]:
    frequency = count_word_frequency(text)

    return {
        "original": text,
        "normalized": normalize_text(text),
        "character_count": len(text),
        "word_count": count_words(text),
        "unique_word_count": len(frequency),
        "frequency": sort_word_counts(frequency),
    }


def build_model(training_data: list[tuple[str, str]]) -> dict[str, Any]:
    category_document_count = Counter()
    category_word_count = Counter()
    category_word_frequency = {}
    vocabulary = set()

    for category, text in training_data:
        category_document_count[category] += 1
        words = extract_model_words(text)
        vocabulary.update(words)
        category_word_frequency.setdefault(category, Counter()).update(words)
        category_word_count[category] += len(words)

    return {
        "document_count": len(training_data),
        "category_document_count": category_document_count,
        "category_word_count": category_word_count,
        "category_word_frequency": category_word_frequency,
        "vocabulary": vocabulary,
    }


MODEL = build_model(TRAINING_DATA)


def get_training_summary() -> dict[str, Any]:
    category_summary: list[dict[str, Any]] = []
    for category in get_categories():
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


def extract_feature_words(limit: int = 30) -> list[tuple[str, int]]:
    all_words = Counter()
    for frequency in MODEL["category_word_frequency"].values():
        all_words.update(frequency)
    return sort_word_counts(all_words, limit)


def extract_category_feature_words(limit: int = 8) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for category in get_categories():
        frequency = MODEL["category_word_frequency"][category]
        words = sort_word_counts(frequency, limit)
        result.append(
            {
                "category": category,
                "name": CATEGORY_NAMES[category],
                "words": words,
            }
        )
    return result


def calculate_category_score(
    category: str,
    words: list[str],
    model: dict[str, Any],
) -> float:
    prior = model["category_document_count"][category] / model["document_count"]
    score = prior
    total_words = model["category_word_count"][category]
    word_frequency = model["category_word_frequency"][category]
    vocabulary_size = max(len(model["vocabulary"]), 1)

    for word in words:
        word_count = word_frequency.get(word, 0)
        probability = (word_count + 1) / (total_words + vocabulary_size)
        score *= probability

    return score


def build_probabilities(scores: list[tuple[str, float]]) -> list[dict[str, Any]]:
    total_score = sum(score for _, score in scores)
    probabilities = []

    for category, score in scores:
        probability = score / total_score if total_score else 0
        probabilities.append(
            {
                "category": category,
                "name": CATEGORY_NAMES[category],
                "probability": probability,
            }
        )

    probabilities.sort(key=lambda item: item["probability"], reverse=True)
    return probabilities


def get_evidence_words(
    words: list[str],
    predicted_category: str,
    model: dict[str, Any],
    limit: int = 10,
) -> list[dict[str, Any]]:
    word_frequency = model["category_word_frequency"][predicted_category]
    matched_words = sorted(set(words) & model["vocabulary"])
    evidence_words = []

    for word in matched_words:
        count = word_frequency.get(word, 0)
        if count > 0:
            evidence_words.append({"word": word, "count": count})

    evidence_words.sort(key=lambda item: (-item["count"], item["word"]))
    return evidence_words[:limit]


def build_prediction_comment(
    predicted_name: str,
    probability: float,
    evidence_words: list[dict[str, Any]],
) -> str:
    if probability >= 0.8:
        confidence_text = "độ tin cậy cao"
    elif probability >= 0.5:
        confidence_text = "độ tin cậy trung bình"
    else:
        confidence_text = "độ tin cậy thấp"

    if evidence_words:
        evidence_text = ", ".join(item["word"] for item in evidence_words[:3])
        return (
            f"Văn bản được xếp vào nhóm {predicted_name} với {confidence_text}, "
            f"do có các từ/cụm nổi bật: {evidence_text}."
        )

    return (
        f"Văn bản được xếp vào nhóm {predicted_name} với {confidence_text}, "
        "nhưng có ít từ/cụm trùng với tập dữ liệu mẫu."
    )


def classify_text(text: str, model: dict[str, Any] | None = None) -> dict[str, Any]:
    model = model or MODEL
    segmented_words = split_words(text)
    filtered_words = split_words(text, remove_stop_words=True)
    words = expand_feature_terms(filtered_words)
    scores = []

    for category in get_categories():
        score = calculate_category_score(category, words, model)
        scores.append((category, score))

    probabilities = build_probabilities(scores)
    best = probabilities[0]
    matched_words = sorted(set(words) & model["vocabulary"])
    evidence_words = get_evidence_words(words, best["category"], model)

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
        "comment": build_prediction_comment(
            best["name"],
            best["probability"],
            evidence_words,
        ),
    }


def create_confusion_matrix(categories: list[str]) -> dict[str, dict[str, int]]:
    confusion: dict[str, dict[str, int]] = {}

    for actual_category in categories:
        confusion[actual_category] = {}
        for predicted_category in categories:
            confusion[actual_category][predicted_category] = 0

    return confusion


def calculate_category_scores(
    confusion: dict[str, dict[str, int]],
    categories: list[str],
) -> list[dict[str, Any]]:
    category_scores: list[dict[str, Any]] = []

    for category in categories:
        correct_count = confusion[category][category]
        actual_total = sum(confusion[category].values())
        predicted_total = 0

        for actual_category in categories:
            predicted_total += confusion[actual_category][category]

        precision = correct_count / predicted_total if predicted_total else 0
        recall = correct_count / actual_total if actual_total else 0
        category_scores.append(
            {
                "category": category,
                "name": CATEGORY_NAMES[category],
                "precision": precision,
                "recall": recall,
                "correct": correct_count,
                "total": actual_total,
            }
        )

    return category_scores


def evaluate_training_data() -> dict[str, Any]:
    categories = get_categories()
    confusion = create_confusion_matrix(categories)
    results = []
    correct = 0

    for index, (actual_category, text) in enumerate(TRAINING_DATA):
        training_without_current_text = TRAINING_DATA[:index] + TRAINING_DATA[index + 1 :]
        model = build_model(training_without_current_text)
        prediction = classify_text(text, model=model)
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
        "category_scores": calculate_category_scores(confusion, categories),
        "results": results,
    }
