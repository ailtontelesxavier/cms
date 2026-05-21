from enum import Enum


class Acao(str, Enum):
    CRIAR = "criar"
    LER = "ler"
    ATUALIZAR = "atualizar"
    EXCLUIR = "excluir"
    SUPERUSER = "superuser"


class Modulo(str, Enum):
    ADMINISTRATIVO = "administrativo"
    EDITOR = "educacional"
    AVALIACOES = "avaliacoes"
    DOCUMENTOS = "documentos"
    PROCESSOS = "processos"
    AUDITORIA = "auditoria"
    RELATORIOS = "relatorios"


PERMISSOES_PADRAO: dict[str, dict[str, list[Acao]]] = {
    "Administrador Master": {
        Modulo.ADMINISTRATIVO.value: list(Acao),
        Modulo.EDUCACIONAL.value: list(Acao),
        Modulo.AVALIACOES.value: list(Acao),
        Modulo.PROCESSOS.value: list(Acao),
        Modulo.RELATORIOS.value: list(Acao),
        Modulo.AUDITORIA.value: list(Acao),
        Modulo.DOCUMENTOS.value: list(Acao),
    },
    "Diretor": {
        Modulo.ADMINISTRATIVO.value: [Acao.LER, Acao.ATUALIZAR],
        Modulo.EDUCACIONAL.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR],
        Modulo.AVALIACOES.value: [Acao.LER, Acao.HOMOLOGAR],
        Modulo.PROCESSOS.value: [Acao.CRIAR, Acao.LER, Acao.ASSINAR],
        Modulo.RELATORIOS.value: [Acao.LER],
        Modulo.DOCUMENTOS.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR, Acao.ASSINAR],
    },
    "Secretario": {
        Modulo.ADMINISTRATIVO.value: [Acao.LER],
        Modulo.EDUCACIONAL.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR],
        Modulo.AVALIACOES.value: [Acao.LER],
        Modulo.PROCESSOS.value: [Acao.CRIAR, Acao.LER],
        Modulo.RELATORIOS.value: [Acao.LER],
    },
    "Coordenador Pedagogico": {
        Modulo.EDUCACIONAL.value: [Acao.LER, Acao.ATUALIZAR],
        Modulo.AVALIACOES.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR],
        Modulo.PROCESSOS.value: [Acao.LER],
        Modulo.RELATORIOS.value: [Acao.CRIAR, Acao.LER],
    },
    "Coordenador de Area": {
        Modulo.AVALIACOES.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR],
        Modulo.RELATORIOS.value: [Acao.LER],
    },
    "Professor": {
        Modulo.AVALIACOES.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR],
        Modulo.RELATORIOS.value: [Acao.LER],
    },
    "Professor Orientador": {
        Modulo.EDUCACIONAL.value: [Acao.LER],
        Modulo.AVALIACOES.value: [Acao.CRIAR, Acao.LER, Acao.ATUALIZAR],
        Modulo.RELATORIOS.value: [Acao.LER],
    },
    "Parecerista": {
        Modulo.PROCESSOS.value: [Acao.LER, Acao.CRIAR],
        Modulo.RELATORIOS.value: [Acao.LER],
    },
}
