import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查一下 CSS 中还有哪些冲突的权重导致没生效。我们把媒体查询里的所有内容加上 !important 确保压制外部样式。
old_btn = """    /* 修正输入框和选择框在卡片里的样式 */
    td input, td select {
      text-align: right;
      width: 100%;
      background: #f8fafc;
      border-color: #e2e8f0;
    }"""
    
new_btn = """    /* 修正输入框和选择框在卡片里的样式 */
    td input, td select {
      text-align: right !important;
      width: 100% !important;
      background: #f8fafc !important;
      border-color: #e2e8f0 !important;
      margin: 0 !important;
    }"""
content = content.replace(old_btn, new_btn)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Repair 2 completed.")
