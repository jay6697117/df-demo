import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 替换小屏幕（<768px）和（<480px）下的表格展现形式为纯响应式多行卡片 (Table-to-Cards)
old_media = """    /* 中等屏幕：取消区域列和部分列的冻结，仅保留门店名称和锁定框 */
    .main-table th:nth-child(3), .main-table td:nth-child(3){
      position: static;
      box-shadow: none;
    }
  }

  @media (max-width: 480px) {
    .year-stats {
      grid-template-columns: 1fr;
    }
    .month-stat-grid {
      grid-template-columns: repeat(2, 1fr);
    }
    .cards {
      grid-template-columns: 1fr;
    }
    .toolbar button, .toolbar select {
      flex: 1 1 100%; /* 极小屏幕下完全单列排布 */
    }
    
    /* 极小屏幕：取消所有除 Checkbox 外的冻结列，保证有足够空间浏览核心数据 */
    .main-table th:nth-child(2), .main-table td:nth-child(2){
      position: static;
      box-shadow: none;
    }
  }"""

new_media = """    /* 【史诗级大重构】：在手机端将 <table> 断开，化身为直观的多行卡片列表 */
    table, thead, tbody, th, td, tr { 
      display: block; 
    }
    
    /* 隐藏表头，但不要用 display:none 以兼顾访问性 */
    thead tr { 
      position: absolute;
      top: -9999px;
      left: -9999px;
    }
    
    /* 每一行 TR 变成一个带阴影和圆角的卡片 */
    tr {
      background: #ffffff !important;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      margin-bottom: 16px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.05);
      padding: 12px;
    }
    
    /* TD 变成卡片里的每一行小属性 */
    td { 
      border: none;
      border-bottom: 1px solid #f1f5f9; 
      position: relative;
      padding: 10px 0 10px 40%; 
      text-align: right;
      min-height: 48px;
    }
    td:last-child {
      border-bottom: none;
    }
    
    /* 清除之前 PC 端的固定定位 */
    .main-table th:nth-child(1), .main-table td:nth-child(1),
    .main-table th:nth-child(2), .main-table td:nth-child(2),
    .main-table th:nth-child(3), .main-table td:nth-child(3) {
      position: relative; left: unset; z-index: unset; box-shadow: none; background: transparent;
    }

    /* 使用 CSS 伪元素模拟每个单元格的标题，数据来自 JS 动态注入的 data-label */
    td:before { 
      content: attr(data-label);
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 35%; 
      padding-right: 10px; 
      white-space: nowrap;
      text-align: left;
      font-weight: 600;
      color: #64748b;
      font-size: 13px;
    }
    
    /* 修正输入框和选择框在卡片里的样式 */
    td input, td select {
      text-align: right;
      width: 100%;
      background: #f8fafc;
      border-color: #e2e8f0;
    }
  }

  @media (max-width: 480px) {
    .year-stats {
      grid-template-columns: 1fr;
    }
    .month-stat-grid {
      grid-template-columns: repeat(2, 1fr);
    }
    .cards {
      grid-template-columns: 1fr;
    }
    .toolbar button, .toolbar select {
      flex: 1 1 100%; /* 极小屏幕下完全单列排布 */
    }
  }"""

content = content.replace(old_media, new_media)

# 2. 更新 JavaScript 渲染逻辑，动态往 <td> 中注入 data-label 以适配假表头显示
old_js_render = """      html += `<tr>
        <td><input type="checkbox" value="${idx}" class="cursor-pointer"></td>
        <td><input onblur="updateData(${idx}, 'name', this.value)" value="${item.name || ''}" placeholder="门店名称"></td>
        <td><input onblur="updateData(${idx}, 'area', this.value)" value="${item.area || ''}" placeholder="区域"></td>
        <td><input onblur="updateData(${idx}, 'manager', this.value)" value="${item.manager || ''}" placeholder="负责人"></td>
        <td><input type="date" onchange="updateData(${idx}, 'planDate', this.value)" value="${item.planDate || ''}" class="cursor-pointer"></td>
        <td><input type="date" onchange="updateData(${idx}, 'realDate', this.value)" value="${item.realDate || ''}" class="cursor-pointer"></td>
        ${stepsHtml}
        <td><div class="progress-bar"><div class="progress-fill" style="width:${progress}%"></div><div class="progress-text">${progress}%</div></div></td>
        <td class="status-${(item.status || '').replace(/已|中|未启动/g,'').toLowerCase()}">${item.status || '-'}</td>
        <td>${warnStatus}</td>
        <td><input onblur="updateData(${idx}, 'note', this.value)" value="${item.note || ''}" placeholder="卡点备注"></td>
        <td>${delayHtml}</td>
      </tr>`;"""

# 修复 stepsHtml 本身的生成
old_steps_html = """      (item.steps || Array(9).fill('未开始')).forEach((val, sIdx) => {
        stepsHtml += `<td>
          <select onchange="updateStep(${idx}, ${sIdx}, this.value)" class="cursor-pointer">"""
new_steps_html = """      const stepNames = ['签约','图纸','装修','水电','设备','培训','证照','验收','物料'];
      (item.steps || Array(9).fill('未开始')).forEach((val, sIdx) => {
        stepsHtml += `<td data-label="${stepNames[sIdx]}进度">
          <select onchange="updateStep(${idx}, ${sIdx}, this.value)" class="cursor-pointer">"""

content = content.replace(old_steps_html, new_steps_html)

new_js_render = """      html += `<tr>
        <td data-label="选择操作"><input type="checkbox" value="${idx}" class="cursor-pointer"></td>
        <td data-label="门店名称"><input onblur="updateData(${idx}, 'name', this.value)" value="${item.name || ''}" placeholder="输入门店名称"></td>
        <td data-label="所属区域"><input onblur="updateData(${idx}, 'area', this.value)" value="${item.area || ''}" placeholder="输入区域"></td>
        <td data-label="负责人"><input onblur="updateData(${idx}, 'manager', this.value)" value="${item.manager || ''}" placeholder="输入负责人姓名"></td>
        <td data-label="预计开业"><input type="date" onchange="updateData(${idx}, 'planDate', this.value)" value="${item.planDate || ''}" class="cursor-pointer"></td>
        <td data-label="实际开业"><input type="date" onchange="updateData(${idx}, 'realDate', this.value)" value="${item.realDate || ''}" class="cursor-pointer"></td>
        ${stepsHtml}
        <td data-label="整体进度"><div class="progress-bar"><div class="progress-fill" style="width:${progress}%"></div><div class="progress-text">${progress}%</div></div></td>
        <td data-label="当前状态" class="status-${(item.status || '').replace(/已|中|未启动/g,'').toLowerCase()}">${item.status || '-'}</td>
        <td data-label="预警状态">${warnStatus}</td>
        <td data-label="卡点备注"><input onblur="updateData(${idx}, 'note', this.value)" value="${item.note || ''}" placeholder="卡点备注"></td>
        <td data-label="延期 / 整改">${delayHtml}</td>
      </tr>`;"""

content = content.replace(old_js_render, new_js_render)

# 同时更新上方两个基础明细表的渲染逻辑（计划/实际）
def replace_detail_body(content, body_id, js_fn):
    old_regex = r"(`<tr>\s*<td>\$\{item.name \|\| '-'\}</td>\s*<td>\$\{item.area \|\| '-'\}</td>\s*<td>\$\{item.[\w]+Date \|\| '-'\}</td>\s*<td>\$\{item.manager \|\| '-'\}</td>\s*<td class=\"status-\$\{\(item.status \|\| ''\).replace\(/已\|中\|未启动/g,''\).toLowerCase\(\)\}\">\$\{item.status \|\| '-'\}</td>\s*<td>\$\{warnText\}</td>\s*</tr>`;)"
    match = re.search(old_regex, content)
    if match:
        old_str = match.group(1)
        if 'planDate' in old_str:
            new_str = """`<tr>
        <td data-label="门店名称">${item.name || '-'}</td>
        <td data-label="所属区域">${item.area || '-'}</td>
        <td data-label="预计开业日期">${item.planDate || '-'}</td>
        <td data-label="负责人">${item.manager || '-'}</td>
        <td data-label="当前状态" class="status-${(item.status || '').replace(/已|中|未启动/g,'').toLowerCase()}">${item.status || '-'}</td>
        <td data-label="预警状态">${warnText}</td>
      </tr>`;"""
        else:
            new_str = """`<tr>
        <td data-label="门店名称">${item.name || '-'}</td>
        <td data-label="所属区域">${item.area || '-'}</td>
        <td data-label="实际开业日期">${item.realDate || '-'}</td>
        <td data-label="负责人">${item.manager || '-'}</td>
        <td data-label="当前状态" class="status-${(item.status || '').replace(/已|中|未启动/g,'').toLowerCase()}">${item.status || '-'}</td>
        <td data-label="预警状态">${warnText}</td>
      </tr>`;"""
        return content.replace(old_str, new_str)
    return content

content = replace_detail_body(content, 'planDetailBody', 'renderPlanDetail')
content = replace_detail_body(content, 'actualDetailBody', 'renderActualDetail')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Table-to-cards script completed.")
