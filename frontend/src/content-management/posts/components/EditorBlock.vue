<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import EditorJS, { type ToolConstructable } from '@editorjs/editorjs'
import Header from 'editorjs-header-with-alignment'
import Paragraph from 'editorjs-paragraph-with-alignment'
import List from '@editorjs/list'
import Checklist from '@editorjs/checklist'
import Table from '@editorjs/table'
import Quote from '@editorjs/quote'
import CodeTool from '@editorjs/code'
import Delimiter from '@editorjs/delimiter'
import ImageTool from '@editorjs/image'
import LinkTool from '@editorjs/link'
import Underline from '@editorjs/underline'
import Marker from '@editorjs/marker'
import InlineCode from '@editorjs/inline-code'
import Strikethrough from '@sotaproject/strikethrough'
import IndentTune from 'editorjs-indent-tune'
import 'editorjs-font-size-plugin'
import { postsApi } from '@/shared/api/posts'

const FontSizeTool = (window as any).FontSizeTool

const props = defineProps<{
  modelValue: string
  postId?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const editorRef = ref<HTMLDivElement>()
const editorInstance = ref<EditorJS>()

const COLORS = [
  '#000000', '#434343', '#666666', '#999999', '#b7b7b7', '#d9d9d9',
  '#980000', '#ff0000', '#ff6600', '#ff9900', '#ffff00', '#00b050',
  '#00ff00', '#00ffff', '#0070c0', '#0000ff', '#7030a0', '#ff00ff',
]

class TextColor {
  api: any
  config: any
  button: HTMLButtonElement | null = null
  node: HTMLElement | null = null
  tag = 'SPAN'
  _preferredColor: string
  COLORS: string[]

  static get isInline() {
    return true
  }

  static get sanitize() {
    return {
      span: {
        style: true,
      },
    }
  }

  constructor({ api, config }: { api: any; config: any }) {
    this.api = api
    this.config = config || {}
    this.COLORS = config.colors || COLORS
    this._preferredColor = this.COLORS[0]
  }

  render() {
    this.button = document.createElement('button')
    this.button.type = 'button'
    this.button.innerHTML = '<span style="text-decoration:underline;font-weight:bold;font-family:serif">A</span>'
    this.button.classList.add(this.api.styles.inlineToolButton)
    return this.button
  }

  surround(range: Range) {
    if (!range) return
    const term = range.extractContents()
    const span = document.createElement(this.tag)
    span.style.color = this._preferredColor
    span.appendChild(term)
    range.insertNode(span)
    this.api.selection.expandToTag(span)
  }

  checkState(selection: Selection) {
    if (!selection) return false
    const anchor = selection.anchorNode
    if (!anchor) return false
    const parent = anchor.nodeType === 3 ? anchor.parentElement : anchor as HTMLElement
    if (!parent) return false
    const span = parent.closest(this.tag) as HTMLElement | null
    if (span && span.style.color) {
      this.node = span
      this.button?.classList.add(this.api.styles.inlineToolButtonActive)
      return true
    }
    this.node = null
    this.button?.classList.remove(this.api.styles.inlineToolButtonActive)
    return false
  }

  unwrap(_range: Range) {
    if (!this.node) return
    const text = this.node.textContent || ''
    const parent = this.node.parentNode
    if (!parent) return
    parent.replaceChild(document.createTextNode(text), this.node)
    this.node = null
  }

  renderActions() {
    const picker = document.createElement('div')
    picker.style.cssText = 'display:grid;grid-template-columns:repeat(6,28px);gap:4px;padding:8px;align-items:center'

    this.COLORS.forEach(color => {
      const swatch = document.createElement('button')
      swatch.type = 'button'
      swatch.style.cssText = `width:28px;height:28px;border-radius:50%;background-color:${color};border:2px solid ${color === '#ffffff' || color === '#d9d9d9' ? '#ccc' : color};cursor:pointer`
      swatch.dataset.color = color
      swatch.addEventListener('click', () => {
        this._preferredColor = color
        if (this.node) {
          this.node.style.color = color
        }
        picker.remove()
      })
      picker.appendChild(swatch)
    })

    return picker
  }
}

const inlineToolbar = ['bold', 'italic', 'underline', 'strikethrough', 'marker', 'inlineCode', 'link', 'color', 'fontSize']

type EditorTools = Record<string, {
  class: ToolConstructable | any
  config?: Record<string, unknown>
  inlineToolbar?: boolean | string[]
  tunes?: string[]
}>

const toolsConfig = computed(() => {
  const tools: EditorTools = {
    header: {
      class: Header,
      config: { levels: [1, 2, 3, 4], defaultLevel: 1 },
      inlineToolbar,
      tunes: ['indentTune'],
    },
    paragraph: {
      class: Paragraph,
      config: { placeholder: 'Comece a escrever...' },
      inlineToolbar,
      tunes: ['indentTune'],
    },
    list: {
      class: List,
      inlineToolbar,
      tunes: ['indentTune'],
    },
    checklist: {
      class: Checklist,
      inlineToolbar,
      tunes: ['indentTune'],
    },
    table: {
      class: Table,
    },
    quote: {
      class: Quote,
      inlineToolbar,
      tunes: ['indentTune'],
    },
    code: {
      class: CodeTool,
    },
    delimiter: {
      class: Delimiter,
    },
    linkTool: {
      class: LinkTool,
      config: {
        endpoint: '',
      },
    },
    underline: {
      class: Underline,
    },
    marker: {
      class: Marker,
    },
    inlineCode: {
      class: InlineCode,
    },
    strikethrough: {
      class: Strikethrough,
    },
    color: {
      class: TextColor as any,
      config: { colors: COLORS },
    },
    fontSize: {
      class: FontSizeTool as any,
      config: {
        fontSizes: [
          { size: '12px', label: 'Pequeno' },
          { size: '14px', label: 'Normal' },
          { size: '16px', label: 'Médio' },
          { size: '18px', label: 'Grande' },
          { size: '20px', label: 'Extra Grande' },
          { size: '24px', label: 'XXG' },
          { size: '28px', label: 'XXXG' },
          { size: '32px', label: 'Enorme' },
        ],
        defaultSize: '14px',
      },
    },
    indentTune: {
      class: IndentTune as any,
      config: {
        version: EditorJS.version,
      },
    },
  }

  if (props.postId) {
    tools.image = {
      class: ImageTool,
      config: {
        uploader: {
          async uploadByFile(file: File) {
            const res = await postsApi.uploadImage(props.postId!, file)
            return { success: 1, file: { url: res.data.url } }
          },
          async uploadByUrl(url: string) {
            return { success: 1, file: { url } }
          },
        },
      },
    }
  }

  return tools
})

async function initEditor() {
  if (!editorRef.value) return

  try {
    const blocks = htmlToBlocks(props.modelValue)

    const editor = new EditorJS({
      holder: editorRef.value,
      data: { blocks },
      tools: toolsConfig.value,
      autofocus: true,
      placeholder: 'Comece a escrever...',
    })

    editorInstance.value = editor
  } catch {
    editorInstance.value = undefined
  }
}

async function save(): Promise<string> {
  const editor = editorInstance.value
  if (!editor) return props.modelValue

  try {
    const output = await editor.save()
    return blocksToHtml(output.blocks)
  } catch {
    return props.modelValue
  }
}

function htmlToBlocks(html: string): { type: string; data: Record<string, unknown> }[] {
  if (!html || html === '<p></p>') return []

  const parser = new DOMParser()
  const doc = parser.parseFromString(html, 'text/html')
  const nodes = doc.body.childNodes
  const blocks: { type: string; data: Record<string, unknown> }[] = []

  for (const node of nodes) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent?.trim()
      if (text) {
        blocks.push({ type: 'paragraph', data: { text } })
      }
      continue
    }

    const el = node as HTMLElement
    const tag = el.tagName.toLowerCase()

    if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(tag)) {
      const level = parseInt(tag[1])
      const align = el.style.textAlign || 'left'
      blocks.push({ type: 'header', data: { text: el.innerHTML, level, align } })
    } else if (tag === 'p') {
      const alignment = el.style.textAlign || 'left'
      blocks.push({ type: 'paragraph', data: { text: el.innerHTML, alignment } })
    } else if (['ul', 'ol'].includes(tag)) {
      const items: string[] = []
      el.querySelectorAll('li').forEach(li => items.push(li.innerHTML))
      blocks.push({ type: 'list', data: { style: tag === 'ul' ? 'unordered' : 'ordered', items } })
    } else if (tag === 'table') {
      const content: string[][] = []
      el.querySelectorAll('tr').forEach(tr => {
        const row: string[] = []
        tr.querySelectorAll('td, th').forEach(cell => row.push(cell.innerHTML))
        content.push(row)
      })
      blocks.push({ type: 'table', data: { content, withHeadings: false } })
    } else if (tag === 'blockquote') {
      blocks.push({ type: 'quote', data: { text: el.innerHTML, caption: '', alignment: 'left' } })
    } else if (tag === 'pre') {
      blocks.push({ type: 'code', data: { code: el.textContent || '' } })
    } else if (tag === 'hr') {
      blocks.push({ type: 'delimiter', data: {} })
    } else if (tag === 'img') {
      blocks.push({ type: 'image', data: { url: el.getAttribute('src') || '', caption: el.getAttribute('alt') || '' } })
    }
  }

  return blocks
}

function blocksToHtml(blocks: { type: string; data: Record<string, unknown> }[]): string {
  if (!blocks.length) return '<p></p>'

  return blocks.map(block => {
    switch (block.type) {
      case 'header': {
        const d = block.data as { text?: string; level?: number; align?: string }
        const alignStyle = d.align && d.align !== 'left' ? ` style="text-align:${d.align}"` : ''
        return `<h${d.level || 2}${alignStyle}>${d.text || ''}</h${d.level || 2}>`
      }
      case 'paragraph': {
        const d = block.data as { text?: string; alignment?: string }
        const alignStyle = d.alignment && d.alignment !== 'left' ? ` style="text-align:${d.alignment}"` : ''
        return `<p${alignStyle}>${d.text || ''}</p>`
      }
      case 'list': {
        const d = block.data as { style?: string; items?: string[] }
        const tag = d.style === 'ordered' ? 'ol' : 'ul'
        const items = (d.items || []).map(item => `<li>${item}</li>`).join('')
        return `<${tag}>${items}</${tag}>`
      }
      case 'checklist': {
        const d = block.data as { items?: { text: string; checked: boolean }[] }
        const items = (d.items || []).map(item =>
          `<li>${item.checked ? '<input type="checkbox" checked disabled>' : '<input type="checkbox" disabled>'} ${item.text}</li>`
        ).join('')
        return `<ul data-type="checklist">${items}</ul>`
      }
      case 'table': {
        const d = block.data as { content?: string[][]; withHeadings?: boolean }
        const rows = (d.content || []).map(row =>
          `<tr>${row.map(cell => `<td>${cell}</td>`).join('')}</tr>`
        ).join('')
        return `<table><tbody>${rows}</tbody></table>`
      }
      case 'quote': {
        const d = block.data as { text?: string; caption?: string }
        return `<blockquote>${d.text || ''}</blockquote>`
      }
      case 'code': {
        const d = block.data as { code?: string }
        return `<pre><code>${escapeHtml(d.code || '')}</code></pre>`
      }
      case 'delimiter':
        return '<hr>'
      case 'image': {
        const d = block.data as { url?: string; caption?: string }
        return `<img src="${d.url || ''}" alt="${d.caption || ''}" />`
      }
      default:
        return ''
    }
  }).filter(Boolean).join('\n') || '<p></p>'
}

function escapeHtml(text: string): string {
  const div = document.createElement('div')
  div.appendChild(document.createTextNode(text))
  return div.innerHTML
}

async function handleSave() {
  const html = await save()
  emit('update:modelValue', html)
}

watch(() => props.postId, () => {
  if (editorInstance.value) {
    editorInstance.value.destroy()
    editorInstance.value = undefined
  }
  initEditor()
})

onMounted(initEditor)

onBeforeUnmount(() => {
  if (editorInstance.value && typeof editorInstance.value.destroy === 'function') {
    editorInstance.value.destroy()
  }
})

defineExpose({ save, handleSave })
</script>

<template>
  <div>
    <div ref="editorRef" class="editor-wrapper rounded-md border border-gray-300 px-3 py-2" />
    <button type="button" @click="handleSave"
      class="mt-2 rounded-md bg-sky-600 px-3 py-1 text-xs font-medium text-white hover:bg-sky-500">
      Sincronizar editor
    </button>
  </div>
</template>

<style scoped>
.editor-wrapper :deep(.ce-header) {
  font-weight: 700;
}

.editor-wrapper :deep(h1.ce-header) {
  font-size: 2em;
  line-height: 1.2;
  margin: 0.67em 0;
}

.editor-wrapper :deep(h2.ce-header) {
  font-size: 1.5em;
  line-height: 1.3;
  margin: 0.83em 0;
}

.editor-wrapper :deep(h3.ce-header) {
  font-size: 1.17em;
  line-height: 1.4;
  margin: 1em 0;
}

.editor-wrapper :deep(h4.ce-header) {
  font-size: 1em;
  line-height: 1.5;
  margin: 1.33em 0;
}
</style>
