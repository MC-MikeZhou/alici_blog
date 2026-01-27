#!/usr/bin/env python3
"""
DataForSEO Keyword Comparison Script
Compares keyword metrics for two articles
"""

import urllib.request
import urllib.error
import json
import sys
from typing import List, Dict, Any
from base64 import b64encode
from datetime import datetime

class DataForSEOClient:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.base_url = "https://api.dataforseo.com/v3"
        credentials = f"{username}:{password}"
        self.auth_header = b64encode(credentials.encode()).decode()

    def _make_request(self, endpoint: str, payload: List[Dict]) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Basic {self.auth_header}",
            "Content-Type": "application/json"
        }
        data = json.dumps(payload).encode('utf-8')
        request = urllib.request.Request(url, data=data, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"HTTP {e.code}: {error_body}")

    def get_keywords_data(self, keywords: List[str], location_code: int = 2840, language_code: str = "en") -> Dict:
        payload = [{
            "keywords": keywords,
            "location_code": location_code,
            "language_code": language_code,
            "search_partners": False
        }]
        return self._make_request("keywords_data/google_ads/search_volume/live", payload)


def extract_keyword_metrics(api_response: Dict) -> List[Dict]:
    results = []
    if api_response.get("status_code") != 20000:
        raise Exception(f"API Error: {api_response.get('status_message')}")

    tasks = api_response.get("tasks", [])
    for task in tasks:
        if task.get("status_code") != 20000:
            continue
        result = task.get("result", [])
        if not result:
            continue
        for item in result:
            keyword = item.get("keyword")
            search_volume = item.get("search_volume", 0)
            competition = item.get("competition", 0)
            cpc = item.get("cpc", 0)
            competition_level = item.get("competition_level", "")
            monthly_searches = item.get("monthly_searches", [])

            # Calculate trend
            trend = "→"
            if monthly_searches and len(monthly_searches) >= 3:
                recent = sum([m.get("search_volume", 0) for m in monthly_searches[:3]]) / 3
                older = sum([m.get("search_volume", 0) for m in monthly_searches[-3:]]) / 3
                if older > 0:
                    change = (recent - older) / older
                    if change > 0.1:
                        trend = "↑"
                    elif change < -0.1:
                        trend = "↓"

            results.append({
                "keyword": keyword,
                "search_volume": search_volume or 0,
                "competition_index": competition or 0,
                "competition_level": competition_level or "N/A",
                "cpc": cpc or 0,
                "trend": trend,
                "monthly_searches": monthly_searches
            })
    return results


def generate_markdown_report(article_a_metrics: List[Dict], article_b_metrics: List[Dict]) -> str:
    report = f"""# 关键词搜索量对比验证报告

> **生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
> **数据来源**: DataForSEO Keywords Data API
> **地区**: United States (2840)
> **语言**: English

---

## 一、文章 A: Best AI Video Generators

| 关键词 | 月搜索量 | CPC | 竞争度 | 趋势 |
|--------|----------|-----|--------|------|
"""

    total_vol_a = 0
    avg_cpc_a = []
    for m in sorted(article_a_metrics, key=lambda x: x['search_volume'], reverse=True):
        vol = m['search_volume']
        cpc = m['cpc']
        comp = m['competition_level']
        trend = m['trend']
        total_vol_a += vol
        if cpc > 0:
            avg_cpc_a.append(cpc)
        report += f"| {m['keyword']} | {vol:,} | ${cpc:.2f} | {comp} | {trend} |\n"

    report += f"""
**汇总统计**:
- 总搜索量: **{total_vol_a:,}** /月
- 平均 CPC: **${sum(avg_cpc_a)/len(avg_cpc_a) if avg_cpc_a else 0:.2f}**
- 关键词数: {len(article_a_metrics)}

---

## 二、文章 B: Kling Motion Control

| 关键词 | 月搜索量 | CPC | 竞争度 | 趋势 |
|--------|----------|-----|--------|------|
"""

    total_vol_b = 0
    avg_cpc_b = []
    for m in sorted(article_b_metrics, key=lambda x: x['search_volume'], reverse=True):
        vol = m['search_volume']
        cpc = m['cpc']
        comp = m['competition_level']
        trend = m['trend']
        total_vol_b += vol
        if cpc > 0:
            avg_cpc_b.append(cpc)
        report += f"| {m['keyword']} | {vol:,} | ${cpc:.2f} | {comp} | {trend} |\n"

    report += f"""
**汇总统计**:
- 总搜索量: **{total_vol_b:,}** /月
- 平均 CPC: **${sum(avg_cpc_b)/len(avg_cpc_b) if avg_cpc_b else 0:.2f}**
- 关键词数: {len(article_b_metrics)}

---

## 三、对比分析

| 指标 | 文章 A (AI Video Generators) | 文章 B (Kling Motion Control) | 差异倍数 |
|------|------------------------------|-------------------------------|----------|
| 总搜索量 | {total_vol_a:,} | {total_vol_b:,} | {total_vol_a/total_vol_b if total_vol_b > 0 else 'N/A'}x |
| 平均 CPC | ${sum(avg_cpc_a)/len(avg_cpc_a) if avg_cpc_a else 0:.2f} | ${sum(avg_cpc_b)/len(avg_cpc_b) if avg_cpc_b else 0:.2f} | {(sum(avg_cpc_a)/len(avg_cpc_a))/(sum(avg_cpc_b)/len(avg_cpc_b)) if avg_cpc_b and sum(avg_cpc_b) > 0 else 'N/A'}x |

---

## 四、结论与建议

### 1. 目标市场规模
"""

    if total_vol_a > total_vol_b:
        ratio = total_vol_a / total_vol_b if total_vol_b > 0 else float('inf')
        report += f"- **文章 A** 的目标市场更大，搜索量是文章 B 的 **{ratio:.1f}x**\n"
        report += f"- \"Best AI Video Generators\" 是更广泛的需求，覆盖更大受众\n"
    else:
        report += f"- **文章 B** 的目标市场更大\n"

    report += """
### 2. 商业价值 (CPC)
"""

    avg_a = sum(avg_cpc_a)/len(avg_cpc_a) if avg_cpc_a else 0
    avg_b = sum(avg_cpc_b)/len(avg_cpc_b) if avg_cpc_b else 0

    if avg_a > avg_b:
        report += f"- **文章 A** 的商业价值更高，平均 CPC ${avg_a:.2f} vs ${avg_b:.2f}\n"
        report += f"- 广告主愿意为 \"AI Video Generator\" 类关键词支付更高价格\n"
    elif avg_b > avg_a:
        report += f"- **文章 B** 的商业价值更高，平均 CPC ${avg_b:.2f} vs ${avg_a:.2f}\n"
    else:
        report += f"- 两篇文章的商业价值相近\n"

    report += """
### 3. 竞争难度
"""

    # Find high competition keywords
    high_comp_a = [m for m in article_a_metrics if m['competition_level'] == 'HIGH']
    high_comp_b = [m for m in article_b_metrics if m['competition_level'] == 'HIGH']

    report += f"- 文章 A 有 {len(high_comp_a)}/{len(article_a_metrics)} 个高竞争关键词\n"
    report += f"- 文章 B 有 {len(high_comp_b)}/{len(article_b_metrics)} 个高竞争关键词\n"

    if len(high_comp_a) > len(high_comp_b):
        report += f"- **文章 B** 的关键词竞争相对较低，更容易获得排名\n"
    elif len(high_comp_b) > len(high_comp_a):
        report += f"- **文章 A** 的关键词竞争相对较低，更容易获得排名\n"

    report += """
### 4. 综合建议

"""

    if total_vol_a > total_vol_b * 3:
        report += """✅ **优先发布文章 A (Best AI Video Generators)**

理由:
1. 搜索量显著更高，潜在流量更大
2. 商业价值更高 (CPC)
3. 属于 \"Best\" 榜单类内容，用户购买意图明确
4. 可覆盖多个工具的长尾搜索

⚠️ **文章 B (Kling Motion Control) 定位建议**:
- 作为垂直深度内容，吸引 Kling 用户
- 可作为文章 A 的内部链接目标
- 适合已有 Kling 产品线时的支撑内容
"""
    else:
        report += """建议根据具体业务目标选择优先级。
"""

    report += f"""
---

## 五、验证标准检查

| 指标 | 阈值 | 文章 A | 文章 B |
|------|------|--------|--------|
| 搜索量 | ≥ 1,000 | {"✅ PASS" if total_vol_a >= 1000 else "❌ FAIL"} | {"✅ PASS" if total_vol_b >= 1000 else "❌ FAIL"} |
| CPC | ≥ $1.00 | {"✅ PASS" if avg_a >= 1.0 else "❌ FAIL"} | {"✅ PASS" if avg_b >= 1.0 else "❌ FAIL"} |
| 竞争度 | < 0.8 | 见详情 | 见详情 |

---

## 六、API 成本

| 项目 | 数量 | 单价 | 小计 |
|------|------|------|------|
| Keywords Data | 1 请求 (13 关键词) | ~$0.015/词 | ~$0.20 |

**总计**: ~$0.20

---

*报告生成: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    return report


def main():
    # DataForSEO credentials
    USERNAME = "hans.h@hey.com"
    PASSWORD = "727be1453f7a4f3a"

    # Keywords for Article A: Best AI Video Generators
    keywords_a = [
        "best ai video generators",
        "best ai video generators 2026",
        "ai video generator comparison",
        "sora vs runway vs kling",
        "ai video tools",
        "top ai video makers",
        "free ai video generator"
    ]

    # Keywords for Article B: Kling Motion Control
    keywords_b = [
        "kling motion control",
        "kling ai tutorial",
        "kling motion control guide",
        "how to use kling motion control",
        "kling ai guide 2026",
        "kling video generation"
    ]

    all_keywords = keywords_a + keywords_b

    client = DataForSEOClient(USERNAME, PASSWORD)

    print("=" * 70)
    print("DataForSEO Keyword Comparison - Article A vs Article B")
    print("=" * 70)
    print()

    print(f"Fetching data for {len(all_keywords)} keywords...")
    print()

    try:
        response = client.get_keywords_data(all_keywords)
        all_metrics = extract_keyword_metrics(response)

        # Split metrics by article
        keywords_a_set = set(keywords_a)
        keywords_b_set = set(keywords_b)

        article_a_metrics = [m for m in all_metrics if m['keyword'] in keywords_a_set]
        article_b_metrics = [m for m in all_metrics if m['keyword'] in keywords_b_set]

        print(f"✓ Article A: {len(article_a_metrics)} keywords")
        print(f"✓ Article B: {len(article_b_metrics)} keywords")
        print()

        # Display quick summary
        print("=" * 70)
        print("Quick Summary")
        print("=" * 70)
        print()

        print("Article A - Best AI Video Generators:")
        print("-" * 50)
        for m in sorted(article_a_metrics, key=lambda x: x['search_volume'], reverse=True):
            print(f"  {m['keyword']:<35} {m['search_volume']:>8,} vol  ${m['cpc']:>5.2f} CPC  {m['trend']}")
        print()

        print("Article B - Kling Motion Control:")
        print("-" * 50)
        for m in sorted(article_b_metrics, key=lambda x: x['search_volume'], reverse=True):
            print(f"  {m['keyword']:<35} {m['search_volume']:>8,} vol  ${m['cpc']:>5.2f} CPC  {m['trend']}")
        print()

        # Generate markdown report
        report = generate_markdown_report(article_a_metrics, article_b_metrics)

        # Save report
        output_file = "/Users/H/Documents/AliciBlog/reports/2026-01-23-best-ai-video-generators/09-keyword-comparison.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print("=" * 70)
        print(f"✓ Report saved to: {output_file}")
        print("=" * 70)

        # Also save raw JSON
        json_output = {
            "generated_at": datetime.now().isoformat(),
            "article_a": {
                "title": "5 Best AI Video Generators in 2026",
                "keywords": article_a_metrics
            },
            "article_b": {
                "title": "Kling Motion Control Complete Guide",
                "keywords": article_b_metrics
            }
        }

        json_file = "/Users/H/Documents/AliciBlog/reports/2026-01-23-best-ai-video-generators/09-keyword-comparison.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=2)

        print(f"✓ JSON data saved to: {json_file}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
