# [Frontend] Gestão de Tags — CRUD Completo

## Objetivo

Implementar a interface administrativa de tags: listagem paginada, criação, edição e exclusão com feedback de validação. Estilização com Tailwind v4.

Referência: spec:94772f59-b09f-4841-b5c0-dc363baa319c/3daeb8d8-9ba4-4ff6-a970-bd4fec21a764.

## Componentes

### `TagsView.vue` (rota `/tags`)

View fina que compõe `TagTable` e `TagFormModal`. Gerencia estado de modal aberto/fechado e tag em edição.

### `TagTable.vue`

Props: `tags: TagOut[]`, `loading: boolean`
Emits: `edit(tag: TagOut)`, `delete(tag: TagOut)`

Tabela com colunas: Nome, Slug, Descrição, Status (badge `Ativa`/`Inativa`), Ações (Editar / Excluir).
Estado vazio usa `EmptyState`. Estado de carregamento usa `LoadingSpinner`.

### `TagFormModal.vue`

Props: `open: boolean`, `tag: TagOut | null` (null = criação)
Emits: `saved`, `close`

Campos: Nome (obrigatório), Slug (auto-gerado a partir do nome, editável), Descrição (opcional).
Exibe erros de campo vindos do backend (422) e erro de conflito de slug (409) diretamente no campo slug.

```wireframe

<html>
<head>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: sans-serif; }
body { background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; min-height: 100vh; }
.modal { background: #fff; border-radius: 10px; padding: 28px; width: 440px; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
h2 { font-size: 17px; font-weight: 600; color: #0f172a; }
.close { background: none; border: none; font-size: 20px; color: #94a3b8; cursor: pointer; }
.field { margin-bottom: 16px; }
label { display: block; font-size: 13px; font-weight: 500; color: #374151; margin-bottom: 5px; }
input, textarea { width: 100%; padding: 9px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; }
input.error-field { border-color: #f87171; }
.field-error { font-size: 12px; color: #dc2626; margin-top: 4px; }
textarea { resize: vertical; min-height: 64px; }
.actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 24px; }
.btn { padding: 9px 18px; border-radius: 6px; font-size: 14px; font-weight: 500; cursor: pointer; border: none; }
.btn-cancel { background: #f1f5f9; color: #475569; }
.btn-save { background: #2563eb; color: #fff; }
</style>
</head>
<body>
<div class="modal">
  <div class="modal-header"><h2>Nova Tag</h2><button class="close">×</button></div>
  <div class="field"><label>Nome *</label><input type="text" placeholder="Educação" /></div>
  <div class="field">
    <label>Slug *</label>
    <input type="text" class="error-field" value="educacao" />
    <div class="field-error">Slug já está em uso por outra tag.</div>
  </div>
  <div class="field"><label>Descrição</label><textarea placeholder="Descrição opcional..."></textarea></div>
  <div class="actions"><button class="btn btn-cancel">Cancelar</button><button class="btn btn-save">Salvar</button></div>
</div>
</body>
</html>
```

## Composable `useTags` (file:frontend/src/modules/content-management/composables/useTags.ts)

Estado: `tags`, `total`, `page`, `isLoading`, `error`.
Métodos: `fetchTags()`, `createTag(data)`, `updateTag(id, data)`, `deleteTag(id)`.

## Tipos (file:frontend/src/types/tag.ts)

```
interface TagOut { id: number; name: string; slug: string; description: string | null; is_active: boolean; created_at: string; updated_at: string }
interface TagCreate { name: string; slug: string; description?: string }
interface TagUpdate { name?: string; description?: string }
```

## Critérios de Aceite

Lista de tags carrega com paginação funcional.Criar tag com dados válidos adiciona à lista e fecha o modal.Slug é auto-gerado a partir do nome (slugify) e pode ser editado manualmente.Erro 409 (slug duplicado) exibe mensagem no campo slug sem fechar o modal.Erros 422 são mapeados para os campos correspondentes.Editar tag pré-preenche o formulário com os dados atuais.Excluir tag exibe confirmação antes de chamar a API.Estado de carregamento exibe spinner; estado vazio exibe EmptyState.