# 09 Human Review Checklist — v1.1.1

输入：`01-article-draft-3.md`  
输出：`01-article-draft-4.md`  
日期：2026-02-03

## Step 0: Reader Persona（读者画像）
- **Who**：AI image 爱好者、设计/营销/产品团队，需要做海报/广告/信息图/产品页视觉
- **Pain**：图片内文字不可读、一致性差、同一套素材批量产出困难
- **Search**：nano banana pro is here / nano banana pro vs nano banana / text in image / consistent character
- **Goal**：快速知道怎么选（Nano vs Pro）+ 立刻能用的工作流与 prompt
- **Language**：中文为主，允许少量必要英文术语（prompt、UI）

## Module 1: Title CTR Check
- **Current Title**：Nano Banana Pro is Here (2026)：全功能解读 + 实战用法指南（Alici AI 上线）
- **CTR Score（估算）**：78/100 ⚠️ WARNING
  - ✅ 年份：2026
  - ✅ Power Word/承诺：全功能解读、实战、指南
  - ❌ 数字：标题未显式包含数字（正文已包含“30 秒选型/1 分钟体验”）
- **处理**：不强行改标题（用户已选定口吻），保留。

## Module 2: Title-Reader Alignment
- ✅ 搜索语义匹配（is here / guide / 上线 / 用法）
- ✅ 关键词包含 Nano Banana Pro
- ⚠️ 读者可能也会搜 “vs”，但标题已在正文强化对比表与“30 秒选型”，可接受

## Module 3: Competitor Mention Scan（⛔ BLOCKING 检查）
- 检测到竞品/来源提及：Higgsfield、InVideo
- ✅ 语气为“来源/参考资料”，未出现“推荐你去用 X”
- ✅ 无竞品 CTA（CTA 指向 alici.ai）
- ✅ 竞品链接仅用于 Source Attribution（信息来源）
- 结论：PASS

## Module 4: Internal Link Audit
- ✅ 添加 1 条内链：AI Image 支柱页 `https://alici.ai/blog/ai-image-guide`
- ✅ 锚文本自然，不是裸链接（已优化为 markdown link）

## Module 5: H2 AEO Citable Check
- ✅ 关键 H2 可被引用：上新变化、对比表、工作流、FAQ
- ⚠️ 可改进：后续若要更强可引用性，可把“对比表”前增加 1 段“结论摘要（3 行）”

## Module 6: Promise-Delivery Check（Feedback 类）
- 承诺：Full Review + Guide（解读 + 选型 + 工作流 + prompts）
- ✅ 已交付：4 个升级点、对比表、2 套工作流、3 个 prompts、FAQ、来源与披露

## Module 7: TL;DR Value Statement
- ✅ Key Takeaways + Direct Answer 已满足

## Module 8: Brand Voice Check
- ✅ 语气偏“工作流与方法论”，无夸大承诺
- ✅ Disclosure 存在，降低信任风险

## Module 9: Reader Persona Check
- ✅ 术语总体可读；“prompt/UI”在目标人群可接受
- ✅ 场景落点是 AI image（海报/广告/信息图/UI mock），未导流到 Thumbnail 产品线

## Module 10: Internal Language Leak（⛔ BLOCKING）
- ✅ 已修复：删除/替换了内部流程提示（如 “Step 11” 等），并移除“数据钩子”等写作框架术语
- 结论：PASS

## Auto-Fixes Applied（本轮改动）
- Hero 图注释：`![Cover image placeholder — will be replaced in Step 11]` → `![Cover image]`
- 术语清理：将“数据钩子/brief”等内部/不必要表达改为读者语言（“规格差别/同一个 prompt”）
- 竞品链接收敛：不在开头重复放竞品链接，仅保留 Source Attribution

