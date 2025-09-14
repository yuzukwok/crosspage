Page({
  data: {
    size: 12,
    grid: [],
    layout: [],
    clues: {},
    cells: [],
    showClue: false,
    currentClue: '',
    currentIndex: 0,
    currentDirection: 'across'
  },
  onLoad() {
    // TODO: 修改为你的API地址
    const api = wx.getStorageSync('api') || 'http://10.10.0.81:8000/api/crossword'
    const words = wx.getStorageSync('words') || ['apple','banana','orange','grape','pear','peach']
    wx.request({
      url: api,
      method: 'POST',
      data: { words, size: 12, use_llm: true },
      success: (res) => {
        const { grid, layout, clues } = res.data
        const size = grid.length
        const cells = []
        for (let r=0; r<size; r++){
          for (let c=0; c<size; c++){
            const v = grid[r][c]
            cells.push({ r, c, value: v ? '' : '', isBlock: !v, focus: false })
          }
        }
        // 预计算方向索引列表和题目列表
        const acrossIdxs = [], downIdxs = [], acrossList = [], downList = []
        let numMap = {}
        let number = 1
        for (const e of layout) {
          numMap[`${e.row},${e.col},${e.direction}`] = number++
        }
        layout.forEach((e, i)=>{
          const clue = clues[e.word.toLowerCase()] || ''
          const num = numMap[`${e.row},${e.col},${e.direction}`]
          if (e.direction==='across') { acrossIdxs.push(i); acrossList.push({idx:i, num, clue}) }
          else { downIdxs.push(i); downList.push({idx:i, num, clue}) }
        })
        this.setData({ grid, layout, clues, size, cells, currentIndex: 0, currentDirection: 'across', acrossIdxs, downIdxs, acrossList, downList })
        this.highlightByIndex(0)
      },
      fail: (err) => {
        wx.showToast({ title: '获取题目失败', icon: 'none' })
      }
    })
  },
  highlightCells(cells){
    // 检查是否需要更新高亮
    const currentHighlighted = this.data.cells.filter(c => c.highlight).map(c => `${c.r},${c.c}`)
    const newHighlighted = cells.map(c => `${c.r},${c.c}`)
    if (JSON.stringify(currentHighlighted.sort()) === JSON.stringify(newHighlighted.sort())) {
      return // 高亮未变化，不更新
    }
    
    const arr = this.data.cells.slice()
    for (let i=0;i<arr.length;i++) arr[i].highlight = false
    for (const {r,c} of cells){
      const idx = r*this.data.size + c
      if (arr[idx]) arr[idx].highlight = true
    }
    this.setData({ cells: arr })
  },
  highlightByIndex(idx){
    // 每次切换题目都弹出 clue-popup
    const entry = this.data.layout[idx]
    if (!entry) return
    const cells = this.getEntryCells(entry)
    this.highlightCells(cells)
    const clue = this.data.clues[entry.word.toLowerCase()] || ''
    this.setData({ 
      currentDirection: entry.direction, 
      currentIndex: idx,
      showClue: true, 
      currentClue: `${entry.direction.toUpperCase()}: ${clue}` 
    })
  },
  jumpTo(e){
    const idx = e.currentTarget.dataset.idx
    this.highlightByIndex(Number(idx))
  },
  getEntryCells(entry){
    const cells = []
    for (let i=0;i<entry.word.length;i++){
      if (entry.direction==='across') cells.push({r: entry.row, c: entry.col+i})
      else cells.push({r: entry.row+i, c: entry.col})
    }
    return cells
  },
  getNextEntryIndex(direction, currentIdx){
    const { acrossIdxs, downIdxs } = this.data
    if (direction==='across'){
      const pos = acrossIdxs.indexOf(currentIdx)
      if (pos>=0 && pos < acrossIdxs.length-1) return { idx: acrossIdxs[pos+1], dir: 'across' }
      // 智能切换：横向最后一个后，切换到竖向首词
      if (downIdxs.length>0) return { idx: downIdxs[0], dir: 'down' }
      return { idx: acrossIdxs[0] || 0, dir: 'across' }
    } else {
      const pos = downIdxs.indexOf(currentIdx)
      if (pos>=0 && pos < downIdxs.length-1) return { idx: downIdxs[pos+1], dir: 'down' }
      // 智能切换：竖向最后一个后，切换到横向首词
      if (acrossIdxs.length>0) return { idx: acrossIdxs[0], dir: 'across' }
      return { idx: downIdxs[0] || 0, dir: 'down' }
    }
  },
  findWordByCell(r,c){
    for (const e of this.data.layout){
      const len = e.word.length
      if (e.direction === 'across' && e.row === r && c >= e.col && c < e.col + len) return e
      if (e.direction === 'down' && e.col === c && r >= e.row && r < e.row + len) return e
    }
    return null
  },
  onCellTap(e){
    const idx = e.currentTarget.dataset.index
    const cell = this.data.cells[idx]
    if (cell.isBlock) return
    const entry = this.findWordByCell(cell.r, cell.c)
    if (entry){
      const entryIdx = this.data.layout.findIndex(x=>x===entry)
      if (entryIdx !== this.data.currentIndex) {
        this.highlightByIndex(entryIdx)
      }
    }
  },
  closeClue(){ this.setData({ showClue:false }) },
  onInput(e){
    const idx = e.currentTarget.dataset.index
    const v = (e.detail.value || '').toUpperCase().slice(-1)
    const arr = this.data.cells.slice()
    // 设置当前格内容
    arr[idx].value = v
    // 先全部 focus 设为 false
    arr.forEach(cell => cell.focus = false)
    // 跳到下一个格
    const cell = arr[idx]
    if (!cell) { this.setData({ cells: arr }); return }
    const entry = this.data.layout[this.data.currentIndex]
    if (!entry) { this.setData({ cells: arr }); return }
    const cells = this.getEntryCells(entry)
    const pos = cells.findIndex(p=>p.r===cell.r && p.c===cell.c)
    if (pos < 0) { this.setData({ cells: arr }); return }
    let nextIdx = null
    if (pos < cells.length-1){
      const next = cells[pos+1]
      nextIdx = next.r * this.data.size + next.c
    } else {
      // 回绕到下一单词（同方向优先），若无则智能切换方向到首词
      const { idx: nextEntryIdx } = this.getNextEntryIndex(entry.direction, this.data.currentIndex)
      this.highlightByIndex(nextEntryIdx)
      const nextEntry = this.data.layout[nextEntryIdx]
      if (nextEntry) nextIdx = nextEntry.row * this.data.size + nextEntry.col
    }
    if (nextIdx !== null && arr[nextIdx] && !arr[nextIdx].isBlock) {
      arr[nextIdx].focus = true
    }
    this.setData({ cells: arr })
  },
  check(){
    const { cells, grid } = this.data
    let correct = 0, total = 0
    const arr = cells.slice()
    for (let i=0; i<arr.length; i++){
      const { r, c, isBlock } = arr[i]
      if (!isBlock){
        total++
        const ans = (grid[r][c]||'')
        const cur = (arr[i].value||'').toUpperCase()
        const ok = cur === ans
        if (ok) correct++
        arr[i].wrong = !ok && !!cur
        // 显示答案效果：直接填充正确字母
        arr[i].value = ans
      }
    }
    this.setData({ cells: arr })
    wx.showToast({ title: `正确 ${correct}/${total}`, icon:'none' })
  },
  clearAll(){
    const arr = this.data.cells.slice()
    for (let i=0;i<arr.length;i++) if (!arr[i].isBlock) arr[i].value = ''
    this.setData({ cells: arr })
  },
  // 已移除：prev/next/reveal/hint/switchDirection/onFocus
})
