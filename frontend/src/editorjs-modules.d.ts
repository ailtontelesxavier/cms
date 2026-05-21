declare module 'editorjs-header-with-alignment' {
  import type { ToolConstructable } from '@editorjs/editorjs'
  const Header: ToolConstructable
  export default Header
}

declare module 'editorjs-paragraph-with-alignment' {
  import type { ToolConstructable } from '@editorjs/editorjs'
  const Paragraph: ToolConstructable
  export default Paragraph
}

declare module '@editorjs/checklist' {
  import type { ToolConstructable } from '@editorjs/editorjs'
  const Checklist: ToolConstructable
  export default Checklist
}

declare module '@editorjs/table' {
  import type { ToolConstructable } from '@editorjs/editorjs'
  const Table: ToolConstructable
  export default Table
}

declare module '@editorjs/link' {
  import type { ToolConstructable } from '@editorjs/editorjs'
  const LinkTool: ToolConstructable
  export default LinkTool
}

declare module '@editorjs/underline' {
  import type { ToolConstructable } from '@editorjs/editorjs'
  const Underline: ToolConstructable
  export default Underline
}

declare module '@editorjs/marker' {
  import type { ToolConstructable } from '@editorjs/editorjs'
  const Marker: ToolConstructable
  export default Marker
}

declare module '@editorjs/inline-code' {
  import type { ToolConstructable } from '@editorjs/editorjs'
  const InlineCode: ToolConstructable
  export default InlineCode
}

declare module '@sotaproject/strikethrough' {
  import type { ToolConstructable } from '@editorjs/editorjs'
  const Strikethrough: ToolConstructable
  export default Strikethrough
}

declare module 'editorjs-font-size-plugin' {
  const FontSizeTool: any
  export default FontSizeTool
}

declare module 'editorjs-indent-tune' {
  import type { ToolConstructable } from '@editorjs/editorjs'
  const IndentTune: ToolConstructable & { version: string }
  export default IndentTune
}
