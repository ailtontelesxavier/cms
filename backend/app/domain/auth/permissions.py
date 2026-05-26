from enum import Enum


class Acao(str, Enum):
    CRIAR = "criar"
    LER = "ler"
    ATUALIZAR = "atualizar"
    EXCLUIR = "excluir"
    ASSINAR = "assinar"
    ADMINISTRAR = "administrar"
    RELATORIOS = "relatorios"


class Modulo(str, Enum):
    PERMISSAO = "permissao"
    ADMINISTRATIVO = "administrativo"
    AUTH = "auth"
    POSTS = "posts"
    DOCUMENTOS = "documentos"
    PROCESSOS = "processos"
    AUDITORIA = "auditoria"
    RELATORIOS = "relatorios"
    FROTA = "frota"


# """Permissões padrão para cada perfil. Essas permissões são atribuídas automaticamente
# quando um perfil é criado, mas podem ser personalizadas posteriormente."""
PERMISSOES_PADRAO: dict[str, dict[str, list[Acao]]] = {
    "Administrador": {
        Modulo.ADMINISTRATIVO.value: list(Acao),
        Modulo.AUTH.value: list(Acao),
        Modulo.POSTS.value: list(Acao),
        Modulo.PROCESSOS.value: list(Acao),
        Modulo.RELATORIOS.value: list(Acao),
        Modulo.AUDITORIA.value: list(Acao),
        Modulo.DOCUMENTOS.value: list(Acao),
    },
    "Diretor": {
        Modulo.ADMINISTRATIVO.value: [Acao.LER, Acao.ATUALIZAR],
        Modulo.AUTH.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR],
        Modulo.POSTS.value: [Acao.LER, Acao.ATUALIZAR],
        Modulo.PROCESSOS.value: [Acao.CRIAR, Acao.LER, Acao.ASSINAR],
        Modulo.RELATORIOS.value: [Acao.LER],
        Modulo.DOCUMENTOS.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR, Acao.ASSINAR],
    },
    "Secretario": {
        Modulo.ADMINISTRATIVO.value: [Acao.LER],
        Modulo.AUTH.value: [Acao.LER,],
        Modulo.POSTS.value: [Acao.LER, Acao.ATUALIZAR],
        Modulo.PROCESSOS.value: [Acao.CRIAR, Acao.LER],
        Modulo.RELATORIOS.value: [Acao.LER],
    },
    "Editor": {
        Modulo.POSTS.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR],
        Modulo.PROCESSOS.value: [Acao.LER],
        Modulo.RELATORIOS.value: [Acao.LER],
    },
    "Usuario": {
        Modulo.POSTS.value: [Acao.LER],
        Modulo.PROCESSOS.value: [Acao.LER],
        Modulo.RELATORIOS.value: [Acao.CRIAR, Acao.LER],
    },
}
