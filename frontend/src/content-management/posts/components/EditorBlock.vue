<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import EditorJS, { type ToolConstructable } from '@editorjs/editorjs'
import Header from '@editorjs/header'
import List from '@editorjs/list'
import Quote from '@editorjs/quote'
import CodeTool from '@editorjs/code'
import Delimiter from '@editorjs/delimiter'
import ImageTool from '@editorjs/image'
import { postsApi } from '@/shared/api/posts'

const props = defineProps<{
  modelValue: string
  postId?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const editorRef = ref<HTMLDivElement>()
const editorInstance = ref<EditorJS>()

type EditorTools = Record<string, { class: ToolConstructable; config?: Record<string, unknown>; inlineToolbar?: boolean }>

const toolsConfig = computed(() => {
  const tools: EditorTools = {
    header: {
      class: Header,
      config: { levels: [2, 3, 4], defaultLevel: 2 },
    },
    list: {
      class: List,
      inlineToolbar: true,
    },
    quote: {
      class: Quote,
      inlineToolbar: true,
    },
    code: {
      class: CodeTool,
    },
    delimiter: {
      class: Delimiter,
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

  const blocks = htmlToBlocks(props.modelValue)

  const editor = new EditorJS({
    holder: editorRef.value,
    data: { blocks },
    tools: toolsConfig.value,
    autofocus: true,
    placeholder: 'Comece a escrever...',
  })

  editorInstance.value = editor
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
      blocks.push({ type: 'header', data: { text: el.innerHTML, level } })
    } else if (tag === 'p') {
      blocks.push({ type: 'paragraph', data: { text: el.innerHTML } })
    } else if (['ul', 'ol'].includes(tag)) {
      const items: string[] = []
      el.querySelectorAll('li').forEach(li => items.push(li.innerHTML))
      blocks.push({ type: 'list', data: { style: tag === 'ul' ? 'unordered' : 'ordered', items } })
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
        const d = block.data as { text?: string; level?: number }
        return `<h${d.level || 2}>${d.text || ''}</h${d.level || 2}>`
      }
      case 'paragraph': {
        const d = block.data as { text?: string }
        return `<p>${d.text || ''}</p>`
      }
      case 'list': {
        const d = block.data as { style?: string; items?: string[] }
        const tag = d.style === 'ordered' ? 'ol' : 'ul'
        const items = (d.items || []).map(item => `<li>${item}</li>`).join('')
        return `<${tag}>${items}</${tag}>`
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
    initEditor()
  }
})

onMounted(initEditor)

onBeforeUnmount(() => {
  editorInstance.value?.destroy()
})

defineExpose({ save, handleSave })
</script>

<template>
  <div>
    <div ref="editorRef" class="prose prose-sm max-w-none rounded-md border border-gray-300 px-3 py-2" />
    <button type="button" @click="handleSave"
      class="mt-2 rounded-md bg-sky-600 px-3 py-1 text-xs font-medium text-white hover:bg-sky-500">
      Sincronizar editor
    </button>
  </div>
</template>
