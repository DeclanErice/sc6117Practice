import requests
import json
from urllib.parse import urlparse
from datetime import datetime  

# 有些山寨币拿不到的
def get_crypto_news(currency='ETH'):
    # 这是我自己的key
    api_token = "03f3e3a74337d90e75c6cba043464a5af95a4f79" 
    
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={api_token}&currencies={currency}&filter=rising"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # 检查请求是否成功
        data = response.json()
        
        results = data.get('results', [])

        # 打出来结果看看
        if results:
            print(f"成功获取到 {len(results)} 条新闻。以下是第一条数据的完整结构：\n")
            # json.dumps 用于将字典转换为字符串，indent=4 表示缩进4格，ensure_ascii=False 防止中文乱码
            print(json.dumps(results[0], indent=4, ensure_ascii=False))
        else:
            print("API 返回了响应，但在 results 中没有找到新闻。可能没有符合条件的数据。")
            
        return results

    except Exception as e:
        print(f"请求出错: {e}")
        return []
def _safe_str(x):
    """避免 None 造成后续出错，统一转成字符串。"""
    if x is None:
        return ""
    return str(x).strip()

def _extract_source_domain(url: str) -> str:
    if not url:
        return ""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return ""

def preprocess_news(raw_items):
    """
    将 Cryptopanic 返回的原始新闻列表标准化为统一 JSON 结构。
    :param raw_items: list[dict] from get_crypto_news
    :return: list[dict] cleaned_items
    """
    cleaned_items = []

    for item in raw_items:
        # 1. 基础字段
        news_id = item.get("id")
        title = _safe_str(item.get("title"))
        url = _safe_str(item.get("url"))
        source_info = item.get("source") or {}
        source_name = _safe_str(source_info.get("title") or source_info.get("name"))
        published_at = _safe_str(item.get("published_at"))
        created_at = _safe_str(item.get("created_at"))

        # 2. 正文内容（如果没有，先用标题代替）
        body = _safe_str(item.get("body") or item.get("description") or title)

        # 3. 符号/币种列表
        currencies = item.get("currencies") or []
        symbols = []
        for c in currencies:
            code = c.get("code")
            if code:
                symbols.append(str(code).upper())

        # 4. 语言（如果有）
        language = item.get("language") or item.get("lang") or None
        if language is not None:
            language = str(language).lower()

        # 5. 是否热点/重要（Cryptopanic 有 is_hot, is_pinned 等字段时）
        is_hot = bool(item.get("hot") or item.get("is_hot") or False)

        # 6. 构建标准化 JSON
        cleaned = {
            "id": news_id,
            "title": title,
            "body": body,
            "url": url,
            "source": source_name,
            "source_domain": _extract_source_domain(url),
            "published_at": published_at,  # 后续可再转换为 datetime
            "created_at": created_at,
            "symbols": symbols,
            "currencies_raw": currencies,  # 原始列表，用于 debug，可选
            "language": language,
            "is_hot": is_hot,
            # 原始数据备份，可选：也可以不存，避免文件体积太大
            # "raw": item
        }

        cleaned_items.append(cleaned)

    return cleaned_items


if __name__ == "__main__":
    raw_results = get_crypto_news(currency="ETH")
    cleaned_news = preprocess_news(raw_results)

    # 示例：打印前两条清洗后结果
    print("\n=== 预处理后的前两条新闻示例 ===")
    for n in cleaned_news[:2]:
        print(json.dumps(n, ensure_ascii=False, indent=2))

    # 可选：保存为 ndjson 文件，供后续分析/训练使用
    # 在文件名中加入生成日期，格式如 crypto_news_ETH_2025-11-26.ndjson
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    output_path = f"crypto_news_ETH_{today_str}.ndjson"
    with open(output_path, "w", encoding="utf-8") as f:
        for rec in cleaned_news:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"\n标准化后的新闻已保存到: {output_path} (生成日期: {today_str})")